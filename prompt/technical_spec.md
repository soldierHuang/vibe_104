# 104人力銀行資料分析系統技術規格

## 系統架構

### 核心共用模組 (common.py)

此模組是系統的核心，負責：

#### 1. 集中式套件管理
- 統一匯入所有必要套件
- 標準化套件使用方式
- 版本相容性管理

#### 2. 工具函數庫
- 檔案操作工具
- 資料轉換工具
- 共用輔助函數

#### 3. 全域設定管理
- 系統常數定義
- 環境變數控制
- 設定檔整合

### 模組依賴關係

#### 1. 主要依賴
- `main.py` 依賴 `common.py`
- `common.py` 依賴 `config.py`
- 所有功能模組依賴 `common.py`

#### 2. 外部依賴
- 基礎系統套件
- 資料處理套件
- 網路請求套件

## 技術堆疊

### 1. 核心套件

#### 基礎套件
- os, sys：系統操作
- json：資料序列化
- datetime：時間處理
- pathlib：路徑管理
- typing：型別提示

#### 資料處理
- pandas：資料框架
- numpy：數值計算
- tqdm：進度顯示

#### 網路工具
- requests：HTTP 客戶端
- urllib：URL 處理

### 2. 開發工具
- Python 3.8+
- pip/conda：套件管理
- git：版本控制

## 資料流程

### 1. 資料擷取
- 來源：104人力銀行 API
- 方法：HTTP GET 請求
- 格式：JSON 回應

### 2. 資料處理
- 解析 JSON 資料
- 資料清理和轉換
- 結構化資料儲存

### 3. 資料分析
- 統計分析處理
- 資料聚合運算
- 結果格式化

### 4. 結果輸出
- CSV 檔案產生
- 記錄檔寫入
- 報告產生

## 系統需求

### 1. 環境需求
- Python 3.8 或以上
- 記憶體 4GB+
- 網路連線

### 2. 相依套件
```python
# 從 common.py 匯入
from modules.common import (
    pd,  # pandas
    np,  # numpy
    requests,  # HTTP 請求
    logger  # 記錄系統
)
```

## 安全性考量

### 1. 資料安全
- HTTPS 通訊加密
- 敏感資訊保護
- 存取權限控制

### 2. 錯誤處理
- 異常捕捉與記錄
- 自動重試機制
- 資料驗證

## 效能優化

### 1. 記憶體管理
- 批次處理大型資料
- 即時釋放資源
- 使用快取策略

### 2. 網路優化
- 連線池管理
- 請求重試機制
- 並行請求處理

## 維護性

### 1. 程式碼組織
- 模組化設計
- 清晰的職責分工
- 統一的編碼風格

### 2. 文件化
- 完整的註解
- API 文件
- 使用範例

## API 規格

### 1. 輸入參數
```python
{
    'KEYWORDS_STR': str,     # 搜尋關鍵字
    'JOBCAT_CODE': str,      # 職務類別代碼
    'ORDER_SETTING': int     # 排序方式
}
```

### 2. 回傳格式
```python
{
    'status': int,           # 狀態碼
    'message': str,          # 訊息
    'data': List[Dict]       # 資料內容
}
```

## 部署指南

### 1. 環境設定
```bash
# 建立虛擬環境
uv init 104_jobs_analysis

# 啟動虛擬環境
# source venv/bin/activate  # Unix
venv\Scripts\activate    # Windows

# 安裝相依套件
uv pip install -r requirements.txt
```

### 2. 設定檔配置
```python
# config.py
OUTPUT_DIR = 'path/to/output'
LOG_LEVEL = 'INFO'
```

### 3. 執行程式
```bash
# 執行分析
python main.py --mode all
```

## 日誌系統

### 1. 日誌架構

#### 目錄結構
- `/logs`：所有日誌檔案的根目錄
  - `analysis.log`：主系統日誌
  - `skill_analysis.log`：技能分析日誌
  - `salary_analysis.log`：薪資分析日誌

#### 日誌級別
- DEBUG：詳細的除錯資訊
- INFO：一般執行資訊
- WARNING：警告訊息
- ERROR：錯誤訊息
- CRITICAL：嚴重錯誤

#### 輸出設定
- 終端機：顯示 INFO 以上級別的訊息
- 檔案：記錄 DEBUG 以上級別的訊息

### 2. 日誌管理

#### LoggerManager 類別
- 單例模式管理所有日誌實例
- 避免重複建立日誌實例
- 統一日誌格式和處理方式

#### 專用日誌實例
- 主系統日誌：一般系統操作記錄
- 技能分析日誌：技能相關分析記錄
- 薪資分析日誌：薪資相關分析記錄

#### 日誌格式
```
時間戳記 - 模組名稱 - 日誌級別 - 訊息內容
```

### 3. 錯誤處理整合

#### 例外捕捉
- 網路請求錯誤
- 資料解析錯誤
- 檔案操作錯誤

#### 錯誤記錄
- 錯誤發生時間
- 錯誤堆疊追蹤
- 相關參數資訊

#### 錯誤處理流程
1. 捕捉例外
2. 記錄錯誤資訊
3. 進行錯誤恢復
4. 通知上層處理
