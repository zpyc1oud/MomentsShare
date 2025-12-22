<template>
  <div class="growth-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>用户增长趋势 (近30天)</span>
              <el-radio-group v-model="dateRange" size="small" @change="handleRangeChange">
                <el-radio-button label="7">7天</el-radio-button>
                <el-radio-button label="14">14天</el-radio-button>
                <el-radio-button label="30">30天</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div ref="growthChart" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>日活跃用户 (DAU) 趋势</span>
            </div>
          </template>
          <div ref="dauChart" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, onUnmounted } from 'vue'
import { init, use } from 'echarts/core'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components'
import { LineChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { statisticsAPI } from '@/api/admin'
import dayjs from 'dayjs'

use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  CanvasRenderer
])

const growthChart = ref()
const dauChart = ref()
let growthInstance = null
let dauInstance = null
const dateRange = ref('30')

const initCharts = () => {
  if (growthChart.value) {
    growthInstance = init(growthChart.value)
  }
  if (dauChart.value) {
    dauInstance = init(dauChart.value)
  }
}

const fetchAndRender = async () => {
  try {
    const days = parseInt(dateRange.value)
    const data = await statisticsAPI.getAllStats(days)
    const dailyStats = data.daily_stats || data
    
    // 准备数据
    const dates = dailyStats.map(item => dayjs(item.date).format('MM-DD'))
    const newUsers = dailyStats.map(item => item.daily_new_users)
    const dau = dailyStats.map(item => item.dau)

    // 渲染增长图表
    const growthOption = {
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['新增用户']
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: dates
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '新增用户',
          type: 'line',
          smooth: true,
          data: newUsers,
          itemStyle: { color: '#409EFF' },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [{ offset: 0, color: 'rgba(64,158,255,0.5)' }, { offset: 1, color: 'rgba(64,158,255,0.1)' }]
            }
          }
        }
      ]
    }
    growthInstance?.setOption(growthOption)

    // 渲染DAU图表
    const dauOption = {
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['日活跃用户']
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: dates
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '日活跃用户',
          type: 'line',
          smooth: true,
          data: dau,
          itemStyle: { color: '#67C23A' },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [{ offset: 0, color: 'rgba(103,194,58,0.5)' }, { offset: 1, color: 'rgba(103,194,58,0.1)' }]
            }
          }
        }
      ]
    }
    dauInstance?.setOption(dauOption)

  } catch (error) {
    console.error('获取统计数据失败', error)
  }
}

const handleRangeChange = () => {
  fetchAndRender()
}

const handleResize = () => {
  growthInstance?.resize()
  dauInstance?.resize()
}

onMounted(() => {
  nextTick(() => {
    initCharts()
    fetchAndRender()
    window.addEventListener('resize', handleResize)
  })
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  growthInstance?.dispose()
  dauInstance?.dispose()
})
</script>

<style scoped>
.growth-container {
  padding: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart {
  height: 350px;
  width: 100%;
}
</style>
