<template>
  <div class="upload-wrapper">
    <el-card class="upload-card">
      <h1>上传合同</h1>
      <el-upload :show-file-list="false" :http-request="customUpload" class="upload-area">
        <el-button type="primary" class="upload-btn">点击上传合同</el-button>
      </el-upload>
      <div v-if="fileName" class="upload-success">
        <p>已上传：{{ fileName }}</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import request from '../api/request'
import { ElMessage } from 'element-plus'

const router = useRouter()
const fileName = ref('')

const customUpload = async (options) => {
  const file = options.file
  const formData = new FormData()
  formData.append('file', file)
  try {
    await request.post('/upload', formData)
    fileName.value = file.name
    ElMessage.success('上传成功')
    router.push('/review')
  } catch (err) {
    ElMessage.error('上传失败')
  }
}
</script>

<style scoped>
/* 全屏背景 + 去滚动条 */
html,
body,
#app {
  height: 100%;
  margin: 0;
  overflow: hidden;
  /* 取消滚动条 */
  background-color: #e6f0ff;
  font-family: "Microsoft YaHei", sans-serif;
}

.upload-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}

.upload-card {
  width: 100%;
  max-width: 700px;
  padding: 80px 60px;
  text-align: center;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  background-color: #fff;
}

.upload-card h1 {
  font-size: 32px;
  /* 放大标题 */
  font-weight: 600;
  margin-bottom: 40px;
}

.upload-btn {
  background-color: #3578e5;
  color: #fff;
  border-radius: 8px;
  padding: 16px 50px;
  /* 放大按钮 */
  font-size: 18px;
}

.upload-btn:hover {
  background-color: #285bb5;
}

.upload-success {
  margin-top: 30px;
  font-size: 18px;
  font-weight: 500;
}
</style>