# MomentsShare 前端风格指南

> MomentsShare 设计系统 - 马卡龙色系 × 毛玻璃拟态风格指南

## 📋 目录

- [设计理念](#设计理念)
- [色彩系统](#色彩系统)
- [视觉元素](#视觉元素)
- [组件规范](#组件规范)
- [动画规范](#动画规范)
- [布局规范](#布局规范)
- [字体规范](#字体规范)
- [使用指南](#使用指南)

---

## 🎨 设计理念

### 核心理念
MomentsShare 采用 **"马卡龙色系 + 毛玻璃拟态"** 设计风格，营造温馨、梦幻、现代的社交体验。

### 设计关键词
- **梦幻感** (Dreamy) - 柔和色彩与光效
- **轻盈感** (Lightweight) - 毛玻璃透明效果
- **现代感** (Modern) - 流畅动画与交互
- **友好感** (Friendly) - 圆润设计语言
- **品质感** (Premium) - 精致细节与微交互

---

## 🌈 色彩系统

### 主色调 - 马卡龙色系

```scss
// 主色调 - 甜蜜粉系列
$pink-primary: #FCAEC1;        // 主强调色 - 温柔粉
$pink-light: #FCD1DB;          // 辅助浅粉
$pink-soft: rgba(252, 174, 193, 0.6);

// 辅助色 - 香芋紫
$lavender: #B7A8D6;            // 过渡色，增加梦幻感
$lavender-soft: rgba(183, 168, 214, 0.6);

// 点缀色 - 冰川蓝
$baby-blue: #ADD9F3;           // 冷暖对比点缀
$baby-blue-soft: rgba(173, 217, 243, 0.6);
```

### 渐变色系

```scss
// 主要渐变
$primary-gradient: linear-gradient(135deg, $pink-primary 0%, $lavender 50%, $baby-blue 100%);
$primary-gradient-soft: linear-gradient(135deg, $pink-light 0%, rgba($lavender, 0.8) 50%, rgba($baby-blue, 0.8) 100%);
$button-gradient: linear-gradient(135deg, $lavender 0%, $pink-primary 100%);
```

### 背景色系

```scss
// 柔和背景渐变
$bg-base: #FAF7F9;             // 最浅的基础背景
$bg-secondary: rgba(255, 255, 255, 0.6);
$bg-card: rgba(255, 255, 255, 0.5);
$bg-card-hover: rgba(255, 255, 255, 0.7);
$bg-input: rgba(255, 255, 255, 0.6);
```

### 文字色系

```scss
// 文字色 - 深灰紫色系（保持柔和度）
$text-primary: #4A4458;        // 主要文字 - 深灰紫
$text-secondary: #6E6783;      // 次要文字
$text-muted: #9B93A8;          // 弱化文字
$text-placeholder: #B8B1C4;    // 占位符文字
$text-white: #FFFFFF;          // 白色文字
```

### 状态色

```scss
$success-color: #7DD3A8;       // 柔和绿
$warning-color: #FFD789;       // 柔和黄
$error-color: #F5A5A5;         // 柔和红
$info-color: #89C4E8;          // 柔和蓝
```

### 边框色

```scss
$border-color: rgba(183, 168, 214, 0.3);
$border-light: rgba(255, 255, 255, 0.4);
$border-focus: rgba($pink-primary, 0.5);
```

---

## ✨ 视觉元素

### 毛玻璃拟态 (Glassmorphism)

#### 基础毛玻璃样式
```scss
.glass-effect {
  background: rgba(255, 255, 255, 0.45);           // 半透明白色背景
  backdrop-filter: blur(20px);                    // 背景模糊
  -webkit-backdrop-filter: blur(20px);            // iOS 兼容
  border: 1px solid rgba(255, 255, 255, 0.5);     // 半透明边框
  border-radius: 16px;                           // 大圆角
  box-shadow: 0 4px 20px rgba(183, 168, 214, 0.2); // 柔和阴影
}
```

#### 重度毛玻璃样式
```scss
.glass-heavy {
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(183, 168, 214, 0.2);
}
```

### 网格渐变背景 (Mesh Gradient)

```scss
.mesh-gradient-bg {
  // 网格渐变背景 - 多个径向渐变叠加
  background:
    radial-gradient(ellipse at 20% 20%, rgba($pink-primary, 0.5) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 30%, rgba($baby-blue, 0.4) 0%, transparent 45%),
    radial-gradient(ellipse at 40% 80%, rgba($lavender, 0.5) 0%, transparent 50%),
    radial-gradient(ellipse at 90% 90%, rgba($pink-light, 0.3) 0%, transparent 40%),
    linear-gradient(180deg, #FDF7F9 0%, #F5F0F7 50%, #F0F7FB 100%);
}
```

### 弥散光斑动画

```scss
.light-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.7;
  animation: float 20s ease-in-out infinite;

  &--pink {
    background: rgba($pink-primary, 0.5);
  }

  &--lavender {
    background: rgba($lavender, 0.5);
  }

  &--blue {
    background: rgba($baby-blue, 0.5);
  }
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(30px, -30px) scale(1.05);
  }
  50% {
    transform: translate(-20px, 20px) scale(0.95);
  }
  75% {
    transform: translate(-30px, -20px) scale(1.02);
  }
}
```

---

## 🧩 组件规范

### 按钮设计

#### 主按钮 - 果冻质感
```scss
.btn-primary {
  background: $button-gradient;                    // 粉紫渐变
  border-radius: 50px;                            // 完全圆角
  box-shadow: 0 6px 20px rgba(183, 168, 214, 0.4), // 外阴影
              inset 0 2px 4px rgba(255, 255, 255, 0.8); // 内阴影高光
  color: white;
  font-weight: 500;
  padding: 14px 28px;
  position: relative;
  overflow: hidden;

  // 顶部高光效果
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 50%;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.25) 0%, transparent 100%);
    border-radius: 50px 50px 0 0;
  }

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 24px rgba(252, 174, 193, 0.35), inset 0 2px 4px rgba(255, 255, 255, 0.8);
  }

  &:active {
    transform: translateY(0) scale(0.98);
  }
}
```

#### 次要按钮 - 毛玻璃效果
```scss
.btn-secondary {
  background: $glass-bg-heavy;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 50px;
  color: $text-primary;
  box-shadow: 0 2px 12px rgba(183, 168, 214, 0.15);

  &:hover {
    background: rgba(255, 255, 255, 0.8);
    transform: translateY(-1px);
  }
}
```

### 卡片设计

```scss
.card {
  background: $glass-bg;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(183, 168, 214, 0.15);

  &:hover {
    background: $glass-bg-heavy;
    transform: translateY(-4px);
    box-shadow: 0 4px 20px rgba(183, 168, 214, 0.2);
  }
}
```

### 输入框设计

```scss
.input-field {
  width: 100%;
  padding: 16px 20px;
  background: $glass-bg-heavy;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 16px;
  color: $text-primary;
  font-size: 15px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);

  &:focus {
    border-color: rgba($pink-primary, 0.6);
    box-shadow: 0 0 0 4px rgba($pink-primary, 0.1);
    background: rgba(255, 255, 255, 0.75);
  }

  &::placeholder {
    color: $text-placeholder;
  }
}
```

### 头像设计

```scss
.avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  background: linear-gradient(135deg, $pink-light, $baby-blue);
  border: 2px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 2px 12px rgba(183, 168, 214, 0.15);

  &--sm { width: 32px; height: 32px; }
  &--lg { width: 56px; height: 56px; }
  &--xl { width: 80px; height: 80px; }
}
```

---

## 🎬 动画规范

### 动画时长与缓动函数

```scss
$transition-fast: 0.15s ease;
$transition-normal: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
$transition-slow: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
$transition-bounce: 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### 页面切换动画

```scss
.page-slide-enter-active,
.page-slide-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.page-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
```

### 交互动画

#### 悬停效果
```scss
.hover-lift {
  transition: all $transition-normal;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 28px rgba(183, 168, 214, 0.25);
  }
}

.hover-scale {
  transition: transform $transition-normal;

  &:hover {
    transform: scale(1.05);
  }
}
```

#### 点击反馈
```scss
.click-feedback {
  transition: transform $transition-fast;

  &:active {
    transform: scale(0.95);
  }
}
```

---

## 📐 布局规范

### 间距系统

```scss
$spacing-xs: 4px;
$spacing-sm: 8px;
$spacing-md: 16px;
$spacing-lg: 24px;
$spacing-xl: 32px;
$spacing-2xl: 48px;
```

### 圆角系统

```scss
$radius-sm: 12px;
$radius-md: 16px;
$radius-lg: 20px;
$radius-xl: 28px;
$radius-2xl: 36px;
$radius-full: 9999px;
```

### 手机模拟器尺寸

```scss
$phone-width: 393px;
$phone-height: 852px;
$phone-radius: 50px;
$navbar-height: 56px;
$tabbar-height: 65px;
$status-bar-height: 44px;
```

---

## 🔤 字体规范

### 字体族

```scss
$font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### 字号系统

```scss
$font-size-xs: 11px;
$font-size-sm: 13px;
$font-size-base: 15px;
$font-size-lg: 17px;
$font-size-xl: 20px;
$font-size-2xl: 24px;
$font-size-3xl: 32px;
```

### 字重

```scss
$font-weight-light: 300;
$font-weight-normal: 400;
$font-weight-medium: 500;
$font-weight-semibold: 600;
$font-weight-bold: 700;
```

---

## 🎯 使用指南

### 快速开始

1. **引入样式文件**
```scss
@import '@/assets/styles/variables.scss';
@import '@/assets/styles/global.scss';
```

2. **使用颜色变量**
```scss
.my-component {
  background-color: $glass-bg;
  color: $text-primary;
  border-color: $border-color;
}
```

3. **应用毛玻璃效果**
```html
<div class="glass-effect">
  <!-- 内容 -->
</div>
```

### 常用组合模式

#### 1. 标准页面布局
```html
<div class="app-container">
  <!-- 网格渐变背景 -->
  <div class="mesh-gradient-bg">
    <div class="light-blob light-blob--1"></div>
    <div class="light-blob light-blob--2"></div>
    <div class="light-blob light-blob--3"></div>
  </div>

  <!-- 手机模拟器 -->
  <PhoneSimulator>
    <!-- 页面内容 -->
  </PhoneSimulator>
</div>
```

#### 2. 毛玻璃卡片
```html
<div class="card glass-effect hover-lift">
  <h3 class="card-title">标题</h3>
  <p class="card-content">内容</p>
  <button class="btn-primary">操作按钮</button>
</div>
```

#### 3. 表单输入组
```html
<div class="input-wrapper">
  <div class="input-field glass-heavy"></div>
  <div class="input-wrapper glass-effect"></div>
</div>
```

### 交互最佳实践

#### 1. 按钮交互
- 主按钮使用果冻质感和渐变背景
- 次要按钮使用毛玻璃效果
- 悬停时轻微上浮或缩放
- 点击时缩放反馈

#### 2. 卡片交互
- 悬停时上浮并增强阴影
- 点击时轻微缩放
- 避免过于夸张的动画效果

#### 3. 页面切换
- 使用平滑的滑入滑出动画
- 保持动画时长在 0.3-0.5 秒之间
- 使用贝塞尔曲线实现自然的动画效果

### 性能优化建议

1. **毛玻璃效果优化**
   - 适度使用 `backdrop-filter`，避免过度渲染
   - 在低端设备上可降级为半透明背景

2. **动画性能**
   - 优先使用 `transform` 和 `opacity` 进行动画
   - 避免频繁改变 `width`、`height` 等布局属性

3. **背景优化**
   - 复杂背景考虑使用静态图片替代动态渐变
   - 限制同时动画的光斑数量

### 组件开发规范

#### 1. 命名规范
- 使用 BEM 命名规范
- 组件类名以组件名前缀开头
- 状态类名使用 `is-` 或 `has-` 前缀

#### 2. 响应式设计
- 所有组件必须适配手机模拟器尺寸
- 考虑横屏和小屏设备的显示效果

#### 3. 可访问性
- 确保颜色对比度符合 WCAG 标准
- 为交互元素提供适当的焦点样式
- 支持键盘导航

---

## 📚 参考资源

### 设计工具
- **Figma**: 建议使用设计系统建立组件库
- **Adobe Color**: 用于生成马卡龙色系配色方案

### 开发资源
- **CSS Variables**: 方便主题切换和定制
- **Sass/SCSS**: 用于变量和混合函数管理
- **Vue 3**: 响应式组件开发

### 灵感来源
- Dribbble 上的毛玻璃设计作品
- iOS 系统的毛玻璃效果
- Material Design 3 的动态色彩系统

---

## 🔄 版本历史

### v1.0.0 (当前版本)
- 建立基础设计系统
- 完善马卡龙色系规范
- 制定毛玻璃拟态组件标准

---

**最后更新**: 2025年12月18日
**维护者**: MomentsShare 前端团队

> 💡 **提示**: 这份文档会随着项目发展持续更新，请定期查看最新版本。