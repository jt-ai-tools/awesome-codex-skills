# Python MCP 伺服器實作指南 (Python MCP Server Implementation Guide)

## 概覽 (Overview)

本文件提供了使用 MCP Python SDK 實作 MCP 伺服器時，Python 特定的最佳實踐與範例。內容涵蓋伺服器設定、工具註冊模式、使用 Pydantic 進行輸入驗證、錯誤處理以及完整的運作範例。

---

## 快速參考 (Quick Reference)

### 關鍵匯入
```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
import httpx
```

### 伺服器初始化
```python
mcp = FastMCP("service_mcp")
```

### 工具註冊模式
```python
@mcp.tool(name="tool_name", annotations={...})
async def tool_function(params: InputModel) -> str:
    # 實作內容
    pass
```

---

## MCP Python SDK 與 FastMCP

官方的 MCP Python SDK 提供了 FastMCP，這是一個用於建構 MCP 伺服器的高階框架。它具備：
- 根據函式簽名與文件字串 (Docstrings) 自動生成描述與 `inputSchema`。
- 整合 Pydantic 模型進行輸入驗證。
- 使用 `@mcp.tool` 裝飾器進行工具註冊。

**若要獲取完整的 SDK 文件，請使用 WebFetch 載入：**
`https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`

## 伺服器命名慣例

Python MCP 伺服器必須遵循以下命名模式：
- **格式**：`{service}_mcp`（全小寫加底線）。
- **範例**：`github_mcp`, `jira_mcp`, `stripe_mcp`。

名稱應具備以下特性：
- 通用性（不與特定功能綁定）。
- 能描述所整合的服務/API。
- 易於從任務描述中推斷。
- 不包含版本號或日期。

## 工具實作 (Tool Implementation)

### 工具命名

工具名稱應使用蛇形命名法 (snake_case)（例如：`search_users`, `create_project`, `get_channel_info`），並使用清晰且以行動為導向的名稱。

**避免命名衝突**：包含服務上下文以防止重疊：
- 使用 `slack_send_message` 而非僅用 `send_message`。
- 使用 `github_create_issue` 而非僅用 `create_issue`。
- 使用 `asana_list_tasks` 而非僅用 `list_tasks`。

### 使用 FastMCP 的工具結構

工具是使用 `@mcp.tool` 裝飾器定義的，並配合 Pydantic 模型進行輸入驗證：

```python
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 伺服器
mcp = FastMCP("example_mcp")

# 定義用於輸入驗證的 Pydantic 模型
class ServiceToolInput(BaseModel):
    '''服務工具操作的輸入模型。'''
    model_config = ConfigDict(
        str_strip_whitespace=True,  # 自動修剪字串前後空白
        validate_assignment=True,    # 賦值時進行驗證
        extra='forbid'              # 禁止額外欄位
    )

    param1: str = Field(..., description="第一個參數的描述 (例如 'user123', 'project-abc')", min_length=1, max_length=100)
    param2: Optional[int] = Field(default=None, description="具備約束的選填整數參數", ge=0, le=1000)
    tags: Optional[List[str]] = Field(default_factory=list, description="要套用的標籤列表", max_items=10)

@mcp.tool(
    name="service_tool_name",
    annotations={
        "title": "人類可讀的工具標題",
        "readOnlyHint": True,     # 工具不會修改環境
        "destructiveHint": False,  # 工具不會執行破壞性操作
        "idempotentHint": True,    # 重複調用沒有額外效果（冪等性）
        "openWorldHint": False     # 工具不會與外部實體互動
    }
)
async def service_tool_name(params: ServiceToolInput) -> str:
    '''工具描述會自動成為 'description' 欄位。

    此工具在服務上執行特定操作。在處理之前，它會使用
    ServiceToolInput Pydantic 模型驗證所有輸入。

    參數 (Args):
        params (ServiceToolInput): 已驗證的輸入參數，包含：
            - param1 (str): 第一個參數的描述
            - param2 (Optional[int]): 帶有預設值的選填參數
            - tags (Optional[List[str]]): 標籤清單

    傳回值 (Returns):
        str: 包含操作結果的 JSON 格式回應
    '''
    # 此處為實作內容
    pass
```

## Pydantic v2 關鍵特性

- 使用 `model_config` 取代嵌套的 `Config` 類別。
- 使用 `field_validator` 取代已棄用的 `validator`。
- 使用 `model_dump()` 取代已棄用的 `dict()`。
- 驗證器需要 `@classmethod` 裝飾器。
- 驗證器方法必須提供型別提示 (Type Hints)。

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict

class CreateUserInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    name: str = Field(..., description="使用者全名", min_length=1, max_length=100)
    email: str = Field(..., description="使用者電子郵件地址", pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., description="使用者年齡", ge=0, le=150)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("電子郵件不能為空")
        return v.lower()
```

## 回應格式選項 (Response Format Options)

支援多種輸出格式以維持靈活性：

```python
from enum import Enum

class ResponseFormat(str, Enum):
    '''工具回應的輸出格式。'''
    MARKDOWN = "markdown"
    JSON = "json"

class UserSearchInput(BaseModel):
    query: str = Field(..., description="搜尋查詢字串")
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="輸出格式：'markdown' 用於人類可讀，'json' 用於機器可讀"
    )
```

**Markdown 格式**：
- 使用標題、列表與格式化以增加清晰度。
- 將時間戳記轉換為人類可讀格式（例如 "2024-01-15 10:30:00 UTC" 而非 Epoch 時間）。
- 顯示名稱時，在括號中附上 ID（例如 "@john.doe (U123456)"）。
- 省略冗長的中繼資料（例如僅顯示一個頭像網址，而非所有尺寸）。
- 邏輯性地對相關資訊進行分組。

**JSON 格式**：
- 回傳完整、結構化的數據，適合程式化處理。
- 包含所有可用欄位與中繼資料。
- 使用一致的欄位名稱與型別。

## 分頁實作 (Pagination Implementation)

對於列出資源的工具：

```python
class ListInput(BaseModel):
    limit: Optional[int] = Field(default=20, description="回傳的最大結果數量", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="分頁時跳過的結果數量", ge=0)

async def list_items(params: ListInput) -> str:
    # 發送帶有分頁參數的 API 請求
    data = await api_request(limit=params.limit, offset=params.offset)

    # 回傳分頁資訊
    response = {
        "total": data["total"],
        "count": len(data["items"]),
        "offset": params.offset,
        "items": data["items"],
        "has_more": data["total"] > params.offset + len(data["items"]),
        "next_offset": params.offset + len(data["items"]) if data["total"] > params.offset + len(data["items"]) else None
    }
    return json.dumps(response, indent=2)
```

## 字元限制與截斷 (Character Limits and Truncation)

新增 `CHARACTER_LIMIT` 常數以防止回應過大：

```python
# 在模組層級
CHARACTER_LIMIT = 25000  # 最大回應字元數

async def search_tool(params: SearchInput) -> str:
    result = generate_response(data)

    # 檢查字元限制，必要時進行截斷
    if len(result) > CHARACTER_LIMIT:
        # 截斷數據並新增通知
        truncated_data = data[:max(1, len(data) // 2)]
        response["data"] = truncated_data
        response["truncated"] = True
        response["truncation_message"] = (
            f"回應已從 {len(data)} 個項目截斷至 {len(truncated_data)} 個項目。"
            f"請使用 'offset' 參數或新增過濾條件以查看更多結果。"
        )
        result = json.dumps(response, indent=2)

    return result
```

## 錯誤處理 (Error Handling)

提供清晰且具引導性的錯誤訊息：

```python
def _handle_api_error(e: Exception) -> str:
    '''所有工具一致的錯誤格式化。'''
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 404:
            return "錯誤：找不到資源。請檢查 ID 是否正確。"
        elif e.response.status_code == 403:
            return "錯誤：權限不足。您沒有存取此資源的權限。"
        elif e.response.status_code == 429:
            return "錯誤：超出速率限制。請稍後再嘗試請求。"
        return f"錯誤：API 請求失敗，狀態碼為 {e.response.status_code}"
    elif isinstance(e, httpx.TimeoutException):
        return "錯誤：請求逾時。請再試一次。"
    return f"錯誤：發生非預期錯誤：{type(e).__name__}"
```

## 共用公用程式 (Shared Utilities)

將常用功能擷取到可重複使用的函式中：

```python
# 共用 API 請求函式
async def _make_api_request(endpoint: str, method: str = "GET", **kwargs) -> dict:
    '''所有 API 調用的可重用函式。'''
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{API_BASE_URL}/{endpoint}",
            timeout=30.0,
            **kwargs
        )
        response.raise_for_status()
        return response.json()
```

## Async/Await 最佳實踐

網路請求與 I/O 操作務必使用 async/await：

```python
# 優良：非同步網路請求
async def fetch_data(resource_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/resource/{resource_id}")
        response.raise_for_status()
        return response.json()

# 拙劣：同步請求
def fetch_data(resource_id: str) -> dict:
    response = requests.get(f"{API_URL}/resource/{resource_id}")  # 會造成阻塞
    return response.json()
```

## 型別提示 (Type Hints)

全程使用型別提示：

```python
from typing import Optional, List, Dict, Any

async def get_user(user_id: str) -> Dict[str, Any]:
    data = await fetch_user(user_id)
    return {"id": data["id"], "name": data["name"]}
```

## 工具文件字串 (Docstrings)

每個工具必須具備包含明確型別資訊的詳盡文件字串：

```python
async def search_users(params: UserSearchInput) -> str:
    '''
    在 Example 系統中按名稱、電子郵件或團隊搜尋使用者。

    此工具搜尋 Example 平台上的所有使用者個人資料，支援部分匹配與各種搜尋過濾器。
    它「不會」建立或修改使用者，僅搜尋現有使用者。

    參數 (Args):
        params (UserSearchInput): 已驗證的輸入參數，包含：
            - query (str): 與名稱/電子郵件匹配的搜尋字串 (例如 "john", "@example.com", "team:marketing")
            - limit (Optional[int]): 回傳的最大結果數量，介於 1-100 之間 (預設: 20)
            - offset (Optional[int]): 分頁時跳過的結果數量 (預設: 0)

    傳回值 (Returns):
        str: 包含搜尋結果的 JSON 格式字串，具備以下結構綱要：

        成功回應：
        {
            "total": int,           # 找到的匹配項總數
            "count": int,           # 此回應中的結果數量
            "offset": int,          # 當前分頁偏移量
            "users": [
                {
                    "id": str,      # 使用者 ID (例如 "U123456789")
                    "name": str,    # 全名 (例如 "John Doe")
                    "email": str,   # 電子郵件地址 (例如 "john@example.com")
                    "team": str     # 團隊名稱 (例如 "Marketing") - 選填
                }
            ]
        }

        錯誤回應：
        "Error: <錯誤訊息>" 或 "No users found matching '<query>'"

    使用範例：
        - 何時使用：「尋找行銷團隊的所有成員」 -> params 中 query="team:marketing"
        - 何時使用：「搜尋 John 的帳戶」 -> params 中 query="john"
        - 「不要」在何時使用：當您需要建立使用者時（請改用 example_create_user）
        - 「不要」在何時使用：當您已有使用者 ID 並需要完整細節時（請改用 example_get_user）

    錯誤處理：
        - 輸入驗證錯誤由 Pydantic 模型處理
        - 若請求過多則回傳 "Error: Rate limit exceeded" (429 狀態碼)
        - 若 API 金鑰無效則回傳 "Error: Invalid API authentication" (401 狀態碼)
        - 回傳格式化後的結果列表或 "No users found matching 'query'"
    '''
```

## 完整範例 (Complete Example)

以下是一個完整的 Python MCP 伺服器範例：

```python
#!/usr/bin/env python3
'''
Example 服務的 MCP 伺服器。

此伺服器提供與 Example API 互動的工具，包括使用者搜尋、
專案管理與數據匯出功能。
'''

from typing import Optional, List, Dict, Any
from enum import Enum
import httpx
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 伺服器
mcp = FastMCP("example_mcp")

# 常數
API_BASE_URL = "https://api.example.com/v1"
CHARACTER_LIMIT = 25000  # 最大回應字元數

# 列舉
class ResponseFormat(str, Enum):
    '''工具回應的輸出格式。'''
    MARKDOWN = "markdown"
    JSON = "json"

# 用於輸入驗證的 Pydantic 模型
class UserSearchInput(BaseModel):
    '''使用者搜尋操作的輸入模型。'''
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    query: str = Field(..., description="與名稱/電子郵件匹配的搜尋字串", min_length=2, max_length=200)
    limit: Optional[int] = Field(default=20, description="回傳的最大結果數量", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="跳過的結果數量", ge=0)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="輸出格式")

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("查詢字串不能為空或僅包含空白")
        return v.strip()

# 共用輔助函式
async def _make_api_request(endpoint: str, method: str = "GET", **kwargs) -> dict:
    '''所有 API 調用的可重用函式。'''
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{API_BASE_URL}/{endpoint}",
            timeout=30.0,
            **kwargs
        )
        response.raise_for_status()
        return response.json()

def _handle_api_error(e: Exception) -> str:
    '''所有工具一致的錯誤格式化。'''
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 404:
            return "錯誤：找不到資源。請檢查 ID 是否正確。"
        elif e.response.status_code == 403:
            return "錯誤：權限不足。您沒有存取此資源的權限。"
        elif e.response.status_code == 429:
            return "錯誤：超出速率限制。請稍後再嘗試請求。"
        return f"錯誤：API 請求失敗，狀態碼為 {e.response.status_code}"
    elif isinstance(e, httpx.TimeoutException):
        return "錯誤：請求逾時。請再試一次。"
    return f"錯誤：發生非預期錯誤：{type(e).__name__}"

# 工具定義
@mcp.tool(
    name="example_search_users",
    annotations={
        "title": "搜尋範例使用者 (Search Example Users)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def example_search_users(params: UserSearchInput) -> str:
    '''在 Example 系統中按名稱、電子郵件或團隊搜尋使用者。

    [此處省略上文顯示的完整文件字串]
    '''
    try:
        # 使用驗證後的參數發送 API 請求
        data = await _make_api_request(
            "users/search",
            params={
                "q": params.query,
                "limit": params.limit,
                "offset": params.offset
            }
        )

        users = data.get("users", [])
        total = data.get("total", 0)

        if not users:
            return f"找不到與 '{params.query}' 匹配的使用者"

        # 根據要求的格式格式化回應
        if params.response_format == ResponseFormat.MARKDOWN:
            lines = [f"# 使用者搜尋結果：'{params.query}'", ""]
            lines.append(f"找到 {total} 位使用者（顯示其中 {len(users)} 位）")
            lines.append("")

            for user in users:
                lines.append(f"## {user['name']} ({user['id']})")
                lines.append(f"- **電子郵件**: {user['email']}")
                if user.get('team'):
                    lines.append(f"- **團隊**: {user['team']}")
                lines.append("")

            return "
".join(lines)

        else:
            # 機器可讀的 JSON 格式
            import json
            response = {
                "total": total,
                "count": len(users),
                "offset": params.offset,
                "users": users
            }
            return json.dumps(response, indent=2)

    except Exception as e:
        return _handle_api_error(e)

if __name__ == "__main__":
    mcp.run()
```

---

## 進階 FastMCP 功能

### 上下文參數注入 (Context Parameter Injection)

FastMCP 可以自動將 `Context` 參數注入到工具中，以啟用日誌紀錄、進度回報、資源讀取與使用者互動等進階功能：

```python
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("example_mcp")

@mcp.tool()
async def advanced_search(query: str, ctx: Context) -> str:
    '''具備上下文存取權限的進階工具，可用於日誌與進度回報。'''

    # 為長時間操作回報進度
    await ctx.report_progress(0.25, "正在開始搜尋...")

    # 記錄用於偵錯的資訊
    await ctx.log_info("正在處理查詢", {"query": query, "timestamp": datetime.now()})

    # 執行搜尋
    results = await search_api(query)
    await ctx.report_progress(0.75, "正在格式化結果...")

    # 存取伺服器配置
    server_name = ctx.fastmcp.name

    return format_results(results)

@mcp.tool()
async def interactive_tool(resource_id: str, ctx: Context) -> str:
    '''可以向使用者請求額外輸入的工具。'''

    # 在需要時請求敏感資訊
    api_key = await ctx.elicit(
        prompt="請提供您的 API 金鑰：",
        input_type="password"
    )

    # 使用提供的金鑰
    return await api_call(resource_id, api_key)
```

**Context 功能：**
- `ctx.report_progress(progress, message)` - 回報長時間操作的進度。
- `ctx.log_info(message, data)` / `ctx.log_error()` / `ctx.log_debug()` - 日誌紀錄。
- `ctx.elicit(prompt, input_type)` - 向使用者獲取輸入。
- `ctx.fastmcp.name` - 存取伺服器配置。
- `ctx.read_resource(uri)` - 讀取 MCP 資源。

### 資源註冊 (Resource Registration)

將數據公開為資源，以實現高效的、基於模板的存取：

```python
@mcp.resource("file://documents/{name}")
async def get_document(name: str) -> str:
    '''將文件公開為 MCP 資源。

    資源適用於不需要複雜參數的靜態或半靜態數據。
    它們使用 URI 模板實現靈活存取。
    '''
    document_path = f"./docs/{name}"
    with open(document_path, "r") as f:
        return f.read()

@mcp.resource("config://settings/{key}")
async def get_setting(key: str, ctx: Context) -> str:
    '''將配置公開為帶有上下文的資源。'''
    settings = await load_settings()
    return json.dumps(settings.get(key, {}))
```

**何時使用資源 (Resources) vs 工具 (Tools)：**
- **資源**：適用於參數簡單（URI 模板）的數據存取。
- **工具**：適用於需要驗證與商業邏輯的複雜操作。

### 結構化輸出型別 (Structured Output Types)

FastMCP 支援除了字串以外的多種傳回型別：

```python
from typing import TypedDict
from dataclasses import dataclass
from pydantic import BaseModel

# 用於結構化傳回的 TypedDict
class UserData(TypedDict):
    id: str
    name: str
    email: str

@mcp.tool()
async def get_user_typed(user_id: str) -> UserData:
    '''回傳結構化數據 - FastMCP 會處理序列化。'''
    return {"id": user_id, "name": "John Doe", "email": "john@example.com"}

# 用於複雜驗證的 Pydantic 模型
class DetailedUser(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    metadata: Dict[str, Any]

@mcp.tool()
async def get_user_detailed(user_id: str) -> DetailedUser:
    '''回傳 Pydantic 模型 - 會自動生成結構綱要。'''
    user = await fetch_user(user_id)
    return DetailedUser(**user)
```

### 生命週期管理 (Lifespan Management)

初始化可在多個請求間持久存在的資源：

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def app_lifespan():
    '''管理在伺服器存續期間內存在的資源。'''
    # 初始化連線、載入配置等
    db = await connect_to_database()
    config = load_configuration()

    # 使其對所有工具可用
    yield {"db": db, "config": config}

    # 關閉時進行清理
    await db.close()

mcp = FastMCP("example_mcp", lifespan=app_lifespan)

@mcp.tool()
async def query_data(query: str, ctx: Context) -> str:
    '''透過上下文存取生命週期資源。'''
    db = ctx.request_context.lifespan_state["db"]
    results = await db.query(query)
    return format_results(results)
```

### 多種傳輸選項

FastMCP 支援不同的傳輸機制：

```python
# 預設：Stdio 傳輸（適用於 CLI 工具）
if __name__ == "__main__":
    mcp.run()

# HTTP 傳輸（適用於網頁服務）
if __name__ == "__main__":
    mcp.run(transport="streamable_http", port=8000)

# SSE 傳輸（適用於即時更新）
if __name__ == "__main__":
    mcp.run(transport="sse", port=8000)
```

**傳輸選擇：**
- **Stdio**：命令列工具、子程序整合。
- **HTTP**：網頁服務、遠端存取、多客戶端。
- **SSE**：即時更新、推播通知。

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

### Python 特定最佳實踐

1. **使用型別提示 (Type Hints)**：始終為函式參數與傳回值包含型別註解。
2. **Pydantic 模型**：為所有輸入驗證定義清晰的 Pydantic 模型。
3. **避免手動驗證**：讓 Pydantic 透過約束條件來處理輸入驗證。
4. **正確的匯入 (Imports)**：將匯入分組（標準庫、第三方、本地）。
5. **錯誤處理**：使用特定的例外型別（如 `httpx.HTTPStatusError`，而非通用的 `Exception`）。
6. **非同步內容管理器**：對需要清理的資源使用 `async with`。
7. **常數**：在模組層級使用全大寫字母 (`UPPER_CASE`) 定義常數。

## 品質檢查清單 (Quality Checklist)

在完成您的 Python MCP 伺服器實作前，請確保：

### 策略性設計
- [ ] 工具旨在實現完整的工作流程，而非僅是 API 端點的封裝。
- [ ] 工具名稱反映了自然的任務劃分。
- [ ] 回應格式針對代理人的上下文效率進行了優化。
- [ ] 在合適處使用人類可讀的識別碼。
- [ ] 錯誤訊息能引導代理人採取正確用法。

### 實作品質
- [ ] **專注實作**：已實作最重要且最具價值的工具。
- [ ] 所有工具均具備描述性名稱與文件說明。
- [ ] 相似操作的傳回型別保持一致。
- [ ] 為所有外部調用實作了錯誤處理。
- [ ] 伺服器名稱遵循格式：`{service}_mcp`。
- [ ] 所有網路操作均使用 async/await。
- [ ] 常用功能已擷取至可重複使用的函式中。
- [ ] 錯誤訊息清晰、具引導性且具備教育意義。
- [ ] 輸出已正確驗證並格式化。

### 工具配置
- [ ] 所有工具均在裝飾器中實作了 'name' 與 'annotations'。
- [ ] 註釋已正確設定 (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`)。
- [ ] 所有工具均使用 Pydantic BaseModel 進行輸入驗證，並具備 `Field()` 定義。
- [ ] 所有 Pydantic Field 均具備明確型別、描述與約束條件。
- [ ] 所有工具均具備包含明確輸入/輸出型別的詳盡文件字串。
- [ ] 文件字串包含 dict/JSON 傳回值的完整結構。
- [ ] Pydantic 模型負責處理輸入驗證（無需手動驗證）。

### 進階功能（若適用）
- [ ] 使用了上下文注入來進行日誌紀錄、進度報報或獲取使用者輸入。
- [ ] 為適當的數據端點註冊了資源。
- [ ] 為持久連線實作了生命週期管理。
- [ ] 使用了結構化輸出型別 (TypedDict, Pydantic 模型)。
- [ ] 配置了適當的傳輸層 (stdio, HTTP, SSE)。

### 程式碼品質
- [ ] 檔案包含正確的匯入，包括 Pydantic 匯入。
- [ ] 在適用處已正確實作分頁功能。
- [ ] 大型回應會檢查 `CHARACTER_LIMIT` 並附帶清晰訊息進行截斷。
- [ ] 為可能的大型結果集提供了過濾選項。
- [ ] 所有非同步函式均使用 `async def` 正確定義。
- [ ] HTTP 客戶端的使用遵循非同步模式並配合正確的內容管理器。
- [ ] 程式碼中全程使用型別提示。
- [ ] 常數在模組層級以全大寫字母 (`UPPER_CASE`) 定義。

### 測試
- [ ] 伺服器成功執行：`python your_server.py --help`。
- [ ] 所有匯入均能正確解析。
- [ ] 範例工具調用運作符合預期。
- [ ] 錯誤情境能優雅處理。
