<template>
  <div class="page">
    <div class="card">
      <h1 class="title">合同列表</h1>

      <!-- 表格始终显示 -->
      <el-table :data="contracts" style="width: 100%" border empty-text="暂无合同数据">
        <el-table-column prop="name" label="合同名称" />
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column prop="result" label="AI分析结果" />

        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button size="small" @click="viewDetail(scope.row)">
              查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import request from "../api/request"
import { useRouter } from "vue-router"

const contracts = ref([])
const router = useRouter()

const getContracts = async () => {
  try {
    const res = await request.get("/contracts")
    contracts.value = res.data || []
  } catch (e) {
    console.log("接口报错，但页面继续显示", e)

    // ⭐关键：就算报错也给空数组
    contracts.value = []
  }
}

const viewDetail = (row) => {
  router.push({
    path: "/review",
    query: { id: row.id }
  })
}

onMounted(() => {
  getContracts()
})
</script>

<style scoped>
.page {
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, #e0f2ff, #f7faff);
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  width: 85%;
  height: 85%;
  background: #fff;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.title {
  text-align: center;
  font-size: 34px;
  margin-bottom: 30px;
}
</style>