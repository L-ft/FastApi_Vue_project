<template>
  <el-container class="env-detail-container">
    <el-main class="env-detail-main">
      <div class="env-detail-content">
        <h2 style="margin-bottom: 24px;">环境详情</h2>
        <div v-if="env">
          <div style="margin-bottom: 16px;"><strong>环境名称：</strong>{{ env.name }}</div>
          <div style="margin-bottom: 16px;"><strong>环境值：</strong>{{ env.value }}</div>
          <div style="margin-bottom: 16px;"><strong>环境变量：</strong>
            <div v-if="env.variables && env.variables.length">
              <el-table :data="env.variables" style="width: 100%;">
                <el-table-column prop="key" label="变量名" />
                <el-table-column prop="value" label="变量值" />
              </el-table>
            </div>
            <div v-else>暂无环境变量</div>
          </div>
        </div>
        <div v-else>加载中...</div>
      </div>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getEnvironments } from '../api/environmentManage'

const route = useRoute()
const env = ref(null)

onMounted(async () => {
  const res = await getEnvironments()
  const found = res.data.find(e => String(e.id) === String(route.params.id))
  env.value = found || null
})
</script>

<style scoped>
.env-detail-container {
  min-height: 100vh;
  display: flex;
  width: 100%;
  background-color: #f5f7fa;
  padding: 16px;
  gap: 16px;
}
.env-detail-main {
  flex: 1;
  background-color: #f8fafc;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  position: relative;
  transition: all 0.3s ease-in-out;
}
.env-detail-content {
  background: #f8fafc;
  width: 100%;
  padding: 24px;
  min-height: 100%;
}
</style>
