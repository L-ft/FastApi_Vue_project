<template>
  <el-container class="app-container">
    <el-main class="main-content">
      <div class="detail-wrapper">
        <el-card class="detail-card">
          <div class="detail-header">
            <span class="detail-title">H5获取token（成功）</span>
            <el-button type="primary" style="float:right">发送</el-button>
            <el-button style="float:right; margin-right:10px">保存</el-button>
            <el-button style="float:right; margin-right:10px">删除</el-button>
          </div>
          <el-tabs v-model="activeTab" class="detail-tabs">
            <el-tab-pane label="Params" name="params">
              <el-table :data="params" style="width:100%">
                <el-table-column prop="name" label="参数名" />
                <el-table-column prop="value" label="参数值" />
                <el-table-column prop="type" label="类型" />
                <el-table-column prop="desc" label="说明" />
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="Body" name="body">
              <el-input type="textarea" :rows="10" v-model="body" />
            </el-tab-pane>
            <el-tab-pane label="Header" name="header">
              <el-table :data="headers" style="width:100%">
                <el-table-column prop="name" label="名称" />
                <el-table-column prop="value" label="值" />
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="实际请求" name="request">
              <el-card>
                <div class="request-info">
                  <div>POST {{ url }}</div>
                  <div>耗时：{{ responseTime }} ms</div>
                  <div>状态：<span style="color:green">成功 ({{ statusCode }})</span></div>
                </div>
                <el-input type="textarea" :rows="10" v-model="response" />
              </el-card>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </div>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeTab = ref('params')
const url = ref('https://zmp-test1.nbm2m.com/api/auth/oauth/token')
const responseTime = ref(479)
const statusCode = ref(200)
const response = ref(`{
  "code": "200",
  "msg": "SUCCESS",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "tokenHead": "Bearer ",
    "expiresIn": "43199",
    "userId": "0",
    "exp": "0",
    "cldentity": "WWSB11132",
    "nb": "0",
    "jti": "16574d24-8063-4f24-b025-de1505978f57",
    "cldentityList": "0"
  },
  "success": true
}`)
const params = ref([
  { name: 'cldentity', value: 'WWSB11132', type: 'array', desc: '' },
  { name: 'grant_type', value: 'device', type: 'string', desc: '' },
  { name: 'client_id', value: 'zmp-h5', type: 'string', desc: '' },
  { name: 'client_secret', value: 'VIIA38m0G2YwGagS', type: 'string', desc: '' },
  { name: 'path', value: 'https%3A%2F%2Fzmp-test1.nbm2m.com', type: 'string', desc: '' }
])
const headers = ref([
  { name: 'tokenHead', value: 'Bearer' },
  { name: 'expiresIn', value: '43199' },
  { name: 'userId', value: '0' },
  { name: 'exp', value: '0' },
  { name: 'cldentity', value: 'WWSB11132' },
  { name: 'nb', value: '0' },
  { name: 'jti', value: '16574d24-8063-4f24-b025-de1505978f57' },
  { name: 'cldentityList', value: '0' }
])
const body = ref('')
</script>

<style scoped>
.detail-wrapper {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  margin-top: 30px;
}
.detail-card {
  width: 1000px;
  min-height: 600px;
  box-shadow: 0 2px 8px #f0f1f2;
  border-radius: 8px;
}
.detail-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
.detail-title {
  font-size: 20px;
  font-weight: bold;
  margin-right: 20px;
}
.detail-tabs {
  margin-top: 10px;
}
.request-info {
  margin-bottom: 10px;
  font-size: 15px;
}
</style>
