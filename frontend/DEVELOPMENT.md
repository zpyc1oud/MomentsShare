# MomentsShare 小程序前端开发规范

## 📁 项目目录结构

```
frontend/
├── index.html                 # 入口 HTML
├── package.json               # 依赖配置
├── vite.config.js             # Vite 配置
├── DEVELOPMENT.md             # 开发规范文档（本文件）
│
└── src/
    ├── main.js                # 应用入口
    ├── App.vue                # 根组件
    │
    ├── api/                   # API 接口层
    │   ├── index.js           # 统一导出
    │   ├── request.js         # Axios 实例配置
    │   ├── auth.js            # 认证相关接口
    │   ├── moments.js         # 动态相关接口
    │   ├── friends.js         # 好友相关接口
    │   └── ai.js              # AI 服务接口
    │
    ├── assets/                # 静态资源
    │   └── styles/
    │       ├── variables.scss # SCSS 变量定义
    │       └── global.scss    # 全局样式
    │
    ├── components/            # 组件目录
    │   ├── layout/            # 布局组件
    │   │   ├── PhoneSimulator.vue   # 📱 手机模拟器外壳
    │   │   ├── PageLayout.vue       # 页面布局模板
    │   │   ├── NavBar.vue           # 导航栏
    │   │   └── TabBar.vue           # 底部标签栏
    │   │
    │   ├── common/            # 通用组件
    │   │   ├── Loading.vue          # 加载状态
    │   │   ├── Toast.vue            # 轻提示
    │   │   ├── Modal.vue            # 弹窗
    │   │   ├── ImagePreview.vue     # 图片预览
    │   │   ├── VideoPlayer.vue      # 视频播放器
    │   │   └── PullRefresh.vue      # 下拉刷新
    │   │
    │   ├── business/          # 业务组件
    │   │   └── MomentCard.vue       # 动态卡片
    │   │
    │   └── icons/             # 图标组件
    │       ├── IconHome.vue
    │       ├── IconSearch.vue
    │       ├── IconAdd.vue
    │       ├── IconMessage.vue
    │       └── IconProfile.vue
    │
    ├── router/                # 路由配置
    │   └── index.js
    │
    ├── stores/                # Pinia 状态管理
    │   └── auth.js            # 认证状态
    │
    ├── utils/                 # 工具函数
    │   └── index.js
    │
    └── views/                 # 页面视图
        ├── auth/              # P1: 登录/注册
        │   ├── LoginPage.vue
        │   └── RegisterPage.vue
        │
        ├── home/              # P2: 首页 Feed 流
        │   └── HomePage.vue
        │
        ├── publish/           # P3: 发布页
        │   └── PublishPage.vue
        │
        ├── discover/          # P4: 发现与搜索
        │   └── DiscoverPage.vue
        │
        ├── messages/          # P5: 消息与好友
        │   ├── MessagesPage.vue
        │   ├── FriendsPage.vue
        │   └── FriendRequestsPage.vue
        │
        ├── moment/            # P6: 动态详情
        │   └── MomentDetailPage.vue
        │
        ├── profile/           # P7: 个人中心
        │   ├── ProfilePage.vue
        │   ├── ProfileEditPage.vue
        │   ├── UserProfilePage.vue
        │   └── SettingsPage.vue
        │
        └── error/             # 错误页面
            └── NotFoundPage.vue
```

---

## 📱 手机模拟器使用说明

本项目使用 **PhoneSimulator** 组件模拟 iPhone 14 Pro 的外观效果，所有页面都会在这个模拟器内显示。

### 模拟器结构

```
┌─────────────────────────────────────┐
│  ╭───────────────────────────────╮  │ ← 手机外壳边框
│  │ 09:41    [灵动岛]    📶 🔋   │  │ ← 状态栏
│  ├───────────────────────────────┤  │
│  │                               │  │
│  │      页面内容区域              │  │ ← PageLayout
│  │      (router-view)            │  │
│  │                               │  │
│  ├───────────────────────────────┤  │
│  │   🏠    🔍    ➕    💬    👤   │  │ ← TabBar
│  ╰───────────────────────────────╯  │
│            ═══════════              │ ← 底部指示条
└─────────────────────────────────────┘
```

### 尺寸规格

| 元素 | 尺寸 |
|------|------|
| 手机宽度 | 393px |
| 手机高度 | 852px |
| 圆角半径 | 50px |
| 状态栏高度 | 44px |
| 导航栏高度 | 56px |
| 标签栏高度 | 60px |

---

## 🧩 页面模板使用规范

### 基础页面模板

每个页面必须使用 `PageLayout` 组件作为根容器：

```vue
<template>
  <PageLayout 
    title="页面标题"
    :show-back="true"
    :show-tabbar="true"
  >
    <!-- 导航栏左侧插槽 -->
    <template #nav-left>
      <button>自定义按钮</button>
    </template>
    
    <!-- 导航栏右侧插槽 -->
    <template #nav-right>
      <button>操作</button>
    </template>
    
    <!-- 页面主体内容 -->
    <div class="page-content">
      ...
    </div>
  </PageLayout>
</template>

<script setup>
import PageLayout from '@/components/layout/PageLayout.vue'
</script>
```

### PageLayout Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `title` | String | `''` | 导航栏标题 |
| `showNavbar` | Boolean | `true` | 是否显示导航栏 |
| `showBack` | Boolean | `false` | 是否显示返回按钮 |
| `showTabbar` | Boolean | `true` | 是否显示底部标签栏 |
| `scrollable` | Boolean | `true` | 内容区是否可滚动 |
| `navTransparent` | Boolean | `false` | 导航栏是否透明 |

### PageLayout Events

| 事件 | 参数 | 说明 |
|------|------|------|
| `@scroll` | `{ scrollTop, scrollHeight, clientHeight }` | 滚动事件 |
| `@back` | - | 返回按钮点击事件 |

---

## 🎨 设计规范

### 颜色系统

```scss
// 主色调
$primary-color: #667eea;        // 主色
$primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

// 背景色
$bg-dark: #0f0f23;              // 深色背景
$bg-card: #1a1a2e;              // 卡片背景
$bg-input: #2a2a4a;             // 输入框背景

// 文字色
$text-primary: #ffffff;          // 主文字
$text-secondary: rgba(255, 255, 255, 0.7);  // 次要文字
$text-muted: rgba(255, 255, 255, 0.45);     // 辅助文字

// 状态色
$success-color: #52c41a;
$warning-color: #faad14;
$error-color: #ff4d4f;
```

### 字体规范

```scss
$font-family: 'Noto Sans SC', -apple-system, sans-serif;

$font-size-xs: 11px;
$font-size-sm: 13px;
$font-size-base: 15px;
$font-size-lg: 17px;
$font-size-xl: 20px;
$font-size-2xl: 24px;
```

### 间距规范

```scss
$spacing-xs: 4px;
$spacing-sm: 8px;
$spacing-md: 16px;
$spacing-lg: 24px;
$spacing-xl: 32px;
```

### 圆角规范

```scss
$radius-sm: 8px;
$radius-md: 12px;
$radius-lg: 16px;
$radius-xl: 24px;
$radius-full: 9999px;
```

---

## 📝 组件开发规范

### 1. 文件命名

- 组件文件使用 **PascalCase**: `MomentCard.vue`
- 页面文件使用 **PascalCase + Page 后缀**: `HomePage.vue`
- 工具函数使用 **camelCase**: `formatTime.js`

### 2. 组件结构

```vue
<template>
  <!-- 模板内容 -->
</template>

<script setup>
// 1. 导入
import { ref, computed, onMounted } from 'vue'

// 2. Props 定义
const props = defineProps({
  title: {
    type: String,
    required: true
  }
})

// 3. Emits 定义
const emit = defineEmits(['update', 'delete'])

// 4. 响应式数据
const loading = ref(false)

// 5. 计算属性
const displayTitle = computed(() => props.title.toUpperCase())

// 6. 方法
const handleClick = () => {
  emit('update')
}

// 7. 生命周期
onMounted(() => {
  // 初始化逻辑
})
</script>

<style lang="scss" scoped>
/* 样式 */
</style>
```

### 3. CSS 类名规范

采用 **BEM 命名法**：

```scss
.component-name {
  // 块样式
  
  &__element {
    // 元素样式
  }
  
  &--modifier {
    // 修饰符样式
  }
}
```

### 4. 公共样式类

项目提供了一系列全局工具类：

```html
<!-- 弹性布局 -->
<div class="flex flex-center flex-between">

<!-- 文字处理 -->
<p class="text-center text-ellipsis text-clamp-2">

<!-- 按钮 -->
<button class="btn btn--primary btn--block">

<!-- 卡片 -->
<div class="card card--hover">

<!-- 头像 -->
<img class="avatar avatar--lg">

<!-- 标签 -->
<span class="tag">
```

---

## 🔌 API 调用规范

### 1. 接口定义

所有 API 接口定义在 `src/api/` 目录下：

```javascript
// src/api/moments.js
import request from './request'

export const momentsApi = {
  // 获取动态列表
  getFeed(page = 1) {
    return request.get('/moments/feed/', { params: { page } })
  },
  
  // 发布动态
  create(data) {
    const formData = new FormData()
    // ... 处理数据
    return request.post('/moments/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}
```

### 2. 在组件中使用

```vue
<script setup>
import { ref, onMounted } from 'vue'
import { momentsApi } from '@/api/moments'

const moments = ref([])
const loading = ref(false)

const fetchMoments = async () => {
  loading.value = true
  try {
    const response = await momentsApi.getFeed()
    moments.value = response.results
  } catch (error) {
    console.error('Fetch error:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchMoments()
})
</script>
```

### 3. 错误处理

API 请求的错误统一在 `request.js` 中处理：
- 401 错误：自动刷新 Token 或跳转登录
- 其他错误：返回给调用方处理

---

## 🚦 路由规范

### 路由配置

```javascript
{
  path: '/moment/:id',
  name: 'MomentDetail',
  component: () => import('@/views/moment/MomentDetailPage.vue'),
  meta: {
    requiresAuth: true,    // 需要登录
    hideTabbar: true       // 隐藏底部标签栏
  }
}
```

### 路由 Meta 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `requiresAuth` | Boolean | 是否需要登录才能访问 |
| `hideTabbar` | Boolean | 是否隐藏底部标签栏 |

---

## 🗃️ 状态管理规范

使用 **Pinia** 进行状态管理：

```javascript
// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const accessToken = ref('')

  // Getters
  const isLoggedIn = computed(() => !!accessToken.value)

  // Actions
  const login = async (phone, password) => {
    // 登录逻辑
  }

  return { user, accessToken, isLoggedIn, login }
})
```

---

## 🛠️ 开发流程

### 1. 环境准备

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

### 2. 开发新页面步骤

1. 在 `src/views/` 下创建页面组件
2. 在 `src/router/index.js` 中添加路由
3. 使用 `PageLayout` 模板包裹页面内容
4. 调用 API 获取数据
5. 测试并确保在手机模拟器中正确显示

### 3. 开发新组件步骤

1. 确定组件类型（layout/common/business）
2. 在对应目录下创建 `.vue` 文件
3. 定义 Props、Emits
4. 编写模板和样式
5. 导出并在需要的地方引用

---

## 📋 任务分配对应表

| 成员 | 负责页面 | 对应文件 |
|------|----------|----------|
| **Member C** (查鹏宇) | P2 首页 Feed 流、P6 动态详情 | `HomePage.vue`, `MomentDetailPage.vue`, `MomentCard.vue` |
| **Member D** (杨智涵) | P3 发布页、AI 功能集成 | `PublishPage.vue` |
| **Member E** (万炜杰) | P1 登录/注册、P7 个人中心、P5 好友 | `LoginPage.vue`, `RegisterPage.vue`, `ProfilePage.vue`, `FriendsPage.vue` |
| **Member F** (杨迪) | P4 发现与搜索、全局组件封装 | `DiscoverPage.vue`, `ImagePreview.vue`, `VideoPlayer.vue` |

---

## ✅ Checklist

开发前请确认：

- [ ] 已阅读本规范文档
- [ ] 已安装项目依赖 (`npm install`)
- [ ] 已启动后端服务 (端口 8000)
- [ ] 使用 `PageLayout` 作为页面容器
- [ ] 遵循 BEM 命名规范
- [ ] API 调用使用 `src/api/` 下的模块
- [ ] 提交前测试页面在手机模拟器中的显示效果

---

## 📞 常见问题

### Q: 如何在页面中隐藏底部标签栏？

在路由配置中设置 `meta: { hideTabbar: true }`，并在页面组件中设置 `:show-tabbar="false"`。

### Q: 如何自定义导航栏按钮？

使用 `#nav-left` 或 `#nav-right` 插槽：

```vue
<PageLayout title="标题">
  <template #nav-right>
    <button @click="handleAction">操作</button>
  </template>
</PageLayout>
```

### Q: 如何使用全局 SCSS 变量？

变量在 `vite.config.js` 中已全局引入，可直接在组件样式中使用：

```scss
<style lang="scss" scoped>
.my-class {
  color: $primary-color;
  padding: $spacing-md;
}
</style>
```

### Q: 如何添加新的 API 接口？

1. 在 `src/api/` 下找到对应模块文件
2. 添加新的方法
3. 在 `src/api/index.js` 中导出（如果是新模块）

---

## 🎯 质量要求

1. **响应式**: 页面在模拟器中正确显示
2. **加载状态**: 异步操作显示 Loading
3. **错误处理**: 异常情况有友好提示
4. **空状态**: 列表为空时显示占位内容
5. **交互反馈**: 按钮点击有视觉反馈

---

*最后更新: 2024年12月*

