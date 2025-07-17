<template>
  <el-container class="app-container">
    <el-main class="main-content">
      <!-- 接口管理页面 -->
      <div class="content-wrapper">
        <div class="header-section">
          <div class="left-section">
            <el-select v-model="selectedGroup" placeholder="选择分组" style="width: 180px" @change="fetchApis">
              <el-option label="全部分组" :value="null" />
              <el-option v-for="g in groups" :key="g.id" :label="g.name" :value="g.id" />
            </el-select>
            <el-input
              v-model="search"
              placeholder="搜索接口名称/URL"
              style="width: 220px; margin-left: 10px"
              clearable
              @keyup.enter="handleSearch"
            />
            <el-button type="primary" style="margin-left: 10px;" @click="handleSearch">查询</el-button>
          </div>
          <div class="right-section">
            <el-button type="primary" @click="openApiForm()">新增接口</el-button>
          </div>
        </div>
        <div class="table-section" style="overflow-x:auto;">
          <el-table :data="pagedApiList" :border="false" style="min-width: 900px; width: auto; table-layout: auto;">
            <el-table-column prop="name" label="名称" min-width="120" />
            <el-table-column prop="url" label="URL" min-width="180" />
            <el-table-column prop="method" label="方法" min-width="80" />
            <el-table-column prop="group_name" label="分组" min-width="100" />
            <el-table-column prop="env_name" label="所属环境" min-width="100" />
            <el-table-column prop="description" label="描述" min-width="180" />
            <el-table-column label="操作" min-width="180" fixed="right">
              <template #default="scope">
                <el-button size="mini" @click="editApi(scope.row)">编辑</el-button>
                <el-button size="mini" type="danger" @click="handleDeleteApi(scope.row.id)">删除</el-button>
                <el-button size="mini" type="success" style="color: #222;" @click="runApi(scope.row)">运行</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="apiPage"
              :page-size="apiPageSize"
              :total="pagedApis.length"
              layout="prev, pager, next"
              :small="isSmallScreen"
            />
          </div>
        </div>
      </div>
      
      <!-- 添加/编辑接口对话框 -->
      <el-dialog 
        v-model="apiDialogVisible" 
        :title="isEdit ? '编辑接口' : '新增接口'" 
        width="500px" 
        :close-on-click-modal="false"
        class="api-dialog"
        destroy-on-close
      >
        <el-form 
          :model="apiForm" 
          label-position="top" 
          class="api-form"
          :validate-on-rule-change="false"
        >
          <div class="form-content">
            <el-form-item 
              label="接口名称" 
              required
              prop="name"
            >
              <el-input 
                v-model="apiForm.name" 
                placeholder="例如：获取用户详情" 
              />
            </el-form-item>

            <el-row :gutter="16">
              <el-col :span="10">
                <el-form-item 
                  label="请求方法" 
                  required
                  prop="method"
                >
                  <el-select 
                    v-model="apiForm.method" 
                    placeholder="选择方法"
                    class="full-width"
                  >
                    <el-option label="GET" value="GET" class="method-option" />
                    <el-option label="POST" value="POST" class="method-option" />
                    <el-option label="PUT" value="PUT" class="method-option" />
                    <el-option label="DELETE" value="DELETE" class="method-option" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item 
                  label="所属环境" 
                  prop="env_id"
                >
                  <el-select 
                    v-model="apiForm.env_id" 
                    placeholder="选择环境"
                    class="full-width"
                  >
                    <el-option 
                      v-for="e in envs" 
                      :key="e.id" 
                      :label="e.name" 
                      :value="e.id" 
                    />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item 
                  label="所属分组" 
                  required
                  prop="group_id"
                >
                  <el-select 
                    v-model="apiForm.group_id" 
                    placeholder="选择分组"
                    class="full-width"
                  >
                    <el-option 
                      v-for="g in groups" 
                      :key="g.id" 
                      :label="g.name" 
                      :value="g.id" 
                    />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item 
              label="接口路径" 
              required
              prop="url"
            >
              <el-input 
                v-model="apiForm.url" 
                placeholder="/api/v1/users/:id"
                class="monospace-input" 
              />
            </el-form-item>

            <el-form-item 
              label="接口描述"
              prop="description"
              class="mb-0"
            >
              <el-input 
                v-model="apiForm.description" 
                type="textarea" 
                :rows="3" 
                placeholder="请描述接口的用途、参数要求等"
                resize="none"
              />
            </el-form-item>
          </div>
        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="apiDialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="submitApiForm">确 定</el-button>
          </div>
        </template>
      </el-dialog>

      <!-- 接口调试对话框 -->
      <el-dialog 
        v-model="debugDialogVisible" 
        title="接口调试" 
        :width="dialogWidth"
        class="debug-dialog"
        :close-on-click-modal="false"
        destroy-on-close
      >
        <el-form label-position="top">
          <!-- 请求方法选择 -->
          <el-form-item label="请求方法">
            <el-select v-model="debugMethod" style="width: 120px">
              <el-option label="GET" value="GET" />
              <el-option label="POST" value="POST" />
              <el-option label="PUT" value="PUT" />
              <el-option label="DELETE" value="DELETE" />
            </el-select>
          </el-form-item>
          <!-- 请求地址输入 -->
          <el-form-item label="请求地址">
            <el-input v-model="debugUrl" placeholder="请输入请求地址" />
          </el-form-item>
          <!-- 参数类型选择 -->
          <el-form-item label="参数类型">
            <div class="param-type-selector">
              <el-radio-group v-model="debugParamType">
                <el-radio label="params">Params</el-radio>
                <el-radio label="json">JSON</el-radio>
                <el-radio label="form">Form</el-radio>
              </el-radio-group>
            </div>
          </el-form-item>

          <!-- 请求参数表格 -->
          <el-form-item v-if="debugParamType === 'params'" label="请求参数 (key=value, 多行)">
            <div class="param-table">
              <div class="param-table-header">
                <div class="param-col param-name">参数名</div>
                <div class="param-col param-value">参数值</div>
                <div class="param-col param-type">类型</div>
                <div class="param-col param-desc">说明</div>
                <div class="param-col param-action">操作</div>
              </div>
              <div class="param-table-body">
                <div v-for="(item, index) in debugParamsList" :key="index" class="param-row">
                  <el-input v-model="item.key" class="param-name" placeholder="参数名" size="default" />
                  <el-input v-model="item.value" class="param-value" placeholder="参数值" size="default" />
                  <el-select v-model="item.type" class="param-type" size="default" placeholder="类型">
                    <el-option label="string" value="string" />
                    <el-option label="number" value="number" />
                    <el-option label="boolean" value="boolean" />
                    <el-option label="array" value="array" />
                  </el-select>
                  <el-input v-model="item.desc" class="param-desc" placeholder="说明" size="default" />
                  <div class="param-action">
                    <el-button 
                      type="danger" 
                      circle 
                      size="small"
                      @click="removeParam(index)"
                    >
                      <el-icon><Delete /></el-icon>
                    </el-button>
                  </div>
                </div>
              </div>
              <div class="param-add-btn">
                <el-button type="primary" plain @click="addParam">
                  <el-icon><Plus /></el-icon>
                  添加参数
                </el-button>
              </div>
            </div>
          </el-form-item>

          <!-- JSON参数输入 -->
          <el-form-item v-if="debugParamType === 'json'" label="请求体 (JSON)">
            <el-input
              v-model="debugJson"
              type="textarea"
              :rows="4"
              placeholder="请输入JSON格式的请求体"
            />
          </el-form-item>

          <!-- Form参数输入 -->
          <el-form-item v-if="debugParamType === 'form'" label="Form Data">
            <el-input
              v-model="debugForm"
              type="textarea"
              :rows="4"
              placeholder="请输入key=value格式的表单数据，每行一个"
            />
          </el-form-item>

          <!-- Header输入 -->
          <el-form-item label="请求Header (JSON)">
            <el-input
              v-model="debugHeaders"
              type="textarea"
              :rows="3"
              placeholder="如: {&quot;Authorization&quot;: &quot;Bearer xxx&quot;}"
            />
          </el-form-item>

          <!-- 发送请求按钮 -->
          <el-form-item>
            <el-button type="primary" @click="doDebugRequest">发送请求</el-button>
          </el-form-item>

          <!-- 响应结果部分 -->
          <el-form-item label="响应结果">
            <div class="response-panel">
              <div class="response-header">
                <el-tabs v-model="activeTab">
                  <el-tab-pane label="Body" name="body">
                    <div class="body-tab-content">
                      <div class="view-options">
                        <el-radio-group v-model="responseViewType" size="small">
                          <el-radio-button label="pretty">Pretty</el-radio-button>
                          <el-radio-button label="raw">Raw</el-radio-button>
                          <el-radio-button label="preview">Preview</el-radio-button>
                          <el-radio-button label="visualize">Visualize</el-radio-button>
                        </el-radio-group>
                      </div>
                      <div class="response-status">
                        <template v-if="debugStatus">状态码: <span :class="{'success-status': debugStatus === 200}">{{debugStatus}}</span></template>
                        <template v-if="debugTime"> 耗时: {{debugTime}}ms</template>
                        <template v-if="debugSize"> 大小: {{debugSize}}</template>
                      </div>
                    </div>
                  </el-tab-pane>
                  <el-tab-pane label="Cookie" name="cookie" />
                  <el-tab-pane label="Header" name="header" />
                </el-tabs>
              </div>
              
              <div class="response-content">
                <template v-if="activeTab === 'body'">
                  <div v-show="responseViewType === 'pretty'" class="response-view">
                    <pre v-if="debugResult" class="json-content"><code v-html="highlightedJson(debugResult)"></code></pre>
                    <div v-else class="empty-content">暂无内容</div>
                  </div>
                  <div v-show="responseViewType === 'raw'" class="response-view">
                    <pre class="raw-content">{{debugResult || '暂无内容'}}</pre>
                  </div>
                  <div v-show="responseViewType === 'preview'" class="response-view">
                    <div class="empty-content">暂不支持</div>
                  </div>
                  <div v-show="responseViewType === 'visualize'" class="response-view">
                    <div class="empty-content">暂不支持</div>
                  </div>
                </template>
                <template v-else>
                  <div class="empty-content">暂无内容</div>
                </template>
              </div>
            </div>
          </el-form-item>
        </el-form>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getApiList, deleteApi, addApi, updateApi } from '../api/apiManage'
import { getApiGroups } from '../api/apiManage'
import { getEnvironments } from '../api/environmentManage'
import axios from 'axios'

// 接口相关
const pagedApis = ref([])
const selectedGroup = ref(null)
const search = ref('')
const activeTab = ref('body')
const responseViewType = ref('pretty')
const debugStatus = ref('')
const debugTime = ref('')
const debugSize = ref('')

// 新增接口弹窗相关
const apiDialogVisible = ref(false)
const apiForm = ref({
  name: '',
  url: '',
  method: '',
  group_id: null,
  env_id: null,
  description: ''
})

const groups = ref([])
const envs = ref([])

// 调试相关
const debugDialogVisible = ref(false)
const debugMethod = ref('GET')
const debugUrl = ref('')
const debugParamType = ref('params')
const debugParamsList = ref([])
const debugJson = ref('')
const debugForm = ref('')
const debugHeaders = ref('')
const debugResult = ref(null)
const debugApi = ref(null)
const isEdit = ref(false)
const dialogWidth = computed(() => {
  return window.innerWidth <= 768 ? '98%' : '900px'
})

// Methods
const openApiForm = (row = null) => {
  if (row) {
    apiForm.value = {
      ...row,
      description: row.description || '',
      env_id: row.env_id || null
    }
    isEdit.value = true
  } else {
    apiForm.value = { name: '', url: '', method: '', group_id: null, env_id: null, description: '' }
    isEdit.value = false
  }
  apiDialogVisible.value = true
}

const submitApiForm = async () => {
  if (isEdit.value) {
    await updateApi(apiForm.value.id, apiForm.value)
  } else {
    await addApi(apiForm.value)
  }
  apiDialogVisible.value = false
  fetchApis()
}

const editApi = (row) => {
  openApiForm(row)
}

// 删除接口
const handleDeleteApi = async (id) => {
  await deleteApi(id)
  fetchApis()
}
// 接口分页
const apiPage = ref(1)
const apiPageSize = ref(10)

const pagedApiList = computed(() => {
  const start = (apiPage.value - 1) * apiPageSize.value
  return pagedApis.value.slice(start, start + apiPageSize.value)
})

const handleSearch = async () => {
  apiPage.value = 1;
  await fetchApis();
}

const fetchApis = async () => {
  const res = await getApiList();
  let data = res.data;
  if (selectedGroup.value) {
    data = data.filter(api => api.group_id === selectedGroup.value);
  }
  if (search.value && search.value.trim()) {
    const keyword = search.value.trim().toLowerCase();
    data = data.filter(api =>
      (api.name && api.name.toLowerCase().includes(keyword)) ||
      (api.url && api.url.toLowerCase().includes(keyword))
    );
  }
  data = data.map(api => ({
    ...api,
    group_name: groups.value.find(g => g.id === api.group_id)?.name || '',
    env_name: envs.value.find(e => e.id === api.env_id)?.name || ''
  }))
  pagedApis.value = data
}

const fetchGroups = async () => {
  const res = await getApiGroups()
  groups.value = res.data
  await fetchApis()
}
const fetchEnvs = async () => {
  const res = await getEnvironments()
  envs.value = res.data
}
// 页面初始化时只调用 fetchGroups 和 fetchEnvs
fetchGroups()
fetchEnvs()

// 检测屏幕尺寸
const isSmallScreen = ref(window.innerWidth <= 768)

const handleResize = () => {
  isSmallScreen.value = window.innerWidth <= 768
}

// 添加窗口大小监听
onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

const openGroupForm = () => {
  // 触发新增分组事件，您可以根据需要修改实现
  console.log('Open group form')
}

// 调试相关
const runApi = (row) => {
  debugApi.value = row
  debugMethod.value = row.method
  // 获取环境变量
  const env = envs.value.find(e => e.id === row.env_id)
  let baseUrl = ''
  if (env) baseUrl = env.value
  debugUrl.value = baseUrl ? baseUrl.replace(/\/$/, '') + row.url : row.url
  debugParamType.value = 'params'
  debugParamsList.value = [{ key: '', value: '', type: 'string', desc: '' }]
  debugJson.value = ''
  debugForm.value = ''
  debugHeaders.value = ''
  debugResult.value = ''
  debugDialogVisible.value = true
}

const addParam = () => {
  debugParamsList.value.push({ key: '', value: '', type: 'string', desc: '' })
}
const removeParam = (idx) => {
  if (debugParamsList.value.length === 1) {
    debugParamsList.value[0] = { key: '', value: '' }
  } else {
    debugParamsList.value.splice(idx, 1)
  }
}

const doDebugRequest = async () => {
  let params = {}
  let data = undefined
  let headers = {}
  // 处理header
  try {
    if (debugHeaders.value.trim()) headers = JSON.parse(debugHeaders.value)
  } catch (e) {
    debugResult.value = 'Header格式错误，需为JSON字符串'; return
  }
  // 处理参数
  if (debugParamType.value === 'params') {
    params = {}
    debugParamsList.value.forEach(item => {
      if (item.key) {
        // 类型转换
        let v = item.value
        if (item.type === 'number') v = Number(item.value)
        else if (item.type === 'boolean') v = item.value === 'true' || item.value === true
        else if (item.type === 'array') {
          try { v = JSON.parse(item.value) } catch { v = [item.value] }
        }
        params[item.key] = v
      }
    })
  } else if (debugParamType.value === 'json') {
    try {
      data = debugJson.value.trim() ? JSON.parse(debugJson.value) : undefined
    } catch (e) {
      debugResult.value = 'JSON格式错误'; return
    }
  } else if (debugParamType.value === 'form') {
    data = new URLSearchParams()
    debugForm.value.split('\n').filter(Boolean).forEach(line => {
      const [k, v] = line.split('=')
      data.append(k, v)
    })
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
  }
  // 打印实际请求内容
  console.log('实际请求：', {
    url: debugUrl.value,
    method: debugMethod.value,
    headers,
    params,
    data
  })
  const start = Date.now()
  try {
    const res = await axios({
      url: debugUrl.value,
      method: debugMethod.value.toLowerCase(),
      headers,
      params: debugParamType.value === 'params' ? params : undefined,
      data,
      responseType: 'text'
    })
    debugResult.value = formatJson(res.data)
    debugStatus.value = res.status
    debugTime.value = Date.now() - start
    debugSize.value = res.headers['content-length'] ? res.headers['content-length'] + ' B' : (typeof res.data === 'string' ? (new Blob([res.data]).size + ' B') : '')
  } catch (err) {
    debugResult.value = err?.response ? formatJson(err.response.data) : String(err)
    debugStatus.value = err?.response?.status || ''
    debugTime.value = Date.now() - start
    debugSize.value = err?.response?.headers?.['content-length'] ? err.response.headers['content-length'] + ' B' : (err?.response?.data ? (typeof err.response.data === 'string' ? (new Blob([err.response.data]).size + ' B') : '') : '')
  }
}
function highlightedJson(jsonStr) {
  if (!jsonStr) return ''
  let html = jsonStr
  try {
    const obj = JSON.parse(jsonStr)
    html = JSON.stringify(obj, null, 2)
    html = html.replace(/(&)/g, '&amp;').replace(/(\<)/g, '&lt;').replace(/(\>)/g, '&gt;')
    html = html.replace(/("[^"]+": )/g, '<span class="key">$1</span>')
      .replace(/(:\s?"[^"]+")/g, '<span class="string">$1</span>')
      .replace(/(:\s?\d+)/g, '<span class="number">$1</span>')
      .replace(/(:\s?true|false)/g, '<span class="boolean">$1</span>')
      .replace(/(:\s?null)/g, '<span class="null">$1</span>')
  } catch {}
  return html
}
// JSON格式化
function formatJson(data) {
  if (typeof data === 'string') {
    try {
      return JSON.stringify(JSON.parse(data), null, 2)
    } catch {
      return data
    }
  }
  return JSON.stringify(data, null, 2)
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  width: 100%;
  background-color: #f5f7fa;
  padding: 16px;
  gap: 16px;
}

.main-content {
  flex: 1;
  background-color: #f8fafc;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  position: relative;
  transition: all 0.3s ease-in-out;
}

.content-wrapper {
  background: #f8fafc;
  width: 100%;
  padding: 24px;
  min-height: 100%;
}

.header-section {
  background: #fff;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  margin: 0 0 24px 0;
  position: relative;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05),
              0 4px 6px -1px rgba(0, 0, 0, 0.03);
  background: linear-gradient(to bottom, #ffffff, #fafafa);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.header-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, 
    rgba(255,255,255,0) 0%,
    rgba(255,255,255,0.8) 50%,
    rgba(255,255,255,0) 100%);
}

.left-section {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.right-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

@media (max-width: 768px) {
  .app-container {
    padding: 10px;
  }
  
  .header-section {
    flex-direction: column;
    align-items: stretch;
    
    .left-section,
    .right-section {
      width: 100%;
      justify-content: space-between;
    }
  }

  .debug-param-card {
    overflow-x: auto;
  }
}

.table-section {
  background: #ffffff;
  margin: 0;
  padding: 20px;
  overflow-x: auto;
  position: relative;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.table-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 20px;
  right: 20px;
  height: 1px;
  background: linear-gradient(90deg, 
    rgba(0,0,0,0.02) 0%, 
    rgba(0,0,0,0.05) 50%, 
    rgba(0,0,0,0.02) 100%);
}

.table-section::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 40px;
  background: linear-gradient(to top, rgba(255,255,255,0.95), rgba(255,255,255,0));
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.table-section:hover::after {
  opacity: 1;
}

.el-table {
  background: transparent;
  margin-bottom: 16px;
  width: 100%;
}

@media (max-width: 768px) {
  .el-table {
    font-size: 14px;
  }
  
  :deep(.el-table .cell) {
    padding: 4px 6px;
  }
  
  :deep(.el-table--mini) {
    font-size: 12px;
  }
  
  :deep(.el-button--mini) {
    padding: 6px 12px;
  }
}

/* 分页响应式样式 */
.pagination-container {
  margin-top: 16px;
  padding: 16px 0;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid #e4e7ed;
}

@media (max-width: 480px) {
  .pagination-container {
    justify-content: center;
  }
}

/* 美化搜索框和选择框 */
.el-input,
.el-select {
  .el-input__wrapper {
    background-color: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
    transition: all 0.3s;
    height: 36px;
    padding: 0 12px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    
    &:hover {
      border-color: #40a9ff;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    &.is-focus {
      border-color: #40a9ff;
      box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1), 
                  0 1px 2px rgba(0, 0, 0, 0.05);
    }
  }

  .el-input__inner {
    font-size: 14px;
    color: #1f2937;
    height: 100%;
    line-height: 36px;
    
    &::placeholder {
      color: #9ca3af;
    }
  }
}

/* 表格样式增强 */
.el-table {
  --el-table-border-color: #e2e8f0;
  --el-table-header-background-color: #f1f5f9;
  --el-table-row-hover-background-color: #f8fafc;
  margin: 0;
  
  :deep(th.el-table__cell) {
    background-color: #f8fafc;
    color: #4a5568;
    font-weight: 600;
    font-size: 13px;
    height: 48px;
    border-bottom: 2px solid #e2e8f0;
    padding: 12px 16px;
    transition: background-color 0.3s;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    
    &:first-child {
      padding-left: 24px;
    }
    
    &:last-child {
      padding-right: 24px;
    }
  }

  :deep(td.el-table__cell) {
    padding: 16px;
    height: 60px;
    color: #2d3748;
    font-size: 14px;
    line-height: 1.5;
    border-bottom: 1px solid #edf2f7;
    transition: all 0.3s ease;
    
    &:first-child {
      padding-left: 24px;
    }
    
    &:last-child {
      padding-right: 24px;
    }
  }

  :deep(.el-table__inner-wrapper) {
    background-color: #fff;
    border: 1px solid #f0f0f0;
  }
}

/* 表格行样式优化 */
.el-table__row {
  transition: all 0.2s ease;
  border-bottom: 1px solid #ebeef5;

  &:hover {
    background-color: #f5f7fa !important;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
    z-index: 1;
    position: relative;
  }

  &:last-child {
    border-bottom: none;
  }
}

/* 表单样式 */
.api-form {
  .form-content {
    max-height: 60vh;
    overflow-y: auto;
    padding-right: 10px;

    :deep(.el-form-item) {
      margin-bottom: 20px;

      &.mb-0 {
        margin-bottom: 0;
      }

      .el-form-item__label {
        padding: 0 0 6px;
        line-height: 1.4;
        font-size: 13px;
        font-weight: 500;
        color: #374151;
        height: auto;

        &::before {
          margin-right: 4px;
          color: #f56c6c;
        }
      }

      .el-form-item__content {
        line-height: 1;

        .el-input__wrapper {
          box-shadow: none !important;
          border: 1px solid #e5e7eb;
          border-radius: 4px;
          padding: 0 11px;
          height: 32px;
          background: #ffffff;
          transition: all 0.2s;

          &:hover {
            border-color: #40a9ff;
            background-color: #ffffff;
          }

          &.is-focus {
            border-color: #1890ff;
            box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2) !important;
          }
        }

        .el-input__inner {
          height: 30px;
          font-size: 13px;
          color: #1f2937;
          padding: 0;
          
          &::placeholder {
            color: #9ca3af;
          }
        }

        .el-select {
          width: 100%;

          &.full-width {
            display: block;
          }

          .el-input .el-select__caret {
            color: #9ca3af;
            font-size: 12px;
            transition: transform 0.2s;
          }

          &.is-focus {
            .el-input__wrapper {
              border-color: #1890ff;
              box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2) !important;
            }
          }
        }

        .el-textarea__inner {
          box-shadow: none;
          padding: 8px 11px;
          min-height: 72px;
          font-size: 13px;
          line-height: 1.6;
          border: 1px solid #e5e7eb;
          border-radius: 4px;
          background-color: #f9fafb;
          transition: all 0.2s;
          resize: none;

          &:hover {
            border-color: #40a9ff;
            background-color: #ffffff;
          }

          &:focus {
            border-color: #1890ff;
            background-color: #ffffff;
            box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
          }

          &::placeholder {
            color: #9ca3af;
          }
        }
      }

      &__error {
        font-size: 12px;
        padding-top: 4px;
        color: #dc2626;
      }
    }

    .monospace-input {
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
      letter-spacing: -0.2px;

      :deep(.el-input__inner) {
        font-size: 12px;
      }
    }

    .method-option {
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
      font-size: 12px;
      height: 32px;
      line-height: 32px;
    }
  }
}

/* Dialog 样式优化 */
.api-dialog {
  :deep(.el-dialog) {
    border-radius: 6px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
                0 10px 10px -5px rgba(0, 0, 0, 0.04);
    overflow: hidden;
    margin-top: 15vh !important;
    
    .el-dialog__header {
      margin: 0;
      padding: 14px 16px;
      background: #ffffff;
      border-bottom: 1px solid #f0f0f0;
      
      .el-dialog__title {
        font-size: 14px;
        font-weight: 600;
        color: #111827;
      }

      .el-dialog__headerbtn {
        top: 14px;
        right: 14px;
      }

      .el-dialog__close {
        font-size: 16px;
        color: #9ca3af;
        
        &:hover {
          color: #1890ff;
        }
      }
    }
    
    .el-dialog__body {
      padding: 0;
      padding-top: 10px;
    }
    
    .el-dialog__footer {
      margin: 0;
      padding: 12px 16px;
      background: #f9fafb;
      border-top: 1px solid #f0f0f0;
      
      .dialog-footer {
        display: flex;
        justify-content: flex-end;
        gap: 8px;

        .el-button {
          margin: 0;
          min-width: 64px;
          height: 32px;
          padding: 0 12px;
          font-size: 13px;
          border-radius: 4px;
          
          &--primary {
            background-color: #1890ff;
            border-color: #1890ff;
            
            &:hover {
              background-color: #40a9ff;
              border-color: #40a9ff;
            }
            
            &:active {
              background-color: #096dd9;
              border-color: #096dd9;
            }
          }

          &:not(.el-button--primary) {
            border-color: #e5e7eb;
            color: #374151;
            
            &:hover {
              color: #1890ff;
              border-color: #1890ff;
              background-color: #ffffff;
            }
          }
        }
      }
    }
  }
}

/* 按钮样式 */
.el-button {
  border-radius: 2px;
  font-weight: 400;
  height: 32px;
  padding: 0 15px;
  font-size: 14px;
  border: 1px solid #d9d9d9;
  transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
  
  &.el-button--primary {
    background-color: #1890ff;
    border-color: #1890ff;
    color: #fff;
    text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.12);
    box-shadow: 0 2px 0 rgba(0, 0, 0, 0.045);
    
    &:hover {
      background-color: #40a9ff;
      border-color: #40a9ff;
    }
    
    &:active {
      background-color: #096dd9;
      border-color: #096dd9;
    }
  }

  &.el-button--mini {
    height: 24px;
    padding: 0 7px;
    font-size: 12px;
    border-radius: 2px;
  }

  &:not(.el-button--primary) {
    background: #fff;
    
    &:hover {
      color: #40a9ff;
      border-color: #40a9ff;
    }
    
    &:active {
      color: #096dd9;
      border-color: #096dd9;
    }
  }

  &.el-button--danger {
    color: #ff4d4f;
    border-color: #ff4d4f;
    background: #fff;
    
    &:hover {
      background: #ff4d4f;
      border-color: #ff4d4f;
      color: #fff;
    }
    
    &:active {
      background: #cf1322;
      border-color: #cf1322;
      color: #fff;
    }
  }
  
  & + .el-button {
    margin-left: 8px;
  }
}

.debug-dialog {
  :deep(.el-dialog) {
    --el-dialog-padding-primary: 20px;
    border-radius: 8px;
    max-width: calc(100vw - 32px);
    margin: 16px auto;
  }
  
  :deep(.el-dialog__header) {
    margin: 0;
    padding: 20px;
    border-bottom: 1px solid var(--el-border-color-lighter);
  }
  
  :deep(.el-dialog__body) {
    padding: 20px;
    max-height: calc(100vh - 200px);
    overflow-y: auto;
  }
}

.param-type-selector {
  margin-bottom: 16px;
  
  :deep(.el-radio) {
    margin-right: 24px;
    
    &:last-child {
      margin-right: 0;
    }
  }
}

.param-table {
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 4px;
  background-color: var(--el-bg-color);
}

.param-table-header {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background-color: var(--el-fill-color-light);
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.param-table-body {
  padding: 8px 16px;
}

.param-row {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  gap: 8px;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.param-col {
  font-size: 14px;
  color: var(--el-text-color-regular);
  
  &.param-name { width: 160px; }
  &.param-value { width: 200px; }
  &.param-type { width: 120px; }
  &.param-desc { flex: 1; min-width: 120px; }
  &.param-action { width: 50px; text-align: center; }
}

.param-add-btn {
  padding: 16px;
  text-align: center;
  border-top: 1px solid var(--el-border-color-lighter);
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .param-row {
    flex-wrap: wrap;
    
    .param-name,
    .param-value,
    .param-type,
    .param-desc {
      width: 100%;
    }
    
    .param-action {
      width: 100%;
      text-align: right;
      margin-top: 8px;
    }
  }
  
  .response-header {
    flex-direction: column;
    
    .view-options,
    .response-status {
      width: 100%;
      margin-bottom: 8px;
    }
  }
}

/* 保留之前的响应面板相关样式 */
.response-panel {
  border: none;
  border-radius: 0;
  background: none;
  box-shadow: none;
  width: 100%;
  margin: 0;
  padding: 0;
}

.response-header {
  background: none;
  border-bottom: 1px solid #e4e7ed;
  padding: 0 0 8px 0;
}

.response-content {
  min-height: 120px;
  background: none;
  padding: 0;
  width: 100%;
}

.response-view {
  width: 100%;
  padding: 0;
  margin: 0;
}

.body-tab-content {
  padding: 0;
  display: flex;
  align-items: center;
  border-bottom: none;
}

.json-content, .raw-content {
  background: none;
  border: none;
  box-shadow: none;
  width: 100%;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
  font-size: 13px;
  line-height: 1.5;
  color: #24292e;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
  padding: 16px 0;
}

.empty-content {
  color: #909399;
  font-size: 14px;
  padding: 40px 0;
  text-align: left;
}
</style>