# main.py

"""104人力銀行資料分析工具主程式

此程式為系統的進入點，負責：
1. 解析命令列參數
2. 協調各個分析模組的執行
3. 處理執行結果
4. 錯誤處理
"""

import argparse
from modules.common import (
    datetime, logger,
    Path, Optional, Dict, List
)
from modules.skill_analyzer import run_skill_analysis
from modules.salary_analyzer import run_salary_analysis
from modules.fetcher import run_job_analysis
from config import OUTPUT_DIR, DEFAULT_PARAMS

def parse_args():
    """解析命令列參數
    
    Returns:
        argparse.Namespace: 解析後的參數物件
    """
    parser = argparse.ArgumentParser(
        description='104人力銀行資料分析工具',
        epilog='範例: python main.py --mode all --category "2007001000" --keywords "Python"'
    )
    
    parser.add_argument(
        '--mode', 
        choices=['all', 'job', 'skill', 'salary'],
        default='all',
        help='分析模式：all=全部, job=職缺, skill=技能, salary=薪資'
    )
    
    parser.add_argument(
        '--category',
        help='職務類別代碼，例如：2007001000 表示資料工程師'
    )
    
    parser.add_argument(
        '--keywords',
        help='搜尋關鍵字，例如：Python, AWS, 資料分析'
    )
    
    return parser.parse_args()

def main() -> int:
    """主程式
    
    執行流程：
    1. 解析命令列參數
    2. 根據模式執行相應的分析
    3. 處理可能的錯誤
    
    Returns:
        int: 執行狀態碼，0 表示成功，非 0 表示失敗
    """
    args = parse_args()
    logger.info("===== 開始執行資料分析 =====")
    
    try:
        # 職缺分析
        if args.mode in ['all', 'job']:
            logger.info("===== 開始執行職缺分析 =====")
            run_job_analysis(args.category, args.keywords)
            logger.info("===== 職缺分析執行完畢 =====")
        
        # 技能分析    
        if args.mode in ['all', 'skill']:
            logger.info("===== 開始執行技能分析 =====")
            run_skill_analysis()
            logger.info("===== 技能分析執行完畢 =====")
        
        # 薪資分析    
        if args.mode in ['all', 'salary']:
            logger.info("===== 開始執行薪資分析 =====")
            run_salary_analysis()
            logger.info("===== 薪資分析執行完畢 =====")
            
    except Exception as e:
        logger.error(f"執行過程中發生錯誤: {str(e)}")
        return 1
    
    logger.info("===== 資料分析執行完畢 =====")
    return 0

if __name__ == '__main__':
    exit(main())