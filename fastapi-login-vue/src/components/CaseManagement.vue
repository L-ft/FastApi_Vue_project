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
/* 样式区域仅保留CSS，无JS代码 */
  :deep(.el-table__inner-wrapper) {
    background-color: #fff;
    border: 1px solid #f0f0f0;
  }
}
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
</style>
<template>
  <el-container class="app-container">
    <el-main class="main-content">
      <div class="content-wrapper">
        <div class="header-section">
          <div class="left-section">
            <el-select v-model="selectedGroup" placeholder="选择分组" style="width: 180px" @change="fetchCases">
              <el-option label="全部分组" :value="null" />
              <el-option v-for="g in groupList" :key="g.id" :label="g.name" :value="g.id" />
            </el-select>
            <el-input
              v-model="search"
              placeholder="搜索用例名称"
              style="width: 220px; margin-left: 10px"
              clearable
              @keyup.enter="handleSearch"
            />
            <el-button type="primary" style="margin-left: 10px;" @click="handleSearch">查询</el-button>
          </div>
          <div class="right-section">
            <el-button type="primary" @click="openCaseForm()">新增用例</el-button>
          </div>
        </div>
        <div class="table-section" style="overflow-x:auto;">
          <el-table :data="pagedCaseList" :border="false" style="min-width: 900px; width: auto; table-layout: auto;">
            <el-table-column prop="name" label="用例名称" min-width="120">
              <template #default="scope">
                <el-link type="primary" @click="goDetail(scope.row)">{{ scope.row.name }}</el-link>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="描述" min-width="180" />
            <el-table-column prop="group_id" label="所属分组" min-width="100">
              <template #default="scope">{{ getGroupName(scope.row.group_id) }}</template>
            </el-table-column>
            <el-table-column prop="api_id" label="所属API" min-width="100">
              <template #default="scope">{{ getApiName(scope.row.api_id) }}</template>
            </el-table-column>
            <el-table-column prop="method" label="请求方法" min-width="80" />
            <el-table-column prop="request_url" label="请求地址" min-width="180" />
            <el-table-column prop="creator" label="创建人" min-width="100" />
            <el-table-column label="操作" min-width="180" fixed="right">
              <template #default="scope">
                <el-button size="mini" @click="editCase(scope.row)">编辑</el-button>
                <el-button size="mini" type="danger" @click="deleteCase(scope.row.id)">删除</el-button>
                <el-button size="mini" type="success" @click="runCase(scope.row)">运行</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="casePage"
              :page-size="casePageSize"
              :total="caseList.length"
              layout="prev, pager, next"
              :small="isSmallScreen"
            />
          </div>
        </div>
      </div>
      <!-- 添加/编辑用例对话框 -->
      <el-dialog 
        v-model="caseDialogVisible" 
        :title="editMode ? '编辑用例' : '新增用例'" 
        width="500px" 
        :close-on-click-modal="false"
        class="api-dialog"
        destroy-on-close>
        <el-form 
          :model="form" 
          label-position="top" 
          class="api-form"
          :validate-on-rule-change="false">
          <div class="form-content">
            <el-form-item label="用例名称" required prop="name">
              <el-input v-model="form.name" placeholder="例如：登录用例" />
            </el-form-item>
            <el-form-item label="描述" prop="description">
              <el-input v-model="form.description" type="textarea" :rows="2" placeholder="用例描述" resize="none" />
            </el-form-item>
            <el-row :gutter="16">
              <el-col :span="12">
                <el-form-item label="所属分组" required prop="group_id">
                  <el-select v-model="form.group_id" placeholder="选择分组" class="full-width">
                    <el-option v-for="g in groupList" :key="g.id" :label="g.name" :value="g.id" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="所属API" required prop="api_id">
                  <el-select v-model="form.api_id" placeholder="选择API" class="full-width">
                    <el-option v-for="a in apiList" :key="a.id" :label="a.name" :value="a.id" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="16">
              <el-col :span="12">
                <el-form-item label="请求方法" prop="method">
                  <el-select v-model="form.method" placeholder="选择方法" class="full-width">
                    <el-option label="GET" value="GET" />
                    <el-option label="POST" value="POST" />
                    <el-option label="PUT" value="PUT" />
                    <el-option label="DELETE" value="DELETE" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="请求地址" prop="request_url">
                  <el-input v-model="form.request_url" placeholder="/api/v1/login" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="创建人" prop="creator">
              <el-input v-model="form.creator" placeholder="创建人" />
            </el-form-item>
          </div>
        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="caseDialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="saveCase">确 定</el-button>
          </div>
        </template>
      </el-dialog>
    </el-main>
  </el-container>
  <el-dialog v-model="caseDetailVisible" title="用例详情" width="1000px" :close-on-click-modal="false">
  <el-card class="detail-card">
    <div>
      <div class="detail-header">
        <span class="detail-title">H5获取token（成功）</span>
        <el-button type="primary" style="float:right">发送</el-button>
        <el-button style="float:right; margin-right:10px">保存</el-button>
        <el-button style="float:right; margin-right:10px">删除</el-button>
      </div>
      <el-tabs v-model="activeTab" class="detail-tabs">
        <el-tab-pane label="Params" name="params">
          <el-table :data="params" style="width:100%">
            <el-table-column prop="name" label="参数名"></el-table-column>
            <el-table-column prop="value" label="参数值"></el-table-column>
            <el-table-column prop="type" label="类型"></el-table-column>
            <el-table-column prop="desc" label="说明"></el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="Body" name="body">
          <div>
            <el-input type="textarea" :rows="10" v-model="body"></el-input>
          </div>
        </el-tab-pane>
        <el-tab-pane label="Header" name="header">
          <el-table :data="headers" style="width:100%">
            <el-table-column prop="name" label="名称"></el-table-column>
            <el-table-column prop="value" label="值"></el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="实际请求" name="request">
          <div>
            <div class="request-info">
              <div>POST {{ url }}</div>
              <div>耗时：{{ responseTime }} ms</div>
              <div>状态：<span style="color:green">成功 ({{ statusCode }})</span></div>
            </div>
            <el-input type="textarea" :rows="10" v-model="response"></el-input>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </el-card>
</el-dialog>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCases, addCase, updateCase, deleteCaseById, getGroups, getApis } from '../api/apiManage'
import axios from 'axios'
import { ElMessageBox, ElMessage } from 'element-plus'

const caseList = ref([])
const groupList = ref([])
const apiList = ref([])
const selectedGroup = ref(null)
const search = ref('')
const caseDialogVisible = ref(false)
const editMode = ref(false)
const form = ref({
  id: null,
  name: '',
  description: '',
  group_id: '',
  api_id: '',
  method: '',
  request_url: '',
  creator: ''
})
// 分页相关
const casePage = ref(1)
const casePageSize = ref(10)
const isSmallScreen = ref(window.innerWidth <= 768)
const pagedCaseList = computed(() => {
  let data = caseList.value
  if (selectedGroup.value) {
    data = data.filter(c => c.group_id === selectedGroup.value)
  }
  if (search.value && search.value.trim()) {
    const keyword = search.value.trim().toLowerCase()
    data = data.filter(c => c.name && c.name.toLowerCase().includes(keyword))
  }
  const start = (casePage.value - 1) * casePageSize.value
  return data.slice(start, start + casePageSize.value)
})
// 获取用例列表
const fetchCases = async () => {
  const res = await getCases()
  caseList.value = res.data || []
}
// 获取分组列表
const fetchGroups = async () => {
  const res = await getGroups()
  groupList.value = res.data || []
}
// 获取API列表
const fetchApis = async () => {
  const res = await getApis()
  apiList.value = res.data || []
}
// 搜索
const handleSearch = () => {
  casePage.value = 1
}
// 新增/编辑用例
const saveCase = async () => {
  if (editMode.value) {
    await updateCase(form.value)
  } else {
    await addCase(form.value)
  }
  caseDialogVisible.value = false
  fetchCases()
}
// 编辑用例
const editCase = (item) => {
  editMode.value = true
  caseDialogVisible.value = true
  form.value = { ...item }
}
// 新增用例弹窗
const openCaseForm = () => {
  editMode.value = false
  form.value = {
    id: null,
    name: '',
    description: '',
    group_id: '',
    api_id: '',
    method: '',
    request_url: '',
    creator: ''
  }
  caseDialogVisible.value = true
}
// 删除用例
const deleteCase = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除此用例吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteCaseById(id)
    ElMessage.success('删除成功')
    await fetchCases()
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('删除失败: ' + (e.response?.data?.detail || e.message || '未知错误'))
    }
  }
}
// 获取分组名称
const getGroupName = (id) => {
  const group = groupList.value.find(g => g.id === id)
  return group ? group.name : id
}
// 获取API名称
const getApiName = (id) => {
  const api = apiList.value.find(a => a.id === id)
  return api ? api.name : id;
}
// 响应式
const handleResize = () => {
  isSmallScreen.value = window.innerWidth <= 768
}
onMounted(() => {
  window.addEventListener('resize', handleResize)
  fetchCases()
  fetchGroups()
  fetchApis()
})
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
const router = useRouter()
// 用例详情弹窗相关变量
const caseDetailVisible = ref(false)
const activeTab = ref('params')
const url = ref('')
const responseTime = ref(0)
const statusCode = ref(200)
const response = ref('')
const params = ref([])
const headers = ref([])
const body = ref('')
const goDetail = (row) => {
  // 这里可根据 row 赋值详情内容
  caseDetailVisible.value = true
  // 示例：
  url.value = row.request_url || ''
  responseTime.value = 0
  statusCode.value = 200
  response.value = ''
  params.value = []
  headers.value = []
  body.value = ''
}
// 运行用例
const runCase = async (row) => {
  // 支持 params/json/form 三种参数类型，优先判断 body 字段
  let params = {}
  let data = undefined
  let headers = {}
  let paramType = row.param_type || 'params'
  try {
    if (row.headers && typeof row.headers === 'string') headers = JSON.parse(row.headers)
    else if (row.headers && typeof row.headers === 'object') headers = row.headers
  } catch (e) {
    ElMessage.error('Header格式错误，需为JSON字符串')
    return
  }
  if (paramType === 'params') {
    params = row.params || {}
  } else if (paramType === 'json') {
    try {
      data = typeof row.body === 'string' ? JSON.parse(row.body) : row.body
    } catch (e) {
      ElMessage.error('JSON格式错误')
      return
    }
  } else if (paramType === 'form') {
    data = new URLSearchParams()
    if (row.body) {
      try {
        const formObj = typeof row.body === 'string' ? JSON.parse(row.body) : row.body
        Object.entries(formObj).forEach(([k, v]) => data.append(k, v))
      } catch {
        // 兼容 body 为 key1=val1&key2=val2 形式
        String(row.body).split('&').forEach(pair => {
          const [k, v] = pair.split('=')
          if (k) data.append(k, v)
        })
      }
    }
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
  }
  const url = row.request_url
  const method = row.method ? row.method.toLowerCase() : 'get'
  const start = Date.now()
  try {
    const res = await axios({
      url,
      method,
      headers,
      params: paramType === 'params' ? params : undefined,
      data,
      responseType: 'text'
    })
    const time = Date.now() - start
    ElMessageBox.alert(
      `<div style='text-align:left;'><b>状态码:</b> ${res.status}<br/><b>耗时:</b> ${time}ms<br/><b>响应:</b><pre style='white-space:pre-wrap;'>${formatJson(res.data)}</pre></div>`,
      '运行结果',
      { dangerouslyUseHTMLString: true, customClass: 'run-result-dialog', confirmButtonText: '关闭' }
    )
  } catch (err) {
    const time = Date.now() - start
    const status = err?.response?.status || ''
    const data = err?.response?.data || String(err)
    ElMessageBox.alert(
      `<div style='text-align:left;'><b>状态码:</b> ${status}<br/><b>耗时:</b> ${time}ms<br/><b>响应:</b><pre style='white-space:pre-wrap;color:red;'>${formatJson(data)}</pre></div>`,
      '运行失败',
      { dangerouslyUseHTMLString: true, customClass: 'run-result-dialog', confirmButtonText: '关闭' }
    )
  }
}

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

