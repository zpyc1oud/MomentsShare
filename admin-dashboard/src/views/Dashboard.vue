<template>
  <div class="dashboard">
    <!-- 数据概览卡片 -->
    <el-row :gutter="20" class="overview-cards">
      <el-col :span="6" v-for="(card, index) in overviewCards" :key="index">
        <el-card class="overview-card" :body-style="{ padding: '20px' }">
          <div class="card-content">
            <div class="card-icon" :style="{ backgroundColor: card.color }">
              <el-icon :size="24"><component :is="card.icon" /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">{{ card.title }}</div>
              <div class="card-value">{{ card.value }}</div>
              <div class="card-trend" :class="card.trend.type">
                <el-icon><component :is="card.trend.icon" /></el-icon>
                <span>{{ card.trend.text }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-section">
      <!-- 近7日新增用户趋势图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <div ref="userTrendChart" class="chart"></div>
        </el-card>
      </el-col>

      <!-- DAU曲线图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <div ref="dauChart" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 内容类型分布 -->
    <el-row :gutter="20" class="chart-section">
      <el-col :span="12">
        <el-card class="chart-card">
          <div ref="contentDistributionChart" class="chart"></div>
        </el-card>
      </el-col>

      <!-- 实时动态 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>实时动态</span>
              <el-button type="text" @click="refreshMoments">
                <el-icon><Refresh /></el-icon>
              </el-button>
            </div>
          </template>
          <div class="moments-list">
            <div
              v-for="moment in recentMoments"
              :key="moment.id"
              class="moment-item"
            >
              <div class="moment-avatar">
                <el-avatar :size="32">{{ moment.user.charAt(0) }}</el-avatar>
              </div>
              <div class="moment-content">
                <div class="moment-user">{{ moment.user }}</div>
                <div class="moment-text">{{ moment.content }}</div>
                <div class="moment-time">{{ moment.time }}</div>
              </div>
              <div class="moment-action">
                <el-button
                  type="danger"
                  size="small"
                  text
                  @click="deleteMoment(moment.id)"
                >
                  删除
                </el-button>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { init, use } from 'echarts/core'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components'
import { LineChart, PieChart } from 'echarts/charts'
import {
  CanvasRenderer
} from 'echarts/renderers'

// 注册必要组件
use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  PieChart,
  CanvasRenderer
])
import {
  User,
  TrendCharts,
  Document,
  ChatDotRound,
  ArrowUp,
  ArrowDown,
  Minus,
  Refresh
} from '@element-plus/icons-vue'
import { statisticsAPI, contentAPI } from '@/api/admin'
import {
  userTrendChartOptions,
  dauChartOptions,
  contentDistributionChartOptions,
  pieChartColors,
  formatDate,
  formatNumber
} from '@/utils/charts'

// 图表实例
const userTrendChart = ref()
const dauChart = ref()
const contentDistributionChart = ref()

let userTrendInstance = null
let dauInstance = null
let contentDistributionInstance = null

// 数据概览卡片
const overviewCards = reactive([
  {
    title: '今日新增用户',
    value: '0',
    icon: 'User',
    color: '#87CEEB', // 天空蓝 - 马卡龙色系
    trend: {
      type: 'up',
      icon: 'ArrowUp',
      text: '+12.5%'
    }
  },
  {
    title: '今日活跃用户',
    value: '0',
    icon: 'TrendCharts',
    color: '#99D98C', // 清新绿色
    trend: {
      type: 'up',
      icon: 'ArrowUp',
      text: '+8.3%'
    }
  },
  {
    title: '今日发布动态',
    value: '0',
    icon: 'Document',
    color: '#DDA0DD', // 梅花紫 - 马卡龙色系
    trend: {
      type: 'down',
      icon: 'ArrowDown',
      text: '-3.2%'
    }
  },
  {
    title: '今日评论互动',
    value: '0',
    icon: 'ChatDotRound',
    color: '#FFB6C1', // 樱花粉 - 马卡龙色系
    trend: {
      type: 'flat',
      icon: 'Minus',
      text: '0%'
    }
  }
])

// 最近动态 - 从API获取真实数据
const recentMoments = ref([])

// 获取基础统计数据
const fetchBasicStats = async () => {
  try {
    const statsData = await statisticsAPI.getAllStats()

    if (statsData && statsData.daily_stats && statsData.daily_stats.length > 0) {
      // 使用今天的数据（数组最后一个元素）
      const todayData = statsData.daily_stats[statsData.daily_stats.length - 1]

      // 更新概览卡片数据
      overviewCards[0].value = formatNumber(todayData.daily_new_users || 0)
      overviewCards[1].value = formatNumber(todayData.dau || 0)
      overviewCards[2].value = formatNumber(todayData.daily_posts || 0)

      // 获取真实的评论数（从内容列表API）
      try {
        const contentData = await contentAPI.getList({ limit: 100 })
        const totalComments = contentData.results ? contentData.results.reduce((sum, item) => sum + (item.comments_count || 0), 0) : 0
        overviewCards[3].value = formatNumber(totalComments)
      } catch (commentError) {
        console.warn('获取评论数失败，使用估算值:', commentError)
        overviewCards[3].value = formatNumber(todayData.daily_posts || 0)
      }

      console.log('基础统计数据加载成功:', todayData)
    }
  } catch (error) {
    console.error('获取基础统计数据失败:', error)
  }
}

// 获取用户增长趋势数据
const fetchUserTrend = async () => {
  try {
    const data = await statisticsAPI.getUserTrend()

    if (data && data.length > 0) {
      const dates = data.map(item => formatDate(item.date))
      const values = data.map(item => item.count)

      const options = {
        ...userTrendChartOptions,
        xAxis: {
          ...userTrendChartOptions.xAxis,
          data: dates
        },
        series: [
          {
            ...userTrendChartOptions.series[0],
            data: values
          }
        ]
      }

      userTrendInstance.setOption(options)
    }
  } catch (error) {
    console.error('获取用户增长趋势数据失败:', error)
  }
}

// 获取DAU趋势数据
const fetchDAUTrend = async () => {
  try {
    const data = await statisticsAPI.getDAUTrend()

    if (data && data.length > 0) {
      const dates = data.map(item => formatDate(item.date))
      const values = data.map(item => item.count)

      const options = {
        ...dauChartOptions,
        xAxis: {
          ...dauChartOptions.xAxis,
          data: dates
        },
        series: [
          {
            ...dauChartOptions.series[0],
            data: values
          }
        ]
      }

      dauInstance.setOption(options)
    }
  } catch (error) {
    console.error('获取DAU趋势数据失败:', error)
  }
}

// 获取内容类型分布数据
const fetchContentDistribution = async () => {
  try {
    const data = await statisticsAPI.getContentDistribution()

    if (data && data.length > 0) {
      const formattedData = data.map((item, index) => ({
        name: item.type,
        value: item.count,
        itemStyle: {
          color: pieChartColors[index % pieChartColors.length]
        }
      }))

      const options = {
        ...contentDistributionChartOptions,
        series: [
          {
            ...contentDistributionChartOptions.series[0],
            data: formattedData
          }
        ]
      }

      contentDistributionInstance.setOption(options)
    }
  } catch (error) {
    console.error('获取内容类型分布数据失败:', error)
  }
}

// 初始化图表
const initCharts = () => {
  nextTick(() => {
    console.log('开始初始化图表...')

    // 初始化用户增长趋势图
    if (userTrendChart.value) {
      console.log('初始化用户增长趋势图')
      userTrendInstance = init(userTrendChart.value)
      userTrendInstance.setOption(userTrendChartOptions)
    } else {
      console.error('用户增长趋势图容器未找到')
    }

    // 初始化DAU曲线图
    if (dauChart.value) {
      console.log('初始化DAU曲线图')
      dauInstance = init(dauChart.value)
      dauInstance.setOption(dauChartOptions)
    } else {
      console.error('DAU曲线图容器未找到')
    }

    // 初始化内容类型分布图
    if (contentDistributionChart.value) {
      console.log('初始化内容类型分布图')
      contentDistributionInstance = init(contentDistributionChart.value)
      contentDistributionInstance.setOption(contentDistributionChartOptions)
    } else {
      console.error('内容类型分布图容器未找到')
    }

    // 添加窗口大小变化监听
    window.addEventListener('resize', handleResize)
    console.log('图表初始化完成')
  })
}

// 处理窗口大小变化
const handleResize = () => {
  userTrendInstance?.resize()
  dauInstance?.resize()
  contentDistributionInstance?.resize()
}

// 获取最近动态数据
const fetchRecentMoments = async () => {
  try {
    const data = await contentAPI.getList({ limit: 10 })

    console.log('API返回的原始数据:', data)
    console.log('数据类型:', typeof data)
    console.log('是否为数组:', Array.isArray(data))

    // 确保数据是数组格式
    let momentsData = []
    if (Array.isArray(data)) {
      momentsData = data
    } else if (data && data.results && Array.isArray(data.results)) {
      momentsData = data.results
    } else if (data && data.data && Array.isArray(data.data)) {
      momentsData = data.data
    } else if (data && typeof data === 'object') {
      // 如果是分页格式，尝试获取常见的分页字段
      momentsData = data.items || data.list || data.results || data.data || []
    } else {
      console.warn('无法识别的数据格式:', data)
      momentsData = []
    }

    console.log('处理后的动态数据:', momentsData)

    // 转换数据格式以匹配模板
    recentMoments.value = momentsData.map(item => ({
      id: item.id,
      user: item.author?.nickname || item.author?.username || '用户' + item.id,
      content: item.text || (item.images && item.images.length > 0 ? '[图片动态]' : '[文字动态]'),
      time: formatTimeAgo(item.created_at)
    }))

    console.log('最近动态数据加载成功:', recentMoments.value)
  } catch (error) {
    console.error('获取最近动态失败:', error)
    console.error('错误详情:', error.message)
    console.error('错误堆栈:', error.stack)
    // 如果API失败，保持空数组
  }
}

// 格式化时间（X分钟前、X小时前等）
const formatTimeAgo = (dateString) => {
  const now = new Date()
  const date = new Date(dateString)
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return '刚刚'
  if (diffMins < 60) return `${diffMins}分钟前`
  if (diffHours < 24) return `${diffHours}小时前`
  if (diffDays < 7) return `${diffDays}天前`
  return date.toLocaleDateString('zh-CN')
}

// 刷新动态列表
const refreshMoments = async () => {
  try {
    await fetchRecentMoments()
    ElMessage.success('动态列表已刷新')
  } catch (error) {
    console.error('刷新动态失败:', error)
  }
}

// 删除动态
const deleteMoment = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这条动态吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await contentAPI.delete(id)
    ElMessage.success('删除成功')

    // 重新获取动态列表
    refreshMoments()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除动态失败:', error)
    }
  }
}

// 加载所有数据
const loadAllData = async () => {
  try {
    await Promise.all([
      fetchBasicStats(),
      fetchUserTrend(),
      fetchDAUTrend(),
      fetchContentDistribution(),
      fetchRecentMoments()
    ])
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

// 模拟数据（用于演示）
const loadMockData = () => {
  console.log('开始加载模拟数据...')
  console.log('userTrendInstance:', userTrendInstance)
  console.log('dauInstance:', dauInstance)
  console.log('contentDistributionInstance:', contentDistributionInstance)

  // 模拟用户增长趋势数据
  const mockUserTrendData = [
    { date: '2024-01-11', count: 120 },
    { date: '2024-01-12', count: 85 },
    { date: '2024-01-13', count: 156 },
    { date: '2024-01-14', count: 98 },
    { date: '2024-01-15', count: 201 },
    { date: '2024-01-16', count: 134 },
    { date: '2024-01-17', count: 178 }
  ]

  const dates = mockUserTrendData.map(item => formatDate(item.date))
  const userValues = mockUserTrendData.map(item => item.count)

  if (userTrendInstance) {
    const userOptions = {
      ...userTrendChartOptions,
      xAxis: {
        ...userTrendChartOptions.xAxis,
        data: dates
      },
      series: [
        {
          ...userTrendChartOptions.series[0],
          data: userValues
        }
      ]
    }
    userTrendInstance.setOption(userOptions)
    console.log('用户趋势图数据设置完成')
  } else {
    console.error('用户趋势图实例未创建')
  }

  // 模拟DAU数据
  const mockDAUData = [1234, 1456, 1678, 1890, 1567, 1789, 2012]
  if (dauInstance) {
    const dauOptions = {
      ...dauChartOptions,
      xAxis: {
        ...dauChartOptions.xAxis,
        data: dates
      },
      series: [
        {
          ...dauChartOptions.series[0],
          data: mockDAUData
        }
      ]
    }
    dauInstance.setOption(dauOptions)
    console.log('DAU图数据设置完成')
  } else {
    console.error('DAU图实例未创建')
  }

  // 模拟内容类型分布数据
  const mockContentData = [
    { name: '图文动态', value: 1234 },
    { name: '视频动态', value: 567 },
    { name: '纯文字', value: 234 },
    { name: '转发', value: 189 }
  ]

  const formattedContentData = mockContentData.map((item, index) => ({
    name: item.name,
    value: item.value,
    itemStyle: {
      color: pieChartColors[index % pieChartColors.length]
    }
  }))

  if (contentDistributionInstance) {
    const contentOptions = {
      ...contentDistributionChartOptions,
      series: [
        {
          ...contentDistributionChartOptions.series[0],
          data: formattedContentData
        }
      ]
    }
    contentDistributionInstance.setOption(contentOptions)
    console.log('内容分布图数据设置完成')
  } else {
    console.error('内容分布图实例未创建')
  }

  // 更新概览卡片数据
  overviewCards[0].value = '178'
  overviewCards[1].value = '2,012'
  overviewCards[2].value = '89'
  overviewCards[3].value = '234'
}

onMounted(() => {
  console.log('Dashboard组件已挂载')
  console.log('用户增长趋势图ref:', userTrendChart.value)
  console.log('DAU图ref:', dauChart.value)
  console.log('内容分布图ref:', contentDistributionChart.value)

  // 添加延迟确保DOM完全渲染
  setTimeout(() => {
    initCharts()

    // 再等一下确保图表实例创建完成，然后加载数据
    setTimeout(() => {
      console.log('开始加载数据...')
      console.log('userTrendInstance:', userTrendInstance)
      console.log('dauInstance:', dauInstance)
      console.log('contentDistributionInstance:', contentDistributionInstance)

      // loadMockData() // 使用模拟数据进行演示
      loadAllData() // 真实环境使用这个
    }, 200)
  }, 100)
})

onUnmounted(() => {
  // 清理图表实例
  userTrendInstance?.dispose()
  dauInstance?.dispose()
  contentDistributionInstance?.dispose()

  // 移除事件监听
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.dashboard {
  max-width: 1600px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* 概览卡片样式 */
.overview-cards {
  margin-bottom: 20px;
}

.overview-card {
  height: 120px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
  transition: all var(--transition-normal);
  overflow: hidden;
  position: relative;
}

.overview-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--primary-gradient);
}

.overview-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  background: rgba(255, 255, 255, 0.95);
}

.card-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 16px;
  box-shadow: var(--shadow-md);
  backdrop-filter: var(--glass-blur);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.card-info {
  flex: 1;
}

.card-title {
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 8px;
  font-weight: 500;
}

.card-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-trend {
  display: flex;
  align-items: center;
  font-size: 14px;
  font-weight: 600;
}

.card-trend.up {
  color: var(--success-color);
}

.card-trend.down {
  color: #ff595e;
  font-weight: 700;
}

.card-trend.flat {
  color: #888888;
}

.card-trend .el-icon {
  margin-right: 4px;
}

/* 图表区域样式 */
.chart-section {
  margin-bottom: 20px;
}

.chart-card {
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  transition: all var(--transition-normal);
}

.chart-card:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.7);
  border-bottom: 1px solid var(--border-color);
  padding: 16px 20px;
}

.chart {
  height: 320px;
  width: 100%;
  min-height: 320px;
}

/* 动态列表样式 */
.moments-list {
  max-height: 280px;
  overflow-y: auto;
}

.moment-item {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
  background: rgba(255, 255, 255, 0.85);
  margin: 8px;
  border-radius: 16px;
  transition: all var(--transition-normal);
  backdrop-filter: blur(20px);
}

.moment-item:last-child {
  border-bottom: none;
}

.moment-item:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateX(4px);
  box-shadow: var(--shadow-md);
}

.moment-avatar {
  margin-right: 12px;
  flex-shrink: 0;
}

.moment-content {
  flex: 1;
  min-width: 0;
}

.moment-user {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
  background: var(--primary-gradient-soft);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.moment-text {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 6px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.4;
}

.moment-time {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
}

.moment-action {
  flex-shrink: 0;
  margin-left: 8px;
}

/* 滚动条样式 */
.moments-list::-webkit-scrollbar {
  width: 8px;
}

.moments-list::-webkit-scrollbar-thumb {
  background: var(--primary-gradient);
  border-radius: 6px;
  border: 2px solid rgba(255, 255, 255, 0.9);
}

.moments-list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.7);
  border-radius: 6px;
  border: 1px solid var(--border-color);
}

.moments-list::-webkit-scrollbar-thumb:hover {
  background: var(--button-gradient);
}

:deep(.el-card__body) {
  padding: 20px;
}
</style>