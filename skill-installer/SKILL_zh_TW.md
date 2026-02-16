---
name: skill-installer
description: 從精選清單或 GitHub 儲存庫路徑安裝 Codex 技能至 $CODEX_HOME/skills。當使用者要求列出可安裝的技能、安裝精選技能，或從另一個儲存庫（包括私有儲存庫）安裝技能時使用。
metadata:
  short-description: 從 openai/skills 或其他儲存庫安裝精選技能
---

# 技能安裝程式 (Skill Installer)

協助安裝技能。預設來源為 https://github.com/openai/skills/tree/main/skills/.curated，但使用者也可以提供其他位置。

根據任務使用輔助腳本：
- 當使用者詢問有哪些可用技能，或者使用者在未指定動作的情況下使用此技能時，列出精選技能。
- 當使用者提供技能名稱時，從精選清單進行安裝。
- 當使用者提供 GitHub 儲存庫/路徑（包括私有儲存庫）時，從該儲存庫安裝。

使用輔助腳本安裝技能。

## 溝通訊息

列出精選技能時，根據使用者請求的上下文，輸出大致如下：
"""
來自 {repo} 的技能：
1. skill-1
2. skill-2（已安裝）
3. ...
您想要安裝哪一個？
"""

安裝完技能後，請告知使用者：「請重啟 Codex 以載入新技能。」

## 腳本說明

所有這些腳本都需要使用網路，因此在沙盒 (Sandbox) 環境中執行時，請請求權杖提升 (Escalation)。

- `scripts/list-curated-skills.py`（印出包含「已安裝」註記的精選清單）
- `scripts/list-curated-skills.py --format json`
- `scripts/install-skill-from-github.py --repo <擁有者>/<儲存庫> --path <技能路徑> [<技能路徑> ...]`
- `scripts/install-skill-from-github.py --url https://github.com/<擁有者>/<儲存庫>/tree/<引用>/<路徑>`

## 行為與選項

- 對於公開的 GitHub 儲存庫，預設採用直接下載。
- 如果下載因認證/權限錯誤而失敗，將回退至 Git 稀疏檢出 (Sparse checkout)。
- 如果目標技能目錄已存在，則中止作業。
- 安裝至 `$CODEX_HOME/skills/<技能名稱>`（預設為 `~/.codex/skills`）。
- 多個 `--path` 值可以在一次執行中安裝多個技能，除非提供了 `--name`，否則每個技能將按路徑的基本名稱 (Basename) 命名。
- 選項：`--ref <引用>`（預設為 `main`）、`--dest <路徑>`、`--method auto|download|git`。

## 註記

- 精選清單是透過 GitHub API 從 `https://github.com/openai/skills/tree/main/skills/.curated` 獲取的。如果無法存取，請解釋錯誤並退出。
- 私有 GitHub 儲存庫可以透過現有的 Git 憑證或選填的 `GITHUB_TOKEN`/`GH_TOKEN` 進行下載存取。
- Git 回退機制會先嘗試 HTTPS，接著嘗試 SSH。
- 位於 `https://github.com/openai/skills/tree/main/skills/.system` 的技能是預先安裝的，因此無需協助使用者安裝。如果他們詢問，只需解釋即可。如果他們堅持，您可以下載並覆蓋。
- 「已安裝」的註記來自對 `$CODEX_HOME/skills` 的檢查。
