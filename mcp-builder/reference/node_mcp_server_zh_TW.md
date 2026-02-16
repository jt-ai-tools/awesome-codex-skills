# Node/TypeScript MCP 伺服器實作指南 (Node/TypeScript MCP Server Implementation Guide)

## 概覽 (Overview)

本文件提供了使用 MCP TypeScript SDK 實作 MCP 伺服器時，Node/TypeScript 特定的最佳實踐與範例。內容涵蓋專案結構、伺服器設定、工具註冊模式、使用 Zod 進行輸入驗證、錯誤處理以及完整的運作範例。

---

## 快速參考 (Quick Reference)

### 關鍵匯入
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import axios, { AxiosError } from "axios";
```

### 伺服器初始化
```typescript
const server = new McpServer({
  name: "service-mcp-server",
  version: "1.0.0"
});
```

### 工具註冊模式
```typescript
server.registerTool("tool_name", {...config}, async (params) => {
  // 實作內容
});
```

---

## MCP TypeScript SDK

官方的 MCP TypeScript SDK 提供：
- `McpServer` 類別：用於伺服器初始化。
- `registerTool` 方法：用於工具註冊。
- Zod 結構綱要整合：用於執行階段的輸入驗證。
- 型別安全的工具處理程式實作。

完整細節請參閱參考資料中的 MCP SDK 文件。

## 伺服器命名慣例

Node/TypeScript MCP 伺服器必須遵循以下命名模式：
- **格式**：`{service}-mcp-server`（全小寫加連字號）。
- **範例**：`github-mcp-server`, `jira-mcp-server`, `stripe-mcp-server`。

名稱應具備以下特性：
- 通用性（不與特定功能綁定）。
- 能描述所整合的服務/API。
- 易於從任務描述中推斷。
- 不包含版本號或日期。

## 專案結構 (Project Structure)

為 Node/TypeScript MCP 伺服器建立以下結構：

```
{service}-mcp-server/
├── package.json
├── tsconfig.json
├── README.md
├── src/
│   ├── index.ts          # 包含 McpServer 初始化的主進入點
│   ├── types.ts          # TypeScript 型別定義與介面
│   ├── tools/            # 工具實作（每個領域一個檔案）
│   ├── services/         # API 客戶端與共用公用程式
│   ├── schemas/          # Zod 驗證結構綱要
│   └── constants.ts      # 共用常數 (API_URL, CHARACTER_LIMIT 等)
└── dist/                 # 建置後的 JavaScript 檔案 (進入點：dist/index.js)
```

## 工具實作 (Tool Implementation)

### 工具命名

工具名稱應使用蛇形命名法 (snake_case)（例如：`search_users`, `create_project`, `get_channel_info`），並使用清晰且以行動為導向的名稱。

**避免命名衝突**：包含服務上下文以防止重疊：
- 使用 `slack_send_message` 而非僅用 `send_message`。
- 使用 `github_create_issue` 而非僅用 `create_issue`。
- 使用 `asana_list_tasks` 而非僅用 `list_tasks`。

### 工具結構

工具使用 `registerTool` 方法註冊，並需符合以下要求：
- 使用 Zod 結構綱要進行執行階段輸入驗證與型別安全。
- 必須明確提供 `description` 欄位——JSDoc 註解**不會**被自動提取。
- 明確提供 `title`, `description`, `inputSchema` 與 `annotations`。
- `inputSchema` 必須是一個 Zod 結構綱要物件（而非 JSON Schema）。
- 明確定義所有參數與傳回值的型別。

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "example-mcp",
  version: "1.0.0"
});

// 用於輸入驗證的 Zod 結構綱要
const UserSearchInputSchema = z.object({
  query: z.string()
    .min(2, "搜尋字串至少需要 2 個字元")
    .max(200, "搜尋字串不得超過 200 個字元")
    .describe("與名稱/電子郵件匹配的搜尋字串"),
  limit: z.number()
    .int()
    .min(1)
    .max(100)
    .default(20)
    .describe("回傳的最大結果數量"),
  offset: z.number()
    .int()
    .min(0)
    .default(0)
    .describe("分頁時跳過的結果數量"),
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("輸出格式：'markdown' 用於人類可讀，'json' 用於機器可讀")
}).strict();

// 從 Zod 結構綱要衍生型別定義
type UserSearchInput = z.infer<typeof UserSearchInputSchema>;

server.registerTool(
  "example_search_users",
  {
    title: "搜尋範例使用者 (Search Example Users)",
    description: `在 Example 系統中按名稱、電子郵件或團隊搜尋使用者。

此工具搜尋 Example 平台上的所有使用者個人資料，支援部分匹配與各種搜尋過濾器。它「不會」建立或修改使用者，僅搜尋現有使用者。

參數 (Args):
  - query (string): 與名稱/電子郵件匹配的搜尋字串
  - limit (number): 回傳的最大結果數量，介於 1-100 之間 (預設: 20)
  - offset (number): 分頁時跳過的結果數量 (預設: 0)
  - response_format ('markdown' | 'json'): 輸出格式 (預設: 'markdown')

傳回值 (Returns):
  對於 JSON 格式：具備以下結構綱要的結構化數據：
  {
    "total": number,           // 找到的匹配項總數
    "count": number,           // 此回應中的結果數量
    "offset": number,          // 當前分頁偏移量
    "users": [
      {
        "id": string,          // 使用者 ID (例如 "U123456789")
        "name": string,        // 全名 (例如 "John Doe")
        "email": string,       // 電子郵件地址
        "team": string,        // 團隊名稱 (選填)
        "active": boolean      // 使用者是否活躍
      }
    ],
    "has_more": boolean,       // 是否有更多結果可用
    "next_offset": number      // 下一頁的偏移量 (若 has_more 為 true)
  }

使用範例：
  - 何時使用：「尋找行銷團隊的所有成員」 -> params 中 query="team:marketing"
  - 何時使用：「搜尋 John 的帳戶」 -> params 中 query="john"
  - 「不要」在何時使用：當您需要建立使用者時（請改用 example_create_user）

錯誤處理：
  - 若請求過多則回傳 "Error: Rate limit exceeded" (429 狀態碼)
  - 若搜尋結果為空則回傳 "No users found matching '<query>'"`,
    inputSchema: UserSearchInputSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true
    }
  },
  async (params: UserSearchInput) => {
    try {
      // 輸入驗證由 Zod 結構綱要處理
      // 使用驗證後的參數發送 API 請求
      const data = await makeApiRequest<any>(
        "users/search",
        "GET",
        undefined,
        {
          q: params.query,
          limit: params.limit,
          offset: params.offset
        }
      );

      const users = data.users || [];
      const total = data.total || 0;

      if (!users.length) {
        return {
          content: [{
            type: "text",
            text: `找不到與 '${params.query}' 匹配的使用者`
          }]
        };
      }

      // 根據要求的格式格式化回應
      let result: string;

      if (params.response_format === ResponseFormat.MARKDOWN) {
        // 人類可讀的 Markdown 格式
        const lines: string[] = [`# 使用者搜尋結果：'${params.query}'`, ""];
        lines.push(`找到 ${total} 位使用者（顯示其中 ${users.length} 位）`);
        lines.push("");

        for (const user of users) {
          lines.push(`## ${user.name} (${user.id})`);
          lines.push(`- **電子郵件**: ${user.email}`);
          if (user.team) {
            lines.push(`- **團隊**: ${user.team}`);
          }
          lines.push("");
        }

        result = lines.join("
");

      } else {
        // 機器可讀的 JSON 格式
        const response: any = {
          total,
          count: users.length,
          offset: params.offset,
          users: users.map((user: any) => ({
            id: user.id,
            name: user.name,
            email: user.email,
            ...(user.team ? { team: user.team } : {}),
            active: user.active ?? true
          }))
        };

        // 如果有更多結果，新增分頁資訊
        if (total > params.offset + users.length) {
          response.has_more = true;
          response.next_offset = params.offset + users.length;
        }

        result = JSON.stringify(response, null, 2);
      }

      return {
        content: [{
          type: "text",
          text: result
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: "text",
          text: handleApiError(error)
        }]
      };
    }
  }
);
```

## 使用 Zod 結構綱要進行輸入驗證

Zod 提供執行階段的型別驗證：

```typescript
import { z } from "zod";

// 具備驗證功能的基礎結構綱要
const CreateUserSchema = z.object({
  name: z.string()
    .min(1, "必須提供姓名")
    .max(100, "姓名不得超過 100 個字元"),
  email: z.string()
    .email("電子郵件格式無效"),
  age: z.number()
    .int("年齡必須是整數")
    .min(0, "年齡不能為負數")
    .max(150, "年齡不能大於 150")
}).strict();  // 使用 .strict() 禁止額外欄位

// 列舉 (Enums)
enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json"
}

const SearchSchema = z.object({
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("輸出格式")
});

// 帶有預設值的選填欄位
const PaginationSchema = z.object({
  limit: z.number()
    .int()
    .min(1)
    .max(100)
    .default(20)
    .describe("回傳的最大結果數量"),
  offset: z.number()
    .int()
    .min(0)
    .default(0)
    .describe("跳過的結果數量")
});
```

## 回應格式選項 (Response Format Options)

支援多種輸出格式以維持靈活性：

```typescript
enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json"
}

const inputSchema = z.object({
  query: z.string(),
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("輸出格式：'markdown' 用於人類可讀，'json' 用於機器可讀")
});
```

**Markdown 格式**：
- 使用標題、列表與格式化以增加清晰度。
- 將時間戳記轉換為人類可讀格式。
- 顯示名稱並在括號中附上 ID。
- 省略冗長的中繼資料。
- 邏輯性地對相關資訊進行分組。

**JSON 格式**：
- 回傳完整、結構化的數據，適合程式化處理。
- 包含所有可用欄位與中繼資料。
- 使用一致的欄位名稱與型別。

## 分頁實作 (Pagination Implementation)

對於列出資源的工具：

```typescript
const ListSchema = z.object({
  limit: z.number().int().min(1).max(100).default(20),
  offset: z.number().int().min(0).default(0)
});

async function listItems(params: z.infer<typeof ListSchema>) {
  const data = await apiRequest(params.limit, params.offset);

  const response = {
    total: data.total,
    count: data.items.length,
    offset: params.offset,
    items: data.items,
    has_more: data.total > params.offset + data.items.length,
    next_offset: data.total > params.offset + data.items.length
      ? params.offset + data.items.length
      : undefined
  };

  return JSON.stringify(response, null, 2);
}
```

## 字元限制與截斷 (Character Limits and Truncation)

新增 `CHARACTER_LIMIT` 常數以防止回應過大：

```typescript
// 在 constants.ts 的模組層級
export const CHARACTER_LIMIT = 25000;  // 最大回應字元數

async function searchTool(params: SearchInput) {
  let result = generateResponse(data);

  // 檢查字元限制，必要時進行截斷
  if (result.length > CHARACTER_LIMIT) {
    const truncatedData = data.slice(0, Math.max(1, data.length / 2));
    response.data = truncatedData;
    response.truncated = true;
    response.truncation_message =
      `回應已從 ${data.length} 個項目截斷至 ${truncatedData.length} 個項目。` +
      `請使用 'offset' 參數或新增過濾條件以查看更多結果。`;
    result = JSON.stringify(response, null, 2);
  }

  return result;
}
```

## 錯誤處理 (Error Handling)

提供清晰且具引導性的錯誤訊息：

```typescript
import axios, { AxiosError } from "axios";

function handleApiError(error: unknown): string {
  if (error instanceof AxiosError) {
    if (error.response) {
      switch (error.response.status) {
        case 404:
          return "錯誤：找不到資源。請檢查 ID 是否正確。";
        case 403:
          return "錯誤：權限不足。您沒有存取此資源的權限。";
        case 429:
          return "錯誤：超出速率限制。請稍後再嘗試請求。";
        default:
          return `錯誤：API 請求失敗，狀態碼為 ${error.response.status}`;
      }
    } else if (error.code === "ECONNABORTED") {
      return "錯誤：請求逾時。請再試一次。";
    }
  }
  return `錯誤：發生非預期錯誤：${error instanceof Error ? error.message : String(error)}`;
}
```

## 共用公用程式 (Shared Utilities)

將常用功能擷取到可重複使用的函式中：

```typescript
// 共用 API 請求函式
async function makeApiRequest<T>(
  endpoint: string,
  method: "GET" | "POST" | "PUT" | "DELETE" = "GET",
  data?: any,
  params?: any
): Promise<T> {
  try {
    const response = await axios({
      method,
      url: `${API_BASE_URL}/${endpoint}`,
      data,
      params,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      }
    });
    return response.data;
  } catch (error) {
    throw error;
  }
}
```

## Async/Await 最佳實踐

網路請求與 I/O 操作務必使用 async/await：

```typescript
// 優良：非同步網路請求
async function fetchData(resourceId: string): Promise<ResourceData> {
  const response = await axios.get(`${API_URL}/resource/${resourceId}`);
  return response.data;
}

// 拙劣：使用 Promise 鏈
function fetchData(resourceId: string): Promise<ResourceData> {
  return axios.get(`${API_URL}/resource/${resourceId}`)
    .then(response => response.data);  // 難以閱讀與維護
}
```

## TypeScript 最佳實踐

1. **使用嚴格模式 (Strict TypeScript)**：在 `tsconfig.json` 中啟用 `strict` 模式。
2. **定義介面 (Interfaces)**：為所有數據結構建立清晰的介面定義。
3. **避免使用 `any`**：使用正確的型別或 `unknown` 取代 `any`。
4. **使用 Zod 進行執行階段驗證**：使用 Zod 結構綱要驗證外部數據。
5. **型別守衛 (Type Guards)**：為複雜的型別檢查建立型別守衛函式。
6. **錯誤處理**：始終使用 try-catch 並進行正確的錯誤型別檢查。
7. **空值安全 (Null Safety)**：使用選用鏈結 (`?.`) 與空值合併 (`??`)。

```typescript
// 優良：結合 Zod 與介面的型別安全
interface UserResponse {
  id: string;
  name: string;
  email: string;
  team?: string;
  active: boolean;
}

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  team: z.string().optional(),
  active: z.boolean()
});

type User = z.infer<typeof UserSchema>;

async function getUser(id: string): Promise<User> {
  const data = await apiCall(`/users/${id}`);
  return UserSchema.parse(data);  // 執行階段驗證
}

// 拙劣：使用 any
async function getUser(id: string): Promise<any> {
  return await apiCall(`/users/${id}`);  // 失去型別安全
}
```

## 封裝配置 (Package Configuration)

### package.json

```json
{
  "name": "{service}-mcp-server",
  "version": "1.0.0",
  "description": "{Service} API 整合的 MCP 伺服器",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "clean": "rm -rf dist"
  },
  "engines": {
    "node": ">=18"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.6.1",
    "axios": "^1.7.9",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/node": "^22.10.0",
    "tsx": "^4.19.2",
    "typescript": "^5.7.2"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "allowSyntheticDefaultImports": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## 完整範例 (Complete Example)

```typescript
#!/usr/bin/env node
/**
 * Example 服務的 MCP 伺服器。
 *
 * 此伺服器提供與 Example API 互動的工具，包括使用者搜尋、
 * 專案管理與數據匯出功能。
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import axios, { AxiosError } from "axios";

// 常數
const API_BASE_URL = "https://api.example.com/v1";
const CHARACTER_LIMIT = 25000;

// 列舉
enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json"
}

// Zod 結構綱要
const UserSearchInputSchema = z.object({
  query: z.string()
    .min(2, "搜尋字串至少需要 2 個字元")
    .max(200, "搜尋字串不得超過 200 個字元")
    .describe("與名稱/電子郵件匹配的搜尋字串"),
  limit: z.number()
    .int()
    .min(1)
    .max(100)
    .default(20)
    .describe("回傳的最大結果數量"),
  offset: z.number()
    .int()
    .min(0)
    .default(0)
    .describe("分頁時跳過的結果數量"),
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("輸出格式：'markdown' 用於人類可讀，'json' 用於機器可讀")
}).strict();

type UserSearchInput = z.infer<typeof UserSearchInputSchema>;

// 共用輔助函式
async function makeApiRequest<T>(
  endpoint: string,
  method: "GET" | "POST" | "PUT" | "DELETE" = "GET",
  data?: any,
  params?: any
): Promise<T> {
  try {
    const response = await axios({
      method,
      url: `${API_BASE_URL}/${endpoint}`,
      data,
      params,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      }
    });
    return response.data;
  } catch (error) {
    throw error;
  }
}

function handleApiError(error: unknown): string {
  if (error instanceof AxiosError) {
    if (error.response) {
      switch (error.response.status) {
        case 404:
          return "錯誤：找不到資源。請檢查 ID 是否正確。";
        case 403:
          return "錯誤：權限不足。您沒有存取此資源的權限。";
        case 429:
          return "錯誤：超出速率限制。請稍後再嘗試請求。";
        default:
          return `錯誤：API 請求失敗，狀態碼為 ${error.response.status}`;
      }
    } else if (error.code === "ECONNABORTED") {
      return "錯誤：請求逾時。請再試一次。";
    }
  }
  return `錯誤：發生非預期錯誤：${error instanceof Error ? error.message : String(error)}`;
}

// 建立 MCP 伺服器實體
const server = new McpServer({
  name: "example-mcp",
  version: "1.0.0"
});

// 註冊工具
server.registerTool(
  "example_search_users",
  {
    title: "搜尋範例使用者 (Search Example Users)",
    description: `[此處省略上文顯示的完整描述]`,
    inputSchema: UserSearchInputSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true
    }
  },
  async (params: UserSearchInput) => {
    // 此處省略上文顯示的實作內容
  }
);

// 主函式
async function main() {
  // 必要時驗證環境變數
  if (!process.env.EXAMPLE_API_KEY) {
    console.error("錯誤：必須設定 EXAMPLE_API_KEY 環境變數");
    process.exit(1);
  }

  // 建立傳輸層
  const transport = new StdioServerTransport();

  // 將伺服器連線至傳輸層
  await server.connect(transport);

  console.error("Example MCP 伺服器正透過 stdio 執行");
}

// 啟動伺服器
main().catch((error) => {
  console.error("伺服器錯誤：", error);
  process.exit(1);
});
```

---

## 進階 MCP 功能

### 資源註冊 (Resource Registration)

將數據公開為資源，以實現高效的基於 URI 的存取：

```typescript
import { ResourceTemplate } from "@modelcontextprotocol/sdk/types.js";

// 使用 URI 模板註冊資源
server.registerResource(
  {
    uri: "file://documents/{name}",
    name: "文件資源",
    description: "按名稱存取文件",
    mimeType: "text/plain"
  },
  async (uri: string) => {
    // 從 URI 中擷取參數
    const match = uri.match(/^file:\/\/documents\/(.+)$/);
    if (!match) {
      throw new Error("URI 格式無效");
    }

    const documentName = match[1];
    const content = await loadDocument(documentName);

    return {
      contents: [{
        uri,
        mimeType: "text/plain",
        text: content
      }]
    };
  }
);

// 動態列出可用資源
server.registerResourceList(async () => {
  const documents = await getAvailableDocuments();
  return {
    resources: documents.map(doc => ({
      uri: `file://documents/${doc.name}`,
      name: doc.name,
      mimeType: "text/plain",
      description: doc.description
    }))
  };
});
```

**何時使用資源 (Resources) vs 工具 (Tools)：**
- **資源**：適用於使用簡單 URI 參數進行數據存取的場景。
- **工具**：適用於需要驗證與複雜商業邏輯的操作。
- **資源**：當數據相對靜態或基於模板時。
- **工具**：當操作具備副作用或涉及複雜工作流程時。

### 多種傳輸選項

TypeScript SDK 支援不同的傳輸機制：

```typescript
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

// Stdio 傳輸（預設 - 適用於 CLI 工具）
const stdioTransport = new StdioServerTransport();
await server.connect(stdioTransport);

// SSE 傳輸（適用於即時網頁更新）
const sseTransport = new SSEServerTransport("/message", response);
await server.connect(sseTransport);

// HTTP 傳輸（適用於網頁服務）
// 根據您的 HTTP 框架整合進行配置
```

**傳輸選擇指引：**
- **Stdio**：命令列工具、子程序整合、本地開發。
- **HTTP**：網頁服務、遠端存取、多個併發客戶端。
- **SSE**：即時更新、伺服器推播通知、網頁儀表板。

### 通知支援 (Notification Support)

當伺服器狀態變更時通知客戶端：

```typescript
// 當工具清單變更時通知
server.notification({
  method: "notifications/tools/list_changed"
});

// 當資源變更時通知
server.notification({
  method: "notifications/resources/list_changed"
});
```

請謹慎使用通知——僅在伺服器能力確實發生變更時使用。

---

## 程式碼最佳實踐

### 程式碼組合性與可重複使用性

您的實作**必須**優先考慮組合性與程式碼重用：

1. **擷取共用功能**：
   - 為多個工具共用的操作建立可重複使用的輔助函式。
   - 為 HTTP 請求建構共用的 API 客戶端，而非重複撰寫程式碼。
   - 在公用程式函式中集中處理錯誤處理邏輯。
   - 將商業邏輯擷取到可被組合的專用函式中。
   - 擷取共用的 Markdown 或 JSON 欄位選擇與格式化功能。

2. **避免重複**：
   - 「絕不」在工具之間複製貼上相似的程式碼。
   - 如果您發現自己兩次編寫相似的邏輯，請將其擷取至函式中。
   - 分頁、過濾、欄位選擇與格式化等常見操作應共用。
   - 認證/授權邏輯應集中管理。

## 建置與執行

在執行前務必先建置您的 TypeScript 程式碼：

```bash
# 建置專案
npm run build

# 啟動伺服器
npm start

# 開發模式（自動重新載入）
npm run dev
```

在考慮實作完成前，請確保 `npm run build` 成功執行。

## 品質檢查清單 (Quality Checklist)

在完成您的 Node/TypeScript MCP 伺服器實作前，請確保：

### 策略性設計
- [ ] 工具旨在實現完整的工作流程，而非僅是 API 端點的封裝。
- [ ] 工具名稱反映了自然的任務劃分。
- [ ] 回應格式針對代理人的上下文效率進行了優化。
- [ ] 在合適處使用人類可讀的識別碼。
- [ ] 錯誤訊息能引導代理人採取正確用法。

### 實作品質
- [ ] **專注實作**：已實作最重要且最具價值的工具。
- [ ] 所有工具均使用 `registerTool` 進行註冊，並具備完整配置。
- [ ] 所有工具均包含 `title`, `description`, `inputSchema` 與 `annotations`。
- [ ] 註釋已正確設定 (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`)。
- [ ] 所有工具均使用 Zod 結構綱要進行執行階段輸入驗證，並強制執行 `.strict()`。
- [ ] 所有 Zod 結構綱要均具備適當約束與描述性的錯誤訊息。
- [ ] 所有工具均具備包含明確輸入/輸出型別的詳盡描述。
- [ ] 描述中包含傳回值範例與完整的結構綱要文件。
- [ ] 錯誤訊息清晰、具引導性且具備教育意義。

### TypeScript 品質
- [ ] 為所有數據結構定義了 TypeScript 介面。
- [ ] 在 `tsconfig.json` 中啟用了嚴格模式 (Strict mode)。
- [ ] 不使用 `any` 型別——改用 `unknown` 或正確的型別。
- [ ] 所有非同步函式均具備明確的 `Promise<T>` 傳回型別。
- [ ] 錯誤處理使用正確的型別守衛（例如 `axios.isAxiosError`, `z.ZodError`）。

### 進階功能（若適用）
- [ ] 為適當的數據端點註冊了資源。
- [ ] 配置了適當的傳輸層 (stdio, HTTP, SSE)。
- [ ] 針對動態伺服器能力實作了通知機制。
- [ ] 與 SDK 介面保持型別安全。

### 專案配置
- [ ] `package.json` 包含所有必要的依賴項。
- [ ] 建置腳本在 `dist/` 目錄中產出了可運作的 JavaScript。
- [ ] 主進入點已正確配置為 `dist/index.js`。
- [ ] 伺服器名稱遵循格式：`{service}-mcp-server`。
- [ ] `tsconfig.json` 已正確配置嚴格模式。

### 程式碼品質
- [ ] 在適用處已正確實作分頁功能。
- [ ] 大型回應會檢查 `CHARACTER_LIMIT` 常數，並附帶清晰訊息進行截斷。
- [ ] 為可能的大型結果集提供了過濾選項。
- [ ] 所有網路操作均能優雅處理逾時與連線錯誤。
- [ ] 常用功能已擷取至可重複使用的函式中。
- [ ] 相似操作的傳回型別保持一致。

### 測試與建置
- [ ] `npm run build` 成功完成且無誤。
- [ ] `dist/index.js` 已建立且可執行。
- [ ] 伺服器可執行：`node dist/index.js --help`。
- [ ] 所有匯入 (Imports) 均能正確解析。
- [ ] 範例工具調用運作符合預期。
