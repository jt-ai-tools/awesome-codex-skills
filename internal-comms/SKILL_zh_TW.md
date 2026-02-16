---
name: internal-comms
description: 一組資源，協助我使用公司偏好的格式撰寫各種內部溝通內容。當被要求撰寫任何形式的內部溝通（狀態報告、領導層更新、3P 更新、公司電子報、常見問題、事件報告、專案更新等）時，Claude 應使用此技能。
license: 完整條款請參閱 LICENSE.txt
---

## 何時使用此技能
撰寫內部溝通內容時，請使用此技能處理：
- 3P 更新 (Progress 進度、Plans 計畫、Problems 問題)
- 公司電子報 (Company newsletters)
- 常見問題 (FAQ) 回覆
- 狀態報告 (Status reports)
- 領導層更新 (Leadership updates)
- 專案更新 (Project updates)
- 事件報告 (Incident reports)

## 如何使用此技能

撰寫任何內部溝通內容：

1. 從請求中**識別溝通類型**。
2. 從 `examples/` 目錄中**載入對應的指南檔案**：
    - `examples/3p-updates.md` - 用於「進度/計畫/問題」團隊更新。
    - `examples/company-newsletter.md` - 用於全公司性質的電子報。
    - `examples/faq-answers.md` - 用於回答常見問題。
    - `examples/general-comms.md` - 用於上述類型以外的任何其他內容。
3. **遵循該檔案中的具體指令**，包括格式、語氣與內容收集。

如果溝通類型與現有指南均不匹配，請要求澄清或索取更多關於所需格式的背景資訊。

## 關鍵字
3P 更新, 公司電子報, 公司通訊, 每週更新, 常見問題, 通用問題, 更新, 內部溝通
