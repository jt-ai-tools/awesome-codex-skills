---
name: connect-apps
description: 將 Claude 連接到外部應用程式，如 Gmail、Slack、GitHub。當使用者想要發送電子郵件、建立 Issue、發布訊息或在外部服務中執行動作時，請使用此技能。
---

# 連接應用程式 (Connect Apps)

將 Claude 連接到 1000 多個應用程式。不只是生成相關文字，而是真正發送電子郵件、建立 Issue、發布訊息。

## 快速開始

### 第一步：安裝外掛程式

```
/plugin install composio-toolrouter
```

### 第二步：執行設定

```
/composio-toolrouter:setup
```

這將會：
- 要求您輸入免費的 API 金鑰（可在 [platform.composio.dev](https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills) 獲取）。
- 配置 Claude 與 1000 多個應用程式的連接。
- 過程大約需要 60 秒。

### 第三步：開始嘗試！

設定完成後，重新啟動 Claude Code 並嘗試執行：

```
發送一封測試郵件到我的信箱 YOUR_EMAIL@example.com
```

如果成功收到，代表您已連線成功！

## 您可以做什麼

| 要求 Claude... | 實際發生的動作 |
|------------------|--------------|
| 「發送電子郵件給 sarah@acme.com 關於發布會的事」 | 真正發送該郵件 |
| 「建立 GitHub issue：修復登入錯誤」 | 建立該 Issue |
| 「在 Slack #general 頻道發文：部署完成」 | 發布該訊息 |
| 「將會議記錄新增至 Notion」 | 新增到 Notion |

## 支援的應用程式

**電子郵件：** Gmail, Outlook, SendGrid
**通訊軟體：** Slack, Discord, Teams, Telegram
**開發工具：** GitHub, GitLab, Jira, Linear
**文件管理：** Notion, Google Docs, Confluence
**數據工具：** Sheets, Airtable, PostgreSQL
**以及其他 1000 多個應用程式...**

## 運作原理

1. 您向 Claude 提出任務要求。
2. Composio Tool Router 尋找合適的工具。
3. 第一次使用？您將透過 OAuth 進行授權（僅需一次）。
4. 執行動作並回傳結果。

## 疑難排解 (Troubleshooting)

- **「找不到外掛程式 (Plugin not found)」** → 請確保您已執行 `/plugin install composio-toolrouter`。
- **「需要授權 (Need to authorize)」** → 點擊 Claude 提供的 OAuth 連結，然後回覆「完成 (done)」。
- **動作失敗 (Action failed)** → 檢查您在目標應用程式中是否擁有足夠的權限。

---

<p align="center">
  <b>加入 20,000 多名開發者的行列，打造能落地的代理人</b>
</p>

<p align="center">
  <a href="https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills">
    <img src="https://img.shields.io/badge/Get_Started_Free-4F46E5?style=for-the-badge" alt="立即開始"/>
  </a>
</p>
