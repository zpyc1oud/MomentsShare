# 建议使用轻量级的 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# === 关键修正：保留阿里云镜像源（适配校园网环境） ===
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources \
    && sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# === 关键修正：pip 也使用阿里云源 ===
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 复制项目代码
COPY . .

RUN mkdir -p /app/locale

# 复制默认头像（如果本地没有这个文件，构建报错的话可以先把这行注释掉）
RUN mkdir -p /app/defaults && cp /app/media/default_avatar.png /app/defaults/

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]