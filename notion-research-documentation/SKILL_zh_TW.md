---
name: notion-research-documentation
description: 在 Notion 中進行跨頁面研究並綜整為結構化文件；用於從多個 Notion 來源收集資訊，產出附帶引用與來源連結的簡要說明、對比分析或綜合報告。
metadata:
  short-description: 研究 Notion 內容並產出簡要說明或報告
---

# 研究與文件編寫 (Research & Documentation)

拉取相關的 Notion 頁面、綜整發現，並發布清晰的簡要說明或報告（附帶引用與來源連結）。

## 快速開始
1) **尋找來源**：使用針對性查詢透過 `Notion:notion-search` 尋找來源；與使用者確認研究範圍。
2) **獲取頁面**：透過 `Notion:notion-fetch` 獲取頁面內容；紀錄關鍵章節並擷取引用資訊（參考 `reference/citations.md`）。
3) **選擇輸出格式**：參考 `reference/format-selection-guide.md` 選擇合適格式（簡報、摘要、對比分析、綜合報告）。
4) **在 Notion 中草擬**：使用 `Notion:notion-create-pages` 並搭配對應模板（快速版、摘要版、對比版、綜合版）進行編寫。
5) **建立連結**：連結至來源並新增參考文獻/引用章節；隨著新資訊加入，使用 `Notion:notion-update-page` 進行更新。

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

### 1) 收集來源資訊
- 先行搜尋 (`Notion:notion-search`)；優化查詢詞，若出現多個結果請要求使用者確認。
- 獲取相關頁面 (`Notion:notion-fetch`)，略讀其中的事實、指標、主張、限制條件與日期。
- 追蹤每個來源的網址/ID 以供後續引用；對關鍵事實優先採用直接引述方式。

### 2) 選擇格式
- 快速報告 (Quick readout) → 快速簡報 (Quick brief)。
- 單一主題深入研究 → 研究摘要 (Research summary)。
- 選項權衡分析 → 對比分析 (Comparison)。
- 深度探討 / 高階主管就緒 (Exec-ready) → 綜合報告 (Comprehensive report)。
- 參見 `reference/format-selection-guide.md` 以了解各格式的適用時機。

### 3) 綜整資訊 (Synthesize)
- 撰寫前先列大綱；按主題或問題對發現進行分組。
- 標註具備來源 ID 的證據；標記資訊空白處或矛盾之處。
- 始終牢記使用者目標（決策、摘要、計畫、建議）。

### 4) 建立文件
- 從 `reference/` 中選擇匹配的模板（簡報、摘要、對比、綜合）並進行調整。
- 使用 `Notion:notion-create-pages` 建立頁面；內容應包含標題、摘要、關鍵發現、支持證據，以及在相關時提供建議/後續步驟。
- 新增行內引用 (Inline citations) 與參考文獻章節；建立連回來源頁面的連結。

### 5) 定稿與交付
- 加入亮點、風險與待解決問題。
- 若使用者需要後續跟進，在頁面中建立任務或檢查清單；在適用時連結任何任務資料庫條目。
- 更新時，透過 `Notion:notion-update-page` 分享簡短的變更日誌或狀態。

## 參考資料與範例
- `reference/` — 搜尋技巧、格式選擇、模板以及引用規則（例如：`advanced-search.md`, `format-selection-guide.md`, `research-summary-template.md`, `comparison-template.md`, `citations.md`）。
- `examples/` — 完整的端到端流程範例（例如：`competitor-analysis.md`, `technical-investigation.md`, `market-research.md`, `trip-planning.md`）。
