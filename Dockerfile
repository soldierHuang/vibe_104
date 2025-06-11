# 使用官方 Python 映像作為基礎
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 安裝 UV 工具
RUN pip install uv

# 複製專案檔案
COPY . .

# 建立虛擬環境並安裝相依套件
RUN uv init \
    && . .venv/bin/activate \
    && pip install -r requirements.txt

# 建立輸出目錄
RUN mkdir -p output

# 設定環境變數
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 執行命令
ENTRYPOINT ["python", "main.py"]
CMD ["all"]
