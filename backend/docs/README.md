# MomentsShare 项目文档

## 📖 项目概述

MomentsShare 是一个基于 Django REST Framework 的社交分享平台后端服务，支持用户发布图文/视频动态、好友关系管理、评论互动以及 AI 辅助功能。

---

## 🏗️ 技术栈

| 技术 | 版本要求 | 说明 |
|------|----------|------|
| Django | ≥4.2, <5.0 | Web 框架 |
| Django REST Framework | ≥3.14.0 | RESTful API 框架 |
| SimpleJWT | ≥5.3.0 | JWT 认证 |
| Celery | ≥5.3.0 | 异步任务队列 |
| Redis | ≥4.5.0 | Celery Broker & 缓存 |
| Pillow | ≥10.0.0 | 图片处理 |
| google-generativeai | ≥0.8.0 | Google Gemini AI 服务 |
| SQLite / PostgreSQL | - | 数据库 |

---

## 📂 项目结构

```
MomentsShare/
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
│   ├── models.py           # 用户模型
│   ├── views.py            # 用户视图
│   ├── serializers.py      # 用户序列化器
│   ├── backends.py         # 手机号认证后端
│   ├── urls.py             # 用户资料 URL
│   └── auth_urls.py        # 认证 URL
│
├── moments/                # 动态模块
│   ├── models.py           # 动态、标签、图片模型
│   ├── views.py            # 动态视图
│   ├── serializers.py      # 动态序列化器
│   ├── tasks.py            # Celery 任务（视频转码）
│   └── urls.py             # 动态 URL
│
├── friends/                # 好友模块
│   ├── models.py           # 好友关系模型
│   ├── views.py            # 好友视图
│   ├── serializers.py      # 好友序列化器
│   └── urls.py             # 好友 URL
│
├── interactions/           # 互动模块
│   ├── models.py           # 评论模型
│   ├── views.py            # 评论视图
│   ├── serializers.py      # 评论序列化器
│   └── urls.py             # 评论 URL
│
├── ai_service/             # AI 服务模块
│   ├── client.py           # Google Gemini AI 客户端
│   ├── views.py            # AI 视图
│   ├── serializers.py      # AI 序列化器
│   └── urls.py             # AI URL
│
├── admin_panel/            # 管理后台模块
│   ├── views.py            # 管理视图
│   ├── serializers.py      # 管理序列化器
│   ├── permissions.py      # 管理员权限
│   └── urls.py             # 管理 URL
│
├── tests/                  # 测试模块
├── media/                  # 媒体文件存储
├── conftest.py             # pytest 配置
├── pytest.ini              # pytest 配置文件
├── requirements.txt        # 依赖包
└── manage.py               # Django 管理脚本
```

---

## 🔐 认证机制

### JWT Token 认证

项目使用 `djangorestframework-simplejwt` 实现 JWT 认证：

- **Access Token**: 有效期 60 分钟
- **Refresh Token**: 有效期 7 天
- **认证头格式**: `Authorization: Bearer <access_token>`

### 认证后端

支持两种认证方式：
1. **手机号认证** (`PhoneAuthBackend`): 使用手机号 + 密码登录
2. **Django 默认认证** (`ModelBackend`): 备用认证

---

## 🎯 核心功能模块

### 1. 用户模块 (users)

- 用户注册（手机号 + 用户名 + 昵称）
- 用户登录/登出（JWT Token）
- 个人资料查看/编辑
- 手机号变更（需密码验证）

### 2. 动态模块 (moments)

- 发布图文动态（最多 9 张图片）
- 发布视频动态（异步转码处理）
- 动态详情查看
- 好友动态信息流
- 动态搜索（关键词、标签、日期范围）
- 敏感词过滤

### 3. 好友模块 (friends)

- 发起好友申请
- 接受/拒绝好友申请
- 删除好友关系

### 4. 互动模块 (interactions)

- 发布评论
- 回复评论（嵌套评论）
- 评论列表查看

### 5. AI 服务模块 (ai_service)

- **文案润色**: 基于文字/图片生成润色后的社交文案
- **标签推荐**: 智能推荐 3-5 个相关标签

### 6. 管理后台 (admin_panel)

- 管理员登录
- 内容列表查看
- 内容下架删除
- 数据统计（DAU、新增用户、发帖数）

---

## ⚙️ 配置说明

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `DJANGO_SECRET_KEY` | `dev-secret-key` | Django 密钥 |
| `DJANGO_DEBUG` | `True` | 调试模式 |
| `DJANGO_ALLOWED_HOSTS` | `*` | 允许的主机 |
| `DB_ENGINE` | `django.db.backends.sqlite3` | 数据库引擎 |
| `DB_NAME` | `db.sqlite3` | 数据库名 |
| `DB_USER` | - | 数据库用户 |
| `DB_PASSWORD` | - | 数据库密码 |
| `DB_HOST` | - | 数据库主机 |
| `DB_PORT` | - | 数据库端口 |
| `CELERY_BROKER_URL` | `redis://localhost:6379/0` | Celery Broker |
| `CELERY_RESULT_BACKEND` | 同 Broker | Celery 结果后端 |
| `GOOGLE_API_KEY` | - | Google AI API Key |
| `GOOGLE_AI_MODEL` | `gemini-1.5-flash` | AI 模型名称 |
| `SENSITIVE_WORDS` | `违禁,敏感,非法` | 敏感词列表（逗号分隔）|

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 数据库迁移

```bash
python manage.py migrate
```

### 3. 创建超级用户

```bash
python manage.py createsuperuser
```

### 4. 启动开发服务器

```bash
python manage.py runserver
```

### 5. 启动 Celery Worker（用于视频转码）

```bash
celery -A moments_share worker -l info
```

---

## 🧪 测试

项目使用 pytest 进行测试：

```bash
# 运行所有测试
pytest

# 运行测试并查看覆盖率
pytest --cov

# 运行特定模块测试
pytest tests/test_users.py
```

---

## 🌐 在线 API 文档

项目集成了 **drf-spectacular**，启动服务后可访问交互式 API 文档：

| 文档类型 | URL | 说明 |
|----------|-----|------|
| Swagger UI | http://localhost:8000/api/docs/ | 可交互的 API 测试界面 |
| ReDoc | http://localhost:8000/api/redoc/ | 美观的只读文档 |
| OpenAPI Schema | http://localhost:8000/api/schema/ | OpenAPI 3.0 规范 |

---

## 📚 相关文档

- [数据模型文档](MODELS.md)
- [API 接口文档](API.md)
- [部署指南](DEPLOYMENT.md)

---

## 📝 开发规范

### 代码风格

- 遵循 PEP 8 规范
- 使用中文注释和错误消息
- 时区设置: `Asia/Shanghai`
- 语言设置: `zh-hans`

### API 响应格式

成功响应：
```json
{
  "id": 1,
  "field": "value"
}
```

错误响应：
```json
{
  "detail": {
    "field": ["错误信息"]
  }
}
```

分页响应：
```json
{
  "count": 100,
  "next": "http://api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

