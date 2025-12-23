<template>
  <div class="moments-container">
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="用户ID">
          <el-input v-model="filterForm.user_id" placeholder="请输入用户ID" clearable />
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
        
        <el-table-column label="发布者" width="180">
          <template #default="{ row }">
            <div class="user-info">
              <el-avatar :size="30" :src="row.author.avatar" />
              <span class="nickname">{{ row.author.nickname }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="内容预览" min-width="300">
          <template #default="{ row }">
            <div class="content-preview">
              <p class="content-text">{{ row.content }}</p>
              <div v-if="row.images && row.images.length" class="media-list">
                <el-image
                  v-for="(img, index) in row.images.slice(0, 3)"
                  :key="index"
                  :src="img.image_file"
                  :preview-src-list="row.images.map(i => i.image_file)"
                  class="preview-img"
                  fit="cover"
                  preview-teleported
                />
                <span v-if="row.images.length > 3" class="more-count">+{{ row.images.length - 3 }}</span>
              </div>
              <div v-if="row.video_file" class="video-preview">
                <el-tag type="info">视频动态</el-tag>
                <a :href="row.video_file" target="_blank" class="video-link">查看视频</a>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="created_at" label="发布时间" width="180" align="center">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>

        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.is_deleted" type="danger">已下架</el-tag>
            <el-tag v-else type="success">正常</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="120" align="center" fixed="right">
          <template #default="{ row }">
            <el-popconfirm
              v-if="!row.is_deleted"
              title="确定要强制下架这条内容吗？"
              confirm-button-text="确定"
              cancel-button-text="取消"
              @confirm="handleDelete(row)"
            >
              <template #reference>
                <el-button type="danger" size="small" link>强制下架</el-button>
              </template>
            </el-popconfirm>
            <span v-else class="text-gray">不可操作</span>
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
import { contentAPI } from '@/api/admin'
import dayjs from 'dayjs'

const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

const filterForm = reactive({
  user_id: ''
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
      user_id: filterForm.user_id || undefined
    }
    const res = await contentAPI.getList(params)
    tableData.value = res.results
    total.value = res.count
  } catch (error) {
    console.error('获取内容列表失败', error)
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
    await contentAPI.delete(row.id)
    ElMessage.success('下架成功')
    // 更新本地状态或重新加载
    row.is_deleted = true
  } catch (error) {
    console.error('下架失败', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.moments-container {
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

.content-preview {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.content-text {
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.media-list {
  display: flex;
  gap: 5px;
}

.preview-img {
  width: 60px;
  height: 60px;
  border-radius: 4px;
  cursor: pointer;
}

.more-count {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background: #f5f7fa;
  color: #909399;
  border-radius: 4px;
  font-size: 12px;
}

.video-link {
  color: #409eff;
  text-decoration: none;
  font-size: 12px;
  margin-left: 8px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.text-gray {
  color: #909399;
  font-size: 12px;
}
</style>
