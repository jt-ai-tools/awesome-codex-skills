---
name: gh-fix-ci
description: 使用 gh 檢查 GitHub PR 檢查項 (Checks)、擷取失敗的 GitHub Actions 記錄、總結失敗上下文，並在使用者批准後建立修復計畫並執行。當使用者要求對 GitHub Actions 上失敗的 PR CI/CD 檢查進行偵錯或修復，且需要計畫與程式碼變更時使用；對於外部檢查（如 Buildkite），僅回報詳情網址並標記為範圍外。
metadata:
  short-description: 修復失敗的 GitHub CI Actions
---

# GitHub PR 檢查項修復計畫 (Gh Pr Checks Plan Fix)

## 概覽

使用 `gh` 定位失敗的 PR 檢查項，獲取可處理失敗的 GitHub Actions 日誌，總結失敗片段，並在獲得明確批准後提議修復計畫並執行。
- 依賴 `plan` 技能來起草與批准修復計畫。

前置作業：確保 `gh` 已通過認證（例如執行過一次 `gh auth login`），然後以提升的權限執行 `gh auth status`（包含 workflow/repo 範圍），以確保 `gh` 指令能成功執行。如果沙盒 (Sandboxing) 封鎖了 `gh auth status`，請使用 `sandbox_permissions=require_escalated` 重新執行。

## 輸入參數

- `repo`：儲存庫內的路徑（預設為 `.`）
- `pr`：PR 編號或網址（選填；預設為當前分支的 PR）
- 儲存庫主機的 `gh` 認證

## 快速開始

- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<編號或網址>"`
- 如果需要機器友善的輸出以便進行總結，請新增 `--json`。

## 工作流程

1. **驗證 gh 認證狀態**。
   - 在執行 `gh auth login` 後，於儲存庫中以提升的範圍 (workflow/repo) 執行 `gh auth status`。
   - 如果沙盒化的認證狀態檢查失敗，請使用 `sandbox_permissions=require_escalated` 重新執行指令，以允許存取網路/金鑰圈 (Keyring)。
   - 如果未認證，請要求使用者在繼續之前先登入。
2. **解析 PR**。
   - 優先選擇當前分支的 PR：`gh pr view --json number,url`。
   - 如果使用者提供了 PR 編號或網址，則直接使用。
3. **檢查失敗的檢查項（僅限 GitHub Actions）**。
   - **偏好方式**：執行隨附的腳本（處理 gh 欄位變更與作業日誌回退）：
     - `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<編號或網址>"`
     - 新增 `--json` 以獲得機器友善的輸出。
   - **手動回退方式**：
     - `gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow`
       - 如果某個欄位被拒絕，請使用 `gh` 回報的可用欄位重新執行。
     - 對於每個失敗的檢查項，從 `detailsUrl` 中擷取 Run ID 並執行：
       - `gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha`
       - `gh run view <run_id> --log`
     - 如果執行日誌顯示仍在進行中，請直接獲取作業 (Job) 日誌：
       - `gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs" > "<路徑>"`
4. **劃定非 GitHub Actions 檢查項的範圍**。
   - 如果 `detailsUrl` 不是 GitHub Actions 的執行記錄，請將其標記為「外部 (External)」並僅回報其網址。
   - 不要嘗試處理 Buildkite 或其他供應商；保持工作流程精簡。
5. **為使用者總結失敗情況**。
   - 提供失敗的檢查項名稱、執行網址（如有）以及簡潔的日誌片段。
   - 明確指出缺失的日誌。
6. **建立計畫**。
   - 使用 `plan` 技能起草一份簡潔的計畫並請求批准。
7. **批准後執行**。
   - 執行批准後的計畫，總結差異 (Diffs)/測試，並詢問是否要開啟 PR。
8. **重新檢查狀態**。
   - 變更後，建議重新執行相關測試與 `gh pr checks` 以進行確認。

## 隨附資源

### scripts/inspect_pr_checks.py

獲取失敗的 PR 檢查項，拉取 GitHub Actions 日誌，並擷取失敗片段。當仍存在失敗時以非零狀態碼退出，以便用於自動化流程。

使用範例：
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "123"`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "https://github.com/org/repo/pull/123" --json`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --max-lines 200 --context 40`
