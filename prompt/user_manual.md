# 104人力銀行職缺分析系統使用手冊

## 系統簡介

本系統用於分析104人力銀行的職缺資訊，包括三大主要功能：
1. 職缺資訊搜集
2. 技能需求分析
3. 薪資資料分析

## 安裝指南

### 環境需求
- Python 3.8 或以上版本
- pip 套件管理器
- 4GB+ 記憶體
- 網路連線

### 安裝步驟

1. **取得專案程式碼**
   ```bash
   git clone [專案網址]
   cd 104_job_analyzer
   ```

2. **建立虛擬環境**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/Mac
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **安裝相依套件**
   ```bash
   pip install -r requirements.txt
   ```

## 使用說明

### 1. 命令列參數

主程式提供多種執行模式：

```bash
# 完整分析（預設模式）
python main.py --mode all

# 僅執行職缺分析
python main.py --mode job --category "2007001000" --keywords "Python"

# 僅執行技能分析
python main.py --mode skill

# 僅執行薪資分析
python main.py --mode salary
```

參數說明：
- `--mode`：執行模式，可選 `all`、`job`、`skill`、`salary`
- `--category`：職務類別代碼
- `--keywords`：搜尋關鍵字

### 2. 輸出檔案

系統會產生以下輸出：

1. **資料檔案** (output/)
   - `jobs_*.csv`：職缺資料
   - `skills_*.csv`：技能分析結果
   - `salaries_*.csv`：薪資分析結果

2. **日誌檔案** (logs/)
   - `analysis.log`：主要執行日誌
   - `skill_analysis.log`：技能分析日誌
   - `salary_analysis.log`：薪資分析日誌

### 3. 實用範例

1. **搜尋特定職缺**
   ```bash
   # 搜尋資料工程師職缺
   python main.py --mode job --category "2007001000" --keywords "資料工程師"
   
   # 搜尋 Python 相關職缺
   python main.py --mode job --keywords "Python"
   ```

2. **分析技能趨勢**
   ```bash
   # 分析所有已蒐集職缺的技能需求
   python main.py --mode skill
   ```

3. **分析薪資水平**
   ```bash
   # 分析所有已蒐集職缺的薪資資訊
   python main.py --mode salary
   ```

## 錯誤處理

### 常見問題排解

1. **網路連線問題**
   - 檢查網路連線
   - 檢查 logs/analysis.log 中的錯誤訊息
   - 確認 104 網站是否可正常存取

2. **資料解析錯誤**
   - 檢查職缺類別代碼是否正確
   - 確認搜尋關鍵字格式

3. **記憶體不足**
   - 減少並行處理的數量
   - 分批執行資料分析

### 錯誤代碼說明

- 0：正常執行完成
- 1：執行過程中發生錯誤

## 維護與更新

### 日誌管理
- 定期檢查 logs/ 目錄下的日誌檔案
- 可設定日誌檔案的保留時間
- 重要錯誤會同時記錄到檔案和顯示在終端

## 日誌系統使用指南

### 1. 日誌檔案位置

所有日誌檔案都集中存放在 `logs/` 目錄下：

```plaintext
logs/
├── analysis.log       # 主系統日誌
├── skill_analysis.log # 技能分析日誌
└── salary_analysis.log # 薪資分析日誌
```

### 2. 日誌內容說明

1. **主系統日誌 (analysis.log)**
   - 系統啟動和關閉資訊
   - 主要執行流程記錄
   - 一般錯誤訊息

2. **技能分析日誌 (skill_analysis.log)**
   - 技能資料擷取過程
   - 技能分析結果
   - 技能相關錯誤

3. **薪資分析日誌 (salary_analysis.log)**
   - 薪資資料擷取過程
   - 薪資分析結果
   - 薪資相關錯誤

### 3. 日誌級別說明

1. **DEBUG**
   - 詳細的技術資訊
   - 僅記錄在檔案中
   - 用於問題診斷

2. **INFO**
   - 一般執行資訊
   - 同時顯示在終端和記錄在檔案
   - 用於執行狀態追蹤

3. **WARNING**
   - 可能的問題警告
   - 不影響主要功能
   - 需要注意但不需立即處理

4. **ERROR**
   - 影響功能的錯誤
   - 需要立即處理
   - 包含錯誤細節和建議

### 4. 日誌分析與維護

1. **日常維護**
   - 定期備份日誌檔案
   - 檢查日誌大小
   - 清理舊的日誌檔案

2. **問題診斷**
   - 檢查 ERROR 級別的訊息
   - 追蹤相關的 WARNING 訊息
   - 分析 DEBUG 資訊找出問題原因

3. **效能監控**
   - 追蹤執行時間
   - 檢查資源使用情況
   - 評估系統效能

### 5. 常見問題處理

1. **日誌檔案過大**
   - 定期歸檔
   - 使用日誌輪替
   - 刪除舊的日誌檔案

2. **日誌無法寫入**
   - 檢查目錄權限
   - 確認磁碟空間
   - 驗證檔案系統狀態

3. **無法看到即時日誌**
   - 確認終端輸出設定
   - 檢查日誌級別設定
   - 驗證程式執行權限
