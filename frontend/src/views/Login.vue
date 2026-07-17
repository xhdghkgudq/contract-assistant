<template>
  <div class="login-wrapper">
    <div class="login-card">

      <!-- 左侧 -->
      <div class="left">
        <div class="overlay">
          <h1>欢迎使用</h1>
          <p>智能合同管理系统</p>
        </div>
      </div>

      <!-- 右侧 -->
      <div class="right">
        <h2 class="title">登录</h2>

        <el-input v-model="username" placeholder="请输入账号" size="large" />

        <el-input v-model="password" type="password" placeholder="请输入密码" size="large" show-password />

        <el-button type="primary" class="login-btn" size="large" @click="login">
          登 录
        </el-button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { loginApi } from '../api/user'
import { ElMessage } from 'element-plus'

const username = ref('')
const password = ref('')
const router = useRouter()

const login = async () => {
  if (!username.value || !password.value) {
    ElMessage.warning('请输入账号和密码')
    return
  }

  try {
    const res = await loginApi({
      username: username.value,
      password: password.value
    })

    localStorage.setItem('token', res.data.token)
    localStorage.setItem('user', JSON.stringify(res.data.user))

    ElMessage.success('登录成功')
    router.push('/home')

  } catch (err) {
    ElMessage.error('用户名或密码错误')
  }
}
</script>

<style scoped>
/* 整体背景 */
.login-wrapper {
  height: 100vh;
  background: #b7c7da;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 卡片 */
.login-card {
  width: 900px;
  height: 500px;
  display: flex;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

/* 左侧 */
.left {
  width: 50%;
  background: url('https://images.unsplash.com/photo-1497366216548-37526070297c') no-repeat center/cover;
  position: relative;
}

/* 蓝色遮罩 */
.overlay {
  width: 100%;
  height: 100%;
  background: rgba(64, 158, 255, 0.6);
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/* 标题 */
.overlay h1 {
  font-size: 36px;
  margin-bottom: 10px;
}

.overlay p {
  font-size: 16px;
}

/* 右侧 */
.right {
  width: 50%;
  background: #fff;
  padding: 60px 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* 登录标题 */
.title {
  text-align: center;
  margin-bottom: 40px;
}

/* 输入框间距 */
.el-input {
  margin-bottom: 20px;
}

/* 按钮 */
.login-btn {
  width: 100%;
  border-radius: 25px;
}
</style>