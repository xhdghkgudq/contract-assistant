<template>
  <div class="layout">
    <!-- 侧边导航栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>合同分析系统</h2>
      </div>
      <nav class="sidebar-nav">
        <ul>
          <li class="nav-item active">
            <span class="nav-icon">📊</span>
            <span class="nav-text">合同管理</span>
          </li>
          <li class="nav-item">
            <router-link to="/dashboard" class="nav-link">
              <span class="nav-icon">📈</span>
              <span class="nav-text">数据看板</span>
            </router-link>
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
      <!-- 快到期提醒 -->
      <div v-if="expiringContracts.length > 0" class="expire-warning">
        ⚠️ 有 {{ expiringContracts.length }} 份合同即将到期，请及时处理！
      </div>

      <!-- 上传区域 -->
      <div class="upload-box">
        <div class="file-input-wrapper">
          <input type="file" id="file-input" @change="handleFile" class="file-input" />
          <label for="file-input" class="file-label">
            <span class="file-icon">📄</span>
            <span class="file-text">{{ selectedFileName || '选择合同文件' }}</span>
          </label>
        </div>
        <button @click="handleUpload" class="btn-upload" :disabled="!selectedFileName"
          :class="{ 'disabled-btn': !selectedFileName }">上传分析</button>
      </div>



      <!-- 筛选区域 -->
      <div class="filter-box">
        <div class="filter-header">
          <h3>📋 合同筛选</h3>
        </div>
        <div class="filter-form">
          <div class="filter-item">
            <label class="filter-label">开始日期：</label>
            <input type="datetime-local" v-model="filterStartDate" class="filter-date" />
          </div>
          <div class="filter-item">
            <label class="filter-label">结束日期：</label>
            <input type="datetime-local" v-model="filterEndDate" class="filter-date" />
          </div>
          <button @click="applyFilter" class="btn-filter">应用筛选</button>
          <button @click="resetFilter" class="btn-reset">重置</button>
        </div>
      </div>

      <!-- 表格 -->
      <div class="table-box">
        <table>
          <thead>
            <tr>
              <th width="60">序号</th>
              <th width="120">合同编号</th>
              <th width="140">甲方</th>
              <th width="140">乙方</th>
              <th width="180">服务内容</th>
              <th width="160">服务期限</th>
              <th width="120">服务费用</th>
              <th width="180">支付方式</th>
              <th width="120">签署日期</th>
              <th width="120">到期时间</th>
              <th width="80">合规状态</th>
              <th v-if="currentUser.role === 'admin'" width="120">操作</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(item, index) in contracts" :key="item.id"
              :class="{ 'expiring': isExpiring(item.expire_date), 'expired': isExpired(item.expire_date) }">
              <td class="serial-number">{{ index + 1 }}</td>
              <td>{{ item.contract_number || '无' }}</td>
              <td>{{ item.party_a || '无' }}</td>
              <td>{{ item.party_b || '无' }}</td>
              <td class="text-ellipsis" :title="item.service_content || '无'">{{ item.service_content || '无' }}</td>
              <td class="text-ellipsis" :title="item.service_period || '无'">{{ item.service_period || '无' }}</td>
              <td>{{ item.service_fee || '无' }}</td>
              <td>{{ item.payment_method || '无' }}</td>
              <td>{{ item.signing_date ? formatDate(item.signing_date) : '无' }}</td>
              <td
                :class="{ 'expiring-date': isExpiring(item.expire_date), 'expired-date': isExpired(item.expire_date) }">
                {{ item.expire_date ? formatDate(item.expire_date) : '无' }}
              </td>
              <td>
                <span v-if="item.status === 'approved'" class="status-tag status-approved">
                  通过
                </span>
                <span v-else-if="item.status === 'rejected'" class="status-tag status-rejected">
                  不通过
                </span>
                <span v-else class="status-tag status-pending">
                  待审核
                </span>
              </td>
              <td v-if="currentUser.role === 'admin'" class="action-cell">
                <button @click="viewContract(item)" class="btn-view-action">查看</button>
                <button v-if="item.status === 'rejected'" @click="viewRejectReason(item)" class="btn-reject-reason">查看理由</button>
                <button v-else-if="item.status === 'pending'" @click="analyzeContract(item)" class="btn-analyze-action">AI分析</button>
              </td>
            </tr>

            <tr v-if="contracts.length === 0">
              <td :colspan="currentUser.role === 'admin' ? 12 : 11" class="empty-row">暂无数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- 查看合同弹窗 -->
    <div v-if="showViewModal" class="modal-overlay" @click="closeViewModal">
      <div class="modal-content view-contract-modal" @click.stop>
        <div class="modal-header">
          <h3>合同详情</h3>
          <button @click="closeViewModal" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="contract-info-grid">
            <div class="info-item">
              <span class="info-label">合同编号：</span>
              <span class="info-value">{{ currentViewingContract.contract_number || '无' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">合同名称：</span>
              <span class="info-value">{{ currentViewingContract.name || '无' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">甲方：</span>
              <span class="info-value">{{ currentViewingContract.party_a || '无' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">乙方：</span>
              <span class="info-value">{{ currentViewingContract.party_b || '无' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">服务内容：</span>
              <span class="info-value">{{ currentViewingContract.service_content || '无' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">服务期限：</span>
              <span class="info-value">{{ currentViewingContract.service_period || '无' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">服务费用：</span>
              <span class="info-value">{{ currentViewingContract.service_fee || '无' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">支付方式：</span>
              <span class="info-value">{{ currentViewingContract.payment_method || '无' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">签署日期：</span>
              <span class="info-value">{{ currentViewingContract.signing_date ? formatDate(currentViewingContract.signing_date) : '无' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">到期日期：</span>
              <span class="info-value">{{ currentViewingContract.expire_date ? formatDate(currentViewingContract.expire_date) : '无' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">甲方权利义务：</span>
              <span class="info-value">{{ currentViewingContract.party_a_rights || '无' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">乙方权利义务：</span>
              <span class="info-value">{{ currentViewingContract.party_b_rights || '无' }}</span>
            </div>
            <div class="info-item full-width">
              <span class="info-label">验收标准：</span>
              <span class="info-value">{{ currentViewingContract.acceptance_standard || '无' }}</span>
            </div>
            <div class="info-item full-width">
              <span class="info-label">违约责任：</span>
              <span class="info-value">{{ currentViewingContract.liability || '无' }}</span>
            </div>
            <div class="info-item full-width">
              <span class="info-label">争议解决：</span>
              <span class="info-value">{{ currentViewingContract.dispute_resolution || '无' }}</span>
            </div>
            <div class="info-item full-width">
              <span class="info-label">AI分析结论：</span>
              <span class="info-value">{{ currentViewingContract.result || '无' }}</span>
            </div>
            <div class="info-item full-width">
              <span class="info-label">合同原文：</span>
              <span class="info-value text-content">{{ currentViewingContract.content || '无' }}</span>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeViewModal" class="btn-cancel">关闭</button>
        </div>
      </div>
    </div>

    <!-- 查看不通过理由弹窗 -->
    <div v-if="showRejectReasonModal" class="modal-overlay" @click="closeRejectReasonModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>审核不通过理由</h3>
          <button @click="closeRejectReasonModal" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="reject-reason-content">
            <p><strong>合同：</strong>{{ currentRejectContractName }}</p>
            <div class="reason-box">
              <strong>不通过理由：</strong>
              <p>{{ currentRejectReason }}</p>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeRejectReasonModal" class="btn-cancel">关闭</button>
        </div>
      </div>
    </div>

    <!-- AI分析结果弹窗 -->
    <div v-if="showAnalysisModal" class="modal-overlay" @click="closeAnalysisModal">
      <div class="modal-content analysis-modal" @click.stop>
        <div class="modal-header">
          <h3>AI分析结果</h3>
          <button @click="closeAnalysisModal" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="analysis-section">
            <h4>📋 合同信息</h4>
            <div class="info-grid">
              <div class="info-item"><span class="info-label">合同编号：</span>{{ currentAnalysis.contract_number || '未识别' }}</div>
              <div class="info-item"><span class="info-label">甲方：</span>{{ currentAnalysis.party_a || '未识别' }}</div>
              <div class="info-item"><span class="info-label">乙方：</span>{{ currentAnalysis.party_b || '未识别' }}</div>
              <div class="info-item"><span class="info-label">服务内容：</span>{{ currentAnalysis.service_content || '未识别' }}</div>
              <div class="info-item"><span class="info-label">服务期限：</span>{{ currentAnalysis.service_period || '未识别' }}</div>
              <div class="info-item"><span class="info-label">服务费用：</span>{{ currentAnalysis.service_fee || '未识别' }}</div>
            </div>
          </div>
          <div class="analysis-section">
            <h4>✅ 合规检查结果</h4>
            <div class="compliance-list">
              <div class="compliance-item" :class="currentAnalysis.subject_ok ? 'pass' : 'fail'">
                <span>主体合规：</span>
                <span>{{ currentAnalysis.subject_ok ? '通过' : '未通过' }}</span>
              </div>
              <div class="compliance-item" :class="currentAnalysis.object_clear ? 'pass' : 'fail'">
                <span>标的明确：</span>
                <span>{{ currentAnalysis.object_clear ? '通过' : '未通过' }}</span>
              </div>
              <div class="compliance-item" :class="currentAnalysis.price_clear ? 'pass' : 'fail'">
                <span>价款清晰：</span>
                <span>{{ currentAnalysis.price_clear ? '通过' : '未通过' }}</span>
              </div>
              <div class="compliance-item" :class="currentAnalysis.performable ? 'pass' : 'fail'">
                <span>履行可行：</span>
                <span>{{ currentAnalysis.performable ? '通过' : '未通过' }}</span>
              </div>
            </div>
          </div>
          <div class="analysis-section">
            <h4>📝 分析结论</h4>
            <p class="analysis-result">{{ currentAnalysis.result || '暂无分析结果' }}</p>
          </div>
          <div v-if="showRejectReason" class="analysis-section">
            <h4>📛 审核不通过理由</h4>
            <textarea v-model="rejectReason" class="reason-textarea" placeholder="请输入审核不通过的理由"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button v-if="showRejectReason" @click="submitReject" class="btn-reject">提交不通过理由</button>
          <button v-if="!showRejectReason" @click="handleReject" class="btn-reject">审核不通过</button>
          <button @click="handleApprove" class="btn-approve">审核通过</button>
          <button @click="closeAnalysisModal" class="btn-cancel">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import request from '../api/request'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const file = ref(null)
const analysis = ref({})
const contracts = ref([])
const contractContent = ref('')
const selectedFileName = ref('')
const showCancelBtn = ref(false)
const filterStartDate = ref('')
const filterEndDate = ref('')

// 弹窗状态
const showViewModal = ref(false)
const showAnalysisModal = ref(false)
const viewContractContent = ref('')
const currentViewingContract = ref({})
const currentAnalysis = ref({})
const currentContractId = ref(null)
const showRejectReason = ref(false)
const rejectReason = ref('')

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

// 检查是否为管理员
const isAdmin = computed(() => {
  return currentUser.value.role === 'admin'
})

// 计算属性：判断合同是否合规
const isContractValid = computed(() => {
  if (Object.keys(analysis.value).length === 0) return false
  return analysis.value.subject_ok &&
    analysis.value.object_clear &&
    analysis.value.price_clear &&
    analysis.value.performable
})

// 计算属性：获取即将到期的合同
const expiringContracts = computed(() => {
  return contracts.value.filter(item => isExpiring(item.expire_date))
})

// 检查合同是否已经过期
const isExpired = (expireDate) => {
  if (!expireDate) return false
  const now = new Date()
  const expire = new Date(expireDate)
  return expire < now
}

// 检查合同是否即将到期（7天内）
const isExpiring = (expireDate) => {
  if (!expireDate) return false
  const now = new Date()
  const expire = new Date(expireDate)
  const diffTime = expire - now
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays > 0 && diffDays <= 7
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '无'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const handleFile = (e) => {
  file.value = e.target.files[0]
  if (file.value) {
    // 验证文件类型
    const allowedTypes = ['application/pdf', 'text/plain']
    const allowedExtensions = ['.pdf', '.txt']
    const fileName = file.value.name.toLowerCase()
    const fileType = file.value.type

    if (!allowedTypes.includes(fileType) && !allowedExtensions.some(ext => fileName.endsWith(ext))) {
      ElMessage.warning("只支持PDF和TXT文件")
      file.value = null
      selectedFileName.value = ''
      return
    }

    selectedFileName.value = file.value.name
  }
}

const uploadFile = async () => {
  if (!file.value) return ElMessage.warning("请选择文件")

  const formData = new FormData()
  formData.append("file", file.value)

  try {
    console.log("=== 上传文件到 /upload ===")
    console.log("FormData包含:", formData.get("file")?.name || "空")
    console.log("请求URL:", "http://localhost:5000/upload")
    
    const uploadRes = await request.post("/upload", formData)
    console.log("上传响应:", uploadRes)
    console.log("上传响应状态:", uploadRes.status)
    ElMessage.success("上传成功")
  } catch (err) {
    console.error("❌ 上传失败:", err)
    console.error("上传错误状态:", err.response?.status)
    console.error("上传错误内容:", err.response?.data)
    console.error("上传错误消息:", err.message)
    ElMessage.error("上传失败")
    throw err
  }
}

const handleUpload = async () => {
  if (!file.value) return ElMessage.warning("请选择文件")

  try {
    // 1. 上传文件
    console.log("=== 开始上传文件 ===")
    console.log("文件信息:", file.value)
    console.log("文件名:", file.value.name)
    console.log("文件大小:", file.value.size, "bytes")
    console.log("文件类型:", file.value.type)
    
    await uploadFile()
    ElMessage.info("正在进行AI分析...")
    
    // 2. AI分析 - 提取合同数据
    console.log("\n=== 开始AI分析 ===")
    const analyzeRes = await request.get("/review")
    console.log("AI分析响应:", analyzeRes)
    analysis.value = analyzeRes.data.analysis || {}
    console.log("\n=== AI分析提取结果 ===")
    console.log("合同编号:", analysis.value.contract_number)
    console.log("甲方:", analysis.value.party_a)
    console.log("乙方:", analysis.value.party_b)
    console.log("服务内容:", analysis.value.service_content)
    console.log("服务期限:", analysis.value.service_period)
    console.log("服务费用:", analysis.value.service_fee)
    console.log("支付方式:", analysis.value.payment_method)
    console.log("签署日期:", analysis.value.signing_date)
    console.log("到期日期:", analysis.value.expire_date)
    console.log("甲方权利:", analysis.value.party_a_rights)
    console.log("乙方权利:", analysis.value.party_b_rights)
    console.log("验收标准:", analysis.value.acceptance_standard)
    console.log("违约责任:", analysis.value.liability)
    console.log("争议解决:", analysis.value.dispute_resolution)
    console.log("分析结果完整对象:", analysis.value)
    
    // 3. 获取合同内容
    console.log("\n=== 获取合同内容 ===")
    const contentRes = await request.get("/contract/content")
    console.log("合同内容响应:", contentRes)
    contractContent.value = contentRes.data.content || ''
    console.log("合同内容长度:", contractContent.value.length, "字符")
    
    // 4. 使用AI分析结果保存到系统
    console.log("\n=== 使用AI分析结果保存合同 ===")
    await saveContractWithAI()
    ElMessage.success("上传完成，AI分析结果已添加到列表")
    
    // 5. 刷新列表
    loadContracts()
    
    // 6. 重置状态
    cancelAnalysis()
  } catch (err) {
    console.error("=== 上传分析失败 ===")
    console.error("错误信息:", err)
    console.error("错误详情:", err.response ? err.response.data : err.message)
    ElMessage.error("上传分析失败")
    cancelAnalysis()
  }
}

const openModal = () => {
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const analyze = async () => {
  try {
    const res = await request.get("/review")
    analysis.value = res.data.analysis || {}
    showCancelBtn.value = true
  } catch (err) {
    ElMessage.error("分析失败")
  }
}

const viewContract = async (contract = null) => {
  if (contract) {
    // 从表格点击查看
    currentViewingContract.value = contract
    showViewModal.value = true
  } else {
    // 上传后查看
    if (!selectedFileName.value) {
      return ElMessage.warning("请先选择并上传文件")
    }

    try {
      const res = await request.get("/contract/content")
      viewContractContent.value = res.data.content
    } catch (err) {
      ElMessage.error("查看合同失败")
    }
  }
}

const closeViewModal = () => {
  showViewModal.value = false
  viewContractContent.value = ''
  currentViewingContract.value = {}
}

// 查看不通过理由
const showRejectReasonModal = ref(false)
const currentRejectReason = ref('')
const currentRejectContractName = ref('')

const viewRejectReason = (contract) => {
  currentRejectContractName.value = contract.name || contract.contract_number || '合同'
  currentRejectReason.value = contract.reject_reason || '无理由'
  showRejectReasonModal.value = true
}

const closeRejectReasonModal = () => {
  showRejectReasonModal.value = false
  currentRejectReason.value = ''
  currentRejectContractName.value = ''
}

const analyzeContract = async (contract) => {
  if (!contract) {
    return ElMessage.warning("请选择合同")
  }

  try {
    ElMessage.info("正在进行AI分析...")
    const res = await request.post("/review/analyze", {
      contract_id: contract.id
    })
    currentAnalysis.value = res.data.analysis || {}
    currentContractId.value = contract.id
    showRejectReason.value = false
    rejectReason.value = ''
    showAnalysisModal.value = true
  } catch (err) {
    ElMessage.error("分析失败")
  }
}

const closeAnalysisModal = () => {
  showAnalysisModal.value = false
  currentAnalysis.value = {}
  currentContractId.value = null
  showRejectReason.value = false
  rejectReason.value = ''
}

const handleApprove = async () => {
  try {
    await request.post("/contract/approve", {
      contract_id: currentContractId.value,
      status: 'approved'
    })
    ElMessage.success("审核通过")
    closeAnalysisModal()
    loadContracts()
  } catch (err) {
    ElMessage.error("操作失败")
  }
}

const handleReject = () => {
  showRejectReason.value = true
}

const submitReject = async () => {
  if (!rejectReason.value.trim()) {
    return ElMessage.warning("请输入审核不通过的理由")
  }

  try {
    await request.post("/contract/approve", {
      contract_id: currentContractId.value,
      status: 'rejected',
      reason: rejectReason.value
    })
    ElMessage.success("审核不通过已提交")
    closeAnalysisModal()
    loadContracts()
  } catch (err) {
    ElMessage.error("操作失败")
  }
}

const cancelAnalysis = () => {
  analysis.value = {}
  contractContent.value = ''
  file.value = null
  selectedFileName.value = ''
  showCancelBtn.value = false
}

const voidContract = async (contractId) => {
  try {
    console.log("=== 开始作废合同 ===")
    console.log("合同ID:", contractId)

    const token = localStorage.getItem('token')
    if (!token) {
      console.error("未找到token")
      ElMessage.error("未登录，请先登录")
      return
    }

    const res = await request.post("/void_contract", {
      contract_id: contractId
    }, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    console.log("作废合同响应:", res)
    if (res.data && res.data.msg) {
      ElMessage.success(res.data.msg)
    } else {
      ElMessage.success("合同已作废")
    }
    loadContracts()
  } catch (err) {
    console.error("作废合同失败:", err)
    console.error("错误状态:", err.response?.status)
    console.error("错误内容:", err.response?.data)
    console.error("错误详情:", err.message)
    if (err.response?.data?.msg) {
      ElMessage.error(err.response.data.msg)
    } else {
      ElMessage.error("作废合同失败")
    }
  }
}

const editContract = (item) => {
  ElMessage.info(`编辑合同: ${item.contract_number || item.name}`)
}

const saveContract = async () => {
  try {
    if (Object.keys(analysis.value).length === 0) {
      ElMessage.warning("请先进行AI分析")
      return
    }

    console.log("=== 保存合同数据 ===")
    console.log(analysis.value)

    const res = await request.post("/save_contract", {
      contract_number: analysis.value.contract_number || '',
      party_a: analysis.value.party_a || '',
      party_b: analysis.value.party_b || '',
      service_content: analysis.value.service_content || '',
      service_period: analysis.value.service_period || '',
      service_fee: analysis.value.service_fee || '',
      payment_method: analysis.value.payment_method || '',
      party_a_rights: analysis.value.party_a_rights || '',
      party_b_rights: analysis.value.party_b_rights || '',
      acceptance_standard: analysis.value.acceptance_standard || '',
      liability: analysis.value.liability || '',
      dispute_resolution: analysis.value.dispute_resolution || '',
      signing_date: analysis.value.signing_date || null,
      name: "合同_" + Date.now(),
      content: contractContent.value,
      expire_date: analysis.value.expire_date || null,
      result: analysis.value.result,
      subject_ok: analysis.value.subject_ok,
      object_clear: analysis.value.object_clear,
      price_clear: analysis.value.price_clear,
      performable: analysis.value.performable
    })

    if (res.data.is_compliant) {
      ElMessage.success("保存成功 - 合同已合规")
    } else {
      ElMessage.warning("保存成功 - 但合同不合规")
    }

    // 清空当前分析结果
    analysis.value = {}
    file.value = null
    selectedFileName.value = ''
    showCancelBtn.value = false

    // 刷新合同列表
    loadContracts()
  } catch (err) {
    console.error("❌ 保存合同失败:", err)
    console.error("错误详情:", err.response?.data)
    const errorMsg = err.response?.data?.msg || err.response?.data?.error || "保存失败"
    ElMessage.error(errorMsg)
  }
}

// 使用AI分析结果保存合同
const saveContractWithAI = async () => {
  try {
    console.log("=== 使用AI分析结果保存合同 ===")
    
    // 检查当前token
    const token = localStorage.getItem('token')
    console.log("当前Token:", token ? token.substring(0, 20) + "..." : "无token")
    
    // 获取文件名作为合同名称
    const contractName = file.value.name.replace(/\.[^/.]+$/, '') // 去掉扩展名
    console.log("合同名称:", contractName)
    
    // 检查analysis数据
    console.log("analysis数据:", analysis.value)
    console.log("contractContent长度:", contractContent.value.length)
    
    // 使用AI分析结果填充字段
    const postData = {
      contract_number: analysis.value.contract_number || ('CN-' + Date.now()),
      party_a: analysis.value.party_a || '未识别',
      party_b: analysis.value.party_b || '未识别',
      service_content: analysis.value.service_content || '未识别',
      service_period: analysis.value.service_period || '未识别',
      service_fee: analysis.value.service_fee || '未识别',
      payment_method: analysis.value.payment_method || '未识别',
      party_a_rights: analysis.value.party_a_rights || '',
      party_b_rights: analysis.value.party_b_rights || '',
      acceptance_standard: analysis.value.acceptance_standard || '',
      liability: analysis.value.liability || '',
      dispute_resolution: analysis.value.dispute_resolution || '',
      signing_date: analysis.value.signing_date || null,
      expire_date: analysis.value.expire_date || null,
      name: contractName,
      content: contractContent.value,
      result: analysis.value.result || 'AI分析完成',
      subject_ok: analysis.value.subject_ok || false,
      object_clear: analysis.value.object_clear || false,
      price_clear: analysis.value.price_clear || false,
      performable: analysis.value.performable || false,
      is_compliant: (analysis.value.subject_ok && analysis.value.object_clear && analysis.value.price_clear && analysis.value.performable) || false
    }
    
    // 打印要发送的数据
    console.log("准备发送的数据:", JSON.stringify(postData, null, 2))
    
    // 发送请求
    console.log("发送POST请求到 /save_contract...")
    const res = await request.post("/save_contract", postData)
    
    console.log("保存响应:", res.data)
    
    // 清空状态
    analysis.value = {}
    file.value = null
    selectedFileName.value = ''
    showCancelBtn.value = false
    
  } catch (err) {
    console.error("❌ 使用AI分析结果保存合同失败:", err)
    console.error("错误详情:", err.response?.data)
    throw err
  }
}

const loadContracts = async (startDate = '', endDate = '') => {
  try {
    let url = "/contracts"
    const params = []
    if (startDate) {
      params.push(`start_date=${encodeURIComponent(startDate)}`)
    }
    if (endDate) {
      params.push(`end_date=${encodeURIComponent(endDate)}`)
    }
    if (params.length > 0) {
      url += `?${params.join('&')}`
    }
    const res = await request.get(url)
    contracts.value = res.data
  } catch (err) {
    ElMessage.error("获取合同列表失败")
  }
}

const applyFilter = () => {
  loadContracts(filterStartDate.value, filterEndDate.value)
}

const resetFilter = () => {
  filterStartDate.value = ''
  filterEndDate.value = ''
  loadContracts()
}

onMounted(() => {
  getCurrentUser()
  loadContracts()
})
</script>

<style scoped>
/* 页面整体布局 */
.layout {
  display: flex;
  min-height: 100vh;
  background: #f5f7fa;
  overflow: hidden;
}

/* 侧边导航栏 */
.sidebar {
  width: 220px;
  background: linear-gradient(180deg, #1e3a5f 0%, #2d5a87 100%);
  color: white;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  z-index: 100;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  font-size: 18px;
  margin: 0;
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

/* 标题 */
h1 {
  font-size: 28px;
  margin-bottom: 20px;
  color: #333;
}

/* 无权限提示 */
.no-permission {
  color: #ccc;
  font-size: 12px;
}

/* 上传区域 */
.upload-box {
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  padding: 25px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

/* 禁用按钮样式 */
.disabled-btn {
  background-color: #e4e7ed !important;
  cursor: not-allowed !important;
  opacity: 0.6 !important;
  color: #909399 !important;
}



/* 文件输入框美化 */
.file-input-wrapper {
  position: relative;
  display: inline-block;
}

.file-input {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.file-label {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 30px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border: 2px dashed #cbd5e1;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 220px;
  justify-content: center;
}

.file-label:hover {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-color: #60a5fa;
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
}

.file-icon {
  font-size: 22px;
}

.file-text {
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 按钮样式 */
.upload-box button {
  padding: 14px 30px;
  border: none;
  border-radius: 10px;
  color: white;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-upload {
  background: linear-gradient(135deg, #409eff 0%, #3b82f6 100%);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.btn-upload:hover:not(.disabled-btn) {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.4);
}



/* 操作按钮 */
.action-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.btn-view-action,
.btn-analyze-action,
.btn-void-action {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  font-size: 11px;
  transition: all 0.3s;
  white-space: nowrap;
}

.btn-view-action {
  background: #e6a23c;
}

.btn-view-action:hover {
  background: #ebb563;
}

.btn-analyze-action {
  background: #67c23a;
}

.btn-analyze-action:hover {
  background: #85ce61;
}

.btn-void-action {
  background: #909399;
}

.btn-void-action:hover {
  background: #a6a9ad;
}

.btn-reject-reason {
  background: #409eff;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  font-weight: 500;
  border: none;
  color: white;
}

.btn-reject-reason:hover {
  background: #67b1ff;
}

/* 表格 */
.table-box {
  overflow-x: auto;
  margin-top: 20px;
  max-width: 100%;
  border-radius: 8px;
  border: 1px solid #e8e8e8;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

table {
  min-width: 1400px;
  width: 100%;
  border-collapse: collapse;
  background: white;
}

table thead {
  position: sticky;
  top: 0;
  z-index: 1;
}

/* 表头 */
th {
  background: #fafafa;
  color: #666;
  padding: 12px 8px;
  font-weight: 500;
  font-size: 13px;
  text-align: left;
  border-bottom: 2px solid #e8e8e8;
  white-space: nowrap;
}

/* 单元格 */
td {
  padding: 12px 8px;
  border-bottom: 1px solid #f0f0f0;
  vertical-align: middle;
  font-size: 13px;
  color: #333;
  text-align: left;
  white-space: nowrap;
}

/* 表格行 */
tbody tr {
  transition: background-color 0.15s ease;
}

tbody tr:hover {
  background: #f9f9f9;
}

/* 序号列 */
.serial-number {
  color: #999;
  font-size: 12px;
  text-align: center;
}

/* 超长文本处理 */
.text-ellipsis {
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: help;
}

/* 空数据 */
.empty-row {
  text-align: center;
  color: #999;
  padding: 30px;
  font-size: 13px;
}

/* 状态标签 */
.status-tag {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-compliant {
  background: #e8f5e9;
  color: #388e3c;
  border: 1px solid #c8e6c9;
}

.status-non-compliant {
  background: #ffebee;
  color: #c62828;
  border: 1px solid #ffcdd2;
}

.status-pending {
  background: #fef08a;
  color: #854d0e;
}

.status-approved {
  background: #bbf7d0;
  color: #166534;
}

.status-rejected {
  background: #fecaca;
  color: #991b1b;
}

/* 到期日期样式 */
.expiring-date {
  color: #e65100;
  font-weight: 500;
}

.expired-date {
  color: #d32f2f;
  font-weight: 600;
}

/* 操作列 */
.action-cell {
  display: flex;
  gap: 8px;
  align-items: center;
}

/* 操作按钮 */
.btn-edit,
.btn-void {
  padding: 5px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.15s ease;
}

.btn-edit {
  background: #fff;
  color: #1890ff;
  border: 1px solid #1890ff;
}

.btn-edit:hover {
  background: #e6f7ff;
}

.btn-void {
  background: #fff;
  color: #ff4d4f;
  border: 1px solid #ff4d4f;
}

.btn-void:hover {
  background: #fff2f0;
}

/* 合同内容区域 */
.contract-content {
  margin: 30px auto;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  max-height: 400px;
  overflow-y: auto;
  max-width: 90%;
}

.contract-content h3 {
  margin-bottom: 15px;
  color: #333;
}

.contract-content pre {
  white-space: pre-wrap;
  font-family: Arial, sans-serif;
  line-height: 1.8;
  margin: 0;
  text-align: left;
}

/* 禁用按钮样式 */
.disabled-btn {
  background: #c0c4cc !important;
  cursor: not-allowed !important;
  opacity: 0.6;
}

/* 到期提醒 */
.expire-warning {
  margin: 15px auto;
  padding: 15px 20px;
  background: #fef0f0;
  border: 1px solid #fbc4c4;
  border-radius: 6px;
  color: #f56c6c;
  font-size: 14px;
  font-weight: bold;
  max-width: 90%;
}



/* 筛选区域 */
.filter-box {
  margin: 30px 0;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.filter-header {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.filter-header h3 {
  margin: 0;
  color: #334155;
  font-size: 16px;
  font-weight: 600;
}

.filter-form {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-label {
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
}

.filter-date {
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  background: #f8fafc;
  transition: all 0.3s ease;
}

.filter-date:focus {
  outline: none;
  border-color: #409eff;
  box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.1);
}

.btn-filter {
  background: linear-gradient(135deg, #409eff 0%, #3b82f6 100%);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

.btn-filter:hover {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
}

.btn-reset {
  background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(100, 116, 139, 0.3);
}

.btn-reset:hover {
  background: linear-gradient(135deg, #64748b 0%, #475569 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(100, 116, 139, 0.4);
}

/* 即将到期的行 */
tr.expiring {
  background: #fef0f0 !important;
}

/* 过期的行 */
tr.expired {
  background: #fef0f0 !important;
  border-left: 4px solid #f56c6c;
}

/* 即将到期的日期 */
.expiring-date {
  color: #f56c6c;
  font-weight: bold;
}

/* 过期的日期 */
.expired-date {
  color: #f56c6c;
  font-weight: bold;
  text-decoration: line-through;
}

/* 分析结果文本 - 显示完整内容 */
.analysis-text {
  text-align: left;
  line-height: 1.6;
  max-width: 400px;
  word-wrap: break-word;
}

/* 不合规标记 */
.non-compliant {
  color: #f56c6c;
  font-weight: bold;
}

/* 合规标记 */
.compliant {
  color: #67c23a;
  font-weight: bold;
}

/* 弹窗遮罩 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

/* 弹窗内容 */
.modal-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow: hidden;
}

/* 查看合同弹窗 */
.view-contract-modal {
  max-width: 900px;
}

/* AI分析弹窗 */
.analysis-modal {
  max-width: 800px;
}

/* 弹窗头部 */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #eee;
  background: #274D77;
  color: white;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
}

.modal-close {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* 弹窗主体 */
.modal-body {
  padding: 24px;
  max-height: 50vh;
  overflow-y: auto;
}

/* 弹窗底部 */
.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 不通过理由弹窗内容 */
.reject-reason-content {
  padding: 10px;
}

.reject-reason-content p {
  margin: 0 0 12px 0;
  font-size: 14px;
}

.reject-reason-content .reason-box {
  background: #fffbeb;
  border: 1px solid #fef3c7;
  border-radius: 6px;
  padding: 14px;
}

.reject-reason-content .reason-box strong {
  color: #b45309;
  display: block;
  margin-bottom: 8px;
}

.reject-reason-content .reason-box p {
  color: #374151;
  line-height: 1.6;
  margin: 0;
}

/* 合同信息网格 */
.contract-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.contract-info-grid .info-item {
  padding: 10px 14px;
  background: #f8f9fa;
  border-radius: 6px;
}

.contract-info-grid .info-item.full-width {
  grid-column: span 2;
}

.contract-info-grid .info-label {
  color: #666;
  font-weight: 500;
  font-size: 13px;
  display: block;
  margin-bottom: 4px;
}

.contract-info-grid .info-value {
  color: #333;
  font-size: 13px;
  line-height: 1.5;
}

.contract-info-grid .info-value.text-content {
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 200px;
  overflow-y: auto;
  display: block;
}

/* 分析区域 */
.analysis-section {
  margin-bottom: 24px;
}

.analysis-section h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #333;
  border-left: 4px solid #667eea;
  padding-left: 10px;
}

/* 信息网格 */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.info-item {
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 6px;
  font-size: 13px;
}

.info-label {
  color: #666;
  font-weight: 500;
}

/* 合规检查列表 */
.compliance-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.compliance-item {
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 13px;
  display: flex;
  justify-content: space-between;
}

.compliance-item.pass {
  background: #e8f5e9;
  color: #388e3c;
}

.compliance-item.fail {
  background: #ffebee;
  color: #c62828;
}

/* 分析结论 */
.analysis-result {
  padding: 12px 16px;
  background: #fff3e0;
  border-radius: 6px;
  font-size: 14px;
  line-height: 1.6;
  color: #e65100;
  margin: 0;
}

/* 理由文本框 */
.reason-textarea {
  width: 100%;
  height: 100px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  resize: vertical;
  font-size: 14px;
  line-height: 1.5;
  box-sizing: border-box;
}

.reason-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* 弹窗按钮 */
.btn-cancel,
.btn-approve,
.btn-reject {
  padding: 10px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-cancel {
  background: #f5f5f5;
  color: #666;
}

.btn-cancel:hover {
  background: #eee;
}

.btn-approve {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(103, 194, 58, 0.3);
}

.btn-approve:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(103, 194, 58, 0.4);
}

.btn-reject {
  background: linear-gradient(135deg, #f56c6c 0%, #f89898 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(245, 108, 108, 0.3);
}

.btn-reject:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(245, 108, 108, 0.4);
}

</style>
