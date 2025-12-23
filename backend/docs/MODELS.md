# MomentsShare 数据模型文档

本文档详细描述了 MomentsShare 项目中所有数据模型的设计和字段说明。

---

## 目录

1. [用户模型 (User)](#1-用户模型-user)
2. [动态模型 (Moment)](#2-动态模型-moment)
3. [标签模型 (Tag)](#3-标签模型-tag)
4. [动态标签关联 (MomentTag)](#4-动态标签关联-momenttag)
5. [图片模型 (Image)](#5-图片模型-image)
6. [好友关系模型 (Friendship)](#6-好友关系模型-friendship)
7. [评论模型 (Comment)](#7-评论模型-comment)
8. [点赞模型 (Like)](#8-点赞模型-like)
9. [评分模型 (Rating)](#9-评分模型-rating)

---

## 1. 用户模型 (User)

**位置**: `users/models.py`

**说明**: 自定义用户模型，继承自 `AbstractBaseUser` 和 `PermissionsMixin`，使用手机号作为主要登录凭证。

### 字段定义

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| `id` | BigAutoField | PK, Auto | 主键 |
| `phone` | CharField(11) | Unique, Required | 手机号（11位） |
| `username` | CharField(30) | Unique, Required | 用户名 |
| `nickname` | CharField(30) | Required | 昵称 |
| `avatar` | ImageField | Optional | 头像图片 |
| `password` | - | Required | 密码（加密存储） |
| `is_staff` | BooleanField | Default=False | 是否为管理员 |
| `is_active` | BooleanField | Default=True | 账号是否激活 |
| `is_superuser` | BooleanField | Default=False | 是否为超级管理员 |
| `created_at` | DateTimeField | Auto | 注册时间 |
| `last_login` | DateTimeField | Auto | 最后登录时间 |

### 认证配置

```python
USERNAME_FIELD = "phone"       # 使用手机号登录
REQUIRED_FIELDS = ["username", "nickname"]  # 创建用户必填字段
```

### UserManager 方法

```python
def create_user(phone, username, nickname, password=None, **extra_fields)
    """创建普通用户"""

def create_superuser(phone, username, nickname, password=None, **extra_fields)
    """创建超级管理员"""
```

### 模型关系

```
User
 ├── moments (反向: Moment.author)
 ├── comments (反向: Comment.author)
 ├── friend_requests_sent (反向: Friendship.from_user)
 └── friend_requests_received (反向: Friendship.to_user)
```

---

## 2. 动态模型 (Moment)

**位置**: `moments/models.py`

**说明**: 存储用户发布的图文或视频动态。

### 字段定义

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| `id` | BigAutoField | PK, Auto | 主键 |
| `author` | ForeignKey(User) | Required | 发布者 |
| `content` | TextField | Optional | 文字内容 |
| `type` | CharField(10) | Required | 动态类型 |
| `video_file` | FileField | Optional | 视频文件 |
| `video_status` | CharField(15) | Default='READY' | 视频处理状态 |
| `is_deleted` | BooleanField | Default=False | 是否已删除 |
| `created_at` | DateTimeField | Auto | 创建时间 |
| `tags` | ManyToMany(Tag) | Optional | 关联标签 |

### 枚举类型

**MomentType (动态类型)**:
| 值 | 说明 |
|----|------|
| `IMAGE` | 图文动态 |
| `VIDEO` | 视频动态 |

**VideoStatus (视频状态)**:
| 值 | 说明 |
|----|------|
| `PROCESSING` | 处理中 |
| `READY` | 已就绪 |

### 模型关系

```
Moment
 ├── author → User
 ├── images (反向: Image.moment)
 ├── comments (反向: Comment.moment)
 └── tags ↔ Tag (多对多)
```

### 业务规则

1. 图文动态 (`IMAGE`):
   - 最多上传 9 张图片
   - 不能上传视频文件
   - `video_status` 自动设为 `READY`

2. 视频动态 (`VIDEO`):
   - 必须上传视频文件
   - 不能上传图片
   - 上传后 `video_status` 设为 `PROCESSING`
   - 通过 Celery 任务异步转码后设为 `READY`

3. 内容过滤:
   - 发布前检测敏感词
   - 软删除（`is_deleted=True`）

---

## 3. 标签模型 (Tag)

**位置**: `moments/models.py`

**说明**: 动态标签，用于分类和搜索。

### 字段定义

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| `id` | BigAutoField | PK, Auto | 主键 |
| `name` | CharField(10) | Unique | 标签名称 |

### 使用方式

```python
# 创建或获取标签
tag, created = Tag.objects.get_or_create(name="日常")

# 添加到动态
moment.tags.add(tag)

# 通过标签搜索动态
Moment.objects.filter(tags__name="日常")
```

---

## 4. 动态标签关联 (MomentTag)

**位置**: `moments/models.py`

**说明**: 动态与标签的多对多关联表。

### 字段定义

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| `id` | BigAutoField | PK, Auto | 主键 |
| `moment` | ForeignKey(Moment) | Required | 关联动态 |
| `tag` | ForeignKey(Tag) | Required | 关联标签 |

### 约束

```python
class Meta:
    unique_together = ("moment", "tag")  # 联合唯一
```

---

## 5. 图片模型 (Image)

**位置**: `moments/models.py`

**说明**: 存储图文动态的图片附件。

### 字段定义

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| `id` | BigAutoField | PK, Auto | 主键 |
| `moment` | ForeignKey(Moment) | Required | 所属动态 |
| `image_file` | ImageField | Required | 图片文件 |
| `order` | PositiveIntegerField | Default=1 | 显示顺序 |

### 排序规则

```python
class Meta:
    ordering = ["order", "id"]  # 按 order 和 id 排序
```

### 文件存储

- 存储路径: `media/images/`
- 支持格式: JPEG, PNG, GIF, WebP 等

---

## 6. 好友关系模型 (Friendship)

**位置**: `friends/models.py`

**说明**: 存储用户之间的好友关系和申请状态。

### 字段定义

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| `id` | BigAutoField | PK, Auto | 主键 |
| `from_user` | ForeignKey(User) | Required | 申请发起方 |
| `to_user` | ForeignKey(User) | Required | 申请接收方 |
| `status` | CharField(10) | Default='PENDING' | 申请状态 |
| `created_at` | DateTimeField | Auto | 创建时间 |
| `updated_at` | DateTimeField | Auto | 更新时间 |

### 枚举类型

**Status (好友状态)**:
| 值 | 说明 |
|----|------|
| `PENDING` | 待处理 |
| `ACCEPTED` | 已接受 |
| `REJECTED` | 已拒绝 |

### 约束

```python
class Meta:
    unique_together = ("from_user", "to_user")  # 联合唯一
```

### 业务规则

1. 好友关系是单向记录的（A→B）
2. 查询好友列表需同时查询双向记录
3. 状态流转: `PENDING` → `ACCEPTED` / `REJECTED`
4. 不能向自己发起好友申请

### 查询好友列表示例

```python
from django.db.models import Q

# 获取用户的所有已接受好友
friend_ids = Friendship.objects.filter(
    Q(from_user=user, status='ACCEPTED') |
    Q(to_user=user, status='ACCEPTED')
).values_list("from_user_id", "to_user_id")
```

---

## 7. 评论模型 (Comment)

**位置**: `interactions/models.py`

**说明**: 存储动态下的评论和回复。

### 字段定义

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| `id` | BigAutoField | PK, Auto | 主键 |
| `moment` | ForeignKey(Moment) | Required | 所属动态 |
| `author` | ForeignKey(User) | Required | 评论作者 |
| `content` | TextField | Required | 评论内容 |
| `parent` | ForeignKey(self) | Optional | 父评论（回复） |
| `created_at` | DateTimeField | Auto | 创建时间 |
| `is_deleted` | BooleanField | Default=False | 是否已删除 |

### 排序规则

```python
class Meta:
    ordering = ["created_at", "id"]  # 按时间排序
```

### 模型关系

```
Comment
 ├── moment → Moment
 ├── author → User
 ├── parent → Comment (可选，自引用)
 └── replies (反向: Comment.parent)
```

### 业务规则

1. 支持嵌套评论（回复功能）
2. `parent=None` 表示一级评论
3. `parent` 指向父评论表示回复
4. 回复的父评论必须属于同一动态
5. 软删除（`is_deleted=True`）

### 获取评论树示例

```python
# 获取动态的一级评论
Comment.objects.filter(moment_id=1, parent__isnull=True, is_deleted=False)

# 获取某评论的回复
Comment.objects.filter(parent_id=1, is_deleted=False)
```

---

## 8. 点赞模型 (Like)

**位置**: `interactions/models.py`

**说明**: 存储用户对动态的点赞记录。

### 字段定义

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| `id` | BigAutoField | PK, Auto | 主键 |
| `moment` | ForeignKey(Moment) | Required | 所属动态 |
| `user` | ForeignKey(User) | Required | 点赞用户 |
| `created_at` | DateTimeField | Auto | 点赞时间 |

### 约束

```python
class Meta:
    unique_together = ("moment", "user")  # 联合唯一，每个用户只能点赞一次
    ordering = ["-created_at"]  # 按时间倒序
```

### 模型关系

```
Like
 ├── moment → Moment
 └── user → User
```

### 业务规则

1. 每个用户对每个动态只能点赞一次
2. 再次点赞则取消点赞
3. 点赞记录不可修改，只能创建或删除

### 查询示例

```python
# 检查用户是否点赞
Like.objects.filter(moment_id=1, user_id=1).exists()

# 获取动态的点赞数
Like.objects.filter(moment_id=1).count()

# 获取用户点赞的所有动态
Like.objects.filter(user_id=1).values_list('moment_id', flat=True)
```

---

## 9. 评分模型 (Rating)

**位置**: `interactions/models.py`

**说明**: 存储用户对动态的评分记录（打星）。

### 字段定义

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| `id` | BigAutoField | PK, Auto | 主键 |
| `moment` | ForeignKey(Moment) | Required | 所属动态 |
| `user` | ForeignKey(User) | Required | 评分用户 |
| `score` | PositiveSmallIntegerField | Default=5 | 评分 (1-5) |
| `created_at` | DateTimeField | Auto | 评分时间 |

### 约束

```python
class Meta:
    unique_together = ("moment", "user")  # 联合唯一，每个用户只能评分一次
    ordering = ["-created_at"]  # 按时间倒序
```

### 模型关系

```
Rating
 ├── moment → Moment
 └── user → User
```

### 业务规则

1. 每个用户对每个动态只能评分一次
2. 分数范围为 1-5 星
3. 如果用户已评分，再次评分则更新分数
4. 默认分数为 5 星

### 查询示例

```python
from django.db.models import Avg

# 获取动态的平均分
Rating.objects.filter(moment_id=1).aggregate(Avg('score'))['score__avg']

# 获取用户的评分记录
Rating.objects.filter(moment_id=1, user_id=1).first()

# 获取动态的评分数量
Rating.objects.filter(moment_id=1).count()
```

---

## 📊 ER 图 (实体关系图)

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│     User     │         │    Moment    │         │     Tag      │
├──────────────┤    1:N  ├──────────────┤   M:N   ├──────────────┤
│ id           │◄────────│ author_id    │─────────►│ id           │
│ phone        │         │ content      │         │ name         │
│ username     │         │ type         │         └──────────────┘
│ nickname     │         │ video_file   │                │
│ avatar       │         │ video_status │                │ via MomentTag
│ is_staff     │         │ is_deleted   │                ▼
│ is_active    │         │ created_at   │         ┌──────────────┐
│ created_at   │         └──────────────┘         │  MomentTag   │
└──────────────┘                │                 ├──────────────┤
       │                        │ 1:N             │ moment_id    │
       │                        ▼                 │ tag_id       │
       │                 ┌──────────────┐         └──────────────┘
       │                 │    Image     │
       │                 ├──────────────┤
       │                 │ moment_id    │
       │                 │ image_file   │
       │                 │ order        │
       │                 └──────────────┘
       │
       │ M:N (双向)      ┌──────────────┐
       │                 │  Friendship  │
       └────────────────►├──────────────┤
                         │ from_user_id │
                         │ to_user_id   │
                         │ status       │
                         │ created_at   │
                         │ updated_at   │
                         └──────────────┘
       │
       │ 1:N             ┌──────────────┐
       │                 │   Comment    │
       ├────────────────►├──────────────┤
       │                 │ moment_id    │
       │                 │ author_id    │
       │                 │ content      │
       │                 │ parent_id    │──┐ (自引用)
       │                 │ created_at   │◄─┘
       │                 │ is_deleted   │
       │                 └──────────────┘
       │
       │ 1:N             ┌──────────────┐
       │                 │     Like     │
       ├────────────────►├──────────────┤
       │                 │ moment_id    │
       │                 │ user_id      │
       │                 │ created_at   │
       │                 └──────────────┘
       │
       │ 1:N             ┌──────────────┐
       │                 │    Rating    │
       └────────────────►├──────────────┤
                         │ moment_id    │
                         │ user_id      │
                         │ score        │
                         │ created_at   │
                         └──────────────┘
```

---

## 🔧 数据库索引建议

### 用户表 (users_user)

```sql
-- 已有唯一索引
CREATE UNIQUE INDEX users_user_phone ON users_user(phone);
CREATE UNIQUE INDEX users_user_username ON users_user(username);
```

### 动态表 (moments_moment)

```sql
-- 建议添加的索引
CREATE INDEX moments_moment_author_created ON moments_moment(author_id, created_at DESC);
CREATE INDEX moments_moment_is_deleted_created ON moments_moment(is_deleted, created_at DESC);
CREATE INDEX moments_moment_type_status ON moments_moment(type, video_status);
```

### 好友关系表 (friends_friendship)

```sql
-- 已有唯一索引
CREATE UNIQUE INDEX friends_friendship_from_to ON friends_friendship(from_user_id, to_user_id);

-- 建议添加的索引
CREATE INDEX friends_friendship_to_status ON friends_friendship(to_user_id, status);
```

### 评论表 (interactions_comment)

```sql
-- 建议添加的索引
CREATE INDEX interactions_comment_moment_parent ON interactions_comment(moment_id, parent_id, is_deleted);
CREATE INDEX interactions_comment_author ON interactions_comment(author_id);
```

### 点赞表 (interactions_like)

```sql
-- 已有唯一索引
CREATE UNIQUE INDEX interactions_like_moment_user ON interactions_like(moment_id, user_id);
```

### 评分表 (interactions_rating)

```sql
-- 已有唯一索引
CREATE UNIQUE INDEX interactions_rating_moment_user ON interactions_rating(moment_id, user_id);
```

---

## 📝 数据迁移

### 创建迁移

```bash
python manage.py makemigrations
```

### 执行迁移

```bash
python manage.py migrate
```

### 查看迁移状态

```bash
python manage.py showmigrations
```

### 生成迁移 SQL

```bash
python manage.py sqlmigrate <app_name> <migration_number>
```

