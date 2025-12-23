# 建议使用轻量级的 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# === 解决冲突：保留了阿里云镜像源 ===
# 你的队友试图改回官方源，但在你的校园网环境下，官方源会导致构建失败 (timeout)。
# 所以这里保留 sed 命令，强制使用阿里云镜像。
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

# === pip 源保留阿里云 ===
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 复制项目代码
COPY . .

RUN mkdir -p /app/locale

# 复制默认头像到临时位置（volume 挂载后会覆盖 /app/media）
# 注意：确保你本地 backend/media/ 目录下确实有 default_avatar.png，否则这一步会报错
# 如果没有图片，可以暂时注释掉下面这一行
RUN mkdir -p /app/defaults && cp /app/media/default_avatar.png /app/defaults/

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]