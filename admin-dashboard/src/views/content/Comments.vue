<template>
  <div class="comments-container">
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="用户ID">
          <el-input v-model="filterForm.user_id" placeholder="请输入用户ID" clearable />
        </el-form-item>
        <el-form-item label="动态ID">
          <el-input v-model="filterForm.moment_id" placeholder="请输入动态ID" clearable />
        </el-form-item>
        <el-form-item label="关键词">
          <el-input v-model="filterForm.keyword" placeholder="搜索评论内容" clearable />
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
        
        <el-table-column label="评论者" width="180">
          <template #default="{ row }">
            <div class="user-info">
              <el-avatar :size="30" :src="row.author_avatar" />
              <span class="nickname">{{ row.author_name }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="content" label="评论内容" min-width="300" />

        <el-table-column label="所属动态" min-width="200">
          <template #default="{ row }">
            <div class="moment-info">
              <span class="moment-id">#{{ row.moment_id }}</span>
              <span class="moment-text">{{ row.moment_text || '无文本内容' }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="created_at" label="评论时间" width="180" align="center">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="120" align="center" fixed="right">
          <template #default="{ row }">
            <el-popconfirm
              title="确定要删除这条评论吗？"
              confirm-button-text="确定"
              cancel-button-text="取消"
              @confirm="handleDelete(row)"
            >
              <template #reference>
                <el-button type="danger" size="small" link>删除</el-button>
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
import { commentAPI } from '@/api/admin'
import dayjs from 'dayjs'

const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

const filterForm = reactive({
  user_id: '',
  moment_id: '',
  keyword: ''
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
      user_id: filterForm.user_id || undefined,
      moment_id: filterForm.moment_id || undefined,
      keyword: filterForm.keyword || undefined
    }
    const res = await commentAPI.getList(params)
    tableData.value = res.results
    total.value = res.count
  } catch (error) {
    console.error('获取评论列表失败', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchData()
}

const resetFilter = () => {
  filterForm.user_id = ''
  filterForm.moment_id = ''
  filterForm.keyword = ''
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

const handleDelete = async (row) => {
  try {
    await commentAPI.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    console.error('删除失败', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.comments-container {
  padding: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.moment-info {
  display: flex;
  flex-direction: column;
  font-size: 12px;
}

.moment-id {
  color: #409eff;
  font-weight: bold;
}

.moment-text {
  color: #606266;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
