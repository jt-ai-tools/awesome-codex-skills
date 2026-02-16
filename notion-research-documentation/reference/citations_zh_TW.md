# 引用樣式 (Citation Styles)

## 基礎頁面引用

務必使用 Notion 的頁面「提到 (Mentions)」功能來標註來源：

```markdown
<mention-page url="https://notion.so/workspace/Page-Title-uuid">頁面標題</mention-page>
```

必須提供網址。標題為選填，但能提高可讀性：

```markdown
<mention-page url="https://notion.so/workspace/Page-Title-uuid"/>
```

## 行內引用 (Inline Citations)

在引用資訊後立即標註來源：

```markdown
第四季營收較上季成長了 23% (<mention-page url="...">第四季財務報告</mention-page>)。
```

## 多重來源

當資訊來自多個來源時：

```markdown
客戶滿意度在所有指標上皆有所提升 (<mention-page url="...">第三季調查結果</mention-page>, <mention-page url="...">客服分析報告</mention-page>)。
```

## 章節級引用

針對源自單一來源的較長章節：

```markdown
### 工程優先事項

根據 <mention-page url="...">2025 年工程路線圖</mention-page>：

- 專注於 API 的可擴展性。
- 提升開發者體驗。
- 遷移至微服務架構。
```

## 來源章節 (Sources Section)

務必在文件末尾包含「來源」章節：

```markdown
## 來源 (Sources)

- <mention-page url="...">2025 年戰略計畫</mention-page>
- <mention-page url="...">市場分析報告</mention-page>
- <mention-page url="...">第三季競爭對手研究</mention-page>
- <mention-page url="...">客戶訪談筆記</mention-page>
```

若清單較長，請按類別進行分組：

```markdown
## 來源

### 主要來源
- <mention-page url="...">官方路線圖</mention-page>
- <mention-page url="...">戰略文件</mention-page>

### 支持性研究
- <mention-page url="...">市場趨勢</mention-page>
- <mention-page url="...">客戶回饋</mention-page>

### 背景資料
- <mention-page url="...">歷史分析</mention-page>
```

## 引述內容 (Quoting Content)

當直接引述來源內容時：

```markdown
產品團隊指出：「我們需要優先優化行動端體驗」(<mention-page url="...">產品會議記錄</mention-page>)。
```

對於區塊引述 (Block quotes)：

```markdown
> 我們需要優先優化行動端體驗，以達成第四季的目標。這包括效能優化與 UI 更新。
>
> — <mention-page url="...">2025 年 10 月產品會議記錄</mention-page>
```

## 數據引用

呈現數據時，請標明來源：

```markdown
| 指標 | 第三季 | 第四季 | 變動 |
|--------|----|----|--------|
| 營收 | $2.3M | $2.8M | +21.7% |
| 使用者數 | 12.4K | 15.1K | +21.8% |

來源：<mention-page url="...">財務儀表板</mention-page>
```

## 資料庫引用

當引用資料庫內容時：

```markdown
根據對 <mention-database url="...">專案資料庫</mention-database> 的分析，67% 的專案進度正常。
```

## 人員引用

當將資訊歸功於特定人員時：

```markdown
<mention-user url="...">Sarah Chen</mention-user> 在 <mention-page url="...">架構審查</mention-page> 中提到，微服務遷移進度超前。
```

## 引用頻率

**過度引用**（每一句都標註）：
```markdown
營收增長了 (<mention-page url="...">報告</mention-page>)。
成本降低了 (<mention-page url="...">報告</mention-page>)。
利潤率提升了 (<mention-page url="...">報告</mention-page>)。
```

**引用不足**（完全未標註）：
```markdown
營收增長，成本降低，利潤率提升。
```

**適當平衡**（分組引用）：
```markdown
營收增長，成本降低，且利潤率有所提升 (<mention-page url="...">第四季財務報告</mention-page>)。
```

## 過時資訊

標註來源資訊可能已過時的情況：

```markdown
原始 API 設計 (<mention-page url="...">API 規格書 v1</mention-page>, 最後更新於 2024 年 1 月) 已被 <mention-page url="...">API 規格書 v2</mention-page> 中的新架構取代。
```

## 交叉引用

連結至相關的研究文件：

```markdown
## 相關研究

本研究建立於先前的發現之上：
- <mention-page url="...">2025 年第二季市場分析</mention-page>
- <mention-page url="...">競爭格局審查</mention-page>

關於實作細節，請參閱：
- <mention-page url="...">技術實作指南</mention-page>
```

## 引用驗證

在定稿研究報告前：

✓ 每個關鍵主張都有來源引用。
✓ 所有頁面提到 (Mentions) 都有有效的網址。
✓ 來源章節包含了所有被引用的頁面。
✓ 過時來源已明確標註。
✓ 直接引述已清晰標記。
✓ 數據來源已標明。

## 引用風格的一致性

選擇一種引用風格並貫徹全篇：

**行內風格**（輕量級）：
```markdown
營收增長 23% (財務報告)。客戶數增加 18% (指標儀表板)。
```

**正式風格**（完整提到）：
```markdown
營收增長 23% (<mention-page url="...">第四季財務報告</mention-page>)。客戶數增加 18% (<mention-page url="...">指標儀表板</mention-page>)。
```

**推薦在大多數研究文件中使用正式風格**，因為它提供了可點擊的導覽功能。
