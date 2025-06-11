# modules/processor.py

"""資料處理模組：負責處理和轉換原始資料"""

from collections import defaultdict
from .common import (
    pd, tqdm, logger,
    List, Dict, Optional, Any,
    ThreadPoolExecutor, as_completed
)
from .fetcher import (
    fetch_single_skill_request,
    fetch_single_salary_request
)
from config import (
    MAX_WORKERS_SKILL,
    MAX_WORKERS_SALARY,
    ALL_SALARY_TYPES
)

def flatten_job_categories(node_list: List[Dict], parent_name: str = None, parent_code: str = None) -> List[Dict]:
    """遞迴地將樹狀職務類別扁平化
    
    Args:
        node_list: 職務類別節點列表
        parent_name: 父類別名稱
        parent_code: 父類別代碼
        
    Returns:
        List[Dict]: 扁平化後的職務類別列表
    """
    items = []
    for node in node_list:
        if parent_code:  # 只加入有父層的節點
            items.append({
                'parent_code': parent_code,
                'parent_name': parent_name,
                'job_code': node.get('no'),
                'job_name': node.get('des')
            })
        if 'n' in node and node['n']:
            items.extend(flatten_job_categories(
                node['n'],
                node.get('des'),
                node.get('no')
            ))
    return items

def process_all_skills(job_codes: List[str]) -> pd.DataFrame:
    """並行處理 job_code 列表以獲取技能資料。"""
    logger.info(f"準備並行獲取 {len(job_codes)} 個職務的技能資料...")
    processed_data = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS_SKILL) as executor:
        # 建立未來對象到職務代碼的映射
        futures = {
            executor.submit(fetch_single_skill_request, jc): jc 
            for jc in job_codes
        }
        
        # 使用進度條追蹤完成情況
        for future in tqdm(as_completed(futures),
                         total=len(job_codes),
                         desc="獲取技能資料"):
            job_code, skill_json, cert_json = future.result()
            
            # 合併技能和證照資料
            if skill_json and cert_json:
                skill_json.update({
                    'hardToolList': cert_json.get('hardToolList', []),
                    'hardSkillList': cert_json.get('hardSkillList', []),
                    'hardCertList': cert_json.get('hardCertList', [])
                })
                processed_data.append(skill_json)

    if not processed_data:
        logger.warning("未能獲取任何技能資料")
        return pd.DataFrame()

    return pd.DataFrame(processed_data)

def process_all_salaries(job_codes: List[str]) -> Optional[pd.DataFrame]:
    """並行處理多個職務的薪資資料。"""
    logger.info(f"準備並行獲取 {len(job_codes)} 個職務的薪資資料...")
    salary_data = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS_SALARY) as executor:
        futures = []
        # 為每個職務和薪資類型建立請求
        for job_code in job_codes:
            for type_id in ALL_SALARY_TYPES:
                futures.append(
                    executor.submit(fetch_single_salary_request,
                                 job_code,
                                 type_id)
                )

        # 使用進度條追蹤完成情況
        for future in tqdm(as_completed(futures),
                         total=len(futures),
                         desc="獲取薪資資料"):
            job_code, type_id, salary_list = future.result()
            if salary_list:
                for salary in salary_list:
                    salary['job_code'] = job_code
                    salary['salary_type'] = ALL_SALARY_TYPES[type_id]
                    salary_data.append(salary)

    if not salary_data:
        logger.warning("未能獲取任何薪資資料")
        return None

    df = pd.DataFrame(salary_data)
    return df