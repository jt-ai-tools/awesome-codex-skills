---
name: connect
description: 將 Codex 連接到任何應用程式。發送電子郵件、建立 Issue、發布訊息、更新資料庫——在 Gmail、Slack、GitHub、Notion 以及 1000 多個服務中執行真實動作。
---

# 連接 (Connect)

將 Codex 連接到任何應用程式。停止僅僅生成關於「您可以做什麼」的文字——現在就真正動手去做。

## 何時使用此技能

當您需要 Codex 執行以下操作時，請使用此技能：

- **真正發送郵件**，而不僅僅是草擬。
- **真正建立 Issue**，而不僅僅是描述它。
- **真正發布訊息**，而不僅僅是建議內容。
- **真正更新資料庫**，而不僅僅是解釋如何更新。

## 帶來的改變

| 沒有 Connect 時 | 使用 Connect 後 |
|-----------------|--------------|
| 「這是您的草稿郵件...」 | 直接發送郵件 |
| 「您應該建立一個 Issue...」 | 直接建立 Issue |
| 「把這段文字發到 Slack...」 | 直接發文 |
| 「把這個新增到 Notion...」 | 直接新增 |

## 支援的應用程式

**1000 多個整合功能**，包含：

- **電子郵件：** Gmail, Outlook, SendGrid
- **通訊軟體：** Slack, Discord, Teams, Telegram
- **開發工具：** GitHub, GitLab, Jira, Linear
- **文件管理：** Notion, Google Docs, Confluence
- **數據工具：** Sheets, Airtable, PostgreSQL
- **客戶關係管理 (CRM)：** HubSpot, Salesforce, Pipedrive
- **儲存空間：** Drive, Dropbox, S3
- **社群媒體：** Twitter, LinkedIn, Reddit

## 設定

### 1. 獲取 API 金鑰

在 [platform.composio.dev](https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills) 獲取您的免費金鑰。

### 2. 設定環境變數

```bash
export COMPOSIO_API_KEY="您的金鑰"
```

### 3. 安裝

```bash
pip install composio          # Python
npm install @composio/core    # TypeScript
```

大功告成。Codex 現在可以連接到任何應用程式了。

## 範例

### 發送電子郵件
```
Email sarah@acme.com - 主旨："已出貨！" 內容："v2.0 已上線，如有問題請告知"
```

### 建立 GitHub Issue
```
在 my-org/repo 建立 Issue："行動版逾時錯誤"，標籤：bug
```

### 在 Slack 發文
```
在 #engineering 頻道發文："部署完成 - v2.4.0 已上線"
```

### 鏈結動作 (Chain Actions)
```
找出本週標籤為 "bug" 的 GitHub Issue，進行摘要，並發布到 Slack 的 #bugs 頻道。
```

## 運作原理

使用 Composio Tool Router：

1. **您向 Codex 要求**執行任務。
2. **Tool Router 尋找**合適的工具（超過 1000 種選擇）。
3. **自動處理 OAuth**。
4. **執行動作**並回傳結果。

### 程式碼範例

```python
from composio import Composio
import os

composio = Composio(api_key=os.environ["COMPOSIO_API_KEY"])
session = composio.create(user_id="user_123")

options = {
    system_prompt="You can take actions in external apps.",
    mcp_servers={
        "composio": {
            "type": "http",
            "url": session.mcp.url,
            "headers": {"x-api-key": os.environ["COMPOSIO_API_KEY"]},
        }
    },
}

# 將這些選項交給 Codex（或您的 Agent 運行環境），以便工具調用透過 Composio 進行路由。
# Codex 提示範例："發送 Slack 訊息到 #general：您好！"
```

## 授權流程 (Auth Flow)

第一次使用某個應用程式時：
```
要發送電子郵件，我需要 Gmail 的存取權限。
請在此處授權：https://...
完成後請回覆「已連接 (connected)」。
```

之後連線將會持續有效。

## 框架支援

| 框架 | 安裝指令 |
|-----------|---------|
| OpenAI Agents | `pip install composio openai-agents` |
| Vercel AI | `npm install @composio/core @composio/vercel` |
| LangChain | `pip install composio-langchain` |
| 任何 MCP 客戶端 | 使用 `session.mcp.url` |

## 疑難排解 (Troubleshooting)

- **需要授權** → 點擊連結，完成授權，回覆「已連接」。
- **動作失敗** → 檢查您在目標應用程式中的權限。
- **找不到工具** → 請描述具體一點：例如「Slack #general」，而非僅僅「發送訊息」。

---

<p align="center">
  <b>加入 20,000 多名開發者的行列，打造能落地的代理人</b>
</p>

<p align="center">
  <a href="https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills">
    <img src="https://img.shields.io/badge/Get_Started_Free-4F46E5?style=for-the-badge" alt="立即開始"/>
  </a>
</p>
