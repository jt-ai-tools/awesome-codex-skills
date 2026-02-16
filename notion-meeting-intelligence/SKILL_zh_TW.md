---
name: notion-meeting-intelligence
description: 結合 Notion 背景資訊與 Codex 研究能力準備會議資料；用於收集上下文、草擬議程/預讀文件 (Pre-reads)，並針對參與者量身定制資料。
metadata:
  short-description: 結合 Notion 背景資訊與量身定制的議程準備會議
---

# 會議智慧化 (Meeting Intelligence)

透過拉取 Notion 上下文、量身定制議程與預讀文件，並結合 Codex 研究成果來準備會議。

## 快速開始
1) **確認會議資訊**：確認會議目標、參與者、日期/時間，以及需要做出的決策。
2) **收集背景資訊**：使用 `Notion:notion-search` 進行搜尋，接著透過 `Notion:notion-fetch` 獲取內容（包含先前的筆記、規格書、OKR、決策紀錄）。
3) **挑選模板**：參考 `reference/template-selection-guide.md` 選擇正確模板（狀態更新、決策、規劃、回顧、1:1、腦力激盪）。
4) **草擬議程/預讀文件**：在 Notion 中使用 `Notion:notion-create-pages` 建立頁面，嵌入來源連結並標註負責人與每個項目的時間分配 (Timeboxes)。
5) **內容強化**：加入 Codex 研究內容（產業洞察、指標、風險），並隨著計畫變動使用 `Notion:notion-update-page` 更新頁面。

## 工作流程
### 0) 設定 Notion MCP（若尚未配置）
如果任何 MCP 調用因為 Notion MCP 未連線而失敗，請暫停並進行設定：

1. 新增 Notion MCP：
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. 啟用遠端 MCP 客戶端：
   - 在 `config.toml` 中設定 `[features].rmcp_client = true` **或** 執行 `codex --enable rmcp_client`
3. 透過 OAuth 登入：
   - `codex mcp login notion`

成功登入後，使用者必須重新啟動 Codex。您應完成目前的回答並告知使用者，以便他們在下次嘗試時可以從「步驟 1」繼續。

### 1) 收集輸入資訊
- 詢問會議目標、預期成果/決策、參與者、時長、日期/時間以及先前的參考資料。
- 在 Notion 中搜尋相關文件、過去的筆記、規格書與行動項目 (`Notion:notion-search`)，然後獲取關鍵頁面內容 (`Notion:notion-fetch`)。
- 預先記錄阻礙因素/風險與待解決問題。

### 2) 選擇格式
- 狀態/進度更新 → 狀態模板 (Status template)。
- 決策/審核 → 決策模板 (Decision template)。
- 規劃（衝刺/專案） → 規劃模板 (Planning template)。
- 回顧/回饋 → 回顧模板 (Retrospective template)。
- 1:1 面談 → 一對一模板 (One-on-one template)。
- 構思/發想 → 腦力激盪模板 (Brainstorming template)。
- 使用 `reference/template-selection-guide.md` 進行確認。

### 3) 建立議程與預讀文件
- 從 `reference/` 中選擇模板並進行調整（包含背景、目標、議程、每項負責人/時間、決策、風險、預習要求）。
- 包含所提取之 Notion 頁面的連結，以及任何要求的預讀材料。
- 為每個議程項目指派負責人；標註時間分配與預期產出。

### 4) 加入研究內容進行強化
- 在有幫助的地方加入簡潔的 Codex 研究：市場/產業事實、基準指標、風險、最佳實踐。
- 確保所有主張均附帶來源連結；區分事實與觀點。

### 5) 定稿與分享
- 加入後續追蹤的步驟與負責人。
- 如果產生了具體任務，在相關的 Notion 資料庫中建立並連結任務。
- 當細節變更時，透過 `Notion:notion-update-page` 更新頁面；若修改多次，請保留簡短的變更日誌。

## 參考資料與範例
- `reference/` — 模板選擇器與會議模板（例如：`template-selection-guide.md`, `status-update-template.md`, `decision-meeting-template.md`, `sprint-planning-template.md`, `one-on-one-template.md`, `retrospective-template.md`, `brainstorming-template.md`）。
- `examples/` — 端到端的會議準備範例（例如：`executive-review.md`, `project-decision.md`, `sprint-planning.md`, `customer-meeting.md`）。
