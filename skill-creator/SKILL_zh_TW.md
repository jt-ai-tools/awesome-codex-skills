---
name: skill-creator
description: 建立高效技能的指南。當使用者想要建立新技能（或更新現有技能）以透過專業知識、工作流程或工具整合擴展 Codex 的功能時，應使用此技能。
metadata:
  short-description: 建立或更新技能
---

# 技能建立指南 (Skill Creator)

此技能為建立高效的技能提供指引。

## 關於技能 (Skills)

技能是模組化、自包含的套件，透過提供專業知識、工作流程與工具來擴展 Codex 的能力。可以將它們想像為特定領域或任務的「入門指南 (Onboarding guides)」——它們將 Codex 從通用型代理人轉變為配備程序性知識 (Procedural knowledge) 的專業型代理人，而這些知識是任何模型都無法完全具備的。

### 技能提供的內容

1. **專業工作流程**：針對特定領域的多步驟處理程序。
2. **工具整合**：處理特定檔案格式或 API 的指令。
3. **領域專業知識**：公司特定的知識、結構綱要 (Schemas)、商業邏輯。
4. **隨附資源**：用於複雜且重複任務的腳本、參考資料與資產。

## 核心原則

### 簡潔是關鍵 (Concise is Key)

上下文視窗 (Context window) 是一種公共資源。技能與 Codex 所需的其他內容共用上下文視窗：系統提示詞、對話歷史、其他技能的中繼資料以及使用者的實際請求。

**預設假設：Codex 已經非常聰明。** 僅新增 Codex 尚未具備的背景資訊。對每一項資訊提出挑戰：「Codex 真的需要這段解釋嗎？」以及「這段文字值得它所佔用的權杖 (Token) 成本嗎？」

優先使用簡潔的範例，而非冗長的解釋。

### 設定適當的自由度 (Degrees of Freedom)

根據任務的脆弱性 (Fragility) 與變異性來調整具體化程度：

**高自由度（文字指令）**：當多種方法皆有效、決策取決於上下文或由啟發式方法 (Heuristics) 引導時使用。

**中自由度（偽代碼或帶參數的腳本）**：當存在偏好的模式、可接受某些變異，或配置會影響行為時使用。

**低自由度（特定的腳本，極少參數）**：當操作脆弱且容易出錯、一致性至關重要或必須遵循特定順序時使用。

將 Codex 想像成在路徑上探索：一座兩旁是懸崖的窄橋需要特定的護欄（低自由度），而一片開闊的田野則允許許多路線（高自由度）。

### 技能的結構剖析 (Anatomy of a Skill)

每個技能都由一個必備的 `SKILL.md` 檔案與選配的隨附資源組成：

```
skill-name/
├── SKILL.md (必備)
│   ├── YAML 前言中繼資料 (必備)
│   │   ├── name: (必備)
│   │   └── description: (必備)
│   └── Markdown 指令 (必備)
└── 隨附資源 (選配)
    ├── scripts/          - 可執行程式碼 (Python/Bash 等)
    ├── references/       - 旨在根據需要載入上下文的文件
    └── assets/           - 輸出中使用的檔案（模板、圖標、字體等）
```

#### SKILL.md (必備)

每個 `SKILL.md` 包含：

- **前言 (Frontmatter)** (YAML)：包含 `name` 和 `description` 欄位。這是 Codex 讀取以判斷何時使用該技能的唯一欄位，因此清晰且全面地描述技能是什麼以及何時應使用它是非常重要的。
- **正文 (Body)** (Markdown)：使用技能的指令與引導。僅在技能觸發後（如有必要）才載入。

#### 隨附資源 (選配)

##### 腳本 (`scripts/`)

針對需要確定性可靠性 (Deterministic reliability) 或重複編寫的任務，提供可執行程式碼 (Python/Bash 等)。

- **何時包含**：當相同的程式碼被反覆重寫，或需要確定性可靠性時。
- **範例**：用於 PDF 旋轉任務的 `scripts/rotate_pdf.py`。
- **優點**：權杖效率高、具確定性，且可以在不載入上下文的情況下執行。
- **註記**：Codex 可能仍需要讀取腳本以進行修補 (Patching) 或針對環境進行調整。

##### 參考資料 (`references/`)

旨在根據需要載入上下文的文件與參考材料，用以告知 Codex 的處理程序與思考。

- **何時包含**：供 Codex 在工作時參考的文件。
- **範例**：財務結構綱要 `references/finance.md`、公司 NDA 模板 `references/mnda.md`、公司政策 `references/policies.md`、API 規範 `references/api_docs.md`。
- **使用場景**：資料庫結構綱要、API 文件、領域知識、公司政策、詳細的工作流程指南。
- **優點**：保持 `SKILL.md` 精簡，僅在 Codex 判定需要時才載入。
- **最佳實踐**：如果檔案很大（超過 1 萬字），請在 `SKILL.md` 中包含 grep 搜尋模式。
- **避免重複**：資訊應存在於 `SKILL.md` 或參考檔案中，而非兩者皆有。除非對技能至關重要，否則優先將詳細資訊放入參考檔案中——這能保持 `SKILL.md` 精簡，同時讓資訊可被發現，且不霸佔上下文視窗。在 `SKILL.md` 中僅保留核心程序指令與工作流程引導；將詳細的參考材料、結構綱要與範例移動到參考檔案。

##### 資產 (`assets/`)

不打算載入上下文，而是用於 Codex 產出的成品中的檔案。

- **何時包含**：當技能需要將檔案用於最終輸出時。
- **範例**：品牌資產 `assets/logo.png`、PowerPoint 模板 `assets/slides.pptx`、HTML/React 樣板 `assets/frontend-template/`、排版字體 `assets/font.ttf`。
- **使用場景**：模板、圖像、圖標、樣板程式碼 (Boilerplate)、字體、被複製或修改的範例文件。
- **優點**：將輸出資源與文件分離，使 Codex 能在不載入上下文的情況下使用檔案。

#### 技能中不應包含的內容

技能應僅包含直接支援其功能的必要檔案。請勿建立無關的文件或輔助檔案，包括：

- README.md
- INSTALLATION_GUIDE.md (安裝指南)
- QUICK_REFERENCE.md (快速參考)
- CHANGELOG.md (變更日誌)
- 等等。

技能應僅包含 AI 代理人執行當前工作所需的資訊。它不應包含關於其建立過程、安裝與測試程序、面向使用者的文件等輔助背景資訊。建立額外的文件檔案只會增加雜亂與困惑。

### 漸進式揭露設計原則 (Progressive Disclosure)

技能使用三層載入系統來高效管理上下文：

1. **中繼資料 (名稱 + 描述)** - 始終在上下文中（約 100 字）。
2. **SKILL.md 正文** - 技能觸發時載入（小於 5000 字）。
3. **隨附資源** - 根據 Codex 需要載入（無限制，因為腳本可以在不讀入上下文視窗的情況下執行）。

#### 漸進式揭露模式

將 `SKILL.md` 正文保持在核心要點且不超過 500 行，以最小化上下文膨脹。接近此限制時將內容拆分為獨立檔案。將內容拆分到其他檔案時，務必從 `SKILL.md` 中引用它們並清晰描述何時讀取它們，以確保技能的使用者知道它們的存在以及何時使用。

**核心原則：** 當技能支援多種變體、框架或選項時，在 `SKILL.md` 中僅保留核心工作流程與選擇指引。將變體特有的細節（模式、範例、配置）移至獨立的參考檔案。

**模式 1：帶參考資料的高階指南**

```markdown
# PDF 處理 (PDF Processing)

## 快速開始

使用 pdfplumber 提取文字：
[程式碼範例]

## 進階功能

- **表單填寫**：完整指南請參閱 [FORMS.md](FORMS.md)
- **API 參考**：所有方法請參閱 [REFERENCE.md](REFERENCE.md)
- **範例**：常見模式請參閱 [EXAMPLES.md](EXAMPLES.md)
```

Codex 僅在需要時載入 `FORMS.md`、`REFERENCE.md` 或 `EXAMPLES.md`。

**模式 2：特定領域組織**

對於跨多個領域的技能，按領域組織內容以避免載入無關的上下文：

```
bigquery-skill/
├── SKILL.md (概覽與導覽)
└── reference/
    ├── finance.md (營收、計費指標)
    ├── sales.md (機會、業務管道)
    ├── product.md (API 使用、功能)
    └── marketing.md (行銷活動、歸因)
```

當使用者詢問銷售指標時，Codex 僅讀取 `sales.md`。

同樣地，對於支援多個框架或變體的技能，按變體組織：

```
cloud-deploy/
├── SKILL.md (工作流程 + 供應商選擇)
└── references/
    ├── aws.md (AWS 部署模式)
    ├── gcp.md (GCP 部署模式)
    └── azure.md (Azure 部署模式)
```

當使用者選擇 AWS 時，Codex 僅讀取 `aws.md`。

**模式 3：條件式細節**

顯示基礎內容，連結至進階內容：

```markdown
# DOCX 處理

## 建立文件

使用 docx-js 建立新文件。請參閱 [DOCX-JS.md](DOCX-JS.md)。

## 編輯文件

對於簡單編輯，直接修改 XML。

**針對標註修訂 (Tracked changes)**：請參閱 [REDLINING.md](REDLINING.md)
**針對 OOXML 細節**：請參閱 [OOXML.md](OOXML.md)
```

Codex 僅在使用者需要這些功能時才讀取 `REDLINING.md` 或 `OOXML.md`。

**重要準則：**

- **避免深層嵌套的引用** - 保持參考檔案距離 `SKILL.md` 僅一層。所有參考檔案應直接從 `SKILL.md` 連結。
- **結構化較長的參考檔案** - 對於超過 100 行的檔案，在頂部包含目錄 (TOC)，以便 Codex 在預覽時能看到完整範圍。

## 技能建立流程 (Skill Creation Process)

建立技能涉及以下步驟：

1. 透過具體範例理解技能
2. 規劃可重複使用的技能內容（腳本、參考資料、資產）
3. 初始化技能（執行 `init_skill.py`）
4. 編輯技能（實作資源並撰寫 `SKILL.md`）
5. 打包技能（執行 `package_skill.py`）
6. 根據實際使用情況進行迭代

請按順序遵循這些步驟，除非有明確理由說明不適用，否則不要跳過。

### 技能命名

- 僅使用小寫字母、數字與連字號；將使用者提供的標題標準化為連字號分隔 (hyphen-case)（例如：「Plan Mode」 -> `plan-mode`）。
- 生成名稱時，請生成 64 個字元以內（字母、數字、連字號）的名稱。
- 優先使用簡短、動詞引導的短語來描述動作。
- 當工具名稱能提高清晰度或觸發率時，使用工具作為命名空間（例如：`gh-address-comments`, `linear-address-issue`）。
- 技能資料夾的名稱應與技能名稱完全一致。

### 第一步：透過具體範例理解技能

僅在技能的使用模式已非常清晰時才跳過此步驟。即使在處理現有技能時，此步驟仍然非常有價值。

若要建立高效技能，請清晰地理解該技能將如何被使用的具體範例。這種理解可以來自使用者的直接範例，或透過使用者回饋驗證後生成的範例。

例如，在建構 `image-editor` 技能時，相關問題包括：

- 「image-editor 技能應支援哪些功能？編輯、旋轉，還有其他的嗎？」
- 「您能舉一些關於此技能如何被使用的範例嗎？」
- 「我可以想像使用者提出類似『移除這張圖片的紅眼』或『旋轉這張圖片』的要求。您還能想到其他使用方式嗎？」
- 「使用者會說什麼來觸發此技能？」

為了避免讓使用者感到不知所措，避免在單一訊息中詢問過多問題。從最重要的問題開始，並根據需要跟進，以提高效率。

當對技能應支援的功能有了清晰的認識時，即可結束此步驟。

### 第二步：規劃可重複使用的技能內容

為了將具體範例轉化為高效技能，請分析每個範例：

1. 思考如何從頭開始執行該範例。
2. 識別在反覆執行這些工作流程時，哪些腳本、參考資料與資產會有所幫助。

範例：建立 `pdf-editor` 技能來處理如「幫我旋轉這份 PDF」的查詢時，分析顯示：

1. 旋轉 PDF 每次都需要重寫相同的程式碼。
2. 在技能中儲存一個 `scripts/rotate_pdf.py` 腳本會很有幫助。

範例：設計 `frontend-webapp-builder` 技能來處理如「幫我建構一個 Todo 應用程式」的查詢時，分析顯示：

1. 編寫前端網頁應用程式每次都需要相同的 HTML/React 樣板。
2. 在技能中儲存一個包含樣板 HTML/React 專案檔案的 `assets/hello-world/` 模板會很有幫助。

範例：建立 `big-query` 技能來處理如「今天有多少使用者登入？」的查詢時，分析顯示：

1. 查詢 BigQuery 每次都需要重新探索資料表結構綱要與關聯性。
2. 在技能中儲存一個記錄資料表結構綱要的 `references/schema.md` 檔案會很有幫助。

若要確立技能內容，請分析每個具體範例，建立一份要包含的可重複使用資源清單：腳本、參考資料與資產。

### 第三步：初始化技能

在此階段，是時候真正建立技能了。

僅在開發的技能已存在，且需要迭代或打包時，才跳過此步驟並繼續下一步。

從頭開始建立新技能時，務必執行 `init_skill.py` 腳本。該腳本會便捷地生成一個新的模板技能目錄，自動包含技能所需的一切，使技能建立過程更高效、更可靠。

用法：

```bash
scripts/init_skill.py <技能名稱> --path <輸出目錄> [--resources scripts,references,assets] [--examples]
```

範例：

```bash
scripts/init_skill.py my-skill --path skills/public
scripts/init_skill.py my-skill --path skills/public --resources scripts,references
scripts/init_skill.py my-skill --path skills/public --resources scripts --examples
```

該腳本會：

- 在指定路徑建立技能目錄。
- 生成一個帶有正確前言與 TODO 佔位符的 `SKILL.md` 模板。
- 根據 `--resources` 選項建立資源目錄。
- 當設定 `--examples` 時加入範例檔案。

初始化後，根據需要自訂 `SKILL.md` 並新增資源。如果您使用了 `--examples`，請替換或刪除佔位檔案。

### 第四步：編輯技能

編輯（新生成的或現有的）技能時，請記住該技能是為了讓另一個 Codex 實體使用而建立的。請包含對 Codex 有益且非顯而易見的資訊。思考哪些程序性知識、領域特定細節或可重複使用的資產，能協助另一個 Codex 實體更有效地執行這些任務。

#### 學習成熟的設計模式

根據您的技能需求參考這些指南：

- **多步驟流程**：參考 `references/workflows.md` 以了解順序性工作流程與條件邏輯。
- **特定輸出格式或品質標準**：參考 `references/output-patterns.md` 以了解模板與範例模式。

這些檔案包含了高效技能設計的既定最佳實踐。

#### 從可重複使用的技能內容開始

開始實作時，從上述識別出的可重複使用資源開始：`scripts/`、`references/` 與 `assets/` 檔案。請注意，此步驟可能需要使用者輸入。例如，在實作 `brand-guidelines` 技能時，使用者可能需要提供要儲存在 `assets/` 中的品牌資產或模板，或要儲存在 `references/` 中的文件。

新增的腳本必須透過實際執行進行測試，以確保沒有 Bug 且輸出符合預期。如果存在許多相似腳本，只需測試具代表性的樣本，以確保所有腳本都能正常運作，同時平衡完成時間。

如果您使用了 `--examples`，請刪除技能不需要的任何佔位檔案。僅建立實際需要的資源目錄。

#### 更新 SKILL.md

**撰寫準則：** 始終使用命令式 (Imperative) / 不定式 (Infinitive) 形式。

##### 前言 (Frontmatter)

撰寫包含 `name` 和 `description` 的 YAML 前言：

- `name`：技能名稱。
- `description`：這是您技能的主要觸發機制，協助 Codex 瞭解何時使用該技能。
  - 同時包含技能的功能以及具體的觸發點/情境。
  - 將所有「何時使用 (when to use)」資訊放在這裡——而非正文中。正文僅在觸發後載入，因此正文中的「何時使用此技能」章節對 Codex 沒有幫助。
  - `docx` 技能的描述範例：「Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when Codex needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks」

前言中請勿包含任何其他欄位。

##### 正文 (Body)

撰寫使用技能及其隨附資源的指令。

### 第五步：打包技能 (Packaging a Skill)

技能開發完成後，必須打包成可分發的 `.skill` 檔案以與使用者分享。打包程序會先自動驗證技能，以確保其符合所有要求：

```bash
scripts/package_skill.py <技能資料夾路徑>
```

選填的輸出目錄指定方式：

```bash
scripts/package_skill.py <技能資料夾路徑> ./dist
```

打包腳本將會：

1. **自動驗證**技能，檢查：
   - YAML 前言格式與必填欄位。
   - 技能命名慣例與目錄結構。
   - 描述的完整性與品質。
   - 檔案組織與資源引用。

2. 如果驗證通過則**打包**技能，建立一個以技能命名的 `.skill` 檔案（例如：`my-skill.skill`），其中包含所有檔案並維持正確的目錄結構以便分發。`.skill` 檔案是一個後綴為 `.skill` 的 ZIP 壓縮檔。

如果驗證失敗，腳本將回報錯誤並退出，不會建立套件。修正任何驗證錯誤後，再次執行打包指令。

### 第六步：迭代 (Iterate)

測試技能後，使用者可能會要求改進。這通常發生在使用技能後，帶著技能表現的新背景資訊進行。

**迭代工作流程：**

1. 在實際任務中使用技能。
2. 注意遇到的困難或低效率之處。
3. 識別應如何更新 `SKILL.md` 或隨附資源。
4. 實作變更並再次測試。
