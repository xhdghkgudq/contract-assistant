<template>
  <div class="review-wrapper">
    <div class="review-cards">
      <el-card class="card">
        <h3>合同内容</h3>
        <div class="content-box">{{ contractText }}</div>
      </el-card>
      <el-card class="card">
        <h3>AI 审查结果</h3>
        <div class="content-box">
          <div v-if="typeof aiResult === 'object'">
            <p><strong>整体分析：</strong>{{ aiResult.result }}</p>
            <p><strong>主体明确：</strong>{{ aiResult.subject_ok ? '是' : '否' }}</p>
            <p><strong>标的明确：</strong>{{ aiResult.object_clear ? '是' : '否' }}</p>
            <p><strong>价格明确：</strong>{{ aiResult.price_clear ? '是' : '否' }}</p>
            <p><strong>可执行性：</strong>{{ aiResult.performable ? '是' : '否' }}</p>
            <p><strong>违约责任：</strong>{{ aiResult.liability }}</p>
            <p><strong>争议解决：</strong>{{ aiResult.dispute }}</p>
          </div>
          <div v-else>{{ aiResult }}</div>
        </div>
      </el-card>
    </div>

    <div class="btn-group">
      <el-button @click="goUpload">重新上传</el-button>
      <el-button type="success" @click="saveContract">添加到系统</el-button>
      <el-button type="danger" @click="goUpload">取消</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import request from '../api/request'
import { ElMessage } from 'element-plus'

const router = useRouter()
const contractText = ref('加载中...')
const aiResult = ref('AI分析中...')

onMounted(async () => {
  try {
    const res = await request.get('/review')
    contractText.value = res.data.text
    aiResult.value = res.data.analysis
  } catch (err) {
    ElMessage.error('获取分析失败')
  }
})

const goUpload = () => router.push('/upload')
const saveContract = async () => {
  try {
    if (typeof aiResult.value === 'object') {
      await request.post('/save_contract', {
        name: '合同文件',   // 可以后面改成真实文件名
        content: contractText.value,
        result: aiResult.value.result,
        subject_ok: aiResult.value.subject_ok,
        object_clear: aiResult.value.object_clear,
        price_clear: aiResult.value.price_clear,
        performable: aiResult.value.performable,
        liability: aiResult.value.liability,
        dispute: aiResult.value.dispute
      })
    } else {
      await request.post('/save_contract', {
        name: '合同文件',
        content: contractText.value,
        result: aiResult.value,
        subject_ok: false,
        object_clear: false,
        price_clear: false,
        performable: false,
        liability: '',
        dispute: ''
      })
    }

    ElMessage.success('已成功保存到系统')
    router.push('/home') // 或跳到列表页
  } catch (err) {
    ElMessage.error('保存失败')
  }
}


</script>

<style scoped>
.review-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  width: 100vw;
  padding: 20px;
  /* 背景边距 */
  background-color: #e6f0ff;
  box-sizing: border-box;
  overflow: hidden;
}

.review-cards {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
  flex-wrap: wrap;
  justify-content: center;
  width: 100%;
}

.card {
  flex: 1 1 45%;
  border-radius: 12px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
  background-color: #fff;
  padding: 30px;
  max-width: 700px;
  /* ⭐ 卡片宽度放大 */
  min-width: 450px;
}

.content-box {
  margin-top: 15px;
  height: 400px;
  /* ⭐ 内容区高度加大 */
  overflow-y: auto;
  background: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
  white-space: pre-wrap;
}

.btn-group {
  display: flex;
  gap: 20px;
}
</style>