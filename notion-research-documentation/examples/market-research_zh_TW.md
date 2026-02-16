# 範例：市場研究 (Market Research)

**使用者請求**： 「研究 AI 編碼助手市場的現況，並在 Notion 中建立一份摘要文件」

## 工作流程

### 1. 搜尋資訊
```
Notion:notion-search
query: "AI 編碼助手市場"
```
在工程 (Engineering)、戰略 (Strategy) 與產品 (Product) 團隊空間中找到了 3 個相關頁面。

### 2. 獲取與分析內容
```
執行 Notion:notion-fetch (3 次)
```
從來源頁面中擷取市場規模、競爭格局與技術趨勢。

### 3. 建立技術文件
```
Notion:notion-create-pages
```

## 輸出結果（簡約版）

```markdown
# AI 編碼助手市場研究報告 - 2025 年 10 月

## 執行摘要 (Executive Summary)
AI 編碼助手市場正經歷超過 150% 的年增長率。GitHub Copilot 以 60% 的市佔率佔據主導地位，但在特定利基市場中，專業型工具正展現出強勁的市佔增長勢頭。

## 關鍵發現

### 市場規模與增長
2024 年為 8 億美元 → 預計到 2026 年將達到 25 億美元。開發者採用率：2023 年為 23% → 2024 年增長至 47%。
來源：<mention-page url="...">2025 年第三季市場趨勢</mention-page>

### 競爭格局
- **GitHub Copilot**：60% (憑藉強大的 IDE 整合)。
- **Cursor**：15% (快速增長，全功能 IDE)。
- **Tabnine**：10% (主打企業級、地端 [On-premise] 部署)。
- **Cody**：5% (具備程式碼庫感知能力 [Codebase-aware])。
- **CodeWhisperer**：8% (主打 AWS 服務整合)。
來源：<mention-page url="...">AI 工具競爭分析</mention-page>

### 技術趨勢
關鍵差異化因素：上下文感知 (Context awareness)、自訂化、多模態 (Multi-modal) 介面、程式碼驗證。
來源：<mention-page url="...">開發者工具全景圖</mention-page>

## 下一步行動
1. 持續監控 Cursor 的增長與新功能發布。
2. 評估 Cody 的程式碼庫感知能力。
3. 紀錄企業安全性與合規性要求。
4. 追蹤定價趨勢。
```

## 核心收穫
- 成功在多個團隊空間中找到相關頁面。
- 綜整了競爭、市場與技術等多維度視角。
- 使用了正確的來源頁面引用連結。
- 產出了具備引導性的建議事項。
