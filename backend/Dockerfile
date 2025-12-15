# 建议使用轻量级的 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖 (编译某些 Python 包可能需要 gcc, ffmpeg用于视频处理)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令 (开发环境下使用 runserver，生产环境后面再换 gunicorn)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]