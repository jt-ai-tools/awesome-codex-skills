# 資料庫最佳實踐 (Database Best Practices)

建立與維護知識擷取資料庫的通用指引。

## 核心原則

### 1. 保持簡單
- 從核心屬性開始。
- 僅在需要時增加更多屬性。
- 避免過度設計 (Over-engineer)。

### 2. 使用一致的命名
- 使用標題 (Title) 屬性作為主要識別碼。
- 使用狀態 (Status) 進行生命週期追蹤。
- 使用標籤 (Tags) 進行靈活分類。
- 使用負責人 (Owner) 明確責任歸屬。

### 3. 包含中繼資料
- 建立/更新時間戳記。
- 負責人或維護者。
- 最後審查日期。
- 狀態指示器。

### 4. 提升可發現性 (Discovery)
- 廣泛使用標籤。
- 建立有幫助的檢視表 (Views)。
- 連結相關內容。
- 使用清晰的標題。

### 5. 為規模化做規劃
- 儘早考慮過濾器。
- 使用關聯 (Relations) 進行連接。
- 考慮搜尋便利性。
- 使用類別進行組織。

## 建立資料庫

### 使用 `Notion:notion-create-database`

技術文件資料庫範例：

```javascript
{
  "parent": {"page_id": "wiki-page-id"},
  "title": [{"text": {"content": "團隊技術文件"}}],
  "properties": {
    "類型": {
      "select": {
        "options": [
          {"name": "操作指南 (How-To)", "color": "blue"},
          {"name": "概念 (Concept)", "color": "green"},
          {"name": "參考 (Reference)", "color": "gray"},
          {"name": "常見問題 (FAQ)", "color": "yellow"}
        ]
      }
    },
    "類別": {
      "select": {
        "options": [
          {"name": "工程 (Engineering)", "color": "red"},
          {"name": "產品 (Product)", "color": "purple"},
          {"name": "設計 (Design)", "color": "pink"}
        ]
      }
    },
    "標籤": {"multi_select": {"options": []}},
    "負責人": {"people": {}},
    "狀態": {
      "select": {
        "options": [
          {"name": "草稿", "color": "gray"},
          {"name": "定稿", "color": "green"},
          {"name": "已棄用", "color": "red"}
        ]
      }
    }
  }
}
```

### 獲取資料庫結構綱要 (Schema)

在建立頁面之前，務必先獲取資料庫資訊以取得結構綱要：

```
Notion:notion-fetch
id: "資料庫網址或 ID"
```

這將回傳要使用的確切屬性名稱與型別。

## 資料庫選擇指南

| 需求 | 使用此資料庫 |
|------|-------------------|
| 通用技術文件 | [文件資料庫 (Documentation Database)](documentation-database_zh_TW.md) |
| 追蹤決策 | [決策日誌 (Decision Log)](decision-log-database_zh_TW.md) |
| 問答知識庫 | [常見問題資料庫 (FAQ Database)](faq-database_zh_TW.md) |
| 團隊特定內容 | [團隊 Wiki (Team Wiki)](team-wiki-database_zh_TW.md) |
| 逐步引導指南 | [操作指南資料庫 (How-To Guide Database)](how-to-guide-database_zh_TW.md) |
| 事件/專案學習心得 | [學習心得資料庫 (Learning Database)](learning-database_zh_TW.md) |

## 提示 (Tips)

1. **從通用文件資料庫開始** —— 靈活性最高。
2. **隨著需求出現增加專用資料庫**（如 FAQ、決策）。
3. **使用關聯**來連接相關的文件。
4. **為常見使用場景建立檢視表**。
5. **每季審查屬性** —— 移除未使用的屬性。
6. **在資料庫描述中記錄結構綱要**。
7. **培訓團隊**了解屬性的用法與命名慣例。
