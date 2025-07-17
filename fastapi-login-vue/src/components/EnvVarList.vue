<template>
  <div class="env-var-list">
    <h3 style="margin-bottom: 24px;">环境变量列表</h3>
    <el-table :data="envVarData" style="width: 100%;">
      <el-table-column prop="envName" label="环境名称" />
      <el-table-column prop="key" label="变量名" />
      <el-table-column prop="value" label="变量值" />
      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="mini" @click="editVar(scope.row)">编辑</el-button>
          <el-button size="mini" type="danger" @click="deleteVar(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div style="text-align:right; margin-top:16px;">
      <el-button type="primary" @click="addVar">新增变量</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
// 示例数据，实际请从后端获取
const envVarData = ref([
  { envName: '测试', key: 'API_KEY', value: '123456' },
  { envName: '生产', key: 'BASE_URL', value: 'https://api.xxx.com' }
])
const addVar = () => {
  // 新增变量逻辑
}
const editVar = (row) => {
  // 编辑变量逻辑
}
const deleteVar = (row) => {
  // 删除变量逻辑
}
</script>

<style scoped>
.env-var-list {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 24px;
}
</style>
