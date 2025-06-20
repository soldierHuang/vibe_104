# 104人力銀行職缺分析工具

## 專案架構說明

```
104_job_analyzer/
├── config.py           # 設定檔
├── main.py            # 主程式進入點
├── modules/           # 核心功能模組
│   ├── common.py      # 共用工具和常數
│   ├── fetcher.py     # 資料抓取模組
│   ├── processor.py   # 資料處理模組
│   ├── salary_analyzer.py  # 薪資分析模組
│   └── skill_analyzer.py   # 技能分析模組
├── output/           # 輸出資料目錄
│   ├── 104_salaries_*.csv
│   ├── 104_skills_*.csv
│   └── jobs_page_*.csv
├── tests/           # 測試目錄
└── requirements.txt # 相依套件清單
```

### 共用模組 (`modules/common.py`)

這個模組集中管理所有常用的套件匯入和工具函數，方便其他模組使用。

#### 主要功能

1. 集中管理套件匯入
2. 提供共用工具函數
3. 統一設定和常數管理

#### 如何使用

在其他模組中，您可以使用以下方式匯入所需的套件和功能：

```python
# 匯入基礎套件
from modules.common import (
    os,
    pd,
    datetime,
    logging
)

# 匯入資料型別
from modules.common import Optional, List, Dict, Set, Tuple

# 匯入網路請求相關
from modules.common import requests, RequestException

# 匯入工具函數
from modules.common import get_output_path, save_to_csv

# 匯入共用 logger
from modules.common import logger
```

#### 可用的套件和功能

1. **基礎套件**
   - os, sys, json, time
   - datetime, timedelta
   - Path
   - typing 相關型別

2. **資料處理套件**
   - pandas (as pd)
   - numpy (as np)
   - tqdm

3. **網路請求套件**
   - requests
   - RequestException
   - urljoin, urlparse

4. **工具函數**
   - get_output_path()：生成輸出檔案路徑
   - save_to_csv()：將 DataFrame 儲存為 CSV

5. **共用設定**
   - logger：專案共用的 logging 實例
   - OUTPUT_DIR：輸出目錄路徑
   - HEADERS：HTTP 請求標頭
   - DEFAULT_PARAMS：預設請求參數

## 功能模組說明

### 1. 資料抓取模組 (`fetcher.py`)
- 負責從104人力銀行網站抓取職缺資訊
- 處理 HTTP 請求和回應
- 實作資料抓取的重試機制

### 2. 資料處理模組 (`processor.py`)
- 清理和轉換原始職缺資料
- 標準化資料格式
- 過濾無效資料

### 3. 薪資分析模組 (`salary_analyzer.py`)
- 分析職位薪資範圍
- 計算產業薪資統計
- 生成薪資報表

### 4. 技能分析模組 (`skill_analyzer.py`)
- 分析職位要求技能
- 統計熱門技能趨勢
- 產生技能需求報告

## 輸出檔案說明

### 資料檔案
- `104_salaries_YYYYMMDD.csv`: 薪資分析結果
- `104_skills_YYYYMMDD.csv`: 技能分析結果
- `jobs_page_N_YYYYMMDD.csv`: 原始職缺資料

## 使用方式

1. 安裝相依套件：
```bash
pip install -r requirements.txt
```

2. 執行分析：
```bash
python main.py
```

## 注意事項

- 所有新增的共用函數都應該放在 `common.py` 中
- 保持匯入的一致性，避免在不同模組中重複匯入相同的套件
- 使用型別提示（Type Hints）來提高程式碼的可維護性
