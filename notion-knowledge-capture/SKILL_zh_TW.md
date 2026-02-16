---
name: notion-knowledge-capture
description: 將對話與決策擷取至結構化的 Notion 頁面中；當需要將聊天/筆記轉化為 Wiki 條目、操作指南、決策紀錄或附帶適當連結的 FAQ 時使用。
metadata:
  short-description: 將對話擷取至結構化的 Notion 頁面
---

# 知識擷取 (Knowledge Capture)

將對話與筆記轉化為結構化、可連結的 Notion 頁面，以便於重複使用。

## 快速開始
1) **釐清擷取內容**：明確要擷取的對象（決策、操作指南、FAQ、學習心得、技術文件）以及目標受眾。
2) **識別資料庫/模板**：在 `reference/` 中找到正確的資料庫或模板（團隊 Wiki、操作指南、FAQ、決策日誌、學習心得、技術文件）。
3) **拉取先前背景**：使用 `Notion:notion-search` → `Notion:notion-fetch` 從 Notion 獲取相關背景資訊（需更新或連結的現有頁面）。
4) **起草頁面**：使用資料庫的結構綱要 (Schema) 執行 `Notion:notion-create-pages`；內容應包含摘要、上下文、來源連結、標籤以及負責人。
5) **建立連結**：從核心頁面 (Hub pages) 或相關記錄建立連結；隨著資訊演進，使用 `Notion:notion-update-page` 更新狀態與負責人。

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

### 1) 定義擷取內容
- 詢問擷取目的、受眾、資訊時效性，以及這是新建立還是更新現有頁面。
- 確定內容類型：決策、操作指南 (How-to)、FAQ、概念/Wiki 條目、學習心得/筆記、技術文件頁面。

### 2) 定位目標位置
- 參考 `reference/*-database.md` 指南選擇正確的資料庫；確認必要的屬性（標題、標籤、負責人、狀態、日期、關聯）。
- 如果有多個候選資料庫，請詢問使用者要使用哪一個；否則，請在主要的 Wiki 或文件資料庫中建立。

### 3) 擷取與結構化
- 從對話中擷取事實、決策、行動與理由 (Rationale)。
- **針對決策**：記錄替代方案、決策邏輯與最終結果。
- **針對指南/文件**：擷取步驟、前置要求、資產/程式碼連結以及邊緣案例。
- **針對 FAQ**：以問答形式撰寫，提供簡潔的答案並連結至更深層的文件。

### 4) 在 Notion 中建立/更新
- 使用正確的 `data_source_id` 調用 `Notion:notion-create-pages`；設定各項屬性（標題、標籤、負責人、狀態、日期、關聯）。
- 使用 `reference/` 中的模板來架構內容（包含章節標題、檢查清單）。
- 如果是更新現有頁面，先獲取頁面內容，再透過 `Notion:notion-update-page` 進行編輯。

### 5) 建立連結並呈現
- 在核心頁面 (Hub pages)、相關規格書/文件或團隊頁面中新增關聯/反向連結 (Backlinks)。
- 為未來的讀者新增簡短的摘要或變更日誌 (Changelog)。
- 如果存在後續任務，請在相關資料夾中建立任務並進行連結。

## 參考資料與範例
- `reference/` — 資料庫結構綱要與模板（例如：`team-wiki-database.md`, `how-to-guide-database.md`, `faq-database.md`, `decision-log-database.md`, `documentation-database.md`, `learning-database.md`, `database-best-practices.md`）。
- `examples/` — 實務中的擷取模式（例如：`decision-capture.md`, `how-to-guide.md`, `conversation-to-faq.md`）。
