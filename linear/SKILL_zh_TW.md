---
name: linear
description: 在 Linear 中管理任務 (Issues)、專案與團隊工作流程。當使用者想要在 Linear 中讀取、建立或更新工單時使用。
---

# Linear

## 概覽 (Overview)

此技能為在 Linear 中管理任務、專案與團隊工作流程提供了一套結構化流程。它確保與 Linear MCP 伺服器的一致整合，該伺服器為任務、專案、文件與團隊協作提供自然語言的專案管理。

## 前置要求
- Linear MCP 伺服器必須已連線且可透過 OAuth 存取。
- 確認具備相關 Linear 工作區 (Workspace)、團隊與專案的存取權限。

## 必要工作流程

**請按順序執行以下步驟，切勿跳過。**

### 步驟 0：設定 Linear MCP（若尚未配置）

如果任何 MCP 調用因為 Linear MCP 未連線而失敗，請暫停並進行設定：

1. 新增 Linear MCP：
   - `codex mcp add linear --url https://mcp.linear.app/mcp`
2. 啟用遠端 MCP 客戶端：
   - 在 `config.toml` 中設定 `[features] rmcp_client = true` **或** 執行 `codex --enable rmcp_client`
3. 透過 OAuth 登入：
   - `codex mcp login linear`

成功登入後，使用者必須重新啟動 Codex。您應完成目前的回答並告知使用者，以便他們在下次嘗試時可以從「步驟 1」繼續。

**Windows/WSL 註記：** 如果您在 Windows 上看到連線錯誤，請嘗試配置 Linear MCP 透過 WSL 執行：
```json
{"mcpServers": {"linear": {"command": "wsl", "args": ["npx", "-y", "mcp-remote", "https://mcp.linear.app/sse", "--transport", "sse-only"]}}}
```

### 步驟 1
澄清使用者的目標與範圍（例如：任務優先級排序 [Triage]、衝刺計畫 [Sprint Planning]、文件稽核、工作量平衡）。視需要確認團隊/專案、優先級、標籤、週期 (Cycle) 與到期日。

### 步驟 2
選擇合適的工作流程（參見下方的「實用工作流程」）並識別您需要的 Linear MCP 工具。在調用工具前確認必要的識別碼（任務 ID、專案 ID、團隊金鑰）。

### 步驟 3
以邏輯批次執行 Linear MCP 工具調用：
- 先進行讀取（list/get/search）以建立背景資訊。
- 接著建立或更新（任務、專案、標籤、評論），並填入所有必填欄位。
- 對於大量操作，在套用變更前先解釋分組邏輯。

### 步驟 4
總結結果，指出剩餘的差距或阻礙因素 (Blockers)，並提議後續行動（額外的任務、標籤變更、指派對象或後續評論）。

## 可用工具

任務管理：`list_issues`, `get_issue`, `create_issue`, `update_issue`, `list_my_issues`, `list_issue_statuses`, `list_issue_labels`, `create_issue_label`

專案與團隊：`list_projects`, `get_project`, `create_project`, `update_project`, `list_teams`, `get_team`, `list_users`

文件與協作：`list_documents`, `get_document`, `search_documentation`, `list_comments`, `create_comment`, `list_cycles`

## 實用工作流程

- **衝刺計畫 (Sprint Planning)**：審查目標團隊的開啟任務，按優先級挑選首要項目，並建立帶有指派對象的新週期（例如：「Q1 效能衝刺」）。
- **Bug 優先級排序 (Bug Triage)**：列出嚴重/高優先級的 Bug，按使用者影響程度排名，並將首要項目移至「進行中 (In Progress)」。
- **文件稽核 (Documentation Audit)**：搜尋文件（例如：API 認證），針對遺漏或過時章節開啟標記為「documentation」的任務，並附上詳細的修復說明。
- **團隊工作量平衡**：按受指派者對活躍任務進行分組，標記負載過重的人員，並建議或執行重新分配。
- **發布計畫 (Release Planning)**：建立一個專案（例如：「v2.0 發布」）並設定里程碑（功能凍結、Beta 測試、文件、發布），同時生成帶有預估工時的任務。
- **跨專案依賴關係**：找出所有「已阻礙 (Blocked)」的任務，識別阻礙因素，若有遺漏則建立連結的任務。
- **自動狀態更新**：找出更新停滯的任務，並根據當前狀態/阻礙因素新增狀態評論。
- **智慧標籤**：分析未標籤的任務，建議或套用標籤，並建立缺失的標籤類別。
- **衝刺回顧 (Sprint Retrospectives)**：為最後完成的週期生成報告，註記已完成與推遲的工作，並針對特定模式開啟討論任務。

## 最大化效率的提示

- 針對相關變更進行批次操作；考慮為重複出現的任務結構使用智慧模板。
- 盡可能使用自然查詢（例如：「顯示 John 本週正在處理的事項」）。
- 利用背景資訊：在新的請求中參考先前的任務。
- 將大型更新拆分為較小的批次以避免速率限制 (Rate limits)；頻繁列出時請快取 (Cache) 或重複使用篩選器。

## 疑難排解

- **認證問題**：清除瀏覽器 Cookie、重新執行 OAuth、驗證工作區權限、確保已啟用 API 存取。
- **工具調用錯誤**：確認模型支援多個工具調用、提供所有必填欄位，並將複雜請求拆分。
- **數據缺失**：重新整理權杖 (Token)、驗證工作區存取權、檢查是否包含已封存專案，並確認選擇了正確的團隊。
- **效能問題**：注意 Linear API 的速率限制；批次執行大量操作、使用特定篩選器，或快取頻繁的查詢。
