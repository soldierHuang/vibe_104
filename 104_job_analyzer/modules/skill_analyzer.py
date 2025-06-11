"""技能分析模組：負責分析職缺所需的技能資訊"""

from .common import (
    pd, datetime, logger, OUTPUT_DIR, save_to_csv
)
from .fetcher import (
    fetch_job_categories_json,
    fetch_single_skill_request
)
from .processor import (
    flatten_job_categories,
    process_all_skills
)

def run_skill_analysis() -> None:
    """執行技能分析
    
    流程:
    1. 獲取職務類別資料
    2. 扁平化處理類別
    3. 獲取技能資料
    4. 合併並輸出結果
    """
    logger.info("===== 開始執行技能資料分析 =====")
    
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
        
        # 3. 處理技能資料
        df_skills = process_all_skills(job_codes)
        if df_skills is not None and not df_skills.empty:
            # 將 job_code 設為 object 類型以利合併
            df_jobcat['job_code'] = df_jobcat['job_code'].astype(str)
            df_skills['jobCode'] = df_skills['jobCode'].astype(str)
            
            # 合併資料並儲存
            final_df = pd.merge(
                df_jobcat,
                df_skills,
                left_on='job_code',
                right_on='jobCode',
                how='inner'
            )
            save_to_csv(final_df, "104_skills")
            logger.info(f"已處理 {len(final_df)} 筆技能資料")
        else:
            logger.error("技能資料處理失敗")
            
    except Exception as e:
        logger.error(f"技能分析過程中發生錯誤: {str(e)}")
    
    logger.info("===== 技能資料分析執行完畢 =====")
