---
name: langsmith-fetch
description: 透過從 LangSmith Studio 獲取執行追蹤紀錄 (Traces)，偵錯 LangChain 與 LangGraph 代理人 (Agents)。當偵錯代理人行為、調查錯誤、分析工具呼叫、檢查記憶體操作或檢驗代理人效能時使用。自動獲取最近的追蹤紀錄並分析執行模式。需要安裝 langsmith-fetch CLI。
---

# LangSmith Fetch - 代理人偵錯技能 (Agent Debugging Skill)

透過直接在終端機中從 LangSmith Studio 獲取執行追蹤紀錄，偵錯 LangChain 與 LangGraph 代理人。

## 何時使用此技能

當使用者提及以下內容時自動啟動：
- 🐛 「幫我的代理人偵錯」或「哪裡出錯了？」
- 🔍 「顯示最近的追蹤紀錄」或「發生了什麼事？」
- ❌ 「檢查錯誤」或「為什麼失敗了？」
- 💾 「分析記憶體操作」或「檢查長期記憶 (LTM)」
- 📊 「查看代理人效能」或「檢查權杖 (Token) 使用情況」
- 🔧 「呼叫了哪些工具？」或「顯示執行流程」

## 前置作業

### 1. 安裝 langsmith-fetch
```bash
pip install langsmith-fetch
```

### 2. 設定環境變數
```bash
export LANGSMITH_API_KEY="您的_langsmith_api_key"
export LANGSMITH_PROJECT="您的專案名稱"
```

**驗證設定：**
```bash
echo $LANGSMITH_API_KEY
echo $LANGSMITH_PROJECT
```

## 核心工作流程

### 工作流程 1：快速偵錯近期活動

**當使用者詢問：**「剛才發生了什麼事？」或「幫我的代理人偵錯」

**執行指令：**
```bash
langsmith-fetch traces --last-n-minutes 5 --limit 5 --format pretty
```

**分析並回報：**
1. ✅ 找到的追蹤紀錄數量
2. ⚠️ 任何錯誤或失敗
3. 🛠️ 被呼叫的工具
4. ⏱️ 執行時間
5. 💰 權杖 (Token) 使用量

**回覆範例格式：**
```
在過去 5 分鐘內找到 3 條追蹤紀錄：

追蹤紀錄 1：✅ 成功
- 代理人：memento
- 工具：recall_memories, create_entities
- 耗時：2.3s
- Token 使用量：1,245

追蹤紀錄 2：❌ 錯誤
- 代理人：cypher
- 錯誤："Neo4j connection timeout" (Neo4j 連線逾時)
- 耗時：15.1s
- 失敗點：search_nodes 工具

追蹤紀錄 3：✅ 成功
- 代理人：memento
- 工具：store_memory
- 耗時：1.8s
- Token 使用量：892

💡 發現問題：追蹤紀錄 2 由於 Neo4j 逾時而失敗。建議檢查資料庫連線。
```

---

### 工作流程 2：深入探討特定追蹤紀錄

**當使用者提供：** 追蹤紀錄 ID (Trace ID) 或說「調查那個錯誤」

**執行指令：**
```bash
langsmith-fetch trace <trace-id> --format json
```

**分析 JSON 並回報：**
1. 🎯 代理人當時試圖做什麼
2. 🛠️ 按順序呼叫了哪些工具
3. ✅ 工具執行結果（成功/失敗）
4. ❌ 錯誤訊息（如有）
5. 💡 根本原因分析 (Root cause analysis)
6. 🔧 建議的修復方案

**回覆範例格式：**
```
深度分析報告 - 追蹤紀錄 abc123

目標：使用者詢問「尋找 Neo4j 中的所有專案」

執行流程：
1. ✅ search_nodes(query: "projects")
   → 找到 24 個節點

2. ❌ get_node_details(node_id: "proj_123")
   → 錯誤："Node not found" (找不到節點)
   → 這是失敗點

3. ⏹️ 執行停止

根本原因：
search_nodes 工具回傳了資料庫中已不存在的節點 ID，
可能是由於最近的刪除操作所致。

建議修復：
1. 在 get_node_details 工具中新增錯誤處理。
2. 在搜尋結果中過濾已刪除的節點。
3. 更新快取失效 (Cache invalidation) 策略。

Token 使用量：1,842 tokens ($0.0276)
執行時間：8.7 秒
```

---

### 工作流程 3：匯出偵錯環節 (Debug Session)

**當使用者說：**「儲存此環節」或「匯出追蹤紀錄」

**執行指令：**
```bash
# 建立帶有時間戳記的環節資料夾
SESSION_DIR="langsmith-debug/session-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$SESSION_DIR"

# 匯出追蹤紀錄
langsmith-fetch traces "$SESSION_DIR/traces" --last-n-minutes 30 --limit 50 --include-metadata

# 匯出對話討論串 (Threads)
langsmith-fetch threads "$SESSION_DIR/threads" --limit 20
```

**回報：**
```
✅ 環節匯出成功！

位置：langsmith-debug/session-20251224-143022/
- 追蹤紀錄 (Traces)：42 個檔案
- 對話討論串 (Threads)：8 個檔案

您現在可以：
1. 查看個別追蹤紀錄檔案。
2. 與團隊分享資料夾。
3. 使用外部工具進行分析。
4. 封存以供未來參考。

環節大小：2.3 MB
```

---

### 工作流程 4：錯誤偵測

**當使用者詢問：**「顯示錯誤」或「哪些地方失敗了？」

**執行指令：**
```bash
# 獲取最近的追蹤紀錄
langsmith-fetch traces --last-n-minutes 30 --limit 50 --format json > recent-traces.json

# 搜尋錯誤關鍵字
grep -i "error\|failed\|exception" recent-traces.json
```

**分析並回報：**
1. 📊 找到的總錯誤數
2. ❌ 錯誤類型與發生頻率
3. 🕐 錯誤發生的時間
4. 🎯 哪些代理人/工具失敗了
5. 💡 共同模式 (Patterns)

**回覆範例格式：**
```
錯誤分析報告 - 過去 30 分鐘

總追蹤紀錄數：50
失敗紀錄數：7 (14% 失敗率)

錯誤詳情：
1. Neo4j 連線逾時 (發生 4 次)
   - 代理人：cypher
   - 工具：search_nodes
   - 首次發生：14:32
   - 最後發生：14:45
   - 規律：發生在高峰負載期間

2. 記憶體儲存失敗 (發生 2 次)
   - 代理人：memento
   - 工具：store_memory
   - 錯誤："Pinecone rate limit exceeded" (超出 Pinecone 速率限制)
   - 發生時間：14:38, 14:41

3. 找不到工具 (發生 1 次)
   - 代理人：sqlcrm
   - 嘗試呼叫工具："export_report" (該工具不存在)
   - 發生時間：14:35

💡 建議：
1. 為 Neo4j 逾時新增重試邏輯。
2. 為 Pinecone 實作速率限制處理。
3. 修正 sqlcrm 工具配置。
```

---

## 常見使用案例

### 案例 1：「代理人無回應」

**使用者說：**「我的代理人完全沒動作」

**步驟：**
1. 檢查追蹤紀錄是否存在：
   ```bash
   langsmith-fetch traces --last-n-minutes 5 --limit 5
   ```

2. **如果沒有找到追蹤紀錄：**
   - 追蹤功能可能已停用。
   - 檢查環境變數中的 `LANGCHAIN_TRACING_V2=true`。
   - 檢查是否已設定 `LANGCHAIN_API_KEY`。
   - 驗證代理人是否真的有執行。

3. **如果找到追蹤紀錄：**
   - 查看是否有錯誤。
   - 檢查執行時間（是否卡住了？）。
   - 驗證工具呼叫是否已完成。

---

### 案例 2：「呼叫了錯誤的工具」

**使用者說：**「為什麼它用了錯誤的工具？」

**步驟：**
1. 獲取特定的追蹤紀錄。
2. 查看執行時可用的工具。
3. 檢查代理人選擇工具的推理過程。
4. 檢查工具的描述/指令。
5. 建議優化提示詞 (Prompt) 或工具配置。

---

### 案例 3：「記憶體失效」

**使用者說：**「代理人記不住事情」

**步驟：**
1. 搜尋記憶體操作：
   ```bash
   langsmith-fetch traces --last-n-minutes 10 --limit 20 --format raw | grep -i "memory\|recall\|store"
   ```

2. 檢查：
   - 記憶體工具是否被呼叫？
   - 回憶 (Recall) 是否回傳結果？
   - 記憶是否真的被儲存？
   - 檢索到的記憶是否被使用了？

---

### 案例 4：「效能問題」

**使用者說：**「代理人太慢了」

**步驟：**
1. 匯出包含中繼資料 (Metadata) 的紀錄：
   ```bash
   langsmith-fetch traces ./perf-analysis --last-n-minutes 30 --limit 50 --include-metadata
   ```

2. 分析：
   - 每條追蹤紀錄的執行時間。
   - 工具呼叫延遲 (Latency)。
   - Token 使用量（上下文大小）。
   - 迭代次數。
   - 最慢的操作。

3. 識別瓶頸 (Bottlenecks) 並建議優化。

---

## 輸出格式指南

### 美化格式 (Pretty Format - 預設)
```bash
langsmith-fetch traces --limit 5 --format pretty
```
**適用於：** 快速視覺檢查，呈現給使用者。

### JSON 格式
```bash
langsmith-fetch traces --limit 5 --format json
```
**適用於：** 詳細分析，語法高亮審查。

### 原始格式 (Raw Format)
```bash
langsmith-fetch traces --limit 5 --format raw
```
**適用於：** 透過管道 (Pipe) 傳遞給其他指令，自動化流程。

---

## 進階功能

### 基於時間的過濾
```bash
# 特定時間戳記之後
langsmith-fetch traces --after "2025-12-24T13:00:00Z" --limit 20

# 過去 N 分鐘（最常用）
langsmith-fetch traces --last-n-minutes 60 --limit 100
```

### 包含中繼資料 (Metadata)
```bash
# 獲取額外背景資訊
langsmith-fetch traces --limit 10 --include-metadata

# 中繼資料包含：代理人類型、模型、標籤 (Tags)、環境
```

### 併發獲取 (更快速)
```bash
# 加速大量匯出
langsmith-fetch traces ./output --limit 100 --concurrent 10
```

---

## 疑難排解 (Troubleshooting)

### 「No traces found matching criteria」(找不到符合條件的追蹤紀錄)

**可能原因：**
1. 該時段內沒有代理人活動。
2. 追蹤功能已停用。
3. 專案名稱錯誤。
4. API 金鑰問題。

**解決方案：**
```bash
# 1. 嘗試更長的時間範圍
langsmith-fetch traces --last-n-minutes 1440 --limit 50

# 2. 檢查環境變數
echo $LANGSMITH_API_KEY
echo $LANGSMITH_PROJECT

# 3. 改為嘗試獲取討論串 (Threads)
langsmith-fetch threads --limit 10

# 4. 驗證程式碼中是否啟用了追蹤
# 檢查是否有：LANGCHAIN_TRACING_V2=true
```

### 「Project not found」(找不到專案)

**解決方案：**
```bash
# 查看當前配置
langsmith-fetch config show

# 設定正確的專案
export LANGSMITH_PROJECT="正確的專案名稱"

# 或永久配置
langsmith-fetch config set project "您的專案名稱"
```

### 環境變數未持久化

**解決方案：**
```bash
# 新增至 shell 配置檔案 (~/.bashrc 或 ~/.zshrc)
echo 'export LANGSMITH_API_KEY="您的金鑰"' >> ~/.bashrc
echo 'export LANGSMITH_PROJECT="您的專案"' >> ~/.bashrc

# 重新載入 shell 配置
source ~/.bashrc
```

---

## 最佳實踐

### 1. 定期健康檢查
```bash
# 進行變更後的快速檢查
langsmith-fetch traces --last-n-minutes 5 --limit 5
```

### 2. 有組織的儲存方式
```
langsmith-debug/
├── sessions/
│   ├── 2025-12-24/
│   └── 2025-12-25/
├── error-cases/ (錯誤案例)
└── performance-tests/ (效能測試)
```

### 3. 記錄發現
當您發現 Bug 時：
1. 匯出有問題的追蹤紀錄。
2. 儲存至 `error-cases/` 資料夾。
3. 在 README 中記錄出錯原因。
4. 與團隊分享追蹤紀錄 ID。

### 4. 與開發流程整合
```bash
# 在 Commit 程式碼之前
langsmith-fetch traces --last-n-minutes 10 --limit 5

# 如果發現錯誤
langsmith-fetch trace <error-id> --format json > pre-commit-error.json
```

---

## 快速參考

```bash
# 最常用指令

# 快速偵錯
langsmith-fetch traces --last-n-minutes 5 --limit 5 --format pretty

# 特定追蹤紀錄
langsmith-fetch trace <trace-id> --format pretty

# 匯出環節
langsmith-fetch traces ./debug-session --last-n-minutes 30 --limit 50

# 尋找錯誤
langsmith-fetch traces --last-n-minutes 30 --limit 50 --format raw | grep -i error

# 包含中繼資料
langsmith-fetch traces --limit 10 --include-metadata
```

---

## 資源

- **LangSmith Fetch CLI:** https://github.com/langchain-ai/langsmith-fetch
- **LangSmith Studio:** https://smith.langchain.com/
- **LangChain Docs:** https://docs.langchain.com/
- **此技能儲存庫:** https://github.com/OthmanAdi/langsmith-fetch-skill

---

## 給 Claude 的注意事項

- 執行指令前務必檢查是否已安裝 `langsmith-fetch`。
- 驗證環境變數是否已設定。
- 使用 `--format pretty` 輸出人類可讀的結果。
- 需要解析與分析數據時使用 `--format json`。
- 匯出環節時，建立有組織的資料夾結構。
- 始終提供清晰的分析與具體可執行的見解。
- 如果指令失敗，協助排查配置問題。

---

**版本：** 0.1.0
**作者：** Ahmad Othman Ammar Adi
**授權：** MIT
**儲存庫：** https://github.com/OthmanAdi/langsmith-fetch-skill
