# 建议使用轻量级的 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app


RUN find /etc/apt/ -name "*.list" -o -name "*.sources" | xargs sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' && \
    find /etc/apt/ -name "*.list" -o -name "*.sources" | xargs sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g'

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 3. 复制依赖文件
COPY requirements.txt .

# 4. 修改 pip 源为国内镜像（清华源），解决 pip install 缓慢问题
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]