FROM python:3.12

# 安装 tini 和清理 APT 缓存
RUN apt-get update && \
    apt-get install -y tini && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装 Python 依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制所有文件到容器
COPY . .

# 使用 Tini 作为 ENTRYPOINT
ENTRYPOINT ["/usr/bin/tini", "--"]

# 运行 Scrapy 命令
CMD ["scrapy", "crawl", "book"]
