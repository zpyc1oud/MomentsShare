# 建议使用轻量级的 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

<<<<<<< HEAD
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources \
    && sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources
=======
# === 修改点：删除了所有的换源命令，使用官方默认源 ===
# 这样做是为了绕过校园网坏掉的缓存代理服务器

# 安装系统依赖
# 注意：这里直接运行 apt-get，不替换源
>>>>>>> 77cae477b045eb6f9a96f29ef1d025a8a50f3aca
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# === pip 源可以保留阿里云，通常 pip 的代理和 apt 是分开的 ===
# 如果 pip 之后也报错，也可以把这里改回默认
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 复制项目代码
COPY . .

RUN mkdir -p /app/locale

# 复制默认头像到临时位置（volume 挂载后会覆盖 /app/media）
RUN mkdir -p /app/defaults && cp /app/media/default_avatar.png /app/defaults/

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]