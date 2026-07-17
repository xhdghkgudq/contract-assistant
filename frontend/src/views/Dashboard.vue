<template>
  <div class="dashboard">
    <!-- 侧边导航栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>合同分析系统</h2>
      </div>
      <nav class="sidebar-nav">
        <ul>
          <li class="nav-item">
            <router-link to="/home" class="nav-link">
              <span class="nav-icon">📊</span>
              <span class="nav-text">合同管理</span>
            </router-link>
          </li>
          <li class="nav-item active">
            <span class="nav-icon">📈</span>
            <span class="nav-text">数据看板</span>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- 主内容区域 -->
    <main class="main-content">
      <!-- 用户信息区域 -->
      <div class="user-info-bar">
        <div class="user-info" @click="toggleUserMenu">
          <span class="user-icon">👤</span>
          <span class="user-name">{{ currentUser.username }}</span>
          <span class="user-role">{{ currentUser.role === 'admin' ? '管理员' : '普通用户' }}</span>
          <span class="dropdown-arrow">▼</span>
        </div>
        <div v-if="showUserMenu" class="user-menu">
          <div class="menu-item" @click="logout">
            <span class="menu-icon">🚪</span>
            <span>退出登录</span>
          </div>
        </div>
      </div>

      <!-- 页面标题 -->
      <div class="page-header">
        <h1>分析看板</h1>
        <div class="header-actions">
          <button class="refresh-btn" @click="refreshData">🔄 刷新</button>
        </div>
      </div>

      <!-- 数据概览 -->
      <div class="overview-section">
        <h3 class="section-title">数据概览</h3>
        <div class="overview-cards">
          <div class="overview-card card-blue">
            <div class="card-icon">🏠</div>
            <div class="card-content">
              <p class="card-label">当前合同数量</p>
              <p class="card-value">{{ stats.currentContracts }}</p>
            </div>
          </div>
          <div class="overview-card card-yellow">
            <div class="card-icon">📋</div>
            <div class="card-content">
              <p class="card-label">进行中合同数量</p>
              <p class="card-value">{{ stats.inProgressContracts }}</p>
            </div>
          </div>
          <div class="overview-card card-green">
            <div class="card-icon">💰</div>
            <div class="card-content">
              <p class="card-label">应收金额</p>
              <p class="card-value">{{ formatNumber(stats.receivableAmount) }}</p>
            </div>
          </div>
          <div class="overview-card card-red">
            <div class="card-icon">💳</div>
            <div class="card-content">
              <p class="card-label">应付金额</p>
              <p class="card-value">{{ formatNumber(stats.payableAmount) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 图表区域 -->
      <div class="charts-section">
        <div class="chart-row">
          <!-- 全年应收金额图表 -->
          <div class="chart-card">
            <div class="chart-header">
              <h3>全年应收金额</h3>
              <p class="chart-subtitle">{{ receivableMaxMonth }}月应收金额最高 {{ formatNumber(receivableMaxValue) }}元</p>
            </div>
            <div class="chart-container">
              <div class="line-chart">
                <div class="chart-grid">
                  <div v-for="i in 5" :key="i" class="grid-line">
                    <span class="grid-label">{{ (5 - i) * 20000 }}</span>
                  </div>
                </div>
                <svg viewBox="0 0 700 250" class="chart-svg">
                  <defs>
                    <linearGradient id="receivableGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stop-color="rgba(39, 174, 96, 0.3)" />
                      <stop offset="100%" stop-color="rgba(39, 174, 96, 0)" />
                    </linearGradient>
                  </defs>
                  <path :d="receivableAreaPath" fill="url(#receivableGradient)" />
                  <path :d="receivableLinePath" fill="none" stroke="#27ae60" stroke-width="3" stroke-linecap="round"
                    stroke-linejoin="round" />
                  <circle v-for="(point, index) in receivablePoints" :key="index" :cx="point.x" :cy="point.y" r="5"
                    fill="#27ae60" />
                  <text v-for="(point, index) in receivablePoints" :key="'label-' + index" :x="point.x" :y="245"
                    text-anchor="middle" font-size="11" fill="#666">
                    {{ months[index] }}月
                  </text>
                </svg>
              </div>
            </div>
          </div>

          <!-- 应收账款环形图 -->
          <div class="chart-card small-card">
            <div class="chart-header">
              <h3>应收账款</h3>
              <p class="chart-subtitle">未收金额: {{ formatNumber(stats.unreceivedAmount) }}</p>
            </div>
            <div class="chart-container">
              <div class="donut-chart-wrapper">
                <svg viewBox="0 0 200 200" class="donut-svg">
                  <circle cx="100" cy="100" r="70" fill="none" stroke="#e0e0e0" stroke-width="20" />
                  <circle cx="100" cy="100" r="70" fill="none" stroke="#27ae60" stroke-width="20"
                    :stroke-dasharray="receivableDashArray" stroke-dashoffset="0" transform="rotate(-90 100 100)" />
                </svg>
                <div class="donut-center">
                  <p class="donut-value">{{ stats.receivableRate }}%</p>
                  <p class="donut-label">应收率</p>
                </div>
              </div>
              <div class="donut-legend">
                <div class="legend-item">
                  <span class="legend-color" style="background:#27ae60"></span>
                  <span>实收金额: {{ formatNumber(stats.receivedAmount) }}</span>
                </div>
                <div class="legend-item">
                  <span class="legend-color" style="background:#e0e0e0"></span>
                  <span>未收金额: {{ formatNumber(stats.unreceivedAmount) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="chart-row">
          <!-- 全年应付金额图表 -->
          <div class="chart-card">
            <div class="chart-header">
              <h3>全年应付金额</h3>
              <p class="chart-subtitle">{{ payableMaxMonth }}月应付金额最高 {{ formatNumber(payableMaxValue) }}元</p>
            </div>
            <div class="chart-container">
              <div class="line-chart">
                <div class="chart-grid">
                  <div v-for="i in 5" :key="i" class="grid-line">
                    <span class="grid-label">{{ (5 - i) * 20000 }}</span>
                  </div>
                </div>
                <svg viewBox="0 0 700 250" class="chart-svg">
                  <defs>
                    <linearGradient id="payableGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stop-color="rgba(231, 76, 60, 0.3)" />
                      <stop offset="100%" stop-color="rgba(231, 76, 60, 0)" />
                    </linearGradient>
                  </defs>
                  <path :d="payableAreaPath" fill="url(#payableGradient)" />
                  <path :d="payableLinePath" fill="none" stroke="#e74c3c" stroke-width="3" stroke-linecap="round"
                    stroke-linejoin="round" />
                  <circle v-for="(point, index) in payablePoints" :key="index" :cx="point.x" :cy="point.y" r="5"
                    fill="#e74c3c" />
                  <text v-for="(point, index) in payablePoints" :key="'label-' + index" :x="point.x" :y="245"
                    text-anchor="middle" font-size="11" fill="#666">
                    {{ months[index] }}月
                  </text>
                </svg>
              </div>
            </div>
          </div>

          <!-- 应付账款环形图 -->
          <div class="chart-card small-card">
            <div class="chart-header">
              <h3>应付账款</h3>
              <p class="chart-subtitle">未付金额: {{ formatNumber(stats.unpaidAmount) }}</p>
            </div>
            <div class="chart-container">
              <div class="donut-chart-wrapper">
                <svg viewBox="0 0 200 200" class="donut-svg">
                  <circle cx="100" cy="100" r="70" fill="none" stroke="#e0e0e0" stroke-width="20" />
                  <circle cx="100" cy="100" r="70" fill="none" stroke="#e74c3c" stroke-width="20"
                    :stroke-dasharray="payableDashArray" stroke-dashoffset="0" transform="rotate(-90 100 100)" />
                </svg>
                <div class="donut-center">
                  <p class="donut-value">{{ stats.payableRate }}%</p>
                  <p class="donut-label">应付率</p>
                </div>
              </div>
              <div class="donut-legend">
                <div class="legend-item">
                  <span class="legend-color" style="background:#e74c3c"></span>
                  <span>实付金额: {{ formatNumber(stats.paidAmount) }}</span>
                </div>
                <div class="legend-item">
                  <span class="legend-color" style="background:#e0e0e0"></span>
                  <span>未付金额: {{ formatNumber(stats.unpaidAmount) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { RouterLink, useRouter } from 'vue-router'
import request from '../api/request'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 月份
const months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

// 用户信息
const currentUser = ref({
  id: '',
  username: '',
  role: 'user'
})

// 用户菜单显示状态
const showUserMenu = ref(false)

// 获取当前用户信息
const getCurrentUser = () => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    currentUser.value = JSON.parse(userStr)
  }
}

// 切换用户菜单
const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

// 退出登录
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  showUserMenu.value = false
  ElMessage.success('退出成功')
  router.push('/')
}

// 统计数据
const stats = ref({
  currentContracts: 0,
  inProgressContracts: 0,
  receivableAmount: 0,
  payableAmount: 0,
  receivableRate: 0,
  payableRate: 0,
  receivedAmount: 0,
  unreceivedAmount: 0,
  paidAmount: 0,
  unpaidAmount: 0
})

// 应收金额数据
const receivableData = ref([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

// 应付金额数据
const payableData = ref([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

// 获取统计数据
const fetchStats = async () => {
  try {
    const res = await request.get('/stats')
    const data = res.data

    stats.value = {
      currentContracts: data.current_contracts || 0,
      inProgressContracts: data.in_progress_contracts || 0,
      receivableAmount: data.receivable_amount || 0,
      payableAmount: data.payable_amount || 0,
      receivableRate: data.receivable_rate || 0,
      payableRate: data.payable_rate || 0,
      receivedAmount: data.received_amount || 0,
      unreceivedAmount: data.unreceived_amount || 0,
      paidAmount: data.paid_amount || 0,
      unpaidAmount: data.unpaid_amount || 0
    }

    receivableData.value = data.monthly_receivable || [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    payableData.value = data.monthly_payable || [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  }
}

// 刷新数据
const refreshData = () => {
  fetchStats()
}

// 组件挂载时获取数据
onMounted(() => {
  getCurrentUser()
  fetchStats()
})

// 格式化数字
const formatNumber = (num) => {
  return num.toLocaleString()
}

// 应收金额最大值
const receivableMaxValue = computed(() => {
  const max = Math.max(...receivableData.value)
  return max || 0
})

// 应收金额最大月份
const receivableMaxMonth = computed(() => {
  const max = receivableMaxValue.value
  const index = receivableData.value.indexOf(max)
  return index >= 0 ? (index + 1) : 1
})

// 应付金额最大值
const payableMaxValue = computed(() => {
  const max = Math.max(...payableData.value)
  return max || 0
})

// 应付金额最大月份
const payableMaxMonth = computed(() => {
  const max = payableMaxValue.value
  const index = payableData.value.indexOf(max)
  return index >= 0 ? (index + 1) : 1
})

// 计算应收折线图点
const receivablePoints = computed(() => {
  const maxValue = 100000
  const width = 700
  const height = 220
  const padding = 30
  const stepX = (width - padding * 2) / 11

  return receivableData.value.map((value, index) => ({
    x: padding + index * stepX,
    y: height - (value / maxValue) * height + padding
  }))
})

// 应收折线路径
const receivableLinePath = computed(() => {
  const points = receivablePoints.value
  if (!points.length) return ''
  return points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ')
})

// 应收面积路径
const receivableAreaPath = computed(() => {
  const points = receivablePoints.value
  if (!points.length) return ''
  const startX = points[0].x
  const endX = points[points.length - 1].x
  return `${receivableLinePath.value} L ${endX} 250 L ${startX} 250 Z`
})

// 计算应付折线图点
const payablePoints = computed(() => {
  const maxValue = 100000
  const width = 700
  const height = 220
  const padding = 30
  const stepX = (width - padding * 2) / 11

  return payableData.value.map((value, index) => ({
    x: padding + index * stepX,
    y: height - (value / maxValue) * height + padding
  }))
})

// 应付折线路径
const payableLinePath = computed(() => {
  const points = payablePoints.value
  if (!points.length) return ''
  return points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ')
})

// 应付面积路径
const payableAreaPath = computed(() => {
  const points = payablePoints.value
  if (!points.length) return ''
  const startX = points[0].x
  const endX = points[points.length - 1].x
  return `${payableLinePath.value} L ${endX} 250 L ${startX} 250 Z`
})

// 应收环形图参数
const receivableDashArray = computed(() => {
  const circumference = 2 * Math.PI * 70
  const percentage = stats.value.receivableRate / 100
  return `${percentage * circumference} ${circumference}`
})

// 应付环形图参数
const payableDashArray = computed(() => {
  const circumference = 2 * Math.PI * 70
  const percentage = stats.value.payableRate / 100
  return `${percentage * circumference} ${circumference}`
})
</script>

<style scoped>
.dashboard {
  display: flex;
  height: 100vh;
  background: #f0f2f5;
}

/* 侧边导航栏 */
.sidebar {
  width: 220px;
  background: #1e3a5f;
  color: white;
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  z-index: 100;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  background: rgba(255, 255, 255, 0.15);
  border-left-color: #4a90d9;
}

.nav-icon {
  font-size: 18px;
  margin-right: 10px;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
}

.nav-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
  width: 100%;
}

/* 主内容区域 */
.main-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
  margin-left: 220px;
  height: 100vh;
  box-sizing: border-box;
}

/* 用户信息区域 */
.user-info-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-info:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.user-icon {
  font-size: 20px;
}

.user-name {
  font-weight: 500;
  color: #333;
}

.user-role {
  padding: 2px 8px;
  background: #e8f5e9;
  color: #388e3c;
  border-radius: 4px;
  font-size: 12px;
}

.dropdown-arrow {
  font-size: 12px;
  color: #999;
  transition: transform 0.3s ease;
}

.user-info:hover .dropdown-arrow {
  transform: rotate(180deg);
}

/* 用户菜单 */
.user-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  padding: 8px;
  min-width: 140px;
  z-index: 100;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s ease;
  color: #333;
}

.menu-item:hover {
  background: #f5f7fa;
}

.menu-icon {
  font-size: 16px;
}

/* 页面标题 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 28px;
  margin: 0;
  color: #333;
}

.refresh-btn {
  padding: 10px 20px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  background: #3b82f6;
}

/* 数据概览区域 */
.overview-section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 16px;
  color: #666;
  margin-bottom: 15px;
  font-weight: 500;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.overview-card {
  display: flex;
  align-items: center;
  padding: 20px;
  border-radius: 10px;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-blue {
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
}

.card-yellow {
  background: linear-gradient(135deg, #b45309 0%, #f59e0b 100%);
}

.card-green {
  background: linear-gradient(135deg, #166534 0%, #22c55e 100%);
}

.card-red {
  background: linear-gradient(135deg, #991b1b 0%, #ef4444 100%);
}

.card-icon {
  font-size: 40px;
  margin-right: 15px;
}

.card-content {
  flex: 1;
}

.card-label {
  font-size: 13px;
  opacity: 0.9;
  margin: 0 0 5px 0;
}

.card-value {
  font-size: 28px;
  font-weight: 700;
  margin: 0;
}

/* 图表区域 */
.charts-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.chart-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.chart-card.small-card {
  grid-column: span 1;
}

.chart-header {
  margin-bottom: 20px;
}

.chart-header h3 {
  font-size: 16px;
  color: #333;
  margin: 0 0 5px 0;
}

.chart-subtitle {
  font-size: 13px;
  color: #999;
  margin: 0;
}

.chart-container {
  height: 300px;
}

/* 折线图 */
.line-chart {
  position: relative;
  height: 100%;
}

.chart-grid {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 25px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.grid-line {
  border-top: 1px dashed #eee;
  position: relative;
}

.grid-label {
  position: absolute;
  left: 0;
  top: -10px;
  font-size: 10px;
  color: #999;
}

.chart-svg {
  width: 100%;
  height: 100%;
}

/* 环形图 */
.donut-chart-wrapper {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto;
}

.donut-svg {
  width: 100%;
  height: 100%;
}

.donut-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.donut-value {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.donut-label {
  font-size: 14px;
  color: #999;
  margin: 5px 0 0 0;
}

.donut-legend {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #666;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}
</style>
