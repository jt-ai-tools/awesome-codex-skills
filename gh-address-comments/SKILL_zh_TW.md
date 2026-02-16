---
name: gh-address-comments
description: 使用 gh CLI 協助處理當前分支開啟的 GitHub PR 中的審查/Issue 評論；先驗證 gh 認證狀態，若未登入則提示使用者進行認證。
metadata:
  short-description: 處理 GitHub PR 審查中的評論
---

# PR 評論處理器 (PR Comment Handler)

引導尋找當前分支開啟的 PR，並使用 gh CLI 處理其中的評論。請在執行所有 `gh` 指令時使用提升的網路存取權限 (Elevated network access)。

前置作業：確保 `gh` 已通過認證（例如執行過一次 `gh auth login`），然後以提升的權限執行 `gh auth status`（包含 workflow/repo 範圍），以確保 `gh` 指令能成功執行。如果沙盒 (Sandboxing) 封鎖了 `gh auth status`，請使用 `sandbox_permissions=require_escalated` 重新執行。

## 1) 檢查需要關注的評論
- 執行 `scripts/fetch_comments.py`，這將印出 PR 上所有的評論與審查討論串 (Review threads)。

## 2) 要求使用者澄清
- 為所有審查討論串與評論編號，並提供一個簡短摘要，說明修復該問題所需的動作。
- 詢問使用者應處理哪些編號的評論。

## 3) 如果使用者選擇了評論
- 針對所選評論套用修復方案。

註記：
- 如果 `gh` 在執行過程中遇到認證或速率限制 (Rate limit) 問題，請提示使用者使用 `gh auth login` 重新認證，然後重試。
