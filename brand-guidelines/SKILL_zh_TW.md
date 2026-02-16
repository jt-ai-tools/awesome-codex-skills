---
name: brand-guidelines
description: 將 OpenAI 的品牌色彩與字體排版應用於任何需要符合 Codex/OpenAI 視覺風格的成品。當涉及品牌色彩或風格指南、視覺格式化或公司設計標準時，請使用此技能。
license: 完整條款請參閱 LICENSE.txt
---

# OpenAI 品牌風格化 (OpenAI Brand Styling)

## 概覽 (Overview)

使用此技能應用 OpenAI 的品牌識別與風格資源。

**關鍵字**: branding (品牌化), corporate identity (企業識別), visual identity (視覺識別), post-processing (後處理), styling (風格化), brand colors (品牌色彩), typography (字體排版), OpenAI brand, Codex, visual formatting (視覺格式化), visual design (視覺設計)

## 品牌指南 (Brand Guidelines)

### 色彩 (Colors)

**主色調 (Main Colors):**

- 碳黑色 (Charcoal): `#0E0F12` - 主要文字與深色背景
- 板岩色 (Slate): `#202123` - 表面背景
- 薄霧色 (Mist): `#F5F7FA` - 淺色背景與深色背景上的文字
- 鋼鐵色 (Steel): `#9EA1AA` - 次要元素與分隔線

**強調色 (Accent Colors):**

- OpenAI 綠: `#10A37F` - 主要強調色
- 天藍色 (Azure): `#2B8FFF` - 次要強調色
- 石墨色 (Graphite): `#40434A` - 用於圖標或線條的中性強調色

### 字體排版 (Typography)

- **標題**: Inter, Semibold/Bold (備用字體：Arial)
- **內文**: Inter, Regular (備用字體：Arial)
- **程式碼/等寬字體**: IBM Plex Mono (備用字體：Menlo/monospace)
- **注意**: 為了達到最佳效果，建議在您的環境中預先安裝這些字體

## 功能特性 (Features)

### 智慧字體應用

- 將 Inter Semibold/Bold 應用於標題 (24pt 及以上)
- 將 Inter Regular 應用於內文
- 將 IBM Plex Mono 應用於程式碼片段或行內程式碼
- 如果自訂字體不可用，自動回退 (Fallback) 至 Arial/Menlo
- 確保在所有系統上皆具備良好的可讀性

### 文字風格化

- 標題 (24pt+): Inter Semibold/Bold
- 內文: Inter Regular
- 根據背景自動選擇合適顏色 (視情況選用碳黑色或薄霧色)
- 保留文字層級與格式化

### 圖形與強調色

- 非文字圖形使用強調色
- 循環切換強調色使用順序：OpenAI 綠 → 天藍色 → 石墨色
- 在符合品牌的同時保持視覺趣味性

## 技術細節 (Technical Details)

### 字體管理

- 在可用時使用系統安裝的 Inter 和 IBM Plex Mono 字體
- 提供自動回退至 Arial (標題/內文) 和 Menlo/monospace (程式碼) 的機制
- 無需安裝字體即可在現有的系統字體下運作
- 為了獲得最佳效果，請在您的環境中預先安裝 Inter 和 IBM Plex Mono 字體

### 色彩應用

- 使用 RGB 顏色值以實現精確的品牌匹配
- 透過 python-pptx 的 RGBColor 類別進行應用
- 跨不同系統保持色彩忠實度
