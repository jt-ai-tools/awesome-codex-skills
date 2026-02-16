# MCP 伺服器開發最佳實踐與指南 (MCP Server Development Best Practices and Guidelines)

## 概覽 (Overview)

本文件彙整了建構模型上下文協定 (Model Context Protocol, MCP) 伺服器的重要最佳實踐與指南。內容涵蓋命名慣例、工具設計、回應格式、分頁、錯誤處理、安全性以及合規性要求。

---

## 快速參考 (Quick Reference)

### 伺服器命名
- **Python**：`{service}_mcp` (例如：`slack_mcp`)
- **Node/TypeScript**：`{service}-mcp-server` (例如：`slack-mcp-server`)

### 工具命名
- 使用蛇形命名法 (snake_case) 並加上服務前綴。
- 格式：`{service}_{action}_{resource}`
- 範例：`slack_send_message`, `github_create_issue`

### 回應格式
- 同時支援 JSON 與 Markdown 格式。
- JSON 用於程式化處理。
- Markdown 用於人類可讀性。

### 分頁 (Pagination)
- 務必尊重 `limit` 參數。
- 回傳 `has_more` (是否有更多)、`next_offset` (下一頁偏移量)、`total_count` (總數)。
- 預設為 20-50 筆項目。

### 字元限制
- 設定 `CHARACTER_LIMIT` 常數（通常為 25,000）。
- 優雅地截斷並提供清晰的提示訊息。
- 提供如何進行過濾的引導。

---

## 目錄
1. 伺服器命名慣例
2. 工具命名與設計
3. 回應格式指南
4. 分頁最佳實踐
5. 字元限制與截斷
6. 工具開發最佳實踐
7. 傳輸傳送最佳實踐
8. 測試要求
9. OAuth 與安全性最佳實踐
10. 資源管理最佳實踐
11. 提示詞管理最佳實踐
12. 錯誤處理標準
13. 文件要求
14. 合規性與監控

---

## 1. 伺服器命名慣例 (Server Naming Conventions)

請遵循以下標準化的 MCP 伺服器命名模式：

**Python**：使用 `{service}_mcp` 格式（全小寫加底線）。
- 範例：`slack_mcp`, `github_mcp`, `jira_mcp`, `stripe_mcp`

**Node/TypeScript**：使用 `{service}-mcp-server` 格式（全小寫加連字號）。
- 範例：`slack-mcp-server`, `github-mcp-server`, `jira-mcp-server`

名稱應具備以下特性：
- 通用性（不與特定功能綁定）。
- 能描述所整合的服務/API。
- 易於從任務描述中推斷。
- 不包含版本號或日期。

---

## 2. 工具命名與設計 (Tool Naming and Design)

### 工具命名最佳實踐

1. **使用蛇形命名法 (snake_case)**：例如 `search_users`, `create_project`, `get_channel_info`。
2. **包含服務前綴**：考慮到您的 MCP 伺服器可能會與其他 MCP 伺服器同時使用。
   - 使用 `slack_send_message` 而非僅用 `send_message`。
   - 使用 `github_create_issue` 而非僅用 `create_issue`。
   - 使用 `asana_list_tasks` 而非僅用 `list_tasks`。
3. **以行動為導向**：以動詞開頭（get, list, search, create 等）。
4. **具備具體性**：避免可能與其他伺服器衝突的通用名稱。
5. **保持一致性**：在伺服器內部使用一致的命名模式。

### 工具設計指南

- 工具描述必須狹義且無歧義地描述功能。
- 描述必須精確匹配實際功能。
- 不應對其他 MCP 伺服器造成混淆。
- 應提供工具註釋 (Annotations)：`readOnlyHint` (唯讀提示), `destructiveHint` (破壞性提示), `idempotentHint` (冪等提示), `openWorldHint` (開放世界提示)。
- 保持工具操作的專注與原子化 (Atomic)。

---

## 3. 回應格式指南 (Response Format Guidelines)

所有回傳數據的工具都應支援多種格式，以維持靈活性：

### JSON 格式 (`response_format="json"`)
- 機器可讀的結構化數據。
- 包含所有可用欄位與中繼資料 (Metadata)。
- 保持欄位名稱與類型的一致性。
- 適合程式化處理。
- 用於當 LLM 需要進一步處理數據時。

### Markdown 格式 (`response_format="markdown"`, 通常為預設)
- 人類可讀的格式化文本。
- 使用標題、列表與格式化以增加清晰度。
- 將時間戳記轉換為人類可讀格式（例如 "2024-01-15 10:30:00 UTC" 而非 Epoch 時間）。
- 顯示名稱時，在括號中附上 ID（例如 "@john.doe (U123456)"）。
- 省略冗長的細節（例如僅顯示一個頭像網址，而非所有尺寸）。
- 邏輯性地對相關資訊進行分組。
- 用於向使用者呈現資訊時。

---

## 4. 分頁最佳實踐 (Pagination Best Practices)

對於列出資源的工具：

- **務必尊重 `limit` 參數**：當指定了限制時，絕不要載入所有結果。
- **實作分頁功能**：使用 `offset` 或基於游標 (Cursor) 的分頁。
- **回傳分頁中繼資料**：包含 `has_more`, `next_offset`/`next_cursor`, `total_count`。
- **絕不要將所有結果載入記憶體**：對於大型數據集尤其重要。
- **預設合理的限制**：通常為 20-50 個項目。
- **在回應中包含清晰的分頁資訊**：使 LLM 易於請求更多數據。

範例分頁回應結構：
```json
{
  "total": 150,
  "count": 20,
  "offset": 0,
  "items": [...],
  "has_more": true,
  "next_offset": 20
}
```

---

## 5. 字元限制與截斷 (Character Limits and Truncation)

為了防止回應數據量過大導致負載過重：

- **定義 `CHARACTER_LIMIT` 常數**：通常在模組層級設定為 25,000 個字元。
- **在回傳前檢查回應大小**：衡量最終回應的長度。
- **以清晰的標示優雅地截斷**：告知 LLM 數據已被截斷。
- **提供過濾建議**：建議如何使用參數來減少結果數量。
- **包含截斷中繼資料**：顯示哪些內容被截斷以及如何獲取更多。

範例截斷處理：
```python
CHARACTER_LIMIT = 25000

if len(result) > CHARACTER_LIMIT:
    truncated_data = data[:max(1, len(data) // 2)]
    response["truncated"] = True
    response["truncation_message"] = (
        f"回應已從 {len(data)} 個項目截斷至 {len(truncated_data)} 個項目。"
        f"請使用 'offset' 參數或新增過濾條件以查看更多結果。"
    )
```

---

## 6. 傳輸傳送選項 (Transport Options)

MCP 伺服器支援多種傳輸機制，適用於不同部署場景：

### Stdio 傳輸

**最適用於**：命令列工具、本地整合、子程序 (Subprocess) 執行。

**特性**：
- 標準輸入/輸出串流通訊。
- 設定簡單，無需網路配置。
- 作為客戶端的子程序執行。
- 桌面應用程式與 CLI 工具的理想選擇。

**何時使用**：
- 建構本地開發環境工具。
- 與桌面應用程式（如 Claude Desktop）整合。
- 建立命令列公用程式。
- 單一使用者、單一環節 (Session) 的場景。

### HTTP 傳輸

**最適用於**：網頁服務、遠端存取、多客戶端場景。

**特性**：
- 基於 HTTP 的「請求-回應」模式。
- 支援多個併發客戶端。
- 可部署為網頁服務。
- 需要考慮網路配置與安全性。

**何時使用**：
- 同時為多個客戶端提供服務。
- 部署為雲端服務。
- 與網頁應用程式整合。
- 需要負載平衡或擴展性時。

### 伺服器傳送事件 (SSE) 傳輸

**最適用於**：即時更新、推播通知、串流數據。

**特性**：
- 基於 HTTP 的單向「伺服器對客戶端」串流。
- 無需輪詢 (Polling) 即可實現即時更新。
- 支援持續數據流的長連線。
- 建構於標準 HTTP 基礎設施之上。

**何時使用**：
- 客戶端需要即時數據更新。
- 實作推播通知。
- 串流日誌或監控數據。
- 長時間操作的漸進式結果交付。

### 傳輸選擇標準

| 準則 | Stdio | HTTP | SSE |
|-----------|-------|------|-----|
| **部署方式** | 本地 | 遠端 | 遠端 |
| **客戶端數** | 單一 | 多個 | 多個 |
| **通訊方式** | 雙向 | 請求-回應 | 伺服器推播 |
| **複雜度** | 低 | 中 | 中-高 |
| **即時性** | 否 | 否 | 是 |

---

## 7. 工具開發最佳實踐 (Tool Development Best Practices)

### 一般準則
1. 工具名稱應具備描述性且以行動為導向。
2. 使用詳細的 JSON Schema 進行參數驗證。
3. 在工具描述中包含範例。
4. 實作適當的錯誤處理與驗證。
5. 針對長時間操作使用進度回報。
6. 保持工具操作的專注與原子化。
7. 文件化預期的傳回值結構。
8. 實作適當的逾時機制。
9. 針對耗資源操作考慮速率限制。
10. 記錄工具使用日誌以便偵錯與監控。

### 工具安全性考量

#### 輸入驗證
- 根據 Schema 驗證所有參數。
- 消毒 (Sanitize) 檔案路徑與系統指令。
- 驗證 URL 與外部識別碼。
- 檢查參數大小與範圍。
- 防止指令注入 (Command Injection)。

#### 存取控制
- 在需要處實作認證。
- 使用適當的授權檢查。
- 稽核工具使用情況。
- 限制請求速率。
- 監控濫用行為。

#### 錯誤處理
- 不要將內部錯誤洩漏給客戶端。
- 記錄與安全相關的錯誤。
- 適當處理逾時。
- 發生錯誤後清理資源。
- 驗證傳回值。

### 工具註釋 (Tool Annotations)
- 提供 `readOnlyHint` 與 `destructiveHint` 註釋。
- 切記註釋僅是提示，而非安全保證。
- 客戶端不應僅基於註釋做出關鍵安全性決策。

---

## 8. 傳輸傳送最佳實踐 (Transport Best Practices)

### 一般傳輸準則
1. 正確處理連線生命週期。
2. 實作適當的錯誤處理。
3. 使用合適的逾時值。
4. 實作連線狀態管理。
5. 斷開連線時清理資源。

### 傳輸安全性最佳實踐
- 遵循針對 DNS 重導向攻擊 (DNS Rebinding Attacks) 的安全性考量。
- 實作適當的認證機制。
- 驗證訊息格式。
- 優雅地處理格式錯誤的訊息。

### Stdio 傳輸特定規範
- 本地 MCP 伺服器**不得**記錄日誌至 `stdout`（會干擾協定執行）。
- 使用 `stderr` 記錄日誌訊息。
- 正確處理標準 I/O 串流。

---

## 9. 測試要求 (Testing Requirements)

綜合測試策略應涵蓋：

### 功能測試
- 驗證使用有效/無效輸入時的執行正確性。

### 整合測試
- 測試與外部系統的互動。

### 安全性測試
- 驗證認證、輸入消毒、速率限制。

### 效能測試
- 檢查在高負載、逾時情況下的行為。

### 錯誤處理
- 確保正確的錯誤回報與資源清理。

---

## 10. OAuth 與安全性最佳實踐

### 認證與授權 (Authentication and Authorization)

連線至外部服務的 MCP 伺服器應實作正確的認證：

**OAuth 2.1 實作**：
- 使用具備受信任憑證的安全性 OAuth 2.1。
- 在處理請求前驗證存取權杖 (Access Token)。
- 僅接受明確指定給您伺服器的權杖。
- 拒絕缺乏正確受眾 (Audience) 聲明的權杖。
- 絕不要直接透傳從 MCP 客戶端接收到的權杖。

**API 金鑰管理**：
- 將 API 金鑰儲存在環境變數中，絕不要寫在程式碼中。
- 在伺服器啟動時驗證金鑰。
- 認證失敗時提供清晰的錯誤訊息。
- 對敏感憑證使用加密傳輸。

### 輸入驗證與安全性

**務必驗證輸入**：
- 消毒檔案路徑以防止目錄穿越 (Directory Traversal)。
- 驗證 URL 與外部識別碼。
- 檢查參數大小與範圍。
- 防止系統調用中的指令注入。
- 對所有輸入使用 Schema 驗證（Pydantic/Zod）。

**錯誤處理安全性**：
- 不要將內部錯誤洩漏給客戶端。
- 在伺服器端記錄安全相關錯誤。
- 提供有幫助但不過度揭露細節的錯誤訊息。
- 發生錯誤後清理資源。

### 隱私與數據保護

**數據收集原則**：
- 僅收集功能運作絕對必要的數據。
- 不要收集無關的對話數據。
- 除非工具目的明確要求，否則不收集個人識別資訊 (PII)。
- 針對存取的數據提供清晰的說明。

**數據傳輸**：
- 未經揭露不得將數據發送至您組織外的伺服器。
- 對所有網路通訊使用加密傳輸 (HTTPS)。
- 驗證外部服務的憑證。

---

## 11. 資源管理最佳實踐

1. 僅建議必要的資源。
2. 為根目錄 (Roots) 使用清晰且具描述性的名稱。
3. 正確處理資源邊界。
4. 尊重客戶端對資源的控制。
5. 使用由模型控制的原語（工具）來自動揭露數據。

---

## 12. 提示詞管理最佳實踐 (Prompt Management Best Practices)

- 客戶端應向使用者展示提議的提示詞。
- 使用者應能修改或拒絕提示詞。
- 客戶端應向使用者展示補全 (Completions) 結果。
- 使用者應能修改或拒絕補全結果。
- 使用取樣 (Sampling) 時需考慮成本。

---

## 13. 錯誤處理標準

- 使用標準的 JSON-RPC 錯誤代碼。
- 在結果物件中回報工具錯誤（而非協定層級）。
- 提供具幫助性且具體的錯誤訊息。
- 不要揭露內部實作細節。
- 發生錯誤時正確清理資源。

---

## 14. 文件要求 (Documentation Requirements)

- 提供所有工具與功能的清晰文件說明。
- 包含運作範例（每個主功能至少 3 個）。
- 文件化安全性考量。
- 詳述所需的權限與存取層級。
- 文件化速率限制與效能特性。

---

## 15. 合規性與監控

- 實作日誌紀錄以便偵錯與監控。
- 追蹤工具使用模式。
- 監控潛在的濫用行為。
- 為安全性相關操作維持稽核軌跡。
- 準備好應對持續性的合規性審查。

---

## 總結

這些最佳實踐代表了建構安全、高效且合規 MCP 伺服器的綜合指南，確保能在生態系統中良好運作。開發者應遵循這些準則，以確保其 MCP 伺服器符合納入 MCP 目錄的標準，並為使用者提供安全、可靠的體驗。


----------


# 工具 (Tools)

> 讓 LLM 能夠透過您的伺服器執行動作

工具是模型上下文協定 (MCP) 中的一個強大原語 (Primitive)，使伺服機能夠向客戶端公開可執行的功能。透過工具，LLM 可以與外部系統互動、執行運算，並在現實世界中採取行動。

<Note>
  工具被設計為**由模型控制 (model-controlled)**，這意味著工具從伺服器公開給客戶端，其意圖是讓 AI 模型能夠自動調用它們（但在關鍵時刻應由人類介入授權）。
</Note>

## 概覽 (Overview)

MCP 中的工具允許伺服器公開可執行的函式，這些函式可由客戶端調用並由 LLM 用於執行動作。工具的關鍵面向包括：

* **發現 (Discovery)**：客戶端可以透過發送 `tools/list` 請求來獲取可用工具的清單。
* **調用 (Invocation)**：工具透過 `tools/call` 請求被呼叫，伺服器執行請求的操作並回傳結果。
* **靈活性 (Flexibility)**：工具的範圍可以從簡單的運算到複雜的 API 互動。

與[資源 (Resources)](/docs/concepts/resources)類似，工具由唯一的名稱識別，並可包含引導其使用的描述。然而，與資源不同的是，工具代表了可以修改狀態或與外部系統互動的動態操作。

## 工具定義結構

每個工具的定義結構如下：

```typescript
{
  name: string;          // 工具的唯一識別碼
  description?: string;  // 人類可讀的描述
  inputSchema: {         // 工具參數的 JSON Schema
    type: "object",
    properties: { ... }  // 特定工具的參數
  },
  annotations?: {        // 關於工具行為的選填提示
    title?: string;      // 工具的人類可讀標題
    readOnlyHint?: boolean;    // 若為 true，代表工具不會修改其環境
    destructiveHint?: boolean; // 若為 true，代表工具可能會執行破壞性更新
    idempotentHint?: boolean;  // 若為 true，代表使用相同參數重複調用不會產生額外效果
    openWorldHint?: boolean;   // 若為 true，代表工具會與外部實體互動
  }
}
```

## 實作工具

以下是在 MCP 伺服器中實作基本工具的範例：

<Tabs>
  <Tab title="TypeScript">
    ```typescript
    const server = new Server({
      name: "example-server",
      version: "1.0.0"
    }, {
      capabilities: {
        tools: {}
      }
    });

    // 定義可用工具
    server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [{
          name: "calculate_sum",
          description: "將兩個數字相加",
          inputSchema: {
            type: "object",
            properties: {
              a: { type: "number" },
              b: { type: "number" }
            },
            required: ["a", "b"]
          }
        }]
      };
    });

    // 處理工具執行
    server.setRequestHandler(CallToolRequestSchema, async (request) => {
      if (request.params.name === "calculate_sum") {
        const { a, b } = request.params.arguments;
        return {
          content: [
            {
              type: "text",
              text: String(a + b)
            }
          ]
        };
      }
      throw new Error("找不到工具");
    });
    ```
  </Tab>

  <Tab title="Python">
    ```python
    app = Server("example-server")

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="calculate_sum",
                description="將兩個數字相加",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["a", "b"]
                }
            )
        ]

    @app.call_tool()
    async def call_tool(
        name: str,
        arguments: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name == "calculate_sum":
            a = arguments["a"]
            b = arguments["b"]
            result = a + b
            return [types.TextContent(type="text", text=str(result))]
        raise ValueError(f"找不到工具：{name}")
    ```
  </Tab>
</Tabs>

## 工具模式範例

以下是伺服器可以提供的一些工具類型範例：

### 系統操作

與本地系統互動的工具：

```typescript
{
  name: "execute_command",
  description: "執行 shell 指令",
  inputSchema: {
    type: "object",
    properties: {
      command: { type: "string" },
      args: { type: "array", items: { type: "string" } }
    }
  }
}
```

### API 整合

封裝外部 API 的工具：

```typescript
{
  name: "github_create_issue",
  description: "建立 GitHub issue",
  inputSchema: {
    type: "object",
    properties: {
      title: { type: "string" },
      body: { type: "string" },
      labels: { type: "array", items: { type: "string" } }
    }
  }
}
```

### 數據處理

轉換或分析數據的工具：

```typescript
{
  name: "analyze_csv",
  description: "分析 CSV 檔案",
  inputSchema: {
    type: "object",
    properties: {
      filepath: { type: "string" },
      operations: {
        type: "array",
        items: {
          enum: ["sum", "average", "count"]
        }
      }
    }
  }
}
```

## 最佳實踐

實作工具時：

1. 提供清晰、具描述性的名稱與描述。
2. 對參數使用詳細的 JSON Schema 定義。
3. 在工具描述中包含範例，演示模型應如何使用它們。
4. 實作適當的錯誤處理與驗證。
5. 針對長時間操作使用進度回報。
6. 保持工具操作的專注與原子化。
7. 文件化預期的傳回值結構。
8. 實作適當的逾時機制。
9. 針對耗資源操作考慮速率限制。
10. 記錄工具使用日誌以便偵錯與監控。

### 工具名稱衝突

MCP 客戶端應用程式與 MCP 伺服器代理在建立自己的工具清單時可能會遇到名稱衝突。例如，兩個連線的 MCP 伺服器 `web1` 與 `web2` 可能都公開了一個名為 `search_web` 的工具。

應用程式可以使用以下策略之一來消除歧義（但不限於此）：

* 將使用者定義的唯一伺服器名稱與工具名稱連接，例如 `web1___search_web` 與 `web2___search_web`。當使用者已在配置文件中提供唯一的伺服器名稱時，此策略較為理想。
* 為工具名稱生成隨機前綴，例如 `jrwxs___search_web` 與 `6cq52___search_web`。這在無法取得使用者定義名稱的伺服器代理中較為適用。
* 使用伺服器 URI 作為工具名稱的前綴，例如 `web1.example.com:search_web` 與 `web2.example.com:search_web`。這在與遠端 MCP 伺服器協作時非常合適。

請注意，初始化流程中伺服器提供的名稱不保證是唯一的，通常不適合直接用於消除歧義。

## 安全性考量

公開工具時：

### 輸入驗證

* 根據 Schema 驗證所有參數。
* 消毒檔案路徑與系統指令。
* 驗證 URL 與外部識別碼。
* 檢查參數大小與範圍。
* 防止指令注入。

### 存取控制

* 在需要處實作認證。
* 使用適當的授權檢查。
* 稽核工具使用情況。
* 限制請求速率。
* 監控濫用行為。

### 錯誤處理

* 不要將內部錯誤洩漏給客戶端。
* 記錄安全相關錯誤。
* 適當處理逾時。
* 發生錯誤後清理資源。
* 驗證傳回值。

## 工具發現與更新

MCP 支援動態工具發現：

1. 客戶端可以隨時列出可用工具。
2. 伺服器可以使用 `notifications/tools/list_changed` 在工具發生變更時通知客戶端。
3. 可以在執行階段新增或移除工具。
4. 工具定義可以更新（但應謹慎操作）。

## 錯誤處理

工具錯誤應在結果物件中回報，而非作為 MCP 協定層級的錯誤。這允許 LLM 看到並可能處理該錯誤。當工具遇到錯誤時：

1. 在結果中將 `isError` 設定為 `true`。
2. 在 `content` 陣列中包含錯誤詳情。

以下是工具正確處理錯誤的範例：

<Tabs>
  <Tab title="TypeScript">
    ```typescript
    try {
      // 工具操作
      const result = performOperation();
      return {
        content: [
          {
            type: "text",
            text: `操作成功：${result}`
          }
        ]
      };
    } catch (error) {
      return {
        isError: true,
        content: [
          {
            type: "text",
            text: `錯誤：${error.message}`
          }
        ]
      };
    }
    ```
  </Tab>

  <Tab title="Python">
    ```python
    try:
        # 工具操作
        result = perform_operation()
        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=f"操作成功：{result}"
                )
            ]
        )
    except Exception as error:
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"錯誤：{str(error)}"
                )
            ]
        )
    ```
  </Tab>
</Tabs>

這種方法允許 LLM 識別錯誤發生，並可能採取修正行動或請求人類介入。

## 工具註釋 (Tool Annotations)

工具註釋提供了關於工具行為的額外中繼資料，協助客戶端了解如何呈現與管理工具。這些註釋是描述工具性質與影響的提示，但不應作為安全決策的依據。

### 工具註釋的目的

工具註釋具備幾個關鍵目的：

1. 提供 UX 特有的資訊，且不影響模型上下文。
2. 協助客戶端適當地對工具進行分類與呈現。
3. 傳達關於工具潛在副作用的資訊。
4. 輔助開發直觀的工具授權介面。

### 可用的工具註釋

MCP 規範為工具定義了以下註釋：

| 註釋              | 類型    | 預設值 | 描述                                                                                                                          |
| ----------------- | ------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `title`           | string  | -       | 工具的人類可讀標題，適用於 UI 顯示。                                                                           |
| `readOnlyHint`    | boolean | false   | 若為 true，代表該工具不會修改其環境。                                                                          |
| `destructiveHint` | boolean | true    | 若為 true，代表該工具可能會執行破壞性更新（僅在 `readOnlyHint` 為 false 時有意義）。                                     |
| `idempotentHint`  | boolean | false   | 若為 true，代表使用相同參數重複調用該工具不會產生額外效果（僅在 `readOnlyHint` 為 false 時有意義）。 |
| `openWorldHint`   | boolean | true    | 若為 true，代表該工具可能會與外部實體的「開放世界」互動。                                                             |

### 使用範例

以下是如何在不同情境下定義帶有註釋的工具：

```typescript
// 唯讀的搜尋工具
{
  name: "web_search",
  description: "在網路上搜尋資訊",
  inputSchema: {
    type: "object",
    properties: {
      query: { type: "string" }
    },
    required: ["query"]
  },
  annotations: {
    title: "網頁搜尋",
    readOnlyHint: true,
    openWorldHint: true
  }
}

// 破壞性的檔案刪除工具
{
  name: "delete_file",
  description: "從檔案系統中刪除檔案",
  inputSchema: {
    type: "object",
    properties: {
      path: { type: "string" }
    },
    required: ["path"]
  },
  annotations: {
    title: "刪除檔案",
    readOnlyHint: false,
    destructiveHint: true,
    idempotentHint: true,
    openWorldHint: false
  }
}

// 非破壞性的資料庫紀錄建立工具
{
  name: "create_record",
  description: "在資料庫中建立新紀錄",
  inputSchema: {
    type: "object",
    properties: {
      table: { type: "string" },
      data: { type: "object" }
    },
    required: ["table", "data"]
  },
  annotations: {
    title: "建立資料庫紀錄",
    readOnlyHint: false,
    destructiveHint: false,
    idempotentHint: false,
    openWorldHint: false
  }
}
```

### 在伺服器實作中整合註釋

<Tabs>
  <Tab title="TypeScript">
    ```typescript
    server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [{
          name: "calculate_sum",
          description: "將兩個數字相加",
          inputSchema: {
            type: "object",
            properties: {
              a: { type: "number" },
              b: { type: "number" }
            },
            required: ["a", "b"]
          },
          annotations: {
            title: "計算總和",
            readOnlyHint: true,
            openWorldHint: false
          }
        }]
      };
    });
    ```
  </Tab>

  <Tab title="Python">
    ```python
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("example-server")

    @mcp.tool(
        annotations={
            "title": "計算總和",
            "readOnlyHint": True,
            "openWorldHint": False
        }
    )
    async def calculate_sum(a: float, b: float) -> str:
        """將兩個數字相加。

        Args:
            a: 第一個加數
            b: 第二個加數
        """
        result = a + b
        return str(result)
    ```
  </Tab>
</Tabs>

### 工具註釋最佳實踐

1. **準確描述副作用**：清晰標示工具是否修改環境以及該修改是否具備破壞性。

2. **使用具描述性的標題**：提供清晰描述工具目的的人類友善標題。

3. **正確標示冪等性 (Idempotency)**：僅在重複調用確實不會產生額外效果時，才將工具標記為冪等。

4. **設定正確的開放/封閉世界提示**：標示工具是與封閉系統（如資料庫）還是開放系統（如網頁）互動。

5. **切記註釋僅是提示**：`ToolAnnotations` 中的所有屬性皆為提示，不保證能完全忠實地描述工具行為。客戶端絕不應僅基於註釋做出關鍵安全性決策。

## 測試工具

MCP 工具的綜合測試策略應涵蓋：

* **功能測試**：驗證工具在有效輸入下執行正確，並能適當處理無效輸入。
* **整合測試**：使用真實或模擬的依賴項 (Mocked Dependencies) 測試工具與外部系統的互動。
* **安全性測試**：驗證認證、授權、輸入消毒與速率限制。
* **效能測試**：檢查在高負載下的行為、逾時處理與資源清理。
* **錯誤處理**：確保工具能透過 MCP 協定正確回報錯誤並清理資源。
