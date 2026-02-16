# 範例：將對話轉化為 FAQ (Conversation to FAQ)

## 使用者請求

> 「將這段關於部署疑難排解的對話儲存到 FAQ 中」

**背景**：使用者剛完成了一段關於如何排解常見部署錯誤的對話。

## 對話摘要

對話涵蓋了：
1. **問題**：「為什麼部署會失敗並出現 'port already in use'（連接埠已被佔用）錯誤？」
2. **回答**：先前部署的程序仍在執行中，需要強制結束該程序。
3. **問題**：「我該如何找到並結束該程序？」
4. **分享的指令**：`lsof -ti:3000 | xargs kill -9` 或使用 `pm2 restart app`。
5. **問題**：「那 'cannot connect to database'（無法連線至資料庫）錯誤呢？」
6. **回答**：檢查資料庫憑證、驗證資料庫是否正在執行、檢查網路連線性。
7. **最佳實踐**：務必先檢查日誌 (`pm2 logs` 或 `docker logs`)。

## 工作流程執行

### 第一步：識別內容類型

這是問答類內容 → 適用 **FAQ 項目** 格式。

### 第二步：結構化 FAQ 條目

從對話中擷取不同的問答對：

**FAQ 1**：連接埠已被佔用錯誤。
**FAQ 2**：無法連線至資料庫錯誤。
**FAQ 3**：通用疑難排解方法。

### 第三步：確定目的地

```
Notion:notion-search
query: "FAQ deployment"
query_type: "internal"
```

找到：工程文件中的「部署 FAQ」資料庫。

```
Notion:notion-fetch
id: "deployment-faq-database-id"
```

**結構綱要 (Schema)**：
- 問題 (Question) (title)
- 類別 (Category) (select)：部署, 配置, 疑難排解 等。
- 標籤 (Tags) (multi_select)
- 最後審查日 (Last Reviewed) (date)

### 第四步：建立 FAQ 項目

**FAQ 項目 1：連接埠已被佔用 (Port Already in Use)**

```
Notion:notion-create-pages

parent: { data_source_id: "collection://faq-db-uuid" }

pages: [{
  properties: {
    "問題": "為什麼部署會失敗並出現 'port already in use' 錯誤？",
    "類別": "疑難排解",
    "標籤": "deployment, errors, ports",
    "date:最後審查日:start": "2025-10-14",
    "date:最後審查日:is_datetime": 0
  },
  content: "## 簡短回答

部署連接埠（通常是 3000）仍被先前部署的程序佔用。您需要在重新部署前強制結束現有的程序。

## 詳細說明

當您部署應用程式時，它會嘗試綁定到特定連接埠（例如 3000）。如果之前的部署沒有正常關閉，該程序可能仍在執行並佔用連接埠，導致新部署無法啟動。

**常見原因**：
- 先前的部署崩潰且未清理環境。
- 手動啟動了 `node` 程序後忘記關閉。
- PM2 或其他程序管理員未正確重啟。
- 同時嘗試多次部署。

## 解決方案

### 選項 1：強制結束佔用連接埠的程序

```bash
# 尋找並強制結束佔用 3000 連接埠的程序
lsof -ti:3000 | xargs kill -9
```

請將 `3000` 替換為您應用程式的實際連接埠號碼。

### 選項 2：如果使用 PM2

```bash
# 重啟應用程式
pm2 restart app

# 或刪除後重啟
pm2 delete app
pm2 start app.js --name app
```

### 選項 3：檢查所有 node 程序

```bash
# 列出所有 node 程序
ps aux | grep node

# 按 PID 強制結束特定程序
kill -9 <PID>
```

## 預防措施

1. **使用程序管理員**：PM2、systemd 或 Docker 會自動處理清理工作。
2. **優雅關閉 (Graceful shutdown)**：在應用程式中實作正確的關閉處理程式。
3. **健康檢查**：在啟動新部署前監控先前部署是否已關閉。

```javascript
// 優雅關閉範例
process.on('SIGTERM', () => {
  server.close(() => {
    console.log('伺服器已關閉');
    process.exit(0);
  });
});
```

## 驗證方式

結束程序後，驗證連接埠是否已釋放：

```bash
lsof -ti:3000
# 如果連接埠已釋放，則不會回傳任何內容
```

## 相關問題
- <mention-page url="...">如何檢查是誰在佔用連接埠？</mention-page>
- <mention-page url="...">如何配置應用程式連接埠？</mention-page>"
}]
```

**FAQ 項目 2：資料庫連線錯誤 (Database Connection Errors)**

```
Notion:notion-create-pages

parent: { data_source_id: "collection://faq-db-uuid" }

pages: [{
  properties: {
    "問題": "為什麼我在部署期間收到 'cannot connect to database' 錯誤？",
    "類別": "疑難排解",
    "標籤": "deployment, database, errors",
    "date:最後審查日:start": "2025-10-14",
    "date:最後審查日:is_datetime": 0
  },
  content: "## 簡短回答

資料庫連線錯誤通常代表資料庫未執行、憑證錯誤或存在網路連線性問題。請檢查資料庫狀態、驗證憑證並測試連線性。

## 詳細說明

應用程式在啟動期間無法建立與資料庫的連線，導致應用程式無法正常初始化。

**常見原因**：
- 資料庫服務未執行。
- 連線憑證不正確。
- 網路連線性問題（防火牆、安全性群組）。
- 資料庫主機/連接埠配置錯誤。
- 資料庫達到連線數上限。
- SSL/TLS 配置不匹配。

## 疑難排解步驟

### 第一步：檢查資料庫狀態

```bash
# 針對本地 PostgreSQL
pg_isready -h localhost -p 5432

# 針對 Docker
docker ps | grep postgres

# 針對 MongoDB
mongosh --eval "db.adminCommand('ping')"
```

### 第二步：驗證憑證

檢查您的 `.env` 或配置文件：

```bash
# 常見環境變數
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp_production
DB_USER=myapp_user
DB_PASSWORD=***********
```

手動測試連線：

```bash
# PostgreSQL
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME

# MongoDB
mongosh "mongodb://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"
```

### 第三步：檢查網路連線性

```bash
# 測試連接埠是否可到達
telnet $DB_HOST $DB_PORT

# 或使用 nc
nc -zv $DB_HOST $DB_PORT

# 檢查防火牆規則（如適用）
sudo iptables -L
```

### 第四步：檢查應用程式日誌

```bash
# PM2 日誌
pm2 logs app

# Docker 日誌
docker logs container-name

# 應用程式日誌
tail -f /var/log/app/error.log
```

尋找特定的錯誤訊息：
- `ECONNREFUSED`：資料庫未執行或主機/連接埠錯誤。
- `Authentication failed`：憑證錯誤。
- `Timeout`：網路/防火牆問題。
- `Too many connections`：達到資料庫連線上限。"
}]
```

**FAQ 項目 3：通用疑難排解方法 (General Troubleshooting)**

```
Notion:notion-create-pages

parent: { data_source_id: "collection://faq-db-uuid" }

pages: [{
  properties: {
    "問題": "部署失敗時我應該首先檢查什麼？",
    "類別": "疑難排解",
    "標籤": "deployment, debugging, best-practices",
    "date:最後審查日:start": "2025-10-14",
    "date:最後審查日:is_datetime": 0
  },
  content: "## 簡短回答

**務必先檢查日誌。** 日誌中的錯誤訊息能直接指向問題所在。請使用 `pm2 logs`、`docker logs` 或檢查應用程式的日誌檔案。

## 詳細說明

日誌是您首要且最重要的偵錯工具。它們顯示：
- 精確的錯誤訊息
- 堆疊追蹤 (Stack traces)
- 時間資訊
- 配置問題
- 依賴關係問題

大多數部署問題都可以透過仔細閱讀日誌來診斷並修復。

## 如何檢查日誌

### PM2

```bash
# 查看所有日誌
pm2 logs

# 查看特定 App 的日誌
pm2 logs app-name

# 僅查看錯誤日誌
pm2 logs --err

# 即時追蹤日誌
pm2 logs --lines 100
```

### Docker

```bash
# 查看日誌
docker logs container-name

# 追蹤日誌內容
docker logs -f container-name

# 查看最後 100 行
docker logs --tail 100 container-name

# 帶有時間戳記
docker logs -t container-name
```

### 應用程式日誌檔案

```bash
# 追蹤日誌檔案
tail -f /var/log/app/app.log
tail -f /var/log/app/error.log

# 在日誌中搜尋錯誤
grep -i error /var/log/app/*.log

# 結合上下文查看日誌
grep -B 5 -A 5 "ERROR" app.log
```

## 系統化疑難排解方法

### 1. 檢查日誌
- 仔細閱讀錯誤訊息。
- 註記精確的錯誤型別與訊息內容。
- 檢查時間戳記以確定錯誤發生的時間。

### 2. 驗證配置
- 環境變數是否正確設定？
- 配置文件是否存在且有效？
- 路徑與檔案權限是否正確？

### 3. 檢查依賴關係
- 套件是否全部安裝？（`node_modules` 是否存在？）
- 是否安裝了正確的版本？
- 是否有原生模組 (Native module) 編譯錯誤？

### 4. 驗證環境
- 必要服務是否運作（資料庫、Redis 等）？
- 連接埠是否可用？
- 網路連線性是否正常？"
}]
```

### 第五步：更新 FAQ 索引

```
Notion:notion-fetch
id: "faq-index-page-id"
```

```
Notion:notion-update-page
page_id: "faq-index-page-id"
command: "insert_content_after"
selection_with_ellipsis: "## 部署與疑難排解..."
new_str: "
- <mention-page url="...">為什麼部署會失敗並出現 'port already in use' 錯誤？</mention-page>
- <mention-page url="...">為什麼我會收到資料庫連線錯誤？</mention-page>
- <mention-page url="...">部署失敗時我應該首先檢查什麼？</mention-page>
"
```

## 提供給使用者的總結

```markdown
## FAQ 條目已建立 ✅

### 對話內容已擷取
已將部署疑難排解的對話轉化為 3 條完整的 FAQ 條目。

### 已建立的 FAQ 條目

1. **連接埠已被佔用錯誤**
   - 問題：由於連接埠被佔用導致部署失敗
   - 解決方案：強制結束程序、使用 PM2、檢查 node 程序
   - 預防：使用程序管理員、優雅關閉
   - 連結：<mention-page url="...">連接埠佔用 FAQ</mention-page>

2. **資料庫連線錯誤**
   - 問題：部署期間無法連線至資料庫
   - 疑難排解：4 步驟系統化方法
   - 解決方案：按錯誤型別分類（憑證、網路、上限）
   - 預防：連線池 (Pooling)、健康檢查、重試邏輯
   - 連結：<mention-page url="...">資料庫連線 FAQ</mention-page>

3. **通用疑難排解方法**
   - 最佳實踐：務必先檢查日誌
   - 工具：PM2 日誌、Docker 日誌、應用程式日誌
   - 系統化方法：6 步驟偵錯程序
   - 常見錯誤：模組找不到、權限問題、連接埠問題
   - 連結：<mention-page url="...">疑難排解首要步驟 FAQ</mention-page>

### 內容結構

每條 FAQ 均包含：
✅ 簡短回答（快速參考）
✅ 詳細說明（完整背景）
✅ 多種解決方案選項
✅ 程式碼範例與指令
✅ 預防策略
✅ 相關 FAQ 連結
✅ 最後更新日期

### 資料庫整合

- ✅ 已新增至 FAQ 資料庫（而非獨立頁面）
- ✅ 屬性設定：類別（疑難排解）、標籤、日期
- ✅ FAQ 索引頁面已更新連結
- ✅ 相關問題之間的交叉引用

### 帶來的價值

**從對話** → **轉化為結構化知識**：
- 隨性的問答 → 專業的 FAQ 條目
- 隱性知識 → 顯性技術文件
- 一次性協助 → 可重複使用的資源
- 5 分鐘對話 → 永久性的團隊知識

**未來效益**：
- 團隊可以針對常見問題進行「自助式」獲取資訊。
- 新成員可以更快速地入職 (Onboarding)。
- 減少重複性問題。
- 提升疑難排解的速度。

**知識已成功擷取並保存！ 📚**
```

## 示範的關鍵功能

### 內容擷取
- 從對話中識別出獨立的問答對。
- 擷取指令、解決方案與最佳實踐。
- 保留疑難排解的工作流程。

### FAQ 結構
- 簡短回答供快速參考。
- 詳細說明供深入理解。
- 多種解決方案（選項 1, 2, 3）。
- 附帶註解的程式碼範例。
- 預防策略。
- 相關問題的連結。

### 資料庫整合
- 在 FAQ 資料庫中建立（非獨立頁面）。
- 設定適當屬性（類別、標籤、日期）。
- 更新索引頁面連結。
- 交叉引用相關問題。

### 價值轉化
- 將非正式對話轉化為專業文件。
- 增加結構、範例與預防提示。
- 使知識具備可搜尋性與可發現性。
- 建立永久的團隊資源。

非常適合用於：FAQ 建立、知識保存、團隊技術文件編寫。
