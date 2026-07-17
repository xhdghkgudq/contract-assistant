<template>
  <el-container style="height: 100vh">
    <!-- 左侧菜单 -->
    <el-aside width="200px" style="background: #304156; color: #fff">
      <h3 style="text-align:center; padding:20px">合同系统</h3>

      <el-menu router background-color="#304156" text-color="#fff">
        <el-menu-item index="/home">
          首页
        </el-menu-item>

        <el-menu-item index="/home/upload">
          合同上传
        </el-menu-item>

        <el-menu-item index="/home/review">
          合同分析
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 右侧内容 -->
    <el-container>
      <el-header style="background:#fff">
        <span>欢迎进入系统</span>
      </el-header>

      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>