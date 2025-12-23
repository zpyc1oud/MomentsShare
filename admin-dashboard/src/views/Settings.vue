<template>
  <div class="settings-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <span>系统信息</span>
            </div>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="系统名称">MomentsShare 管理后台</el-descriptions-item>
            <el-descriptions-item label="版本号">v1.0.0</el-descriptions-item>
            <el-descriptions-item label="开发团队">MomentsShare Team</el-descriptions-item>
            <el-descriptions-item label="当前环境">Production</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>



</script>

<style scoped>
.settings-container {
  padding: 20px;
}
.settings-card {
  margin-bottom: 20px;
}
</style>
