# 範例：API 功能實作 (API Feature Implementation)

## 使用者請求

> 「為使用者個人資料 API 規格書 (User Profile API spec) 建立實作計畫」

## 工作流程執行

### 第一步：獲取規格書

```
Notion:notion-search
query: "User Profile API 規格書"
query_type: "internal"
```

找到：工程規格書中的「使用者個人資料 API 規格書 (User Profile API Specification)」。

```
Notion:notion-fetch
id: "user-profile-api-spec-page-id"
```

### 第二步：解析規格書

**擷取的規格內容：**

```markdown
# 使用者個人資料 API 規格書

## 概覽
用於使用者個人資料管理的 RESTful API。

## 需求

### 功能性需求
- FR-1：透過 ID 獲取使用者個人資料。
- FR-2：更新使用者個人資料（姓名、簡介、大頭照）。
- FR-3：上傳個人大頭照。
- FR-4：獲取使用者的公開資料（僅限部分欄位）。
- FR-5：按姓名搜尋使用者。

### 非功能性需求
- NFR-1：回應時間 < 200ms (p95)。
- NFR-2：支援 1000 名併發使用者。
- NFR-3：大頭照上傳檔案 < 5MB。
- NFR-4：符合 GDPR 合規性（數據可攜性）。

## API 端點 (Endpoints)

GET /api/v1/users/:id
PUT /api/v1/users/:id
POST /api/v1/users/:id/avatar
GET /api/v1/users/:id/public
GET /api/v1/users/search

## 數據模型
- id (UUID)
- email (string, unique)
- name (string)
- bio (text, max 500 chars)
- avatar_url (string)
- created_at (timestamp)
- updated_at (timestamp)

## 安全性
- 認證：JWT Bearer Token。
- 授權：使用者僅能更新自己的資料。
- 速率限制：每位使用者每分鐘 100 次請求。

## 驗收標準
- AC-1：所有端點回傳正確的 HTTP 狀態碼。
- AC-2：驗證錯誤回傳 400 並附帶錯誤詳情。
- AC-3：未授權存取回傳 401。
- AC-4：超過速率限制回傳 429。
- AC-5：大頭照圖片儲存於 S3。
```

### 第三步：建立實作計畫

```
Notion:notion-create-pages

parent: { page_id: "engineering-plans-parent-id" }

pages: [{
  properties: {
    "title": "實作計畫：使用者個人資料 API"
  },
  content: "[實作計畫內容]"
}]
```

**已建立的實作計畫：**

```markdown
# 實作計畫：使用者個人資料 API

## 概覽
建置具備 CRUD 操作、大頭照上傳與搜尋功能的使用者個人資料管理 RESTful API。

## 關聯規格書
<mention-page url="...">使用者個人資料 API 規格書</mention-page>

## 需求摘要

### 功能性需求
- ✅ 獲取使用者資料（需經過認證）。
- ✅ 更新個人資料欄位（姓名、簡介）。
- ✅ 具備圖像處理功能的大頭照上傳。
- ✅ 公開資料檢視（僅限公開欄位）。
- ✅ 按姓名搜尋使用者。

### 非功能性需求
- **效能**：回應時間 < 200ms (p95)。
- **擴展性**：支援 1000 名併發使用者。
- **儲存**：大頭照檔案 < 5MB，上傳至 S3。
- **合規性**：GDPR 數據可攜性要求。

### 驗收標準
- 所有端點具備正確狀態碼。
- 包含錯誤詳情的輸入驗證。
- 強制 JWT 認證。
- 執行速率限制。
- 大頭照儲存於 S3。

## 技術方案 (Technical Approach)

### 架構設計
- **框架**：Express.js (Node.js)。
- **資料庫**：PostgreSQL。
- **儲存**：AWS S3 用於存放頭像。
- **快取**：Redis 用於快取個人資料。
- **搜尋**：PostgreSQL 全文檢索 (Full-text search)。

### 關鍵設計決策
1. **JWT 認證**：無狀態認證，便於水平擴展。
2. **S3 儲存大頭照**：卸載儲存壓力，方便後續 CDN 整合。
3. **Redis 快取**：針對頻繁存取的資料降低資料庫負載。
4. **速率限制**：採用權杖桶 (Token bucket) 演算法，針對單一使用者設限。

## 實作階段

### 第一階段：基礎建設 (第 1-2 天)
**目標**：建立核心基礎設施

**任務清單**：
- [ ] <mention-page url="...">設定資料庫結構綱要</mention-page>
- [ ] <mention-page url="...">配置 S3 Bucket</mention-page>
- [ ] <mention-page url="...">設定 Redis 快取</mention-page>
- [ ] <mention-page url="...">建立 API 基礎鷹架</mention-page>

**交付物**：具備資料庫、儲存與快取的 API 骨架。  
**預估投入**：2 天。

### 第二階段：核心端點 (第 3-5 天)
**目標**：實作主要 CRUD 操作

**任務清單**：
- [ ] <mention-page url="...">實作 GET 獲取資料</mention-page>
- [ ] <mention-page url="...">實作 PUT 更新資料</mention-page>
- [ ] <mention-page url="...">新增輸入驗證機制</mention-page>
- [ ] <mention-page url="...">加入 JWT 認證中間件</mention-page>
- [ ] <mention-page url="...">實作速率限制</mention-page>

**交付物**：具備認證功能的 CRUD 操作端點。  
**預估投入**：3 天。

### 第三階段：大頭照上傳 (第 6-7 天)
**目標**：整合 S3 的大頭照管理

**任務清單**：
- [ ] <mention-page url="...">實作大頭照上傳端點</mention-page>
- [ ] <mention-page url="...">新增圖片驗證（大小、格式）</mention-page>
- [ ] <mention-page url="...">圖像處理與尺寸調整</mention-page>
- [ ] <mention-page url="...">使用簽名網址 (Signed URLs) 上傳至 S3</mention-page>

**交付物**：大頭照上傳與更新功能。  
**預估投入**：2 天。

### 第四階段：搜尋與公開資料 (第 8-9 天)
**目標**：完成剩餘功能

**任務清單**：
- [ ] <mention-page url="...">實作使用者搜尋</mention-page>
- [ ] <mention-page url="...">實作公開資料端點</mention-page>
- [ ] <mention-page url="...">建立搜尋索引</mention-page>
- [ ] <mention-page url="...">優化搜尋查詢效能</mention-page>

**交付物**：搜尋與公開資料展示功能。  
**預估投入**：2 天。

### 第五階段：測試與優化 (第 10-12 天)
**目標**：達到生產環境品質

**任務清單**：
- [ ] <mention-page url="...">撰寫單元測試</mention-page>
- [ ] <mention-page url="...">撰寫整合測試</mention-page>
- [ ] <mention-page url="...">執行效能測試</mention-page>
- [ ] <mention-page url="...">安全性稽核</mention-page>
- [ ] <mention-page url="...">完成 API 文件</mention-page>

**交付物**：經過測試、具備文件且可上線的 API。  
**預估投入**：3 天。

## 依賴關係

### 外部依賴
- AWS S3 Bucket 已建立 ✅
- Redis 執行體已可用 ✅
- PostgreSQL 資料庫已佈署 ✅

### 內部依賴
- JWT 認證服務（現有）。
- 使用者資料庫表（現有）。
- 日誌基礎設施（現有）。

### 阻礙因素
目前無。

## 風險與緩解措施

### 風險 1：圖像處理效能問題
- **機率**：中
- **影響**：中
- **緩解措施**：使用背景任務隊列處理圖像，並立即回傳上傳簽名網址。

### 風險 2：S3 上傳失敗
- **機率**：低
- **影響**：中
- **緩解措施**：實作指數退避 (Exponential backoff) 重試邏輯，暫時提供本地儲存作為備案。

### 風險 3：速率限制實作複雜
- **機率**：低
- **影響**：低
- **緩解措施**：使用成熟的函式庫 (express-rate-limit 配合 Redis 儲存)。

### 風險 4：搜尋效能瓶頸
- **機率**：中
- **影響**：中
- **緩解措施**：新增資料庫索引，若後續有需求則考慮引入 Elasticsearch。

## 時程表

| 里程碑 | 目標日期 | 狀態 |
|-----------|-------------|--------|
| 第一階段完成 | 10 月 16 日 | ⏳ 已規劃 |
| 第二階段完成 | 10 月 19 日 | ⏳ 已規劃 |
| 第三階段完成 | 10 月 21 日 | ⏳ 已規劃 |
| 第四階段完成 | 10 月 23 日 | ⏳ 已規劃 |
| 第五階段完成 | 10 月 26 日 | ⏳ 已規劃 |
| **正式上線部署** | **10 月 28 日** | ⏳ 已規劃 |

**總時長**：12 個工作日（約 2.5 週）。

## 成功指標 (Success Criteria)

### 技術面成功
- [ ] 5 個端點全部實作並正常運作。
- [ ] 負載測試驗證回應時間 < 200ms (p95)。
- [ ] 可支撐 1000 名併發使用者。
- [ ] 滿足所有驗收標準。
- [ ] 測試涵蓋率 > 80%。
- [ ] 通過安全性掃描。
- [ ] API 文件編寫完成。

### 業務面成功
- [ ] 使用者資料更新功能正常。
- [ ] 大頭照上傳穩定可靠。
- [ ] 搜尋結果在 500ms 內回傳。
- [ ] 上線首週無嚴重 Bug。

## 資源連結

### 技術文件
- <mention-page url="...">使用者個人資料 API 規格書</mention-page> (原始規格)
- <mention-page url="...">認證服務文件</mention-page>
- <mention-page url="...">AWS S3 設定指南</mention-page>

### 相關工作
- <mention-page url="...">使用者認證 API</mention-page> (相似模式)
- <mention-page url="...">檔案上傳服務</mention-page> (頭像上傳參考)

### 外部參考
- Express.js 最佳實踐。
- AWS S3 SDK 文件。
- PostgreSQL 全文檢索指引。

## 進度追蹤

### 階段狀態
- 第一階段：⏳ 未開始
- 第二階段：⏳ 未開始
- 第三階段：⏳ 未開始
- 第四階段：⏳ 未開始
- 第五階段：⏳ 未開始

**整體進度**：已完成 0%

### 最新更新
*實作計畫建立於 2025 年 10 月 14 日*
```

### 第四步：尋找任務資料庫

```
Notion:notion-search
query: "任務資料庫"
query_type: "internal"
```

找到：「工程任務 (Engineering Tasks)」資料庫。

### 第五步：獲取任務資料庫結構綱要

```
Notion:notion-fetch
id: "tasks-database-id"
```

**擷取的結構：**
- 數據源：`collection://tasks-db-uuid`
- 屬性：名稱 (title), 狀態 (select), 優先級 (select), 相關任務 (relation), 故事點數 (number), 標籤 (multi_select)

### 第六步：建立實作任務

現在為第一階段建立任務：

**任務 1：設定資料庫結構綱要**

```
Notion:notion-create-pages

parent: { data_source_id: "collection://tasks-db-uuid" }

pages: [{
  properties: {
    "名稱": "為使用者個人資料 API 設定資料庫結構綱要",
    "狀態": "待處理",
    "優先級": "高",
    "相關任務": ["實作計畫頁面 ID", "規格書頁面 ID"],
    "故事點數": 3,
    "標籤": "backend, database, api"
  },
  content: "## 背景 (Context)
<mention-page url="...">使用者個人資料 API 規格書</mention-page> 的實作任務。

隸屬於 <mention-page url="...">實作計畫：使用者個人資料 API</mention-page> - 第一階段。

## 目標
建立使用者個人資料儲存的資料庫結構綱要。

## 需求
根據規格書中的數據模型：
- id (UUID, 主鍵)
- email (string, 唯一索引)
- name (string, 不可為空)
- bio (text, 最多 500 字)
- avatar_url (string, 可為空)
- created_at (timestamp)
- updated_at (timestamp)

## 驗收標準
- [ ] 遷移 (Migration) 檔案已建立。
- [ ] 結構綱要包含所有必填欄位。
- [ ] 建立 email (唯一) 與 name (搜尋) 的索引。
- [ ] 約束條件已驗證（簡介長度、電子郵件格式）。
- [ ] 在開發環境資料庫測試過遷移腳本。
- [ ] 建立回滾 (Rollback) 遷移腳本。

## 技術方案
```sql
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  bio TEXT CHECK (length(bio) <= 500),
  avatar_url TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_profiles_email ON user_profiles(email);
CREATE INDEX idx_user_profiles_name ON user_profiles USING gin(to_tsvector('english', name));
```

## 依賴關係
- 受阻於：無。
- 阻礙：所有第二階段任務。

## 預估投入
3 故事點數 (約半天工作量)。
"
}]
```

*[針對所有階段建立類似任務 —— 共計 20 個任務]*

### 第七步：將計畫連回規格書

```
Notion:notion-update-page
page_id: "user-profile-api-spec-page-id"
command: "insert_content_after"
selection_with_ellipsis: "## 驗收標準..."
new_str: "

---

## 實作情況 (Implementation)

**實作計畫**：<mention-page url="...">實作計畫：使用者個人資料 API</mention-page>

**實作任務**：詳見計畫中的任務拆解（共 5 個階段 20 個任務）。

**狀態**：規劃已完成，準備開始實作。
"
```

## 提供給使用者的總結

```markdown
## 實作計畫已建立 ✅

### 計畫概覽
- **功能項目**：使用者個人資料 API
- **預計時長**：12 天（約 2.5 週）
- **實作階段**：5 個（基礎建設 → 核心端點 → 大頭照上傳 → 搜尋功能 → 測試優化）
- **建立任務**：已建立 20 個任務
- **目標上線日期**：2025 年 10 月 28 日

### 實作階段說明

**第一階段：基礎建設** (2 天)
- 資料庫結構綱要。
- S3 與 Redis 設定。
- API 基礎鷹架建立。

**第二階段：核心端點** (3 天)
- GET/PUT 使用者資料。
- 認證與輸入驗證。
- 速率限制機制。

**第三階段：大頭照上傳** (2 天)
- 圖片上傳與驗證。
- S3 整合。
- 圖像縮放處理。

**第四階段：搜尋與公開資料** (2 天)
- 使用者搜尋功能。
- 公開資料展示端點。

**第五階段：測試與優化** (3 天)
- 單元測試與整合測試。
- 效能測試。
- 技術文件撰寫。

### 關鍵交付物
- 5 個 REST API 端點。
- 整合 S3 的大頭照上傳功能。
- 使用者搜尋功能。
- 全面的測試報告。
- API 說明文件。

### 已建立的連結
✅ 計畫頁面：<mention-page url="...">實作計畫：使用者個人資料 API</mention-page>
✅ 規格書已更新計畫連結。
✅ 任務資料庫中已建立 20 個任務。
✅ 所有任務均已關聯至計畫與規格書。

### 後續步驟
1. 審閱並批准計畫。
2. 指派任務給團隊成員。
3. 開始執行第一階段（基礎建設）。
4. 每日站立會議追蹤進度。

**準備好開始實作了！ 🚀**
```

## 示範的關鍵功能

### 規格書解析
- 擷取功能性與非功能性需求。
- 識別 API 端點。
- 紀錄數據模型。
- 擷取驗收標準。
- 理解安全性要求。

### 實作規劃
- 拆解為邏輯階段。
- 合理的工作排序（基礎 → 功能 → 測試）。
- 識別依賴關係。
- 預估各階段投入。
- 建立現實的時程表。

### 任務建立
- 生成 20 個具體任務。
- 每個任務均具備背景、驗收標準與技術方案。
- 任務同時連結至規格書與計畫。
- 標註了正確的依賴關係。

### 雙向連結
- 計畫連結至規格書。
- 規格書更新後連結至計畫。
- 任務同時連結至兩者。
- 方便在所有產出物之間導覽。

非常適合用於：功能開發、API 開發、技術專案。
