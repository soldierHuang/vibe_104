# config.py

# URL Templates
URL_JOB_CAT = "https://static.104.com.tw/category-tool/json/JobCat.json"
URL_JOB_CARD_SKILL = "https://be.guide.104.com.tw/wow/jobCard/job?jobCode={job_code}"
URL_JOB_CERT_SKILL = "https://be.guide.104.com.tw/wow/jobCard/cert?jobCode={job_code}"
URL_SALARY = "https://be.guide.104.com.tw/api/job/seniority/{job_code}?type={type_id}"
URL_JOB_SEARCH_BASE = "https://www.104.com.tw/jobs/search"
URL_JOB_SEARCH = "https://www.104.com.tw/jobs/search/list?ro=0"
URL_JOB_DETAIL_BASE = "https://www.104.com.tw/job/ajax/content/"

# Salary Types
ALL_SALARY_TYPES = {
    1: '月薪',
    2: '年薪',
}

# Concurrency Settings
MAX_WORKERS_SKILL = 10
MAX_WORKERS_SALARY = 20
MAX_WORKERS_JOB = 10

# Output Settings
OUTPUT_DIR = "output"
LOG_DIR = "logs"  # 日誌檔案目錄
LOG_FILE = "analysis.log"  # 主要日誌檔案
SKILL_LOG = "skill_analysis.log"  # 技能分析日誌
SALARY_LOG = "salary_analysis.log"  # 薪資分析日誌

# HTTP Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Referer': 'https://www.104.com.tw/jobs/search',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}

# Default Parameters
DEFAULT_PARAMS = {
    'order': 15,  # 15: 符合度高, 16: 最近更新
    'page': 1,
    'mode': 's',  # s: 搜尋模式
    'JOBCAT_CODE': None,  # 職務類別代碼
    'KEYWORDS_STR': None,  # 搜尋關鍵字
}

def build_search_url(ORDER=None, KEYWORDS=None, CATEGORY=None):
    """建立搜尋 URL
    
    Args:
        ORDER: 排序方式
        KEYWORDS: 搜尋關鍵字
        CATEGORY: 職務類別
        
    Returns:
        str: 完整的搜尋 URL
    """
    params = ""
    if ORDER is not None:
        params += f"&order={ORDER}"
    if KEYWORDS:
        params += f"&keyword={KEYWORDS}"
    if CATEGORY:
        params += f"&jobcat={CATEGORY}"
    
    return f"{URL_JOB_SEARCH_BASE}{params}&page="