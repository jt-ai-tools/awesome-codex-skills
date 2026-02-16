---
name: notion-spec-to-implementation
description: 將 Notion 規格書轉化為實作計畫、任務與進度追蹤；用於實作 PRD/功能規格，並從中建立 Notion 計畫與任務。
metadata:
  short-description: 將 Notion 規格書轉化為實作計畫、任務與進度追蹤
---

# 從規格書到實作 (Spec to Implementation)

將 Notion 規格書轉換為相互連結的實作計畫、任務，以及持續的狀態更新。

## 快速開始
1) **定位規格書**：使用 `Notion:notion-search` 定位規格書，接著透過 `Notion:notion-fetch` 獲取內容。
2) **解析需求**：參考 `reference/spec-parsing.md` 解析需求與不確定之處。
3) **建立計畫頁面**：使用 `Notion:notion-create-pages` 建立計畫頁面（選擇模板：快速版 vs. 完整版）。
4) **建立任務**：尋找任務資料庫，確認其結構綱要 (Schema)，然後使用 `Notion:notion-create-pages` 建立任務。
5) **連結關聯**：建立 規格書 ↔ 計畫 ↔ 任務 之間的連結；使用 `Notion:notion-update-page` 保持狀態更新。

## 工作流程

### 0) 設定 Notion MCP（若尚未配置）
如果任何 MCP 調用因為 Notion MCP 未連線而失敗，請暫停並進行設定：

1. 新增 Notion MCP：
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. 啟用遠端 MCP 客戶端：
   - 在 `config.toml` 中設定 `[features].rmcp_client = true` **or** 執行 `codex --enable rmcp_client`
3. 透過 OAuth 登入：
   - `codex mcp login notion`

成功登入後，使用者必須重新啟動 Codex。您應完成目前的回答並告知使用者，以便他們在下次嘗試時可以從「步驟 1」繼續。

### 1) 定位並閱讀規格書
- 先行搜尋 (`Notion:notion-search`)；若出現多個結果，請要求使用者確認要使用哪一個。
- 獲取頁面內容 (`Notion:notion-fetch`) 並掃描其中的需求、驗收標準 (Acceptance criteria)、限制條件與優先級。擷取模式請參考 `reference/spec-parsing.md`。
- 在繼續之前，將資訊空缺處或假設事項彙整到「澄清區塊」中。

### 2) 決定計畫深度
- 簡單變更 → 使用 `reference/quick-implementation-plan.md`。
- 多階段功能/遷移 → 使用 `reference/standard-implementation-plan.md`。
- 透過 `Notion:notion-create-pages` 建立計畫，內容包含：概覽、連結至規格書、需求摘要、各階段規劃、依賴關係/風險，以及成功指標。建立連回規格書的連結。

### 3) 建立任務
- 尋找任務資料庫（透過 `Notion:notion-search` → `Notion:notion-fetch` 確認數據源與必填屬性）。參考 `reference/task-creation.md` 中的模式。
- 將任務大小調整為 1-2 天的工作量。使用 `reference/task-creation-template.md` 撰寫內容（背景、目標、驗收標準、依賴關係、資源）。
- 設定屬性：標題/動詞開頭的行動、狀態、優先級、與規格書和計畫的關聯；若有提供，則設定到期日/故事點 (Story points)/負責人。
- 使用資料庫的 `data_source_id` 透過 `Notion:notion-create-pages` 建立頁面。

### 4) 連結產出物 (Artifacts)
- 計畫連結至規格書；任務同時連結至計畫與規格書。
- （選填）使用 `Notion:notion-update-page` 在規格書中新增一個簡短的「實作 (Implementation)」章節，指向相關的計畫與任務。

### 5) 追蹤進度
- 遵循 `reference/progress-tracking.md` 中的進度節奏 (Cadence)。
- 使用 `reference/progress-update-template.md` 發布更新；使用 `reference/milestone-summary-template.md` 結束階段性目標。
- 保持計畫/任務中的檢查清單與狀態欄位同步；記錄阻礙因素與決策。

## 參考資料與範例
- `reference/` — 解析模式、計畫/任務模板、進度節奏（例如：`spec-parsing.md`, `standard-implementation-plan.md`, `task-creation.md`, `progress-tracking.md`）。
- `examples/` — 完整的端到端流程範例（例如：`ui-component.md`, `api-feature.md`, `database-migration.md`）。
