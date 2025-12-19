<template>
  <div class="not-found-page">
    <div class="error-content">
      <van-icon name="warn-o" class="error-icon" />
      <h1 class="error-code">404</h1>
      <p class="error-message">页面未找到</p>
      <router-link to="/home" class="btn btn--primary">
        返回首页
      </router-link>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.not-found-page {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $spacing-xl;
}

.error-content {
  text-align: center;
}

.error-icon {
  font-size: 64px;
  display: block;
  margin-bottom: $spacing-md;
}

.error-code {
  font-size: 72px;
  font-weight: $font-weight-bold;
  color: $text-primary;
  line-height: 1;
  margin-bottom: $spacing-sm;
}

.error-message {
  font-size: $font-size-lg;
  color: $text-secondary;
  margin-bottom: $spacing-xl;
}
</style>

