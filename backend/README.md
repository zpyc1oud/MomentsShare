# MomentsShare 后端服务

基于 Django REST Framework 构建的社交分享平台后端 API 服务，支持用户动态发布、好友关系、评论互动及 AI 辅助功能。

## 🚀 快速开始（Docker）

### 启动服务

```bash
# 使用 Docker Compose 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f web
```

### 初始化数据

首次启动后需要**生成测试数据**：

```bash
# 数据库迁移（如需要）
docker-compose exec web python manage.py migrate

# 生成测试数据（首次使用前必须执行）
docker-compose exec web python manage.py seed_data --skip-media

# 创建超级用户（可选）
docker-compose exec web python manage.py createsuperuser
```

### 测试数据命令

```bash
# 生成测试数据（如果已存在则跳过）
docker-compose exec web python manage.py seed_data

# 强制重新生成（清除旧数据）
docker-compose exec web python manage.py seed_data --force

# 跳过下载媒体文件（加速测试）
docker-compose exec web python manage.py seed_data --skip-media

# 强制重新生成且跳过媒体
docker-compose exec web python manage.py seed_data --force --skip-media
```

### 停止服务

```bash
# 停止服务
docker-compose down

# 停止服务并删除数据卷
docker-compose down -v
```

## 🧪 测试账号

系统预置了 8 个测试账号，密码统一为 `Test123456`：

| 手机号 | 用户名 | 昵称 | 密码 | 说明 |
|--------|--------|------|------|------|
| **13800000001** | **alice** | **爱丽丝** | **Test123456** | ⭐ 推荐使用，有3个好友 |
| 13800000002 | bob | 鲍勃 | Test123456 | 有3个好友 |
| 13800000003 | charlie | 查理 | Test123456 | 有4个好友 |
| 13800000004 | diana | 戴安娜 | Test123456 | 有3个好友 |
| 13800000005 | evan | 伊万 | Test123456 | 有3个好友 |
| 13800000006 | fiona | 菲奥娜 | Test123456 | 有3个好友 |
| 13800000007 | george | 乔治 | Test123456 | 有3个好友 |
| 13800000008 | helen | 海伦 | Test123456 | 有2个好友 |

### 测试数据说明

- **用户**: 8 个测试用户，每个用户有头像
- **好友关系**: 12 对已接受的好友关系 + 2 个待处理的好友请求
- **动态**: 每个用户 2-4 条动态（图片/视频），共约 20-30 条
- **互动**: 每条动态有随机的点赞、评论、评分
- **标签**: 多种标签（日常、美食、旅行、心情等）

### 推荐测试流程

1. 使用 `alice (13800000001)` 登录
2. 查看好友动态流（Feed）
3. 发布新动态（图片/视频）
4. 点赞、评论好友动态
5. 搜索动态（支持拼音搜索）
6. 查看待处理的好友请求（helen 发给 alice 的请求）
7. 添加新好友

## 📱 核心功能

| 模块 | 功能 | 说明 |
|------|------|------|
| **用户** | 注册/登录 | 手机号 + JWT Token 认证 |
| **动态** | 图文/视频发布 | 最多 9 张图片，异步视频转码 |
| **好友** | 好友关系管理 | 申请、接受、拒绝、删除 |
| **评论** | 互动评论 | 支持嵌套回复 |
| **AI** | 智能辅助 | 文案润色、标签推荐 (Gemini) |
| **管理** | 后台管理 | 内容审核、数据统计 |

## 📂 项目结构

```
backend/
├── moments_share/          # 项目配置
│   ├── settings.py         # Django 配置
│   ├── urls.py             # 根 URL 路由
│   ├── celery.py           # Celery 配置
│   ├── wsgi.py             # WSGI 入口
│   └── asgi.py             # ASGI 入口
│
├── core/                   # 核心公共模块
│   ├── exceptions.py       # 自定义异常处理
│   └── sensitive_words.py  # 敏感词过滤
│
├── users/                  # 用户模块
├── moments/                # 动态模块
├── friends/                # 好友模块
├── interactions/           # 评论互动模块
├── ai_service/             # AI 服务模块 (Google Gemini)
├── admin_panel/            # 管理后台模块
├── tests/                  # 测试模块
│
├── media/                  # 媒体文件存储
├── requirements.txt        # Python 依赖
├── Dockerfile              # Docker 镜像构建
├── docker-compose.yml      # Docker 编排配置
├── conftest.py             # pytest 配置
└── pytest.ini              # pytest 配置文件
```

## 🛠️ 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.10+ | 运行环境 |
| Django | ≥4.2, <5.0 | Web 框架 |
| Django REST Framework | ≥3.14.0 | RESTful API |
| SimpleJWT | ≥5.3.0 | JWT 认证 |
| Celery | ≥5.3.0 | 异步任务队列 |
| Redis | ≥4.5.0 | Celery Broker |
| Pillow | ≥10.0.0 | 图片处理 |
| google-generativeai | ≥0.8.0 | AI 服务 (Gemini) |
| PostgreSQL / SQLite | - | 数据库 |
| drf-spectacular | ≥0.27.0 | API 文档 |

## ⚙️ 环境配置

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `DJANGO_SECRET_KEY` | `dev-secret-key` | Django 密钥 |
| `DJANGO_DEBUG` | `True` | 调试模式 |
| `DJANGO_ALLOWED_HOSTS` | `*` | 允许的主机 |
| `DB_ENGINE` | `sqlite3` | 数据库引擎 |
| `DB_NAME` | `db.sqlite3` | 数据库名 |
| `DB_USER` | - | 数据库用户 |
| `DB_PASSWORD` | - | 数据库密码 |
| `DB_HOST` | - | 数据库主机 |
| `DB_PORT` | - | 数据库端口 |
| `CELERY_BROKER_URL` | `redis://localhost:6379/0` | Celery Broker |
| `GOOGLE_API_KEY` | - | Google AI API Key |
| `GOOGLE_AI_MODEL` | `gemini-1.5-flash` | AI 模型 |
| `SENSITIVE_WORDS` | `违禁,敏感,非法` | 敏感词列表 |

## 🔐 认证机制

- **认证方式**: JWT Token (Bearer)
- **Access Token**: 有效期 60 分钟
- **Refresh Token**: 有效期 7 天
- **认证头格式**: `Authorization: Bearer <access_token>`

支持两种登录方式：
1. **手机号认证** (`PhoneAuthBackend`): 手机号 + 密码
2. **Django 默认认证**: 备用认证

## 🧪 测试

```bash
# 运行所有测试
docker-compose exec web pytest

# 查看测试覆盖率
docker-compose exec web pytest --cov

# 运行特定模块测试
docker-compose exec web pytest tests/test_users.py

# 详细输出
docker-compose exec web pytest -v
```

## 📚 API 文档

启动服务后可访问交互式 API 文档：

| 文档类型 | URL | 说明 |
|----------|-----|------|
| Swagger UI | http://localhost:8000/api/docs/ | 可交互测试界面 |
| ReDoc | http://localhost:8000/api/redoc/ | 美观只读文档 |
| OpenAPI Schema | http://localhost:8000/api/schema/ | OpenAPI 3.0 规范 |

### API 路由汇总

| 方法 | 路径 | 说明 |
|------|------|------|
| **认证** |||
| POST | `/api/v1/auth/register/` | 用户注册 |
| POST | `/api/v1/auth/login/` | 用户登录 |
| POST | `/api/v1/auth/logout/` | 用户登出 |
| **用户** |||
| GET/PUT | `/api/v1/users/me/` | 当前用户信息 |
| POST | `/api/v1/users/me/phone/` | 更换手机号 |
| GET | `/api/v1/users/{id}/` | 获取用户资料 |
| **动态** |||
| POST | `/api/v1/moments/` | 发布动态 |
| GET | `/api/v1/moments/{id}/` | 动态详情 |
| GET | `/api/v1/moments/feed/` | 好友动态流 |
| GET | `/api/v1/moments/search/` | 搜索动态 |
| **好友** |||
| POST | `/api/v1/friends/request/` | 好友申请 |
| POST | `/api/v1/friends/respond/` | 响应申请 |
| DELETE | `/api/v1/friends/{user_id}/` | 删除好友 |
| **评论** |||
| GET/POST | `/api/v1/moments/{id}/comments/` | 评论操作 |
| **私信** |||
| POST | `/api/v1/interactions/messages/` | 发送私信 |
| GET | `/api/v1/interactions/messages/conversations/` | 会话列表 |
| GET | `/api/v1/interactions/messages/{user_id}/` | 消息记录 |
| GET | `/api/v1/interactions/messages/unread/` | 未读消息数 |
| **AI** |||
| POST | `/api/v1/ai/polish/` | 文案润色 |
| POST | `/api/v1/ai/recommend-tags/` | 标签推荐 |
| **管理** |||
| POST | `/api/v1/admin/auth/login/` | 管理员登录 |
| GET | `/api/v1/admin/contents/` | 内容列表 |
| DELETE | `/api/v1/admin/contents/{pk}/` | 下架内容 |
| GET | `/api/v1/admin/stats/` | 统计数据 |

## 🐳 Docker 服务架构

```yaml
services:
  db:       # PostgreSQL 数据库 (端口 5432)
  redis:    # Redis 缓存/消息队列 (端口 6379)
  web:      # Django 后端服务 (端口 8000)
  worker:   # Celery 异步任务处理
```

## 📋 详细文档

- [API 接口文档](docs/API.md) - 完整的 RESTful API 接口说明
- [数据模型文档](docs/MODELS.md) - 数据库模型设计与 ER 图
- [部署指南](docs/DEPLOYMENT.md) - 开发/生产环境部署配置

## 👥 开发分工

| 成员 | 任务 |
|------|------|
| Member A | 用户认证、管理后台 |
| Member B | 动态模块、AI 服务 |

## 📝 开发规范

- **代码风格**: 遵循 PEP 8 规范
- **语言**: 中文注释和错误消息
- **时区**: `Asia/Shanghai`
- **语言代码**: `zh-hans`

---

*MomentsShare Team © 2024*

