---
name: mcp-builder
description: 建立高品質 MCP (Model Context Protocol) 伺服器的指南，使 LLM 能夠透過精心設計的工具與外部服務互動。在建構整合外部 API 或服務的 MCP 伺服器時使用，無論是使用 Python (FastMCP) 還是 Node/TypeScript (MCP SDK)。
license: 完整條款請參閱 LICENSE.txt
---

# MCP 伺服器開發指南 (MCP Server Development Guide)

## 概覽 (Overview)

若要建立高品質的 MCP (Model Context Protocol) 伺服器，使 LLM 能夠有效地與外部服務互動，請使用此技能。MCP 伺服器提供工具，讓 LLM 可以存取外部服務與 API。MCP 伺服器的品質取決於它能否讓 LLM 利用所提供的工具順利完成現實世界的任務。

---

# 開發流程 (Process)

## 🚀 高層級工作流程 (High-Level Workflow)

建立高品質的 MCP 伺服器包含四個主要階段：

### 第一階段：深度研究與規劃

#### 1.1 理解「以代理人為中心」的設計原則 (Agent-Centric Design)

在深入實作之前，請透過審閱以下原則來了解如何為 AI 代理人 (Agents) 設計工具：

**為工作流程而建，而非僅為了 API 端點：**
- 不要只是簡單地封裝現有的 API 端點——要建構深思熟慮且具備高影響力的工作流程工具。
- 整合相關操作（例如：建立一個 `schedule_event` 工具，同時執行檢查可用性與建立活動）。
- 專注於能完成完整任務的工具，而非單個 API 調用。
- 思考代理人實際需要完成哪些工作流程。

**針對有限的上下文進行優化：**
- 代理人的上下文視窗 (Context Window) 有限——讓每個權杖 (Token) 都發揮作用。
- 回傳高價值的資訊，而非詳盡的數據堆砌。
- 提供「簡明」對比「詳細」的回應格式選項。
- 預設使用人類可讀的識別碼而非技術代碼（例如使用名稱而非 ID）。
- 將代理人的上下文預算視為稀缺資源。

**設計具引導性的錯誤訊息 (Actionable Error Messages)：**
- 錯誤訊息應引導代理人採取正確的使用模式。
- 建議具體的後續步驟：例如「嘗試使用 filter='active_only' 以減少結果數量」。
- 讓錯誤訊息具備教育意義，而不僅僅是診斷問題。
- 透過清晰的回饋協助代理人學習正確的工具用法。

**遵循自然的任務劃分：**
- 工具名稱應反映人類思考任務的方式。
- 使用一致的前綴對相關工具進行分組，以提高可發現性 (Discoverability)。
- 圍繞自然的工作流程設計工具，而非僅根據 API 結構。

**採用評估驅動開發 (Evaluation-Driven Development)：**
- 儘早建立現實的評估場景。
- 根據代理人的回饋來改進工具。
- 快速製作原型並根據代理人的實際表現進行迭代。

#### 1.3 研讀 MCP 協定文件

**獲取最新的 MCP 協定文件：**

使用 WebFetch 載入：`https://modelcontextprotocol.io/llms-full.txt`

這份綜合文件包含了完整的 MCP 規範與指南。

#### 1.4 研讀框架文件

**載入並閱讀以下參考檔案：**

- **MCP 最佳實踐**：[📋 查看最佳實踐](./reference/mcp_best_practices_zh_TW.md) - 所有 MCP 伺服器的核心指南。

**對於 Python 實作，亦請載入：**
- **Python SDK 文件**：使用 WebFetch 載入 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python 實作指南](./reference/python_mcp_server_zh_TW.md) - Python 特定的最佳實踐與範例。

**對於 Node/TypeScript 實作，亦請載入：**
- **TypeScript SDK 文件**：使用 WebFetch 載入 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript 實作指南](./reference/node_mcp_server_zh_TW.md) - Node/TypeScript 特定的最佳實踐與範例。

#### 1.5 詳盡研究 API 文件

為了整合某項服務，請通讀**所有**可用的 API 文件：
- 官方 API 參考文件。
- 認證 (Authentication) 與授權 (Authorization) 要求。
- 速率限制 (Rate limiting) 與分頁 (Pagination) 模式。
- 錯誤回應與狀態碼。
- 可用的端點及其參數。
- 數據模型與結構綱要 (Schemas)。

**若要收集全面資訊，請視需要使用網頁搜尋與 WebFetch 工具。**

#### 1.6 制定綜合實作計畫

根據您的研究，制定一個詳細計畫，包含：

**工具選擇：**
- 列出最值得實作的端點/操作。
- 優先處理能實現最常見且最重要使用案例的工具。
- 思考哪些工具可以協同工作以實現複雜的工作流程。

**共用公用程式與輔助函式 (Utilities & Helpers)：**
- 識別常見的 API 請求模式。
- 規劃分頁輔助函式。
- 設計過濾與格式化公用程式。
- 規劃錯誤處理策略。

**輸入/輸出設計：**
- 定義輸入驗證模型（Python 使用 Pydantic，TypeScript 使用 Zod）。
- 設計一致的回應格式（例如 JSON 或 Markdown），以及可配置的細節層級（例如「詳細」或「簡明」）。
- 為大規模使用（數千名使用者/資源）做準備。
- 實作字元限制與截斷 (Truncation) 策略（例如 25,000 個 Token）。

**錯誤處理策略：**
- 規劃優雅的失敗模式。
- 設計清晰、可執行且對 LLM 友善的自然語言錯誤訊息，並能提示後續行動。
- 考慮速率限制與逾時情境。
- 處理認證與授權錯誤。

---

### 第二階段：實作

現在您已經有了一份綜合計畫，請根據特定語言的最佳實踐開始實作。

#### 2.1 設定專案結構

**對於 Python：**
- 建立單個 `.py` 檔案，或在結構複雜時組織成模組（參見 [🐍 Python 指南](./reference/python_mcp_server_zh_TW.md)）。
- 使用 MCP Python SDK 進行工具註冊。
- 定義 Pydantic 模型用於輸入驗證。

**對於 Node/TypeScript：**
- 建立適當的專案結構（參見 [⚡ TypeScript 指南](./reference/node_mcp_server_zh_TW.md)）。
- 設定 `package.json` 與 `tsconfig.json`。
- 使用 MCP TypeScript SDK。
- 定義 Zod 結構綱要用於輸入驗證。

#### 2.2 先實作核心基礎設施

**在實作工具之前，先建立共用公用程式：**
- API 請求輔助函式。
- 錯誤處理公用程式。
- 回應格式化函式（JSON 與 Markdown）。
- 分頁輔助函式。
- 認證/權杖 (Token) 管理。

#### 2.3 有系統地實作工具

針對計畫中的每個工具：

**定義輸入結構綱要 (Input Schema)：**
- 使用 Pydantic (Python) 或 Zod (TypeScript) 進行驗證。
- 包含適當的約束（最小/最大長度、正則表達式、最小/最大值、範圍）。
- 提供清晰且具描述性的欄位說明。
- 在欄位說明中包含多樣化的範例。

**撰寫詳盡的文件字串 (Docstrings) / 描述：**
- 工具功能的單行總結。
- 對目的與功能的詳細解釋。
- 明確的參數類型與範例。
- 完整的傳回類型結構綱要。
- 使用範例（何時使用，何時不使用）。
- 錯誤處理文件，概述在遇到特定錯誤時應如何繼續。

**實作工具邏輯：**
- 使用共用公用程式以避免程式碼重複。
- 對所有 I/O 遵循 async/await 模式。
- 實作適當的錯誤處理。
- 支援多種回應格式（JSON 與 Markdown）。
- 尊重分頁參數。
- 檢查字元限制並進行適當截斷。

**新增工具註釋 (Annotations)：**
- `readOnlyHint`: true (用於唯讀操作)
- `destructiveHint`: false (用於非破壞性操作)
- `idempotentHint`: true (如果重複調用具備相同效果，即冪等性)
- `openWorldHint`: true (如果與外部系統互動)

#### 2.4 遵循特定語言的最佳實踐

**此時請載入對應的語言指南：**

**針對 Python：載入 [🐍 Python 實作指南](./reference/python_mcp_server_zh_TW.md) 並確保以下事項：**
- 使用帶有正確工具註冊的 MCP Python SDK。
- 使用具備 `model_config` 的 Pydantic v2 模型。
- 全程使用型別提示 (Type hints)。
- 所有 I/O 操作皆使用 Async/await。
- 正確組織 Import 語句。
- 模組級常數（CHARACTER_LIMIT, API_BASE_URL）。

**針對 Node/TypeScript：載入 [⚡ TypeScript 實作指南](./reference/node_mcp_server_zh_TW.md) 並確保以下事項：**
- 正確使用 `server.registerTool`。
- 使用帶有 `.strict()` 的 Zod 結構綱要。
- 啟用了 TypeScript 嚴格模式 (Strict mode)。
- 不使用 `any` 類型——請使用正確的型別。
- 明確的 Promise<T> 傳回類型。
- 配置好建置程序 (`npm run build`)。

---

### 第三階段：審查與精煉

初步實作後：

#### 3.1 程式碼品質審查

為了確保品質，請審查程式碼中的：
- **DRY 原則**：工具之間沒有重複的程式碼。
- **組合性 (Composability)**：共用邏輯已擷取至函式中。
- **一致性**：相似的操作回傳相似的格式。
- **錯誤處理**：所有外部調用皆有錯誤處理。
- **型別安全**：完整的型別覆蓋（Python 型別提示、TypeScript 型別）。
- **文件**：每個工具都有詳盡的文件字串/描述。

#### 3.2 測試與建置

**重要提示：** MCP 伺服器是長時間執行的程序，透過 stdio/stdin 或 sse/http 等候請求。直接在主程序中執行它們（例如 `python server.py` 或 `node dist/index.js`）會導致程序無限期卡住 (Hang)。

**測試伺服器的安全方法：**
- 使用評估工具包 (Evaluation Harness)（參見第四階段）——**推薦方法**。
- 在 `tmux` 中執行伺服器，使其位於主程序之外。
- 測試時使用逾時限制：`timeout 5s python server.py`。

**對於 Python：**
- 驗證 Python 語法：`python -m py_compile your_server.py`
- 透過審閱檔案檢查 Import 是否正常運作。
- 手動測試：在 `tmux` 中執行伺服器，然後在主程序中使用評估工具包進行測試。
- 或直接使用評估工具包（它會負責管理 stdio 傳輸的伺服器）。

**對於 Node/TypeScript：**
- 執行 `npm run build` 並確保無誤完成。
- 驗證 `dist/index.js` 已建立。
- 手動測試：在 `tmux` 中執行伺服器，然後在主程序中使用評估工具包進行測試。
- 或直接使用評估工具包（它會負責管理 stdio 傳輸的伺服器）。

#### 3.3 使用品質檢查清單

若要驗證實作品質，請載入特定語言指南中的檢查清單：
- Python：參見 [🐍 Python 指南](./reference/python_mcp_server_zh_TW.md) 中的「品質檢查清單」。
- Node/TypeScript：參見 [⚡ TypeScript 指南](./reference/node_mcp_server_zh_TW.md) 中的「品質檢查清單」。

---

### 第四階段：建立評估 (Evaluations)

實作 MCP 伺服器後，請建立綜合評估以測試其成效。

**載入 [✅ 評估指南](./reference/evaluation_zh_TW.md) 以獲得完整的評估準則。**

#### 4.1 理解評估的目的

評估旨在測試 LLM 能否有效地使用您的 MCP 伺服器來回答現實且複雜的問題。

#### 4.2 建立 10 個評估問題

若要建立有效的評估，請遵循評估指南中概述的流程：

1. **工具檢查**：列出可用工具並了解其功能。
2. **內容探索**：使用「唯讀」操作來探索可用數據。
3. **問題生成**：建立 10 個複雜且現實的問題。
4. **答案驗證**：親自解決每個問題以驗證答案。

#### 4.3 評估要求

每個問題必須符合：
- **獨立性**：不依賴於其他問題。
- **唯讀**：僅需要非破壞性操作。
- **複雜度**：需要多次工具調用與深入探索。
- **現實性**：基於人類關心的真實使用案例。
- **可驗證性**：單一且清晰的答案，可透過字串比對進行驗證。
- **穩定性**：答案不會隨著時間推移而改變。

#### 4.4 輸出格式

建立一個具備以下結構的 XML 檔案：

```xml
<evaluation>
  <qa_pair>
    <question>尋找有關使用動物代號命名的 AI 模型發布討論。其中一個模型需要一個格式為 ASL-X 的特定安全等級。請問以斑點野貓命名的模型被確定的數字 X 是多少？</question>
    <answer>3</answer>
  </qa_pair>
<!-- 更多 qa_pairs... -->
</evaluation>
```

---

# 參考檔案 (Reference Files)

## 📚 文件庫

開發過程中視需要載入這些資源：

### 核心 MCP 文件（優先載入）
- **MCP 協定**：從 `https://modelcontextprotocol.io/llms-full.txt` 獲取完整的 MCP 規範。
- [📋 MCP 最佳實踐](./reference/mcp_best_practices_zh_TW.md) - 通用的 MCP 指南，包含：
  - 伺服器與工具命名慣例。
  - 回應格式準則 (JSON vs Markdown)。
  - 分頁最佳實踐。
  - 字元限制與截斷策略。
  - 工具開發指南。
  - 安全與錯誤處理標準。

### SDK 文件（第一/二階段載入）
- **Python SDK**：從 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 獲取。
- **TypeScript SDK**：從 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 獲取。

### 特定語言實作指南（第二階段載入）
- [🐍 Python 實作指南](./reference/python_mcp_server_zh_TW.md) - 完整的 Python/FastMCP 指南，包含：
  - 伺服器初始化模式。
  - Pydantic 模型範例。
  - 使用 `@mcp.tool` 進行工具註冊。
  - 完整的運作範例。
  - 品質檢查清單。

- [⚡ TypeScript 實作指南](./reference/node_mcp_server_zh_TW.md) - 完整的 TypeScript 指南，包含：
  - 專案結構。
  - Zod 結構綱要模式。
  - 使用 `server.registerTool` 進行工具註冊。
  - 完整的運作範例。
  - 品質檢查清單。

### 評估指南（第四階段載入）
- [✅ 評估指南](./reference/evaluation_zh_TW.md) - 完整的評估建立指南，包含：
  - 問題建立準則。
  - 答案驗證策略。
  - XML 格式規範。
  - 範例問題與答案。
  - 使用提供的腳本執行評估。
