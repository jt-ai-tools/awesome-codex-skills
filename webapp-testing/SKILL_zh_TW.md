---
name: webapp-testing
description: 使用 Playwright 與本地網頁應用程式進行互動與測試的工具包。支持驗證前端功能、偵錯 UI 行為、擷取瀏覽器螢幕截圖以及查看瀏覽器日誌。
license: 完整條款請參閱 LICENSE.txt
---

# 網頁應用程式測試 (Web Application Testing)

若要測試本地網頁應用程式，請編寫原生的 Python Playwright 腳本。

**可用之輔助腳本**：
- `scripts/with_server.py` —— 管理伺服器生命週期（支援多個伺服器）。

**執行腳本前請務必先加上 `--help`** 以查看用法。除非您在嘗試執行後發現絕對需要自訂解決方案，否則「不要」閱讀腳本原始碼。這些腳本可能非常龐大，會污染您的上下文視窗。它們是以「黑箱 (Black-box)」形式直接調用的，而非用於載入至您的上下文。

## 決策樹：選擇您的處理方法

```
使用者任務 → 是靜態 HTML 嗎？
    ├─ 是 → 直接讀取 HTML 檔案以識別選擇器 (Selectors)
    │         ├─ 成功 → 使用選擇器編寫 Playwright 腳本
    │         └─ 失敗/不完整 → 視為動態應用（見下文）
    │
    └─ 否（動態網頁應用） → 伺服器是否已經在執行？
        ├─ 否 → 執行：python scripts/with_server.py --help
        │        然後使用輔助腳本 + 編寫簡化的 Playwright 腳本
        │
        └─ 是 → 採用「先勘查後執行」模式：
            1. 導航至頁面並等待網路閒置 (networkidle)
            2. 擷取螢幕截圖或檢查 DOM
            3. 從渲染後的狀態識別選擇器
            4. 使用找到的選擇器執行操作
```

## 範例：使用 with_server.py

若要啟動伺服器，請先執行 `--help`，然後使用輔助腳本：

**單一伺服器：**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**多個伺服器（例如：後端 + 前端）：**
```bash
python scripts/with_server.py 
  --server "cd backend && python server.py" --port 3000 
  --server "cd frontend && npm run dev" --port 5173 
  -- python your_automation.py
```

建立自動化腳本時，僅需包含 Playwright 邏輯（伺服器會被自動管理）：
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 務必以無頭模式 (Headless mode) 啟動 Chromium
    browser = p.chromium.launch(headless=True) 
    page = browser.new_page()
    page.goto('http://localhost:5173') # 伺服器已啟動並就緒
    # 關鍵：等待 JS 執行完成
    page.wait_for_load_state('networkidle') 
    # ... 您的自動化邏輯
    browser.close()
```

## 「先勘查後執行」模式 (Reconnaissance-Then-Action)

1. **檢查渲染後的 DOM**：
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **識別選擇器**：根據檢查結果確定選擇器。

3. **執行動作**：使用找到的選擇器執行後續動作。

## 常見陷阱

❌ **不要**在動態應用程式等待 `networkidle` 之前就檢查 DOM。
✅ **務必**在檢查前執行 `page.wait_for_load_state('networkidle')`。

## 最佳實踐

- **將隨附腳本視為黑箱** —— 執行任務時，優先考慮 `scripts/` 中的腳本是否能提供協助。這些腳本能可靠地處理常見且複雜的工作流程，且不會佔用上下文空間。使用 `--help` 查看用法後直接調用。
- 針對同步腳本使用 `sync_playwright()`。
- 完成後務必關閉瀏覽器。
- 使用具描述性的選擇器：`text=`、`role=`、CSS 選擇器或 ID。
- 加入適當的等待：`page.wait_for_selector()` 或 `page.wait_for_timeout()`。

## 參考檔案

- **examples/** —— 展示常見模式的範例：
  - `element_discovery.py` —— 發現頁面上的按鈕、連結與輸入框。
  - `static_html_automation.py` —— 針對本地 HTML 使用 file:// 網址。
  - `console_logging.py` —— 在自動化過程中擷取瀏覽器主控台日誌。
