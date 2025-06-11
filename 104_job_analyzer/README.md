# 104人力銀行職缺分析工具

## 專案架構說明

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

## 注意事項

- 所有新增的共用函數都應該放在 `common.py` 中
- 保持匯入的一致性，避免在不同模組中重複匯入相同的套件
- 使用型別提示（Type Hints）來提高程式碼的可維護性
