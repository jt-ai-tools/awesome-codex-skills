# 範例：從討論中產出操作指南 (How-To Guide)

**使用者請求**： 「將我們關於部署到生產環境的討論儲存為操作指南」

## 工作流程

### 1. 從聊天紀錄中擷取內容
從對話中識別出：
- 部署前置要求。
- 逐步操作程序。
- 常見問題與解決方案。
- 最佳實踐與提示。

### 2. 結構化為操作指南 (How-To)
組織為：
- 概覽與前置要求。
- 編號的部署步驟。
- 驗證步驟。
- 疑難排解章節。
- 相關資源。

### 3. 尋找存放位置
```
Notion:notion-search
query: "部署文件"
```
找到：工程 Wiki (Engineering Wiki) → 部署 (Deployment) 章節。

### 4. 建立指南
```
Notion:notion-create-pages
parent: { page_id: "deployment-section-id" }
```

## 輸出結果

```markdown
# 如何部署到生產環境 (How to Deploy to Production)

## 概覽
使用 GitHub Actions 進行零停機滾動更新 (Zero-downtime rolling updates) 的生產環境部署。
**所需時間**：15-20 分鐘 | **複雜度**：中階

## 前置要求
- [ ] PR 已獲批准並合併至 main 分支。
- [ ] 所有 CI 測試均已通過。
- [ ] 資料庫遷移 (Migrations) 已通過審核。
- [ ] 功能開關 (Feature flags) 已配置完成。

## 部署步驟

1. **驗證 main 分支已就緒**
   ```bash
   git checkout main && git pull
   ```

2. **標記發布版本 (Tag release)**
   ```bash
   git tag -a v1.2.3 -m "發布版本 v1.2.3"
   git push origin v1.2.3
   ```

3. **觸發部署**
   - GitHub Actions 會在推送標籤後自動啟動。
   - 監控網址：https://github.com/org/repo/actions

4. **資料庫遷移**（若需要）
   - 在 GitHub Actions 中自動執行。
   - 檢查日誌確認是否完成。

5. **驗證部署**
   - 等待健康檢查 (Health checks) 完成（約 2-3 分鐘）。
   - 測試關鍵 API 端點。
   - 在 Datadog 中檢查錯誤率。

## 驗證檢查清單
- [ ] k8s 儀表板中所有 Pod 狀態皆為健康。
- [ ] 過去 10 分鐘內錯誤率 < 0.1%。
- [ ] 回應時間 p95 < 500ms。
- [ ] 測試登入流程。
- [ ] 查看 Slack #alerts 頻道。

## 疑難排解

**健康檢查失敗**
→ 檢查 Pod 日誌：`kubectl logs -f deployment/api -n production`

**遷移錯誤**
→ 執行回滾 (Rollback)：還原標籤，遷移程式將自動回滾。

**錯誤率過高**
→ 緊急回滾：透過 GitHub Actions 自動部署前一個版本的標籤。

## 最佳實踐
- 在低流量時段進行部署（太平洋時間凌晨 2-4 點）。
- 至少有 2 名工程師在場支援。
- 部署後持續監控 30 分鐘。
- 在 #engineering Slack 頻道發布部署通知。

## 相關文件
- <mention-page url="...">回滾程序 (Rollback Procedure)</mention-page>
- <mention-page url="...">資料庫遷移指南</mention-page>
```

### 5. 提升可發現性 (Discovery)
```
Notion:notion-update-page
page_id: "engineering-wiki-homepage"
command: "insert_content_after"
```
在工程 Wiki 首頁 → 操作指南章節中新增連結。

## 關鍵成功因素
- 擷取了討論中的內部經驗知識 (Tribal knowledge)。
- 結構化為可執行的步驟。
- 納入了實戰經驗中的疑難排解方案。
- 透過在 Wiki 索引建立連結，使其易於發現。
- 增加了中繼資料（時間、複雜度）。
