# 進階搜尋技巧 (Advanced Search Techniques)

## 搜尋過濾 (Search Filtering)

### 按日期範圍

使用 `created_date_range` 尋找近期內容：

```
filters: {
  created_date_range: {
    start_date: "2024-01-01",
    end_date: "2025-01-01"
  }
}
```

**何時使用**：
- 尋找某個主題的最新更新。
- 專注於當前資訊。
- 排除過時內容。

### 按建立者

使用 `created_by_user_ids` 尋找特定人員建立的內容：

```
filters: {
  created_by_user_ids: ["user-id-1", "user-id-2"]
}
```

**何時使用**：
- 獲取領域專家 (SME) 的研究資料。
- 尋找特定團隊的資訊。
- 追蹤貢獻歸屬。

### 組合過濾器

堆疊多個過濾器以實現精準搜尋：

```
filters: {
  created_date_range: {
    start_date: "2024-10-01"
  },
  created_by_user_ids: ["expert-user-id"]
}
```

## 限定範圍搜尋 (Scoped Searches)

### 團隊空間範圍 (Teamspace Scoping)

將搜尋限制在特定的團隊空間：

```
teamspace_id: "teamspace-uuid"
```

**何時使用**：
- 針對特定專案的研究。
- 獲取特定部門的資訊。
- 減少無關結果的干擾。

### 頁面範圍

在特定頁面及其子頁面內進行搜尋：

```
page_url: "https://notion.so/workspace/Page-Title-uuid"
```

**何時使用**：
- 在專案層級架構內進行研究。
- 文件更新。
- 針對性調查。

### 資料庫範圍

在資料庫內容中搜尋：

```
data_source_url: "collection://data-source-uuid"
```

**何時使用**：
- 任務或專案資料庫研究。
- 結構化數據調查。
- 尋找特定條目。

## 搜尋策略

### 由廣入深 (Broad to Narrow)

1. 先使用通用搜尋詞開始。
2. 審查結果中的相關團隊空間或頁面。
3. 使用範圍過濾器重新搜尋。
4. 從排名最前的結果中獲取詳細內容。

**範例**：
```
搜尋 1：query="API integration" → 工作區中出現 50 個結果
搜尋 2：query="API integration", teamspace_id="engineering" → 12 個結果
獲取：最相關的前 3-5 個頁面
```

### 多重查詢法

針對相關術語執行並行搜尋：

```
查詢 1："API integration"
查詢 2："API authentication"
查詢 3："API documentation"
```

結合各項結果以建構完整的全貌。

### 時間性研究

跨時間段搜尋以追蹤演變過程：

```
搜尋 1：created_date_range 2023 → 歷史背景
搜尋 2：created_date_range 2024 → 近期進展
搜尋 3：created_date_range 2025 → 目前現狀
```

## 結果處理

### 識別相關結果

尋找具備以下特性的結果：
- **高度語意匹配**：結果摘要與查詢意圖緊密契合。
- **近期更新**：最後編輯日期較新。
- **權威來源**：由已知專家建立或存放於官方位置。
- **內容全面**：結果摘要顯示其包含詳細資訊。

### 優先獲取順序

按相關性依序獲取頁面內容：

1. **主要來源**：直接文件、官方頁面。
2. **近期更新**：新編輯的內容。
3. **相關背景**：支持性資訊。
4. **歷史參考**：背景與脈絡資料。

不要獲取所有內容 —— 請根據研究需求進行篩選。

### 處理結果過多

若搜尋回傳超過 20 個結果：

1. **增加過濾器**：按日期、建立者或團隊空間縮小範圍。
2. **優化查詢**：使用更具體的詞彙。
3. **使用頁面限定**：在相關的父頁面內進行搜尋。
4. **戰略性抽樣**：獲取多樣化的結果（最新的、熱門的、權威的）。

### 處理結果過少

若搜尋結果少於 3 個：

1. **擴大查詢**：使用更通用的詞彙。
2. **移除過濾器**：搜尋整個工作區。
3. **嘗試同義詞**：使用替代術語。
4. **搜尋相關領域**：檢查相鄰的團隊空間或頁面。

## 搜尋品質

### 有效的搜尋查詢

**優質查詢**（具體、語意化）：
- "Q4 product roadmap"
- "authentication implementation guide"
- "customer feedback themes"

**弱勢查詢**（過於模糊）：
- "roadmap"
- "guide"
- "feedback"

**過度具體查詢**（範圍太窄）：
- "Q4 2024 product roadmap for mobile app version 3.2 feature X"

### 使用者上下文 (User Context)

務必利用可用的使用者背景資訊：
- 查詢詞應匹配使用者的用語慣例。
- 限定在其相關的團隊空間內。
- 考慮其角色與部門。
- 參考其最近瀏覽的頁面。

## 連接的來源 (Connected Sources)

### Notion 整合功能

搜尋範圍可擴展至 Notion 頁面以外的：
- Slack 訊息（若已連線）。
- Google Drive 文件（若已連線）。
- GitHub Issues/PRs（若已連線）。
- Jira 任務（若已連線）。

請注意結果可能來自這些外部來源。

### 來源歸屬 (Source Attribution)

引用來自連線來源的結果時：
- 在文件中註明來源類型。
- 使用適當的「提到 (Mention)」格式。
- 驗證使用者是否具備存取該來源系統的權限。
