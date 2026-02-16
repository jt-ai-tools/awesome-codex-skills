<h1 align="center">Awesome Codex Skills</h1>

<p align="center">
<a href="https://platform.composio.dev/?utm_source=Github&utm_medium=Youtube&utm_campaign=2025-11&utm_content=AwesomeCodexSkills">

  <img width="1280" height="640" alt="Composio banner" src="codex_cover_image.png">
</a>
</p>

<p align="center">
  <a href="https://awesome.re">
    <img src="https://awesome.re/badge.svg" alt="Awesome" />
  </a>
  <a href="https://makeapullrequest.com">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome" />
  </a>
</p>
<div>
<p align="center">
  <a href="https://twitter.com/composio">
    <img src="https://img.shields.io/badge/Follow on X-000000?style=for-the-badge&logo=x&logoColor=white" alt="Follow on X" />
  </a>
  <a href="https://www.linkedin.com/company/composiohq/">
    <img src="https://img.shields.io/badge/Follow on LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="Follow on LinkedIn" />
  </a>
  <a href="https://discord.com/invite/composio">
    <img src="https://img.shields.io/badge/Join our Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Join our Discord" />
  </a>
  </p>
</div>

這是一份精選的實用 Codex 技能清單，旨在自動化 Codex CLI 與 API 的工作流程。

[English Version (README.md)](README_zh_TW.md)

> **想要能執行更多操作而不只是生成文字的技能嗎？** Codex 可以發送電子郵件、建立 Issue、在 Slack 發文，並在 1000 多個應用程式中執行動作。[查看詳情 →](./connect/SKILL_zh_TW.md)

---

## 快速開始：將技能新增至 Codex

### 使用技能安裝程式（推薦）

```bash
git clone https://github.com/ComposioHQ/awesome-codex-skills.git
cd awesome-codex-skills/awesome-codex-skills
# 將一或多個技能安裝到 $CODEX_HOME/skills（預設為 ~/.codex/skills）
python skill-installer/scripts/install-skill-from-github.py --repo ComposioHQ/awesome-codex-skills --path meeting-notes-and-actions
```

安裝程式會獲取技能並將其放置在 `$CODEX_HOME/skills/<skill-name>`。重新啟動 Codex 以載入新技能。

### 手動安裝

1. 將所需的技能資料夾（例如 `./spreadsheet-formula-helper`）複製到 `$CODEX_HOME/skills/`（預設為 `~/.codex/skills/`）。
2. 重新啟動 Codex 以便其載入新中繼資料。
3. 在下一次對話中，描述任務或提及技能名稱；Codex 將根據其 `SKILL.md` 中的 `description` 前言觸發匹配的技能。

---

## 目錄

- [什麼是 Codex 技能？](#什麼是-codex-技能)
- [技能](#技能)
  - [開發與程式碼工具](#開發與程式碼工具)
  - [生產力與協作](#生產力與協作)
  - [溝通與寫作](#溝通與寫作)
  - [數據與分析](#數據與分析)
  - [元指令與工具](#元指令與工具)
- [在 Codex 中使用技能](#在-codex-中使用技能)
- [建立技能](#建立技能)
- [貢獻](#貢獻)
- [加入社群](#加入社群)

## 什麼是 Codex 技能？

Codex 技能是模組化的指令組合，告知 Codex 如何按照您想要的方式執行任務。每個技能都位於其獨立資料夾中，包含一個 `SKILL.md`，其中包含中繼資料（名稱 + 描述）和逐步引導。Codex 讀取中繼資料以決定何時觸發技能，並僅在觸發後載入主體，以保持上下文精簡。

## 技能

### 開發與程式碼工具

- [create-plan/](./create-plan/SKILL_zh_TW.md) - 為程式開發任務快速起草簡明的執行計畫。
- [gh-address-comments/](./gh-address-comments/SKILL_zh_TW.md) - 使用 `gh` 指令處理當前分支開啟的 GitHub PR 中的評論或 Issue。
- [gh-fix-ci/](./gh-fix-ci/SKILL_zh_TW.md) - 檢查失敗的 GitHub Actions 檢測，總結錯誤並提出修復方案。
- [mcp-builder/](./mcp-builder/SKILL_zh_TW.md) - 使用最佳實踐和評估工具包建構與評估 MCP 伺服器。
- [webapp-testing/](./webapp-testing/SKILL_zh_TW.md) - 執行有針對性的 Web 應用程式測試並總結結果。

### 生產力與協作

- [connect/](./connect/SKILL_zh_TW.md) - 透過 Composio 將 Codex 連接到 1000 多個應用程式以執行真實動作（Slack, GitHub, Notion 等）。
- [connect-apps/](./connect-apps/SKILL_zh_TW.md) - 快速設定 Composio 應用程式連接，用於動作與工作流程。
- [linear/](./linear/SKILL_zh_TW.md) - 在 Linear 中管理 Issue、專案與團隊工作流程。
- [meeting-insights-analyzer/](./meeting-insights-analyzer/SKILL_zh_TW.md) - 分析會議逐字稿中的主題、風險與後續行動。
- [meeting-notes-and-actions/](./meeting-notes-and-actions/SKILL_zh_TW.md) - 將會議逐字稿轉化為包含決策與標記負責人的行動清單。
- [internal-comms/](./internal-comms/SKILL_zh_TW.md) - 撰寫內部公告、更新與利害關係人訊息。
- [invoice-organizer/](./invoice-organizer/SKILL_zh_TW.md) - 標準化並擷取發票數據，用於追蹤與報告。
- [notion-knowledge-capture/](./notion-knowledge-capture/SKILL_zh_TW.md) - 將聊天記錄或筆記轉換為結構化的 Notion 頁面並進行適當連結。
- [notion-meeting-intelligence/](./notion-meeting-intelligence/SKILL_zh_TW.md) - 利用 Notion 上下文與 Codex 研究準備會議資料。
- [notion-research-documentation/](./notion-research-documentation/SKILL_zh_TW.md) - 將多個 Notion 來源彙整為簡報、對比或報告，並附上引用。
- [notion-spec-to-implementation/](./notion-spec-to-implementation/SKILL_zh_TW.md) - 將 Notion 規格說明書轉化為執行計畫、任務與進度追蹤。
- [support-ticket-triage/](./support-ticket-triage/SKILL_zh_TW.md) - 處理客戶支援票券，包含分類、優先級、後續動作及草擬回覆。
- [file-organizer/](./file-organizer/SKILL_zh_TW.md) - 整理、重新命名並清理檔案，保持工作區整潔。
- [skill-share/](./skill-share/SKILL_zh_TW.md) - 在團隊成員間分享技能與可重複使用的指令。

### 溝通與寫作

- [email-draft-polish/](./email-draft-polish/SKILL_zh_TW.md) - 草擬、重寫或精簡電子郵件，以符合正確的語氣與受眾。
- [changelog-generator/](./changelog-generator/SKILL_zh_TW.md) - 從 Commit 或摘要建立清晰的變更日誌（Changelog）。
- [content-research-writer/](./content-research-writer/SKILL_zh_TW.md) - 研究並撰寫內容，並附上來源引用。
- [tailored-resume-generator/](./tailored-resume-generator/SKILL_zh_TW.md) - 根據職位描述量身定制履歷，並量化影響力。

### 數據與分析

- [spreadsheet-formula-helper/](./spreadsheet-formula-helper/SKILL_zh_TW.md) - 撰寫與偵錯試算表公式、樞紐分析表與陣列公式。
- [competitive-ads-extractor/](./competitive-ads-extractor/SKILL_zh_TW.md) - 分析競爭對手廣告並擷取結構化洞察。
- [developer-growth-analysis/](./developer-growth-analysis/SKILL_zh_TW.md) - 分析 Codex 聊天紀錄以識別程式碼模式與學習差距。
- [lead-research-assistant/](./lead-research-assistant/SKILL_zh_TW.md) - 研究潛在客戶並使用企業統計數據豐富記錄。
- [domain-name-brainstormer/](./domain-name-brainstormer/SKILL_zh_TW.md) - 根據標準與檢查發想可用的網域名稱。
- [raffle-winner-picker/](./raffle-winner-picker/SKILL_zh_TW.md) - 隨機抽取中獎者，並附帶稽核友善的紀錄。
- [langsmith-fetch/](./langsmith-fetch/SKILL_zh_TW.md) - 獲取 LangSmith 專案/測試數據進行分析。

### 元指令與工具

- [brand-guidelines/](./brand-guidelines/SKILL_zh_TW.md) - 將 OpenAI/Codex 品牌色彩與排版應用於成品。
- [canvas-design/](./canvas-design/SKILL_zh_TW.md) - 生成結構化的畫布佈局與設計成果。
- [image-enhancer/](./image-enhancer/SKILL_zh_TW.md) - 使用可配置的預設值放大並優化圖像。
- [slack-gif-creator/](./slack-gif-creator/SKILL_zh_TW.md) - 為 Slack 生成帶有文字說明與樣式的 GIF。
- [theme-factory/](./theme-factory/SKILL_zh_TW.md) - 建立可重複使用的主題權杖（Tokens）與調色盤。
- [video-downloader/](./video-downloader/SKILL_zh_TW.md) - 下載並準備影片以供離線查閱。
- [template-skill/](./template-skill/SKILL_zh_TW.md) - 建構新技能的入門模板。
- [skill-installer/](./skill-installer/SKILL_zh_TW.md) - 從精選清單或 GitHub 路徑安裝技能的輔助腳本。
- [skill-creator/](./skill-creator/SKILL_zh_TW.md) - 建立高效 Codex 技能的引導（具備漸進式揭露特性）。

## 在 Codex 中使用技能

- 技能存放在 `$CODEX_HOME/skills`（預設為 `~/.codex/skills`）。每個子資料夾都需要一個包含 `name` 和 `description` 前言的 `SKILL.md`。
- 安裝或更新技能後，請重新啟動 Codex 以便其重新載入中繼資料。
- 在對話中，自然地描述任務；Codex 會自動觸發其描述與請求相符的技能。如果您希望考慮特定技能，也可以直接提及技能名稱。
- 若要驗證安裝，請列出已安裝的技能 (`ls ~/.codex/skills`) 並檢查中繼資料 (`head ~/.codex/skills/<skill>/SKILL.md`)。

## 建立技能

技能佈局：

```
skill-name/
├── SKILL.md          # 必備：指令 + YAML 前言
├── scripts/          # 選配：用於確定性步驟的輔助腳本
├── references/       # 選配：僅在需要時載入的長篇文件
└── assets/           # 選配：輸出中使用的模板或檔案
```

基本 SKILL.md 模板：

```markdown
---
name: my-skill-name
description: 技能的功能以及 Codex 應該何時使用它。
---

# 技能名稱

Codex 執行任務的清晰指令與步驟。
```

最佳實踐：

- 讓 `description` 詳盡描述何時觸發；讓主體專注於執行步驟。
- 使用漸進式揭露：將詳細參考資料放入 `references/`，僅在需要時從 `SKILL.md` 調用。
- 為可重複或確定性的操作包含腳本；註明 Codex 應何時執行它們。
- 避免在技能資料夾內放置額外文件（README, changelog），以保持上下文精簡。

## 貢獻

歡迎提交 PR。請新增真實、可重複使用的技能，保持描述精確，並包含任何所需的腳本或參考資料。如果您新增了新技能，請確保 `description` 清楚說明 Codex 何時應觸發，並測試該中繼資料是否符合上下文限制。

## 加入社群

- [加入我們的 Discord](https://discord.com/invite/composio) - 與其他正在建構 Codex 技能的開發者交流。
- [關注 X](https://twitter.com/composio) - 獲取新技能與功能的更新。
- 有疑問嗎？ [support@composio.dev](mailto:support@composio.dev)

---

<p align="center">
  <b>加入數千名開發者的行列，打造能落地的代理人</b>
</p>

<p align="center">
  <a href="https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeCodexSkills">
    <img src="https://img.shields.io/badge/Get_Started_Free-4F46E5?style=for-the-badge" alt="Get Started"/>
  </a>
</p>
