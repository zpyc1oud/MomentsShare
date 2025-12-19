# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码仓库中工作时提供指导。

## 项目概述

MomentsShare 是一个社交分享平台（类似微信朋友圈），采用 Django REST API 后端和 Vue 3 前端。平台支持图文/视频动态发布、好友关系、AI 内容辅助功能，并包含管理后台。

## 开发命令

### 后端 (Django)
```bash
cd backend

# 环境配置
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

# 开发环境
python manage.py runserver 0.0.0.0:8000  # 启动 Django 开发服务器
celery -A moments_share worker -l info      # 启动 Celery Worker 处理视频转码

# 测试
pytest                              # 运行所有测试
pytest --cov                        # 运行测试并查看覆盖率
pytest tests/test_users.py          # 运行特定模块测试
pytest -v                           # 详细测试输出

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# API 文档（服务器运行时访问）
# Swagger UI: http://localhost:8000/api/docs/
# ReDoc: http://localhost:8000/api/redoc/
```

### 前端 (Vue 3 - 移动端应用)
```bash
cd frontend

# 环境配置
npm install

# 开发环境
npm run dev          # 启动开发服务器（端口 3000）

# 构建与代码检查
npm run build        # 生产环境构建
npm run preview      # 预览生产构建
npm run lint         # 运行 ESLint 自动修复
```

### 管理后台 (Vue 3)
```bash
cd admin-dashboard

# 环境配置
npm install

# 开发环境
npm run dev          # 启动开发服务器
npm run build        # 生产环境构建
npm run preview      # 预览生产构建
npm run serve        # 在端口 3000 提供服务
```

### Docker 部署
```bash
cd backend
docker-compose up -d          # 启动所有服务
docker-compose ps              # 检查服务状态
docker-compose down            # 停止所有服务
```

## 架构概览

### 后端结构 (Django)
- **Django 4.2+** 配合 **DRF** 提供 REST API
- **JWT 认证** 通过 django-rest-framework-simplejwt
- **Celery + Redis** 用于异步视频处理
- **PostgreSQL/SQLite** 数据库
- **Google Generative AI (Gemini)** AI 功能集成

#### 核心 Django 应用：
- `users/` - 用户认证、个人资料、手机号认证
- `moments/` - 动态发布（图文/视频）、AI 辅助内容
- `friends/` - 好友关系（申请/接受/删除）
- `interactions/` - 评论和回复
- `ai_service/` - AI 文案润色和标签推荐
- `admin_panel/` - 管理员专用内容管理和统计
- `core/` - 共享工具（异常处理、敏感词过滤）

#### 认证机制：
- 自定义 `PhoneAuthBackend` 支持手机号 + 密码登录
- JWT Token：60分钟访问令牌，7天刷新令牌
- 除 `/auth/` 外所有 API 端点都需要认证

### 前端结构 (Vue 3 移动端)
- **Vue 3 + Composition API** 配合 **Vite 5**
- **Pinia** 状态管理
- **Vue Router 4** 移动端优化路由
- **Vant UI** 移动端组件库
- **手机模拟器** 设计（iPhone 14 Pro 风格）

#### 前端架构：
- 移动优先设计，采用手机模拟器包装
- 毛玻璃拟态 UI 配合马卡龙色系（参见 `docs/STYLE_GUIDE.md`）
- Vue 组件和 Vant UI 自动导入
- SCSS 配合路径别名（`@components`、`@views`、`@api` 等）

### 管理后台 (Vue 3)
- **Vue 3 + Element Plus** 管理界面
- **ECharts** 数据可视化
- Axios API 通信

## 核心开发模式

### 后端 API 设计
- RESTful 端点位于 `/api/v1/`
- 分页：PageNumberPagination（每页 10 项）
- `core.exceptions.py` 中的自定义异常处理
- 启用敏感词过滤
- 通过 drf-spectacular 提供完整的 API 文档

### 前端模式
- 组件结构：`components/common/`、`components/business/`、`components/layout/`
- 按功能组织视图：`views/auth/`、`views/home/`、`views/profile/` 等
- 使用 Pinia 的 `stores/` 目录中的状态模块
- API 调用集中在 `api/` 目录
- 移动端优化，支持触摸交互和下拉刷新

### 环境变量

#### 后端 (.env)
```bash
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL in production)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=moments_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Celery + Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Google AI
GOOGLE_API_KEY=your-google-api-key
GOOGLE_AI_MODEL=gemini-1.5-flash

# Content moderation
SENSITIVE_WORDS=违禁,敏感,非法
```

#### 前端
- 代理配置指向后端 `http://localhost:8000`
- 启用 Vant 组件和 Vue API 自动导入

## 测试策略

### 后端测试
- **pytest** 配合 Django 集成
- 可用覆盖率报告
- 测试文件位于 `tests/` 目录（已配置 conftest.py）
- 使用 DRF 测试客户端进行 API 测试

### 前端测试
- ESLint 配置用于代码质量检查
- 当前未配置单元测试（考虑添加 Vitest）

## 开发指南

### 后端
- 遵循 PEP 8 Python 代码风格
- 使用中文作为错误消息和注释
- 时区：`Asia/Shanghai`，语言：`zh-hans`
- 除认证端点外，所有视图都需要认证
- 用户内容应用敏感词过滤

### 前端
- 遵循 Vue 3 Composition API 模式
- 使用 SCSS 和设计系统变量（参见风格指南）
- 移动优先响应式设计
- 保持毛玻璃拟态 UI 一致性
- 组件应可复用且移动端优化

### API 集成
- 前端代理：`/api` → `http://localhost:8000`
- 认证：`Authorization: Bearer <token>`
- 错误处理：使用一致的错误显示模式
- 加载状态：API 调用期间显示加载指示器

## 特定功能说明

### 视频处理
- 视频上传触发异步 Celery 转码任务
- 视频处理需要 FFmpeg（Docker 中已包含）
- 处理后的视频存储在 `media/` 目录

### AI 功能
- 通过 Google Gemini API 进行文案润色
- 内容发现的标签推荐
- AI 服务集成到发布流程中

### 管理功能
- 独立的管理员认证系统
- 内容审核功能
- 带图表的统计仪表板
- 与普通用户不同的权限级别

## 代码质量工具

### 后端
- 建议使用 Python 类型提示
- DRF 序列化器用于 API 验证
- Django 管理面板配置用于数据管理

### 前端
- ESLint 用于 JavaScript/Vue 代码质量
- Vite 用于快速开发和优化构建
- 为常用 Vue 和 Vant API 配置自动导入

## 部署说明

- Docker Compose 设置包括 PostgreSQL、Redis、Django 和 Celery Worker
- 媒体文件通过 Docker 卷处理
- 静态文件收集到 `staticfiles/` 目录
- 配置 CORS 用于前后端通信