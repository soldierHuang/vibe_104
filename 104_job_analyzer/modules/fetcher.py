# modules/fetcher.py

"""資料擷取模組：負責從 104 人力銀行擷取資料"""

from typing import Optional, Dict, List, Any, Tuple, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime
from .common import (
    pd, requests, json, tqdm, logger,
    save_to_csv, fetch_json
)
from config import (
    URL_JOB_CAT,
    URL_JOB_CARD_SKILL,
    URL_JOB_CERT_SKILL,
    URL_SALARY,
    URL_JOB_SEARCH,
    URL_JOB_DETAIL_BASE,
    HEADERS,
    DEFAULT_PARAMS,
    MAX_WORKERS_JOB,
    OUTPUT_DIR
)

def fetch_job_categories_json() -> Optional[List[Dict[str, Any]]]:
    """獲取所有職務類別的原始 JSON 資料。"""
    logger.info(f"正在從 {URL_JOB_CAT} 獲取職務類別...")
    try:
        headers = HEADERS.copy()
        headers['Accept'] = 'application/json'
        response = requests.get(URL_JOB_CAT, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"獲取職務類別失敗: {e}")
        return None

def fetch_single_skill_request(job_code: str) -> Tuple[str, Optional[Dict], Optional[Dict]]:
    """為單一 job_code 獲取技能和證照的原始 JSON。"""
    try:
        url_skill = URL_JOB_CARD_SKILL.format(job_code=job_code)
        res_skill = requests.get(url_skill, timeout=10)
        res_skill.raise_for_status()
        
        url_cert = URL_JOB_CERT_SKILL.format(job_code=job_code)
        res_cert = requests.get(url_cert, timeout=10)
        res_cert.raise_for_status()
        
        return job_code, res_skill.json(), res_cert.json()
    except requests.RequestException as e:
        logger.warning(f"獲取技能失敗 for job_code={job_code}. Error: {e}")
        return job_code, None, None

def fetch_single_salary_request(job_code: str, type_id: int) -> Tuple[str, int, Optional[List]]:
    """執行單一的薪資請求操作。"""
    url = URL_SALARY.format(job_code=job_code, type_id=type_id)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return job_code, type_id, data.get('salaryList')
    except requests.RequestException as e:
        logger.warning(f"獲取薪資失敗 for job_code={job_code}, type={type_id}. Error: {e}")
        return job_code, type_id, None

def run_job_analysis(category: Optional[str] = None, keywords: Optional[str] = None) -> None:
    """執行職缺分析"""
    try:
        fetcher = JobURLFetcher()
        urls = fetcher.fetch_urls(category, keywords)
        if urls:
            logger.info(f"成功獲取 {len(urls)} 個職缺URL")
        else:
            logger.error("無法獲取職缺列表")
    except Exception as e:
        logger.error(f"職缺分析過程中發生錯誤: {str(e)}")

class JobURLFetcher:
    """職缺URL擷取器：負責從104人力銀行獲取職缺URL列表"""
    
    def __init__(self):
        """初始化職缺URL擷取器"""
        self.headers = HEADERS.copy()
        self.headers.update({
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest'
        })
        self.output_dir = Path(OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_url(self, category: Optional[str] = None,
                keywords: Optional[str] = None,
                order: int = DEFAULT_PARAMS['order']) -> str:
        """建構搜尋URL"""
        params = "ro=0"  # 必要參數
        if order:
            params += f"&order={order}"
        if keywords:
            params += f"&keyword={keywords}"
        if category:
            params += f"&jobcat={category}"
        return f"{URL_JOB_SEARCH}&{params}&page="

    def get_total_pages(self, url: str) -> int:
        """獲取搜尋結果的總頁數"""
        try:
            response = requests.get(url + "1", headers=self.headers, timeout=20)
            response.raise_for_status()
            json_data = response.json()
            if 'data' in json_data and 'totalPage' in json_data['data']:
                return json_data['data']['totalPage']
            else:
                logger.error("回應中未包含總頁數資訊")
                return 0
        except requests.RequestException as e:
            logger.error(f"獲取總頁數時發生請求錯誤: {str(e)}")
            return 0
        except ValueError as e:
            logger.error(f"解析總頁數時發生錯誤: {str(e)}")
            return 0

    def fetch_page_urls(self, url: str, page: int) -> Set[str]:
        """獲取單一頁面的職缺URL"""
        try:
            response = requests.get(url + str(page), headers=self.headers, timeout=20)
            response.raise_for_status()
            json_data = response.json()
            
            if 'data' in json_data and 'list' in json_data['data']:
                # 儲存原始資料
                jobs_data = json_data['data']['list']
                today = datetime.now().strftime("%Y%m%d")
                df = pd.DataFrame(jobs_data)
                output_file = self.output_dir / f"jobs_page_{page}_{today}.csv"
                df.to_csv(output_file, index=False, encoding='utf-8-sig')
                logger.info(f"已儲存資料至 {output_file}")
                
                return {f"{URL_JOB_DETAIL_BASE}{job['link']['job']}"
                       for job in jobs_data}
            else:
                logger.error(f"第 {page} 頁回應格式不正確")
                return set()
                
        except Exception as e:
            logger.error(f"獲取第 {page} 頁職缺URL時發生錯誤: {str(e)}")
            return set()

    def fetch_urls(self, category: Optional[str] = None,
                keywords: Optional[str] = None,
                order: int = DEFAULT_PARAMS['order']) -> Set[str]:
        """獲取所有符合條件的職缺URL"""
        url = self.build_url(category, keywords, order)
        total_pages = self.get_total_pages(url)
        
        if total_pages == 0:
            return set()
            
        job_url_set = set()
        for page in tqdm(range(1, total_pages + 1),
                       desc="獲取職缺URL"):
            urls = self.fetch_page_urls(url, page)
            job_url_set.update(urls)
        
        # 儲存所有URL
        today = datetime.now().strftime("%Y%m%d")
        df = pd.DataFrame({"url": list(job_url_set)})
        output_file = self.output_dir / f"all_job_urls_{today}.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        logger.info(f"已儲存所有職缺URL至 {output_file}")
        
        return job_url_set

class JobDetailFetcher:
    """職缺詳細資訊擷取器"""
    
    def __init__(self):
        """初始化職缺詳細資訊擷取器"""
        self.headers = HEADERS.copy()
        
    def fetch_detail(self, job_url: str) -> Optional[Dict]:
        """獲取職缺詳細資訊"""
        try:
            response = requests.get(job_url, headers=self.headers, timeout=20)
            return response.json()['data']
        except Exception as e:
            logger.error(f"獲取職缺詳細資訊時發生錯誤: {str(e)}")
            return None