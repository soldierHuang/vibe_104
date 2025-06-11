# 104人力銀行資料分析系統架構

## 系統概觀

本系統採用模組化設計，以 `common.py` 作為核心共用模組，集中管理所有套件匯入和共用功能。系統具有完整的日誌追蹤和錯誤處理機制。

## 專案結構

```plaintext
104_job_analyzer/
├── main.py                    # 主程式進入點
├── config.py                  # 系統配置
├── requirements.txt           # 套件相依性清單
├── README.md                 # 專案說明文件
├── modules/                  # 功能模組目錄
│   ├── __init__.py
│   ├── common.py            # 核心共用模組
│   ├── logger_setup.py      # 日誌設定模組
│   ├── fetcher.py           # 資料擷取模組
│   ├── processor.py         # 資料處理模組
│   ├── salary_analyzer.py   # 薪資分析模組
│   └── skill_analyzer.py    # 技能分析模組
├── logs/                    # 日誌檔案目錄
│   ├── analysis.log        # 主要分析日誌
│   ├── skill_analysis.log  # 技能分析日誌
│   └── salary_analysis.log # 薪資分析日誌
├── output/                  # 輸出檔案目錄
│   ├── jobs_*.csv         # 職缺資料
│   ├── skills_*.csv       # 技能資料
│   └── salaries_*.csv     # 薪資資料
└── tests/                  # 測試程式目錄
    └── __init__.py
```

## 核心模組說明

### 共用模組 (common.py)

作為系統的核心，提供以下功能：

1. **套件管理**
   - 基礎系統套件 (os, sys, json, datetime, pathlib)
   - 資料處理套件 (pandas, numpy, tqdm)
   - 網路請求套件 (requests, urllib)
   - 型別提示套件 (typing)

2. **共用工具函數**
   - 檔案路徑管理 (get_output_path)
   - CSV 輸出處理 (save_to_csv)
   - JSON 資料擷取 (fetch_json)
   - 安全資料存取 (safe_get)

3. **全域設定**
   - HTTP 請求標頭
   - 輸出目錄配置
   - 日誌設定
   - 預設參數

### 日誌模組 (logger_setup.py)

負責系統的日誌管理：

1. **日誌配置**
   - 檔案輸出
   - 終端輸出
   - 日誌格式化

2. **日誌級別管理**
   - DEBUG：開發除錯資訊
   - INFO：一般執行資訊
   - WARNING：警告訊息
   - ERROR：錯誤資訊

### 日誌系統架構

#### 1. 日誌管理器 (LoggerManager)

此類別負責統一管理所有日誌實例，提供以下功能：

1. **日誌實例管理**
   - 集中管理所有日誌實例
   - 避免重複建立實例
   - 統一配置和格式

2. **多重輸出**
   - 終端機輸出（即時監控）
   - 檔案輸出（永久記錄）
   - 可配置的輸出級別

3. **專用日誌**
   - 主系統日誌 (analysis.log)
   - 技能分析日誌 (skill_analysis.log)
   - 薪資分析日誌 (salary_analysis.log)

#### 2. 日誌目錄結構

```plaintext
logs/
├── analysis.log       # 主系統日誌
├── skill_analysis.log # 技能分析日誌
└── salary_analysis.log # 薪資分析日誌
```

#### 3. 日誌設定管理

1. **日誌級別**
   - 終端機：INFO 及以上
   - 檔案：DEBUG 及以上

2. **日誌格式**
   ```
   2025-06-11 19:25:43,292 - 104_analyzer - INFO - 開始執行資料分析
   ```

3. **檔案處理**
   - 自動建立日誌目錄
   - UTF-8 編碼支援
   - 檔案輪替管理

#### 4. 整合應用

1. **模組使用方式**
   ```python
   from modules.logger_setup import get_logger
   
   # 取得專用日誌實例
   logger = get_logger("skill_analyzer")
   ```

2. **錯誤處理流程**
   ```python
   try:
       # 程式邏輯
   except Exception as e:
       logger.error(f"發生錯誤: {str(e)}")
       # 錯誤處理
   ```

## 模組間依賴關係

### 主要依賴流程

1. **設定層級**
   - `config.py`：提供系統配置
   - `logger_setup.py`：提供日誌功能

2. **核心層級**
   - `common.py` 依賴 `config.py` 和 `logger_setup.py`

3. **功能層級**
   - 所有功能模組依賴 `common.py`
   - `processor.py` 依賴 `fetcher.py`
   - `skill_analyzer.py` 和 `salary_analyzer.py` 依賴 `processor.py`

4. **應用層級**
   - `main.py` 協調所有模組

### 外部依賴管理

1. **基礎環境**
   - Python 3.8+
   - pip 套件管理

2. **核心套件**
   - pandas, numpy：資料處理
   - requests：網路請求
   - tqdm：進度顯示

3. **開發工具**
   - pytest：單元測試
   - black：程式碼格式化
   - flake8：程式碼檢查

## 資料流程

### 資料處理流程

1. **資料擷取階段**
   - 來源：104人力銀行 API
   - 處理元件：`fetcher.py`
   - 輸出：原始 JSON 資料

2. **資料處理階段**
   - 輸入：原始 JSON 資料
   - 處理元件：`processor.py`
   - 輸出：結構化資料

3. **資料分析階段**
   - 輸入：結構化資料
   - 處理元件：分析模組
   - 輸出：分析結果

4. **結果輸出階段**
   - 輸入：分析結果
   - 處理：格式轉換
   - 輸出：CSV 檔案

## 記錄系統

- 使用 `common.py` 中的統一記錄器
- 支援多層級記錄
- 自動檔案輪替

## 錯誤處理

- 集中式異常處理
- 標準化錯誤回報
- 自動重試機制

## 效能考量

- 非同步網路請求
- 批次資料處理
- 記憶體使用最佳化

## 安全性

- HTTPS 通訊
- 資料加密儲存
- 存取控制機制

## 功能模組說明

### 1. 技能分析模組 (skill_analyzer.py)
- 職務技能分析
- 證照要求分析
- 技能統計與匯出

### 2. 薪資分析模組 (salary_analyzer.py)
- 薪資區間分析
- 產業薪資趨勢
- 經驗與薪資關係

### 3. 職缺分析模組 (job_listing_analyzer.py)
- 職缺列表擷取
- 職缺詳細資訊分析
- 工作條件統計

### 4. 基礎模組 (fetcher.py & processor.py)
- 基礎資料擷取功能
- 通用資料處理函式
- 共用工具函式

## 模組執行流程

### 技能分析流程

1. **初始化階段**
   - 獲取職務類別資料
   - 扁平化類別結構

2. **資料擷取階段**
   - 並行擷取技能資料
   - 錯誤處理和重試

3. **處理階段**
   - 合併處理結果
   - 資料清理和轉換

4. **輸出階段**
   - 產生 CSV 檔案
   - 記錄執行結果

### 薪資分析流程

1. **資料準備**
   - 載入職務類別
   - 初始化分析參數

2. **資料處理**
   - 並行擷取薪資資料
   - 資料統計和分析

3. **結果輸出**
   - 產生統計報告
   - 儲存分析結果

### 職缺分析流程

1. **搜尋配置**
   - 設定搜尋條件
   - 初始化參數

2. **資料收集**
   - 擷取職缺列表
   - 取得詳細資訊

3. **資料處理**
   - 資料清理轉換
   - 資訊結構化

4. **結果輸出**
   - 產生分析報告
   - 輸出 CSV 檔案

## 資料格式

### 輸入參數格式

```python
DEFAULT_PARAMS = {
    'KEYWORDS_STR': "雲端工程師",     # 搜尋關鍵字
    'JOBCAT_CODE': "2007000000",    # 職務類別代碼
    'ORDER_SETTING': 15             # 排序方式
}
```

### 輸出檔案格式

所有輸出檔案使用 UTF-8-SIG 編碼的 CSV 格式：
- `104_skills_YYYYMMDD.csv`：技能分析結果
- `104_salaries_YYYYMMDD.csv`：薪資分析結果
- `104_job_listings_YYYYMMDD.csv`：職缺分析結果

## 系統執行說明

### 技能分析執行
```bash
python main.py skills
```

### 薪資分析執行
```bash
python main.py salaries
```

### 職缺分析執行
```bash
python main.py jobs --keywords "雲端工程師" --category "2007000000"
```

### 完整分析執行
```bash
python main.py all
```
