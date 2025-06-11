"""薪資分析模組：負責分析職缺的薪資資訊"""

from .common import (
    pd, datetime, logger, OUTPUT_DIR, save_to_csv
)
from .fetcher import (
    fetch_job_categories_json,
    fetch_single_salary_request
)
from .processor import (
    flatten_job_categories,
    process_all_salaries
)

def run_salary_analysis() -> None:
    """執行薪資分析
    
    流程:
    1. 獲取職務類別資料
    2. 扁平化處理類別
    3. 獲取薪資資料
    4. 輸出結果
    """
    logger.info("===== 開始執行薪資資料分析 =====")
    
    try:
        # 1. 獲取並處理職務類別
        categories_json = fetch_job_categories_json()
        if not categories_json:
            logger.error("無法獲取職務類別資料")
            return

        # 2. 扁平化類別資料
        flattened_cats = flatten_job_categories(categories_json)
        df_jobcat = pd.DataFrame(flattened_cats)
        df_jobcat = df_jobcat.sort_values(by='job_code').reset_index(drop=True)
        job_codes = df_jobcat['job_code'].tolist()

        # 3. 處理薪資資料
        df_salaries = process_all_salaries(job_codes)
        if df_salaries is not None and not df_salaries.empty:
            # 儲存資料
            save_to_csv(df_salaries, "104_salaries")
            logger.info(f"已處理 {len(df_salaries)} 筆薪資資料")
        else:
            logger.error("薪資資料處理失敗")
            
    except Exception as e:
        logger.error(f"薪資分析過程中發生錯誤: {str(e)}")
    
    logger.info("===== 薪資資料分析執行完畢 =====")
