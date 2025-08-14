<template>
  <div class="header-input-section">
    <div class="header-title">
      <span>请求头 Headers</span>
      <div class="header-actions">
        <el-button type="success" size="small" @click="$emit('add-env-var')">
          <template #icon><Setting /></template>
          管理环境变量
        </el-button>
        <el-button type="primary" size="small" @click="addHeader">
          <template #icon><Plus /></template>
          添加Header
        </el-button>
      </div>
    </div>
    
    <div class="header-list" v-if="headers.length > 0">
      <div class="header-list-header">
        <div class="header-col header-key-col">键名</div>
        <div class="header-col header-value-col">键值</div>
        <div class="header-col header-desc-col">描述</div>
        <div class="header-col header-action-col">操作</div>
      </div>
      
      <div v-for="(header, index) in headers" :key="index" class="header-item">
        <div class="header-input-group header-key-col">
          <el-input 
            v-model="header.key" 
            placeholder="请输入Header名称"
            @input="onHeaderChange">
            <template #suffix>
              <el-dropdown @command="(command) => selectEnvVar(index, 'key', command)" trigger="click">
                <el-icon class="env-var-icon" title="选择环境变量">
                  <Setting />
                </el-icon>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item 
                      v-for="envVar in envVariables" 
                      :key="envVar.key"
                      :command="envVar.key">
                      <div class="env-option">
                        <span class="env-key">{{ envVar.key }}</span>
                        <span class="env-desc">{{ envVar.description }}</span>
                      </div>
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
          </el-input>
        </div>
        
        <div class="header-input-group header-value-col">
          <el-input 
            v-model="header.value" 
            placeholder="请输入Header值或使用{{变量名}}"
            @input="onHeaderChange">
            <template #suffix>
              <div class="header-suffix-icons">
                <el-tooltip 
                  v-if="getResolvedValue(header.value) !== header.value"
                  :content="'解析后的值: ' + getResolvedValue(header.value)"
                  placement="top">
                  <el-icon class="resolved-icon">
                    <InfoFilled />
                  </el-icon>
                </el-tooltip>
                <el-dropdown @command="(command) => selectEnvVar(index, 'value', command)" trigger="click">
                  <el-icon class="env-var-icon" title="选择环境变量">
                    <Setting />
                  </el-icon>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item 
                        v-for="envVar in envVariables" 
                        :key="'direct_' + envVar.key"
                        :command="envVar.value">
                        <div class="env-option">
                          <span class="env-key">{{ envVar.key }} (直接值)</span>
                          <span class="env-value">{{ truncateText(envVar.value, 25) }}</span>
                        </div>
                      </el-dropdown-item>
                      <el-divider style="margin: 4px 0;" />
                      <el-dropdown-item 
                        v-for="envVar in envVariables" 
                        :key="'placeholder_' + envVar.key"
                        :command="generatePlaceholder(envVar.key)">
                        <div class="env-option placeholder">
                          <span class="env-placeholder">{{ generatePlaceholder(envVar.key) }}</span>
                          <span class="env-desc">占位符格式</span>
                        </div>
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </template>
          </el-input>
        </div>
        
        <div class="header-input-group header-desc-col">
          <el-input 
            v-model="header.description" 
            placeholder="描述"
            @input="onHeaderChange" />
        </div>
        
        <div class="header-action-col">
          <el-button 
            type="danger" 
            size="small" 
            @click="removeHeader(index)"
            circle>
            <template #icon>
              <Delete />
            </template>
          </el-button>
        </div>
      </div>
    </div>
    
    <!-- 快速添加常用Header -->
    <div class="quick-headers">
      <span>快速添加:</span>
      <el-button 
        v-for="quickHeader in quickHeaders" 
        :key="quickHeader.key"
        size="small" 
        type="text" 
        @click="addQuickHeader(quickHeader)">
        {{ quickHeader.key }}
      </el-button>
    </div>
    
    <!-- 预览解析后的Headers -->
    <div class="resolved-headers" v-if="hasEnvVars">
      <el-collapse>
        <el-collapse-item title="预览解析后的Headers" name="preview">
          <div class="resolved-list">
            <div v-for="(header, index) in resolvedHeaders" :key="index" class="resolved-item">
              <span class="resolved-key">{{ header.key }}:</span>
              <span class="resolved-value">{{ header.value }}</span>
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, watch } from 'vue'
import { Setting, Delete, InfoFilled, Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue', 'add-env-var'])

// 注入环境变量相关数据和方法
const envVariables = inject('envVariables', ref([]))
const replaceEnvVars = inject('replaceEnvVars', (text) => text)

const headers = ref([])

// 生成占位符格式的辅助函数
const generatePlaceholder = (varName) => {
  return `{{${varName}}}`
}

// 初始化headers
const initHeaders = () => {
  if (props.modelValue && props.modelValue.length > 0) {
    headers.value = props.modelValue.map(header => ({
      key: header.key || '',
      value: header.value || '',
      description: header.description || ''
    }))
  } else {
    headers.value = [{ key: '', value: '', description: '' }]
  }
}

const quickHeaders = ref([
  { key: 'Authorization', value: generatePlaceholder('Authorization'), description: '认证令牌' },
  { key: 'Content-Type', value: 'application/json', description: '内容类型' },
  { key: 'User-Agent', value: 'API-Test-Client', description: '用户代理' },
  { key: 'Accept', value: 'application/json', description: '接受类型' },
  { key: 'X-API-Key', value: generatePlaceholder('X-API-Key'), description: 'API密钥' }
])

// 计算解析后的Headers
const resolvedHeaders = computed(() => {
  return headers.value.map(header => ({
    key: replaceEnvVars(header.key),
    value: replaceEnvVars(header.value),
    description: header.description
  })).filter(header => header.key.trim() !== '')
})

// 检查是否有环境变量占位符
const hasEnvVars = computed(() => {
  return headers.value.some(header => 
    (header.key && header.key.includes('{{')) || 
    (header.value && header.value.includes('{{'))
  )
})

// 添加新的Header
const addHeader = () => {
  headers.value.push({ key: '', value: '', description: '' })
  updateModelValue()
}

// 删除Header
const removeHeader = (index) => {
  if (headers.value.length <= 1) {
    // 如果只有一个，清空而不是删除
    headers.value[0] = { key: '', value: '', description: '' }
  } else {
    headers.value.splice(index, 1)
  }
  updateModelValue()
}

// 快速添加Header
const addQuickHeader = (quickHeader) => {
  // 检查是否已存在相同的key
  const existingIndex = headers.value.findIndex(h => h.key === quickHeader.key)
  if (existingIndex > -1) {
    // 如果存在，直接替换
    headers.value[existingIndex] = { ...quickHeader }
    ElMessage.success('Header已替换')
  } else {
    // 如果不存在，添加新的
    // 如果最后一行是空的，替换它
    const lastHeader = headers.value[headers.value.length - 1]
    if (lastHeader && !lastHeader.key && !lastHeader.value) {
      headers.value[headers.value.length - 1] = { ...quickHeader }
    } else {
      headers.value.push({ ...quickHeader })
    }
    ElMessage.success('Header已添加')
  }
  updateModelValue()
}

// 选择环境变量
const selectEnvVar = (index, field, value) => {
  if (field === 'key') {
    headers.value[index].key = value
    // 自动匹配对应的环境变量值
    const envVar = envVariables.value.find(env => env.key === value)
    if (envVar && !headers.value[index].value) {
      headers.value[index].value = generatePlaceholder(envVar.key)
      headers.value[index].description = envVar.description
    }
  } else if (field === 'value') {
    headers.value[index].value = value
  }
  updateModelValue()
}

// Header变化处理
const onHeaderChange = () => {
  updateModelValue()
}

// 更新父组件的值
const updateModelValue = () => {
  // 过滤掉完全空的header，但保留至少一个空行用于输入
  const validHeaders = headers.value.filter(h => h.key.trim() !== '' || h.value.trim() !== '')
  
  // 确保至少有一个空行供用户输入
  if (validHeaders.length === 0 || 
      (validHeaders[validHeaders.length - 1].key.trim() !== '' || 
       validHeaders[validHeaders.length - 1].value.trim() !== '')) {
    // 如果没有空行或最后一行不是空的，确保headers数组有空行
    const hasEmptyRow = headers.value.some(h => h.key.trim() === '' && h.value.trim() === '')
    if (!hasEmptyRow) {
      headers.value.push({ key: '', value: '', description: '' })
    }
  }
  
  emit('update:modelValue', validHeaders)
}

// 获取解析后的值
const getResolvedValue = (value) => {
  return replaceEnvVars(value)
}

// 截断文本
const truncateText = (text, maxLength) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

// 监听props变化
watch(() => props.modelValue, (newValue) => {
  if (newValue && Array.isArray(newValue)) {
    headers.value = newValue.map(header => ({
      key: header.key || '',
      value: header.value || '',
      description: header.description || ''
    }))
    
    // 确保至少有一个空行
    const hasEmptyRow = headers.value.some(h => h.key.trim() === '' && h.value.trim() === '')
    if (!hasEmptyRow) {
      headers.value.push({ key: '', value: '', description: '' })
    }
  } else {
    headers.value = [{ key: '', value: '', description: '' }]
  }
}, { deep: true, immediate: true })

// 初始化
initHeaders()
</script>

<style scoped>
.header-input-section {
  margin: 16px 0;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  background: #fafbfc;
}

.header-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  font-weight: 500;
  font-size: 16px;
  color: #303133;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-list {
  background: white;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
  overflow: hidden;
}

.header-list-header {
  display: flex;
  background-color: #f5f7fa;
  padding: 12px;
  font-weight: 600;
  color: #606266;
  border-bottom: 1px solid #e4e7ed;
}

.header-item {
  display: flex;
  padding: 8px 12px;
  border-bottom: 1px solid #f0f0f0;
  align-items: center;
}

.header-item:last-child {
  border-bottom: none;
}

.header-col {
  padding: 0 4px;
}

.header-key-col {
  flex: 0 0 25%;
  min-width: 150px;
}

.header-value-col {
  flex: 0 0 40%;
  min-width: 200px;
}

.header-desc-col {
  flex: 0 0 25%;
  min-width: 120px;
}

.header-action-col {
  flex: 0 0 10%;
  min-width: 60px;
  display: flex;
  justify-content: center;
}

.header-input-group {
  position: relative;
  width: 100%;
}

.header-suffix-icons {
  display: flex;
  align-items: center;
  gap: 4px;
}

.env-var-icon {
  cursor: pointer;
  color: #409EFF;
  padding: 2px;
  transition: all 0.3s ease;
}

.env-var-icon:hover {
  color: #66b1ff;
  background-color: #f0f9ff;
  border-radius: 2px;
}

.resolved-icon {
  color: #67C23A;
  cursor: help;
}

.env-option {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  padding: 4px 0;
}

.env-key {
  font-weight: 500;
  color: #303133;
  font-size: 13px;
}

.env-value, .env-desc {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}

.env-placeholder {
  font-family: monospace;
  color: #E6A23C;
  font-weight: 500;
  font-size: 12px;
}

.placeholder .env-desc {
  color: #F56C6C;
}

.quick-headers {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #e6e6e6;
}

.quick-headers span {
  margin-right: 8px;
  color: #666;
  font-size: 13px;
  font-weight: 500;
}

.resolved-headers {
  margin-top: 16px;
}

.resolved-list {
  background-color: #f8f9fa;
  padding: 12px;
  border-radius: 4px;
  border: 1px solid #e9ecef;
}

.resolved-item {
  display: flex;
  margin-bottom: 4px;
  font-family: 'Courier New', monospace;
  font-size: 13px;
}

.resolved-item .resolved-key {
  font-weight: 500;
  color: #495057;
  margin-right: 8px;
  min-width: 120px;
}

.resolved-item .resolved-value {
  color: #28a745;
  word-break: break-all;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-title {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .header-actions {
    justify-content: flex-end;
  }
  
  .header-list-header,
  .header-item {
    flex-direction: column;
    gap: 8px;
  }
  
  .header-col {
    flex: 1;
    min-width: unset;
  }
  
  .quick-headers {
    text-align: center;
  }
  
  .quick-headers span {
    display: block;
    margin-bottom: 8px;
  }
}
</style>
