"""共用模組：提供共用的函數和常數

此模組用於集中管理專案中所有常用的套件導入、設定和工具函數。
其他模組可以直接從這裡匯入所需的套件和功能。

匯入方式範例：
    from modules.common import (
        # 基礎套件
        os, sys, json, datetime, Path, argparse,
        # 資料處理
        pd, np, tqdm,
        # 型別提示
        Dict, List, Set, Optional, Any, Tuple,
        # 網路請求
        requests,
        # 工具函數
        save_to_csv, fetch_json, get_output_path,
        # 日誌
        logger
    )
"""

# 基礎系統套件
import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional, Any, Tuple, Union
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

# 資料處理套件
import pandas as pd
import numpy as np
from tqdm import tqdm

# 網路請求套件
import requests
import urllib.parse

# 專案設定
from config import (
    OUTPUT_DIR,
    LOG_DIR,
    HEADERS,
    URL_JOB_SEARCH,
    URL_JOB_DETAIL_BASE,
    URL_JOB_CAT,
    MAX_WORKERS_JOB,
    DEFAULT_PARAMS,
)

from .logger_setup import logger

def get_output_path(filename: str) -> Path:
    """取得輸出檔案的完整路徑
    
    Args:
        filename: 檔案名稱
        
    Returns:
        Path: 完整的檔案路徑
    """
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path / filename

def save_to_csv(df: pd.DataFrame, prefix: str) -> None:
    """儲存DataFrame到CSV檔案
    
    Args:
        df: 要儲存的DataFrame
        prefix: 檔名前綴
    """
    try:
        today = datetime.now().strftime("%Y%m%d")
        output_file = get_output_path(f"{prefix}_{today}.csv")
        
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        logger.info(f"資料已儲存至 {output_file}")
    except Exception as e:
        logger.error(f"儲存CSV檔案時發生錯誤: {str(e)}")

def fetch_json(url: str, headers: Dict = HEADERS) -> Optional[Dict]:
    """從URL獲取JSON資料
    
    Args:
        url: 要請求的URL
        headers: HTTP請求標頭
        
    Returns:
        Optional[Dict]: JSON回應資料，失敗時返回None
    """
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"獲取JSON資料時發生錯誤: {str(e)}")
        return None

def safe_get(data: Dict, *keys: str, default: Any = None) -> Any:
    """安全地從巢狀字典中獲取值
    
    Args:
        data: 字典資料
        *keys: 要獲取的鍵路徑
        default: 當鍵不存在時的預設值
        
    Returns:
        Any: 獲取的值或預設值
    """
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError, IndexError):
            return default
    return data

# 匯出所有需要的名稱
__all__ = [
    # 基礎套件
    'os', 'sys', 'json', 'datetime', 'Path', 'argparse',
    # 資料處理
    'pd', 'np', 'tqdm',
    # 型別提示
    'Dict', 'List', 'Set', 'Optional', 'Any', 'Tuple', 'Union',
    # 並發處理
    'ThreadPoolExecutor', 'as_completed',
    # 集合
    'defaultdict',
    # 網路請求
    'requests', 'urllib',
    # 工具函數
    'save_to_csv', 'fetch_json', 'get_output_path', 'safe_get',
    # 日誌
    'logger',
    # 設定
    'OUTPUT_DIR', 'HEADERS', 'MAX_WORKERS_JOB'
]
