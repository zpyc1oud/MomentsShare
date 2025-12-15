// ECharts基础配置
export const baseChartOptions = {
  backgroundColor: 'transparent',
  textStyle: {
    fontFamily: 'Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial, sans-serif'
  },
  grid: {
    containLabel: true,
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '15%'
  },
  tooltip: {
    backgroundColor: 'rgba(50, 50, 50, 0.9)',
    borderColor: 'transparent',
    textStyle: {
      color: '#fff'
    },
    extraCssText: 'border-radius: 6px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);'
  }
}

// 用户增长趋势图配置
export const userTrendChartOptions = {
  title: {
    text: '近7日新增用户趋势',
    left: 'left',
    textStyle: {
      fontSize: 16,
      fontWeight: 'normal',
      color: '#303133'
    }
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'line',
      lineStyle: {
        color: '#409EFF',
        width: 1
      }
    },
    formatter: function(params) {
      const data = params[0]
      return `${data.axisValue}<br/>新增用户: <span style="color: #409EFF; font-weight: bold;">${data.value}</span> 人`
    }
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    axisLine: {
      lineStyle: {
        color: '#DCDFE6'
      }
    },
    axisLabel: {
      color: '#606266',
      fontSize: 12
    }
  },
  yAxis: {
    type: 'value',
    axisLine: {
      show: false
    },
    axisTick: {
      show: false
    },
    axisLabel: {
      color: '#606266',
      fontSize: 12
    },
    splitLine: {
      lineStyle: {
        color: '#EBEEF5',
        type: 'dashed'
      }
    }
  },
  series: [
    {
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: {
        color: '#409EFF',
        width: 3
      },
      itemStyle: {
        color: '#409EFF',
        borderColor: '#fff',
        borderWidth: 2
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(64, 158, 255, 0.4)' },
            { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
          ]
        }
      },
      data: []
    }
  ]
}

// DAU曲线图配置
export const dauChartOptions = {
  title: {
    text: '日活跃用户(DAU)曲线',
    left: 'left',
    textStyle: {
      fontSize: 16,
      fontWeight: 'normal',
      color: '#303133'
    }
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'line',
      lineStyle: {
        color: '#67C23A',
        width: 1
      }
    },
    formatter: function(params) {
      const data = params[0]
      return `${data.axisValue}<br/>日活用户: <span style="color: #67C23A; font-weight: bold;">${data.value}</span> 人`
    }
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    axisLine: {
      lineStyle: {
        color: '#DCDFE6'
      }
    },
    axisLabel: {
      color: '#606266',
      fontSize: 12
    }
  },
  yAxis: {
    type: 'value',
    axisLine: {
      show: false
    },
    axisTick: {
      show: false
    },
    axisLabel: {
      color: '#606266',
      fontSize: 12
    },
    splitLine: {
      lineStyle: {
        color: '#EBEEF5',
        type: 'dashed'
      }
    }
  },
  series: [
    {
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: {
        color: '#67C23A',
        width: 3
      },
      itemStyle: {
        color: '#67C23A',
        borderColor: '#fff',
        borderWidth: 2
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(103, 194, 58, 0.4)' },
            { offset: 1, color: 'rgba(103, 194, 58, 0.05)' }
          ]
        }
      },
      data: []
    }
  ]
}

// 内容类型分布饼图配置
export const contentDistributionChartOptions = {
  title: {
    text: '内容类型分布',
    left: 'left',
    textStyle: {
      fontSize: 16,
      fontWeight: 'normal',
      color: '#303133'
    }
  },
  tooltip: {
    trigger: 'item',
    formatter: function(params) {
      const percent = params.percent
      return `${params.name}<br/>数量: <span style="font-weight: bold;">${params.value}</span> (${percent}%)`
    }
  },
  legend: {
    orient: 'horizontal',
    bottom: '5%',
    left: 'center',
    itemGap: 20,
    textStyle: {
      color: '#606266',
      fontSize: 12
    }
  },
  series: [
    {
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 6,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold',
          color: '#303133'
        },
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      },
      labelLine: {
        show: false
      },
      data: []
    }
  ]
}

// 饼图默认颜色
export const pieChartColors = [
  '#409EFF', // 蓝色
  '#67C23A', // 绿色
  '#E6A23C', // 橙色
  '#F56C6C', // 红色
  '#909399', // 灰色
  '#B37FEB', // 紫色
  '#F7BA2A', // 黄色
  '#FF7F7F'  // 浅红色
]

// 图表响应式配置
export const responsiveOptions = {
  grid: {
    containLabel: true,
    left: '3%',
    right: '4%',
    bottom: '10%',
    top: '20%'
  }
}

// 格式化日期
export const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getMonth() + 1}-${date.getDate().toString().padStart(2, '0')}`
}

// 格式化数字
export const formatNumber = (num) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}