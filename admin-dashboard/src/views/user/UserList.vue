<template>
  <div class="user-list-container">
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="搜索用户">
          <el-input v-model="filterForm.search" placeholder="手机号/昵称" clearable @keyup.enter="handleSearch" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <el-table
        v-loading="loading"
        :data="tableData"
        style="width: 100%"
        border
      >
        <el-table-column prop="id" label="ID" width="80" align="center" />
        
        <el-table-column label="用户信息" min-width="200">
          <template #default="{ row }">
            <div class="user-info">
              <el-avatar :size="40" :src="row.avatar" />
              <div class="user-detail">
                <div class="nickname">{{ row.nickname }}</div>
                <div class="username">@{{ row.username }}</div>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="phone" label="手机号" width="150" align="center" />

        <el-table-column prop="created_at" label="注册时间" width="180" align="center">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>

        <el-table-column label="角色" width="100" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.is_staff" type="warning">管理员</el-tag>
            <el-tag v-else type="info">普通用户</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.is_active" type="success">正常</el-tag>
            <el-tag v-else type="danger">已封禁</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="{ row }">
            <el-popconfirm
              :title="row.is_active ? '确定要封禁该用户吗？' : '确定要解封该用户吗？'"
              confirm-button-text="确定"
              cancel-button-text="取消"
              @confirm="handleToggleStatus(row)"
            >
              <template #reference>
                <el-button 
                  :type="row.is_active ? 'danger' : 'success'" 
                  size="small"
                  :disabled="row.is_staff"
                >
                  {{ row.is_active ? '封禁' : '解封' }}
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { userAPI } from '@/api/admin'
import dayjs from 'dayjs'

const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

const filterForm = reactive({
  search: ''
})

const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: filterForm.search || undefined
    }
    const res = await userAPI.getList(params)
    tableData.value = res.results
    total.value = res.count
  } catch (error) {
    console.error('获取用户列表失败', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchData()
}

const resetFilter = () => {
  filterForm.search = ''
  handleSearch()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchData()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchData()
}

const handleToggleStatus = async (row) => {
  try {
    const res = await userAPI.toggleStatus(row.id)
    ElMessage.success(res.detail)
    // 更新本地状态
    row.is_active = res.is_active
  } catch (error) {
    console.error('操作失败', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.user-list-container {
  padding: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-detail {
  display: flex;
  flex-direction: column;
}

.nickname {
  font-weight: 500;
  font-size: 14px;
}

.username {
  color: #909399;
  font-size: 12px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
