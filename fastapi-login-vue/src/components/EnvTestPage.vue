<template>
  <div class="env-test-page">
    <h2>环境变量测试页面</h2>
    
    <!-- 当前环境变量显示 -->
    <el-card class="env-variables-card" header="当前环境变量">
      <div v-if="envVariables.length > 0">
        <div v-for="env in envVariables" :key="env.key" class="env-item">
          <strong>{{ env.key }}:</strong> {{ env.value }}
          <span v-if="env.description" class="env-desc">（{{ env.description }}）</span>
        </div>
      </div>
      <div v-else class="no-env">暂无环境变量</div>
    </el-card>

    <!-- 环境变量替换测试 -->
    <el-card class="test-card" header="环境变量替换测试">
      <el-form label-position="top">
        <el-form-item label="输入包含环境变量的文本（使用 {{变量名}} 格式）">
          <el-input
            v-model="testText"
            type="textarea"
            :rows="3"
            placeholder="例如: {{base_url}}/api/users?token={{Authorization}}"
          />
        </el-form-item>
        
        <el-form-item label="替换结果">
          <div class="result-area">
            <pre>{{ resolvedText }}</pre>
          </div>
        </el-form-item>

        <el-form-item label="占位符分析">
          <div class="placeholders-analysis">
            <div v-for="placeholder in placeholders" :key="placeholder.varName" class="placeholder-item">
              <span class="placeholder-name">{{ placeholder.full }}</span>
              <span :class="['placeholder-status', placeholder.hasValue ? 'valid' : 'invalid']">
                {{ placeholder.hasValue ? '✓ 有效' : '✗ 无效' }}
              </span>
              <span v-if="placeholder.hasValue" class="placeholder-value">
                → {{ placeholder.resolvedValue }}
              </span>
            </div>
          </div>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Header测试 -->
    <el-card class="test-card" header="Header格式测试">
      <HeaderInput v-model="testHeaders" @add-env-var="handleAddEnvVar" />
      
      <el-divider>转换结果</el-divider>
      
      <div class="headers-result">
        <h4>对象格式 Headers:</h4>
        <pre>{{ JSON.stringify(headersObject, null, 2) }}</pre>
      </div>
    </el-card>

    <!-- 完整请求测试 -->
    <el-card class="test-card" header="完整请求测试">
      <el-form label-position="top">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="请求方法">
              <el-select v-model="testRequest.method" style="width: 100%">
                <el-option label="GET" value="GET" />
                <el-option label="POST" value="POST" />
                <el-option label="PUT" value="PUT" />
                <el-option label="DELETE" value="DELETE" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="18">
            <el-form-item label="请求地址">
              <el-input v-model="testRequest.url" placeholder="例如: {{base_url}}/api/users" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="环境变量测试请求头">
          <HeaderInput v-model="testRequest.headers" />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="previewRequest">预览请求配置</el-button>
          <el-button type="success" @click="sendTestRequest" :loading="testLoading">发送测试请求</el-button>
        </el-form-item>
        
        <!-- 请求预览 -->
        <el-form-item v-if="requestPreview" label="请求预览">
          <div class="request-preview">
            <h4>解析后的请求配置:</h4>
            <pre>{{ JSON.stringify(requestPreview, null, 2) }}</pre>
          </div>
        </el-form-item>
        
        <!-- 响应结果 -->
        <el-form-item v-if="testResponse" label="响应结果">
          <div class="response-result">
            <div class="response-status">
              状态: {{ testResponse.status }} | 
              耗时: {{ testResponse.time }}ms | 
              大小: {{ testResponse.size }}
            </div>
            <div class="response-body">
              <pre>{{ testResponse.data }}</pre>
            </div>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import HeaderInput from './HeaderInput.vue'

// 注入环境变量相关功能
const envVariables = inject('envVariables', ref([]))
const envUtils = inject('envUtils', null)

const testText = ref('{{base_url}}/api/users?authorization={{Authorization}}&content-type={{Content-Type}}')
const testHeaders = ref([
  { key: 'Authorization', value: '{{Authorization}}', description: '认证令牌' },
  { key: 'Content-Type', value: '{{Content-Type}}', description: '内容类型' },
  { key: 'X-API-Key', value: '{{X-API-Key}}', description: 'API密钥' }
])

// 完整请求测试相关
const testRequest = ref({
  method: 'GET',
  url: '{{base_url}}/api/users',
  headers: [
    { key: 'Authorization', value: '{{Authorization}}', description: '认证令牌' },
    { key: 'Content-Type', value: 'application/json', description: '内容类型' }
  ]
})
const requestPreview = ref(null)
const testResponse = ref(null)
const testLoading = ref(false)

// 计算替换后的文本
const resolvedText = computed(() => {
  if (!envUtils) return testText.value
  return envUtils.replaceVariables(testText.value)
})

// 计算占位符分析
const placeholders = computed(() => {
  if (!envUtils) return []
  const preview = envUtils.previewReplacement(testText.value)
  return preview.placeholders
})

// 计算Headers对象格式
const headersObject = computed(() => {
  if (!envUtils) return {}
  return envUtils.convertHeadersArrayToObject(testHeaders.value)
})

const handleAddEnvVar = () => {
  console.log('跳转到环境变量管理页面')
}

// 预览请求配置
const previewRequest = () => {
  if (!envUtils) {
    requestPreview.value = { error: 'envUtils 未初始化' }
    return
  }
  
  const resolvedUrl = envUtils.replaceVariables(testRequest.value.url)
  const resolvedHeaders = envUtils.convertHeadersArrayToObject(testRequest.value.headers)
  
  requestPreview.value = {
    method: testRequest.value.method,
    url: resolvedUrl,
    headers: resolvedHeaders,
    original: {
      url: testRequest.value.url,
      headers: testRequest.value.headers
    }
  }
}

// 发送测试请求
const sendTestRequest = async () => {
  if (!envUtils) {
    ElMessage.error('envUtils 未初始化')
    return
  }
  
  testLoading.value = true
  testResponse.value = null
  
  try {
    const resolvedUrl = envUtils.replaceVariables(testRequest.value.url)
    const resolvedHeaders = envUtils.convertHeadersArrayToObject(testRequest.value.headers)
    
    console.log('=== 发送测试请求 ===')
    console.log('URL:', resolvedUrl)
    console.log('方法:', testRequest.value.method)
    console.log('请求头:', resolvedHeaders)
    
    const start = Date.now()
    
    // 这里使用axios直接发送请求到解析后的完整URL
    const response = await axios({
      url: resolvedUrl,
      method: testRequest.value.method.toLowerCase(),
      headers: resolvedHeaders,
      timeout: 10000
    })
    
    const endTime = Date.now() - start
    
    testResponse.value = {
      status: response.status,
      time: endTime,
      size: response.headers['content-length'] ? 
        response.headers['content-length'] + ' B' : 
        (typeof response.data === 'string' ? new Blob([response.data]).size + ' B' : '未知'),
      data: typeof response.data === 'object' ? 
        JSON.stringify(response.data, null, 2) : 
        response.data
    }
    
    ElMessage.success(`请求成功 (${endTime}ms)`)
    
  } catch (error) {
    console.error('测试请求失败:', error)
    
    const endTime = Date.now() - (testLoading.value ? 0 : Date.now())
    
    testResponse.value = {
      status: error.response?.status || '网络错误',
      time: endTime,
      size: error.response?.headers?.['content-length'] || '0 B', 
      data: error.response?.data ? 
        (typeof error.response.data === 'object' ? 
          JSON.stringify(error.response.data, null, 2) : 
          error.response.data) :
        error.message
    }
    
    ElMessage.error(`请求失败: ${error.message}`)
  } finally {
    testLoading.value = false
  }
}
</script>

<style scoped>
.env-test-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.env-variables-card,
.test-card {
  margin-bottom: 20px;
}

.env-item {
  margin-bottom: 8px;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.env-desc {
  color: #909399;
  font-size: 12px;
}

.no-env {
  color: #909399;
  text-align: center;
  padding: 20px;
}

.result-area {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 12px;
  min-height: 80px;
}

.result-area pre {
  margin: 0;
  font-family: 'Courier New', monospace;
  color: #28a745;
  white-space: pre-wrap;
  word-break: break-all;
}

.placeholders-analysis {
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 12px;
  background-color: #fafbfc;
}

.placeholder-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  padding: 6px;
  background-color: white;
  border-radius: 3px;
}

.placeholder-name {
  font-family: monospace;
  background-color: #e6f3ff;
  padding: 2px 6px;
  border-radius: 3px;
  margin-right: 8px;
}

.placeholder-status {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  margin-right: 8px;
}

.placeholder-status.valid {
  background-color: #f0f9ff;
  color: #67c23a;
}

.placeholder-status.invalid {
  background-color: #fef0f0;
  color: #f56c6c;
}

.placeholder-value {
  font-family: monospace;
  color: #606266;
}

.headers-result {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 12px;
}

.headers-result h4 {
  margin-top: 0;
  margin-bottom: 8px;
  color: #303133;
}

.headers-result pre {
  margin: 0;
  font-family: 'Courier New', monospace;
  color: #495057;
  background-color: white;
  padding: 8px;
  border-radius: 3px;
  border: 1px solid #dee2e6;
}

.request-preview {
  background-color: #f0f9ff;
  padding: 15px;
  border-radius: 4px;
  border: 1px solid #b3d8ff;
}

.request-preview h4 {
  margin-top: 0;
  color: #409eff;
}

.request-preview pre {
  background-color: white;
  padding: 12px;
  border-radius: 3px;
  border: 1px solid #b3d8ff;
  margin: 0;
  font-family: 'Courier New', monospace;
  font-size: 13px;
}

.response-result {
  background-color: #f6f8fa;
  padding: 15px;
  border-radius: 4px;
  border: 1px solid #d0d7de;
}

.response-status {
  background-color: #e6f7ff;
  padding: 8px 12px;
  border-radius: 3px;
  margin-bottom: 10px;
  font-weight: bold;
  color: #303133;
}

.response-body {
  background-color: white;
  padding: 12px;
  border-radius: 3px;
  border: 1px solid #d0d7de;
}

.response-body pre {
  margin: 0;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.4;
  max-height: 400px;
  overflow-y: auto;
}
</style>
