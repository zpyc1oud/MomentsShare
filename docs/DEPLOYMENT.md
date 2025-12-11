# MomentsShare 部署指南

本文档详细描述了 MomentsShare 项目的部署配置和运维指南。

---

## 目录

1. [环境要求](#1-环境要求)
2. [开发环境部署](#2-开发环境部署)
3. [生产环境部署](#3-生产环境部署)
4. [Docker 部署](#4-docker-部署)
5. [Celery 配置](#5-celery-配置)
6. [Nginx 配置](#6-nginx-配置)
7. [环境变量配置](#7-环境变量配置)
8. [数据库配置](#8-数据库配置)
9. [安全配置](#9-安全配置)
10. [监控与日志](#10-监控与日志)

---

## 1. 环境要求

### 软件版本

| 软件 | 版本要求 | 说明 |
|------|----------|------|
| Python | 3.10+ | 推荐 3.11 |
| PostgreSQL | 13+ | 生产环境数据库 |
| Redis | 6+ | Celery Broker |
| Nginx | 1.18+ | 反向代理 |

### 硬件建议

**开发环境**:
- CPU: 2 核
- 内存: 4 GB
- 存储: 20 GB

**生产环境**:
- CPU: 4 核+
- 内存: 8 GB+
- 存储: 100 GB+ (SSD)

---

## 2. 开发环境部署

### 2.1 克隆项目

```bash
git clone <repository_url>
cd MomentsShare
```

### 2.2 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 2.3 安装依赖

```bash
pip install -r requirements.txt
```

### 2.4 配置环境变量

创建 `.env` 文件：

```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Google AI (可选)
GOOGLE_API_KEY=your-google-api-key

# Sensitive words
SENSITIVE_WORDS=违禁,敏感,非法
```

### 2.5 数据库迁移

```bash
python manage.py migrate
```

### 2.6 创建超级用户

```bash
python manage.py createsuperuser
```

按提示输入手机号、用户名、昵称和密码。

### 2.7 启动开发服务器

```bash
python manage.py runserver
```

服务将在 http://127.0.0.1:8000 启动。

### 2.8 启动 Celery Worker

新开一个终端：

```bash
# Windows
celery -A moments_share worker -l info -P solo

# Linux/macOS
celery -A moments_share worker -l info
```

---

## 3. 生产环境部署

### 3.1 系统准备

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
sudo apt install postgresql postgresql-contrib
sudo apt install redis-server
sudo apt install nginx
```

### 3.2 创建系统用户

```bash
sudo useradd -m -s /bin/bash moments
sudo su - moments
```

### 3.3 项目部署

```bash
cd /home/moments
git clone <repository_url> MomentsShare
cd MomentsShare

python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 3.4 配置生产环境变量

创建 `/home/moments/MomentsShare/.env`：

```env
DJANGO_SECRET_KEY=your-production-secret-key-64-chars-long
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=moments_share
DB_USER=moments_user
DB_PASSWORD=your-secure-db-password
DB_HOST=localhost
DB_PORT=5432

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Google AI
GOOGLE_API_KEY=your-google-api-key
GOOGLE_AI_MODEL=gemini-1.5-flash

# Sensitive words
SENSITIVE_WORDS=违禁,敏感,非法
```

### 3.5 数据库设置

```bash
# 创建 PostgreSQL 数据库和用户
sudo -u postgres psql

CREATE DATABASE moments_share;
CREATE USER moments_user WITH PASSWORD 'your-secure-db-password';
ALTER ROLE moments_user SET client_encoding TO 'utf8';
ALTER ROLE moments_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE moments_user SET timezone TO 'Asia/Shanghai';
GRANT ALL PRIVILEGES ON DATABASE moments_share TO moments_user;
\q
```

### 3.6 收集静态文件和迁移

```bash
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

### 3.7 Gunicorn 服务

创建 `/etc/systemd/system/moments.service`：

```ini
[Unit]
Description=MomentsShare Gunicorn Daemon
After=network.target

[Service]
User=moments
Group=moments
WorkingDirectory=/home/moments/MomentsShare
Environment="PATH=/home/moments/MomentsShare/venv/bin"
EnvironmentFile=/home/moments/MomentsShare/.env
ExecStart=/home/moments/MomentsShare/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/home/moments/MomentsShare/moments.sock \
    --access-logfile /var/log/moments/access.log \
    --error-logfile /var/log/moments/error.log \
    moments_share.wsgi:application

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo mkdir -p /var/log/moments
sudo chown moments:moments /var/log/moments
sudo systemctl daemon-reload
sudo systemctl start moments
sudo systemctl enable moments
```

---

## 4. Docker 部署

### 4.1 Dockerfile

创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn psycopg2-binary

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "moments_share.wsgi:application"]
```

### 4.2 docker-compose.yml

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
      - DJANGO_DEBUG=False
      - DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS}
      - DB_ENGINE=django.db.backends.postgresql
      - DB_NAME=moments_share
      - DB_USER=moments_user
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=db
      - DB_PORT=5432
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - media_data:/app/media
      - static_data:/app/staticfiles

  celery:
    build: .
    command: celery -A moments_share worker -l info
    environment:
      - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
      - DB_ENGINE=django.db.backends.postgresql
      - DB_NAME=moments_share
      - DB_USER=moments_user
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=db
      - DB_PORT=5432
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=moments_share
      - POSTGRES_USER=moments_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - media_data:/app/media:ro
      - static_data:/app/staticfiles:ro
    depends_on:
      - web

volumes:
  postgres_data:
  redis_data:
  media_data:
  static_data:
```

### 4.3 启动容器

```bash
# 创建 .env 文件配置环境变量
docker-compose up -d

# 执行数据库迁移
docker-compose exec web python manage.py migrate

# 创建超级用户
docker-compose exec web python manage.py createsuperuser
```

---

## 5. Celery 配置

### 5.1 Celery 配置文件

项目已有 `moments_share/celery.py`：

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moments_share.settings')

app = Celery('moments_share')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### 5.2 Celery Worker 服务

创建 `/etc/systemd/system/moments-celery.service`：

```ini
[Unit]
Description=MomentsShare Celery Worker
After=network.target

[Service]
User=moments
Group=moments
WorkingDirectory=/home/moments/MomentsShare
Environment="PATH=/home/moments/MomentsShare/venv/bin"
EnvironmentFile=/home/moments/MomentsShare/.env
ExecStart=/home/moments/MomentsShare/venv/bin/celery \
    -A moments_share worker \
    -l info \
    --logfile=/var/log/moments/celery.log

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start moments-celery
sudo systemctl enable moments-celery
```

### 5.3 Celery 任务说明

| 任务 | 模块 | 说明 |
|------|------|------|
| `transcode_video` | `moments.tasks` | 视频转码处理 |

---

## 6. Nginx 配置

创建 `/etc/nginx/sites-available/moments`：

```nginx
upstream moments_app {
    server unix:/home/moments/MomentsShare/moments.sock fail_timeout=0;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL 证书
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # SSL 配置
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;

    # 请求限制
    client_max_body_size 100M;

    # 访问日志
    access_log /var/log/nginx/moments_access.log;
    error_log /var/log/nginx/moments_error.log;

    # 静态文件
    location /static/ {
        alias /home/moments/MomentsShare/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 媒体文件
    location /media/ {
        alias /home/moments/MomentsShare/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    # API 请求
    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_pass http://moments_app;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/moments /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 7. 环境变量配置

### 完整环境变量列表

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `DJANGO_SECRET_KEY` | 是 | - | Django 密钥（生产环境必须设置） |
| `DJANGO_DEBUG` | 否 | True | 调试模式（生产环境设为 False） |
| `DJANGO_ALLOWED_HOSTS` | 是 | * | 允许的主机名（逗号分隔） |
| `DB_ENGINE` | 否 | sqlite3 | 数据库引擎 |
| `DB_NAME` | 是 | db.sqlite3 | 数据库名 |
| `DB_USER` | 条件 | - | 数据库用户（PostgreSQL 必填） |
| `DB_PASSWORD` | 条件 | - | 数据库密码 |
| `DB_HOST` | 条件 | - | 数据库主机 |
| `DB_PORT` | 条件 | - | 数据库端口 |
| `CELERY_BROKER_URL` | 否 | redis://localhost:6379/0 | Celery Broker |
| `CELERY_RESULT_BACKEND` | 否 | 同 Broker | Celery 结果后端 |
| `GOOGLE_API_KEY` | 否 | - | Google AI API Key |
| `GOOGLE_AI_MODEL` | 否 | gemini-1.5-flash | AI 模型名称 |
| `SENSITIVE_WORDS` | 否 | 违禁,敏感,非法 | 敏感词（逗号分隔） |

### 生成 Secret Key

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

或使用命令行：

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 8. 数据库配置

### 8.1 SQLite (开发环境)

默认配置，无需额外设置。

### 8.2 PostgreSQL (生产环境)

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=moments_share
DB_USER=moments_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432
```

### 8.3 数据库备份

```bash
# PostgreSQL 备份
pg_dump -U moments_user -d moments_share > backup_$(date +%Y%m%d).sql

# 恢复
psql -U moments_user -d moments_share < backup_20240101.sql
```

### 8.4 媒体文件备份

```bash
# 备份媒体文件
tar -czvf media_backup_$(date +%Y%m%d).tar.gz /home/moments/MomentsShare/media/
```

---

## 9. 安全配置

### 9.1 生产环境检查清单

- [ ] `DEBUG = False`
- [ ] 设置强密码的 `SECRET_KEY`
- [ ] 配置正确的 `ALLOWED_HOSTS`
- [ ] 使用 HTTPS
- [ ] 数据库使用强密码
- [ ] Redis 设置密码（如需）
- [ ] 限制管理后台访问 IP

### 9.2 Django 安全设置

在 `settings.py` 中添加（生产环境）：

```python
# HTTPS 设置
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookie 安全
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 其他安全头
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 9.3 防火墙配置

```bash
# UFW 示例
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

---

## 10. 监控与日志

### 10.1 日志位置

| 服务 | 日志路径 |
|------|----------|
| Gunicorn 访问日志 | `/var/log/moments/access.log` |
| Gunicorn 错误日志 | `/var/log/moments/error.log` |
| Celery 日志 | `/var/log/moments/celery.log` |
| Nginx 访问日志 | `/var/log/nginx/moments_access.log` |
| Nginx 错误日志 | `/var/log/nginx/moments_error.log` |

### 10.2 日志轮转

创建 `/etc/logrotate.d/moments`：

```
/var/log/moments/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 moments moments
    sharedscripts
    postrotate
        systemctl reload moments >/dev/null 2>&1 || true
        systemctl reload moments-celery >/dev/null 2>&1 || true
    endscript
}
```

### 10.3 服务状态监控

```bash
# 检查服务状态
sudo systemctl status moments
sudo systemctl status moments-celery
sudo systemctl status nginx
sudo systemctl status redis
sudo systemctl status postgresql

# 查看日志
sudo journalctl -u moments -f
sudo journalctl -u moments-celery -f
```

### 10.4 健康检查端点

可以添加健康检查视图：

```python
# core/views.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        "status": "ok",
        "database": "connected",
    })
```

---

## 📋 运维命令速查

```bash
# 服务管理
sudo systemctl start moments
sudo systemctl stop moments
sudo systemctl restart moments
sudo systemctl status moments

# Celery 管理
sudo systemctl start moments-celery
sudo systemctl stop moments-celery
sudo systemctl restart moments-celery

# Nginx 管理
sudo systemctl reload nginx
sudo nginx -t  # 测试配置

# 数据库迁移
source venv/bin/activate
python manage.py migrate

# 收集静态文件
python manage.py collectstatic --noinput

# 创建超级用户
python manage.py createsuperuser

# 进入 Django Shell
python manage.py shell

# 查看迁移状态
python manage.py showmigrations
```

---

## 🔧 常见问题

### Q1: 502 Bad Gateway

检查 Gunicorn 服务是否运行：
```bash
sudo systemctl status moments
```

检查 socket 文件权限。

### Q2: 静态文件 404

确保执行了 `collectstatic`：
```bash
python manage.py collectstatic --noinput
```

检查 Nginx 配置中的路径。

### Q3: Celery 任务不执行

检查 Celery Worker 状态：
```bash
sudo systemctl status moments-celery
```

检查 Redis 连接：
```bash
redis-cli ping
```

### Q4: 数据库连接失败

检查 PostgreSQL 服务：
```bash
sudo systemctl status postgresql
```

验证数据库凭证：
```bash
psql -U moments_user -d moments_share -h localhost
```

