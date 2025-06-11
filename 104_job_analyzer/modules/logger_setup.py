# modules/logger_setup.py

import logging
import sys
from pathlib import Path
from typing import Optional
from config import LOG_DIR, LOG_FILE, SKILL_LOG, SALARY_LOG

class LoggerManager:
    """日誌管理器：負責建立和管理所有日誌實例"""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str = "104_analyzer", log_file: str = LOG_FILE) -> logging.Logger:
        """取得或建立一個日誌實例
        
        Args:
            name: 日誌實例名稱
            log_file: 日誌檔案名稱
            
        Returns:
            logging.Logger: 設定完成的日誌實例
        """
        if name not in cls._loggers:
            cls._loggers[name] = cls._setup_logger(name, log_file)
        return cls._loggers[name]
    
    @staticmethod
    def _setup_logger(name: str, log_file: str) -> logging.Logger:
        """設定一個日誌實例
        
        Args:
            name: 日誌實例名稱
            log_file: 日誌檔案名稱
            
        Returns:
            logging.Logger: 設定完成的日誌實例
        """
        # 確保日誌目錄存在
        log_path = Path(LOG_DIR)
        log_path.mkdir(parents=True, exist_ok=True)
        
        # 建立 logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # 清除既有的 handlers
        if logger.hasHandlers():
            logger.handlers.clear()
        
        # 設定日誌格式
        log_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # 終端輸出（INFO 以上）
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(log_format)
        logger.addHandler(stream_handler)
        
        # 檔案輸出（DEBUG 以上）
        file_handler = logging.FileHandler(
            log_path / log_file,
            mode='w',
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
        
        return logger

# 建立預設日誌實例
logger = LoggerManager.get_logger()

# 建立專用日誌實例
skill_logger = LoggerManager.get_logger("skill_analyzer", SKILL_LOG)
salary_logger = LoggerManager.get_logger("salary_analyzer", SALARY_LOG)

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """取得一個日誌實例
    
    Args:
        name: 日誌實例名稱，如果未提供則使用預設實例
        
    Returns:
        logging.Logger: 日誌實例
    """
    if name == "skill_analyzer":
        return skill_logger
    elif name == "salary_analyzer":
        return salary_logger
    return logger