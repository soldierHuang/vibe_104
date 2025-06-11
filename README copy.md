# 104人力銀行資料分析專案

## 專案說明
此專案提供 104人力銀行職缺資料的自動化分析工具，協助使用者掌握就業市場趨勢。

## 主要功能
- 職缺技能需求分析
- 薪資水準統計
- 資料視覺化呈現

## 快速開始
```bash
# 1. 複製專案
git clone <repository_url>

# 2. 進入專案目錄
cd 104_job_analyzer

# 3. 初始化環境
uv init

# 4. 啟動虛擬環境
.venv/Scripts/Activate.ps1

# 5. 安裝相依套件
pip install -r requirements.txt

# 6. 執行分析
python main.py all
```

### Docker 執行方式
```bash
# 使用 Docker 執行
docker build -t 104-analyzer .
docker run -v ${PWD}/output:/app/output 104-analyzer

# 使用 Docker Compose 執行
docker-compose up
```

## 文件導覽
- [使用者手冊](prompt/user_manual.md) - 詳細的使用說明
- [技術規格](prompt/technical_spec.md) - API 和技術細節
- [開發指南](prompt/dev_guide.md) - 開發規範和最佳實踐
- [程式流程](prompt/diagrams/code_flow.mmd) - 視覺化流程圖

## 系統需求
- Python 3.10+
- UV 套件管理工具
- Windows PowerShell/CMD
- 穩定的網路連線

## 授權資訊
MIT License

## 注意事項
- 請遵守 104人力銀行的使用條款
- 建議控制請求頻率避免 IP 被封鎖
- 定期更新相依套件確保安全性
