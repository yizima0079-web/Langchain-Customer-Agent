<template>
  <div class="dashboard">
    <!-- KPI 指标卡片 -->
    <el-row :gutter="16">
      <el-col v-for="card in kpiCards" :key="card.label" :span="6">
        <el-card :class="['kpi-card', card.tone]" shadow="hover">
          <div class="kpi-top"><span>{{ card.icon }}</span><small>{{ card.label }}</small></div>
          <div class="kpi-value">{{ card.value }}</div>
          <div class="kpi-foot">实时业务概览 <i>↗</i></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 销售趋势 + 订单状态 -->
    <el-row :gutter="16" class="chart-row">
      <el-col :span="16">
        <el-card shadow="never">
          <template #header>近 7 天销售趋势</template>
          <div ref="trendRef" class="chart"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never">
          <template #header>订单状态分布</template>
          <div ref="statusRef" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 分类销量 -->
    <el-row :gutter="16" class="chart-row">
      <el-col :span="24">
        <el-card shadow="never">
          <template #header>分类销量占比</template>
          <div ref="categoryRef" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import * as echarts from 'echarts'
import { getCategoryStats, getOrderStatus, getSalesTrend, getStatsOverview } from '@/api'

const overview = ref({})
const trendRef = ref(null)
const statusRef = ref(null)
const categoryRef = ref(null)

// 已创建的图表实例，用于统一 resize/dispose
const charts = []

/** KPI 卡片数据 */
const kpiCards = computed(() => [
  { label: '注册用户', value: overview.value.user_count ?? 0, icon: '◉', tone: 'blue' },
  { label: '在售商品', value: overview.value.product_count ?? 0, icon: '◇', tone: 'purple' },
  { label: '订单总数', value: overview.value.order_count ?? 0, icon: '↗', tone: 'orange' },
  { label: '累计销售额(元)', value: overview.value.total_sales ?? 0, icon: '¥', tone: 'green' },
])

/** 初始化一个图表实例 */
function initChart(el, option) {
  const chart = echarts.init(el)
  chart.setOption(option)
  charts.push(chart)
  return chart
}

/** 加载所有统计数据并渲染图表 */
async function loadData() {
  const [overviewData, trend, status, category] = await Promise.all([
    getStatsOverview(), getSalesTrend(), getOrderStatus(), getCategoryStats(),
  ])
  overview.value = overviewData

  // 销售趋势：折线(销售额) + 柱状(订单数)
  initChart(trendRef.value, {
    tooltip: { trigger: 'axis' },
    legend: { data: ['销售额', '订单数'] },
    grid: { left: 50, right: 50, top: 40, bottom: 30 },
    xAxis: { type: 'category', data: trend.map((i) => i.date) },
    yAxis: [
      { type: 'value', name: '销售额' },
      { type: 'value', name: '订单数' },
    ],
    series: [
      { name: '销售额', type: 'line', smooth: true, data: trend.map((i) => i.sales) },
      { name: '订单数', type: 'bar', yAxisIndex: 1, data: trend.map((i) => i.orders) },
    ],
  })

  // 订单状态分布：饼图
  initChart(statusRef.value, {
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    legend: { bottom: 0 },
    series: [{ type: 'pie', radius: ['40%', '65%'], data: status }],
  })

  // 分类销量：柱状图
  initChart(categoryRef.value, {
    tooltip: { trigger: 'axis' },
    grid: { left: 50, right: 30, top: 30, bottom: 30 },
    xAxis: { type: 'category', data: category.map((i) => i.name) },
    yAxis: { type: 'value', name: '销量' },
    series: [{ type: 'bar', data: category.map((i) => i.value), barMaxWidth: 48 }],
  })
}

/** 窗口尺寸变化时重绘 */
function resizeAll() {
  charts.forEach((c) => c.resize())
}

onMounted(() => {
  loadData()
  window.addEventListener('resize', resizeAll)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeAll)
  charts.forEach((c) => c.dispose())
})
</script>

<style scoped>
.kpi-card {
  position: relative;
  overflow: hidden;
  min-height: 148px;
  border: 0 !important;
}
.kpi-card::after { content: ''; position: absolute; right: -28px; bottom: -34px; width: 105px; height: 105px; border: 18px solid currentColor; border-radius: 50%; opacity: .13; }
.kpi-top { display: flex; align-items: center; gap: 9px; }
.kpi-top span { display: grid; place-items: center; width: 28px; height: 28px; border: 1px solid currentColor; border-radius: 9px; color: currentColor; font-size: 17px; background: rgba(255,255,255,.78); box-shadow: 0 3px 8px rgba(35, 61, 108, .08); }
.kpi-top small { color: #7d8aa0; font-size: 12px; }
.kpi-card.blue { color: #2868df; background: linear-gradient(135deg, #dceaff 0%, #f5f9ff 72%, #fff 100%); }
.kpi-card.purple { color: #7652d8; background: linear-gradient(135deg, #eae2ff 0%, #f8f5ff 72%, #fff 100%); }
.kpi-card.orange { color: #d97918; background: linear-gradient(135deg, #ffebc9 0%, #fff8ed 72%, #fff 100%); }
.kpi-card.green { color: #23976c; background: linear-gradient(135deg, #d5f3e6 0%, #f2fcf7 72%, #fff 100%); }
.kpi-value { margin-top: 19px; color: #1c2b49; font-size: 30px; font-weight: 750; letter-spacing: -.5px; }
.kpi-foot { margin-top: 8px; color: #a2adbd; font-size: 11px; }
.kpi-foot i { margin-left: 4px; color: currentColor; font-style: normal; }
.chart-row {
  margin-top: 16px;
}
.chart {
  height: 300px;
}
</style>
