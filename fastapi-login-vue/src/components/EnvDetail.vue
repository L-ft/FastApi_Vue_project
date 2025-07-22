<template>
  <el-container class="env-detail-container">
    <el-main class="env-detail-main">
      <div class="env-detail-content">
        <h2 style="margin-bottom: 24px;">环境详情</h2>
        <div v-if="env">
          <div style="margin-bottom: 16px;"><strong>环境名称：</strong>{{ env.name }}</div>
          <div style="margin-bottom: 16px;"><strong>环境值：</strong>{{ env.value }}</div>
          <div style="margin-bottom: 16px;"><strong>环境变量：</strong>
            <div v-if="envVariables && envVariables.length">
              <el-table :data="envVariables" style="width: 100%;">
                <el-table-column prop="key" label="变量名" />
                <el-table-column prop="value" label="变量值" />
                <el-table-column label="所属环境">
                  <template #default="scope">
                    {{ getEnvironmentName(scope.row.env_id) }}
                  </template>
                </el-table-column>
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
import { getEnvironments, getEnvironmentVariables } from '../api/environmentManage'

const route = useRoute()
const env = ref(null)
const envVariables = ref([])
const environmentList = ref([])

const getEnvironmentName = (envId) => {
  if (!envId) return '-';
  const environment = environmentList.value.find(e => e.id === envId);
  return environment ? environment.name : `环境ID: ${envId}`;
}

onMounted(async () => {
  try {
    // 加载环境列表
    const envRes = await getEnvironments()
    environmentList.value = envRes.data || []
    
    // 找到当前环境
    const found = environmentList.value.find(e => String(e.id) === String(route.params.id))
    env.value = found || null
    
    // 加载环境变量列表
    const varRes = await getEnvironmentVariables()
    const allVariables = varRes.data || []
    
    // 筛选当前环境的变量
    if (route.params.id) {
      envVariables.value = allVariables.filter(v => String(v.env_id) === String(route.params.id))
    } else {
      envVariables.value = allVariables
    }
  } catch (error) {
    console.error('Failed to load environment details:', error)
  }
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
