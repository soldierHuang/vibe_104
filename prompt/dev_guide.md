# 104人力銀行職缺分析工具 - 開發指南

## 開發環境配置

### 必要套件

所有必要的套件都已在 `modules/common.py` 中集中管理：

#### 基礎套件
- os, sys：系統操作
- json：資料序列化
- time：時間操作
- datetime：日期時間處理
- pathlib：路徑管理
- typing：型別提示

#### 資料處理套件
- pandas：資料框架處理
- numpy：數值計算
- tqdm：進度顯示

#### 網路請求套件
- requests：HTTP 客戶端
- urllib：URL 處理

## 程式碼風格指南

### 1. 套件匯入規範

#### 正確的匯入方式
```python
from modules.common import pd, requests, logger

# 型別匯入
from modules.common import List, Dict, Optional

# 工具函數匯入
from modules.common import get_output_path, save_to_csv
```

#### 避免的匯入方式
```python
# 不要直接匯入已在 common.py 定義的套件
import pandas as pd
import requests
```

### 2. 型別提示使用

#### 基本型別提示
```python
from modules.common import List, Dict, Optional

def process_data(items: List[Dict]) -> Optional[pd.DataFrame]:
    pass

def get_job_info(job_id: str) -> Dict:
    pass
```

### 3. 記錄檔使用

#### 基本記錄
```python
from modules.common import logger

logger.info("處理開始")
logger.error("發生錯誤")
logger.debug("除錯資訊")
```

## 模組開發指南

### 1. 共用模組開發 (common.py)

#### 新增共用函數
```python
def new_utility_function(param: str) -> bool:
    """函數說明
    
    參數:
        param (str): 參數說明
        
    返回:
        bool: 返回值說明
    """
    pass
```

#### 新增套件
```python
# 在適當分類下新增
# 基礎套件
import new_package

# 資料處理套件
import new_data_package
```

### 2. 功能模組開發

#### 基本模組結構
```python
"""模組說明文件

此模組用於處理特定功能。
"""

from modules.common import (
    pd,
    logger,
    List,
    Dict
)

def main_function():
    """主要功能函數"""
    pass
```

### 3. 錯誤處理指南

#### 基本異常處理
```python
from modules.common import RequestException

try:
    # 程式碼
except RequestException as e:
    logger.error(f"網路請求錯誤：{e}")
    # 錯誤處理邏輯
```

## 測試開發指南

### 1. 測試文件結構
```plaintext
tests/
├── test_skill_analyzer.py
├── test_salary_analyzer.py
└── test_job_analyzer.py
```

### 2. 測試程式碼範例
```python
from modules.common import pd, np
from modules.your_module import your_function

def test_your_function():
    # 測試準備
    input_data = {...}
    
    # 執行測試
    result = your_function(input_data)
    
    # 驗證結果
    assert result is not None
```

## 文件更新指南

### 需要更新的文件

1. 主要文件
   - `README.md`：主要使用說明
   - `prompt/dev_guide.md`：開發指南
   - `prompt/technical_spec.md`：技術規格
   - `prompt/architecture.md`：架構文件
   - `prompt/user_manual.md`：使用者手冊

### 文件更新原則

1. **一致性**
   - 保持文件格式一致
   - 使用統一的術語

2. **即時性**
   - 程式碼變更時同步更新文件
   - 保持文件的時效性

3. **完整性**
   - 涵蓋所有重要資訊
   - 提供足夠的範例

## 日誌系統使用指南

### 基本使用
```python
from modules.logger_setup import logger

# 不同級別的日誌
logger.debug("詳細的除錯資訊")
logger.info("一般執行資訊")
logger.warning("警告訊息")
logger.error("錯誤訊息")
logger.critical("嚴重錯誤")
```

### 自訂日誌
```python
from modules.logger_setup import setup_logger

# 建立特定模組的日誌
skill_logger = setup_logger("skill_analyzer", "skill_analysis.log")
salary_logger = setup_logger("salary_analyzer", "salary_analysis.log")
```

### 最佳實踐
1. 使用適當的日誌級別
   - DEBUG：用於開發階段的詳細資訊
   - INFO：用於重要的執行步驟和結果
   - WARNING：可能的問題但不影響執行
   - ERROR：影響執行但可恢復的錯誤
   - CRITICAL：需要立即處理的嚴重問題

2. 提供有意義的訊息
   - 包含關鍵變數值
   - 描述事件的上下文
   - 註明錯誤的可能原因

3. 結構化日誌
   - 使用一致的格式
   - 加入時間戳記
   - 標註模組名稱

4. 錯誤處理整合
```python
try:
    # 程式碼
except Exception as e:
    logger.error(f"發生錯誤: {str(e)}")
    # 錯誤處理
```
