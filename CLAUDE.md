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

# AI 模型测试
python test_ai_models.py            # 测试所有 AI 模型是否正常工作

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
- `friends/` - 好友关系系统（申请/接受/拒绝/删除）
- `interactions/` - 评论和点赞功能
- `ai_service/` - AI 文案润色和标签推荐
- `admin_panel/` - 管理员专用内容管理和统计
- `core/` - 共享工具（异常处理、敏感词过滤）

#### 好友系统：
- **Friendship 模型**: 支持三种状态（PENDING、ACCEPTED、REJECTED）
- **双向关系**: from_user/to_user 字段维护双向好友关系
- **状态转换**: PENDING → ACCEPTED/REJECTED，REJECTED → PENDING（重新申请）
- **搜索逻辑**: 用户搜索返回所有用户（包括已有关系），通过 `friendship_status` 字段显示关系状态
- **序列化器增强**: `UserSerializer` 包含 `friendship_status` 方法，动态计算用户间关系状态

#### 认证机制：
- 自定义 `PhoneAuthBackend` 支持手机号 + 密码登录
- JWT Token：60分钟访问令牌，7天刷新令牌
- Token刷新端点：`/api/v1/auth/token/refresh/` (使用 `TokenRefreshView`)
- 除 `/auth/` 外所有 API 端点都需要认证
- 前端拦截器自动刷新过期token，失败时清除状态并跳转登录

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

#### 好友系统前端实现：
- **AddFriendPage.vue**: 用户搜索和添加好友，根据 `friendship_status` 显示不同按钮状态
- **FriendsPage.vue**: 好友列表管理，包含本地搜索功能和快速操作栏
- **FriendRequestsPage.vue**: 处理好友申请（接受/拒绝）
- **MessagesPage.vue**: 消息中心，显示好友申请数量徽章

### 管理后台 (Vue 3)
- **Vue 3 + Element Plus** 管理界面
- **ECharts** 数据可视化
- Axios API 通信

## 核心开发模式

### 架构关键点

#### Token刷新流程
需要理解以下文件间的协作：
1. **后端**: `users/auth_urls.py` - 提供 `/auth/token/refresh/` 端点
2. **前端**: `api/request.js` - 响应拦截器捕获401错误并自动刷新token
3. **前端**: `stores/auth.js` - Pinia store 管理token状态，保持与localStorage同步

流程：API调用失败(401) → 拦截器捕获 → 调用refresh端点 → 更新localStorage和Pinia → 重试原请求 → 失败则跳转登录

#### AI模型切换架构
需要理解以下文件间的协作：
1. **后端**: `ai_service/services.py` - `AIService.get_llm()` 根据model_name动态初始化模型
2. **后端**: `ai_service/views.py` - 接收model参数，传递给service层
3. **前端**: `views/publish/PublishPage.vue` - 模型选择器UI，管理selectedModelIndex状态
4. **前端**: `api/ai.js` - API调用时携带model参数，设置AI专用超时

流程：用户选择模型 → 前端保存状态 → API调用携带model参数 → 后端get_llm()初始化指定模型 → 自动检测是否为视觉模型 → 非视觉模型+图片则切换到Qwen3-VL

#### 视频首帧截取流程
1. **前端**: `views/publish/PublishPage.vue` - `captureVideoFrame()` 函数
2. 使用HTML5 Video API加载视频元数据 → 跳转到0秒 → Canvas绘制当前帧 → 转换为Blob → 创建File对象 → 传递给AI API

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

# AI Service Configuration (使用 OpenAI 兼容接口)
AI_PROVIDER=openai                    # 提供商：openai, zhipu 等
AI_API_KEY=your-api-key               # API 密钥
AI_BASE_URL=https://api.siliconflow.cn/v1  # API 基础 URL
AI_MODEL_NAME=Qwen/Qwen2.5-7B-Instruct  # 默认模型
AI_PROXY_URL=                         # 可选：代理 URL

# Google AI (已弃用，保留向后兼容)
GOOGLE_API_KEY=your-google-api-key
GOOGLE_AI_MODEL=gemini-1.5-flash

# Content moderation
SENSITIVE_WORDS=违禁,敏感,非法
```

#### 前端
- Vite 代理配置：`/api` → `http://localhost:8000`，`/media` → `http://localhost:8000`
- 启用 Vant 组件和 Vue API 自动导入
- SCSS 全局变量通过 `vite.config.js` 自动注入每个组件

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

### 好友系统功能
- **用户搜索**: 支持按昵称/手机号搜索，返回所有用户（包括已有关系）
- **关系状态**: 动态显示好友关系（无关系/PENDING/ACCEPTED/REJECTED）
- **状态管理**: 不同状态显示对应操作按钮（添加/已发送/已添加）
- **重新申请**: REJECTED状态用户可重新申请，自动转换为PENDING状态
- **本地搜索**: 通讯录页面支持本地好友搜索，快速定位特定好友

### 视频处理
- 视频上传触发异步 Celery 转码任务
- 视频处理需要 FFmpeg（Docker 中已包含）
- 处理后的视频存储在 `media/` 目录
- **首帧截取**: 前端使用 Canvas API 截取视频首帧，用于 AI 视觉识别
- **视频状态**: `PROCESSING` (处理中) → `READY` (就绪) / `FAILED` (失败)
- **Celery 任务**: 异步转码、生成缩略图、更新视频状态

### AI 功能
- **多模态AI支持**: 基于LangChain框架，使用OpenAI兼容接口调用多个AI模型
- **AI润色**: 使用硅基流动/通义千问/智谱GLM/阶跃星辰等模型进行文案润色优化
- **智能标签**: 根据内容（文本+图片/视频首帧）自动推荐3-5个相关标签
- **视觉模型**: 自动检测模型类型，非视觉模型处理图片时自动切换到Qwen3-VL
- **模型切换**: 前端发布页支持动态切换AI模型（Qwen2.5、Qwen3-VL、GLM-4.6V、stepfun-ai/step3）
- **视频处理**: 上传视频时自动截取首帧用于AI视觉识别
- **超时管理**: 分层超时配置（默认120s → AI专用180s → GLM模型120s）

#### AI模型配置
支持的AI模型（通过环境变量或前端选择）：
- `Qwen/Qwen2.5-7B-Instruct` - 通义千问文本模型（默认）
- `Qwen/Qwen3-VL-8B-Instruct` - 通义千问视觉多模态模型
- `zai-org/GLM-4.6V` - 智谱GLM视觉模型（响应较慢，需要更长超时）
- `stepfun-ai/step3` - 阶跃星辰多模态模型

视觉模型检测关键词：`VL`、`V-`、`4.6V`、`GLM-4.6V`、`step3`、`stepfun`、`vision`、`multimodal`

## AI 功能开发注意事项

### 后端开发 (ai_service/)
- **服务架构**: `AIService` 类封装所有AI调用，使用 LangChain 的 ChatOpenAI 接口
- **模型切换**: 通过 `model_name` 参数动态切换模型，支持运行时模型选择
- **超时配置**: GLM模型需要更长超时（120s），其他模型默认90s
- **视觉检测**: 自动检测模型是否支持视觉，非视觉模型处理图片时自动切换
- **响应清理**: 处理GLM等模型的特殊输出格式（如 `<think>` 标签）
- **降级策略**: AI失败时返回原文内容作为降级响应

### 前端开发
- **超时层级**: `request.js` (120s) → `ai.js` (180s) → 后端 (90-120s)
- **模型选择**: 发布页 `PublishPage.vue` 包含模型选择器，支持4个模型切换
- **视频帧捕获**: 使用 Canvas API 截取视频首帧，转换为 File 对象供AI使用
- **错误处理**: 错误响应的 `detail` 字段可能是对象，需要类型检查后再显示
- **Token刷新**: 响应拦截器自动刷新过期token，同步更新 Pinia store

### AI模型测试
使用 `backend/test_ai_models.py` 脚本测试所有模型：
```bash
cd backend
python test_ai_models.py
```

### 常见问题
- **GLM超时**: GLM模型响应慢，前端显示提示让用户耐心等待
- **视频帧捕获**: 确保视频加载完成（`onloadedmetadata` 和 `onseeked`）后再截取
- **Token过期**: 401错误时前端自动刷新token，刷新失败跳转登录页

### 管理功能
- 独立的管理员认证系统
- 内容审核功能
- 带图表的统计仪表板
- 与普通用户不同的权限级别

## 好友系统开发注意事项

### 后端开发
- **搜索逻辑**: 用户搜索API不应排除已有关系的用户，返回所有用户并通过 `friendship_status` 标识关系
- **状态管理**: 正确处理PENDING、ACCEPTED、REJECTED三种状态及其转换逻辑
- **重新申请**: REJECTED状态允许重新申请，转换为PENDING状态而非创建新记录
- **序列化器**: 在UserSerializer中使用 `SerializerMethodField` 动态计算好友关系状态

### 前端开发
- **状态显示**: 根据 `friendship_status` 显示对应UI状态（添加/已发送/已添加）
- **本地搜索**: 通讯录搜索应过滤现有好友列表，不应跳转到其他页面
- **操作逻辑**: 发送申请后更新本地状态，避免重新请求或移除用户
- **用户体验**: 提供清晰的状态反馈和操作提示

### 常见问题
- **用户搜索**: 搜索结果包含所有用户，基于关系状态显示不同操作选项
- **重复申请**: 检查现有Friendship记录，根据状态决定是否允许新申请
- **状态同步**: 前端操作后及时更新本地状态，保持与后端数据一致性

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