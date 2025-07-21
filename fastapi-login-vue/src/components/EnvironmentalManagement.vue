<template>
  <el-container class="app-container">
    <el-main class="main-content">
      <el-tabs v-model="activeEnvTab" class="env-tabs">
        <el-tab-pane label="环境" name="env">
          <div class="content-wrapper">
            <div class="env-search-bar">
              <div class="env-search-left">
                <el-input
                  v-model="searchEnv"
                  placeholder="搜索环境名称"
                  style="width: 220px;"
                  clearable
                >
                </el-input>
                <el-button type="primary" @click="handleSearch">查询</el-button>
              </div>
              <div class="env-search-right">
                <el-button type="primary" @click="showAddDialog = true">新增环境</el-button>
              </div>
            </div>
            <div class="table-section" style="overflow-x:auto;">
              <el-table 
                :data="pagedEnvs" 
                :border="false" 
                style="min-width: 400px; width: auto; table-layout: auto;"
                v-loading="loading"
                :element-loading-text="'加载中...'"
              >
                <el-table-column prop="name" label="环境名称" min-width="180">
                  <template #default="scope">
                    <span class="env-name-link" @click="goToDetailPage(scope.row)">{{ scope.row.name }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="value" label="环境地址" min-width="220" show-overflow-tooltip>
                  <template #default="scope">
                    <span>{{ scope.row.value }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="150" fixed="right">
                  <template #default="scope">
                    <el-button type="primary" link @click="openEditDialog(scope.row)">编辑</el-button>
                    <el-button type="danger" link @click="openDeleteDialog(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
                <template #empty>
                  <div style="text-align: center; padding: 20px;">
                    {{ loading ? '加载中...' : (searchEnv ? '没有找到匹配的环境' : '暂无环境数据') }}
                  </div>
                </template>
              </el-table>
              <div class="pagination-container">
                <el-pagination
                  v-model:current-page="envPage"
                  :page-size="envPageSize"
                  :total="filteredEnvs.length"
                  layout="prev, pager, next"
                  :small="false"
                />
              </div>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="环境变量" name="envVar">
          <div class="content-wrapper">              <div class="env-var-header-bar">
                <div class="env-var-search-left">
                  <el-input
                    v-model="searchEnvVar"
                    placeholder="搜索环境变量名称"
                    style="width: 220px;"
                    clearable
                  >
                  </el-input>
                  <el-button type="primary" @click="handleEnvVarSearch">查询</el-button>
                </div>
                <div class="env-var-search-right">
                  <el-button type="primary" @click="showEnvVarDialog = true">新增变量</el-button>
                </div>
              </div>
            <div class="env-var-table">
              <el-table 
                :data="pagedEnvVars" 
                border 
                style="width: 100%"
                v-loading="loading"
                :element-loading-text="'加载中...'"
              >
                <el-table-column prop="env_name" label="环境名称" min-width="120" />
                <el-table-column prop="key" label="变量名" min-width="120" />
                <el-table-column prop="value" label="变量值" min-width="180" show-overflow-tooltip />
                <el-table-column label="操作" width="120" fixed="right">
                  <template #default="scope">
                    <el-button type="primary" link @click="editEnvVar(scope.row)">编辑</el-button>
                    <el-button type="danger" link @click="deleteEnvVar(scope.row.id)">删除</el-button>
                  </template>
                </el-table-column>
                <template #empty>
                  <div style="text-align: center; padding: 20px;">
                    {{ loading ? '加载中...' : (searchEnvVar ? '没有找到匹配的环境变量' : '暂无环境变量数据') }}
                  </div>
                </template>
              </el-table>
              <div class="pagination-container">
                <el-pagination
                  v-model:current-page="envVarPage"
                  :page-size="envVarPageSize"
                  :total="filteredEnvVars.length"
                  layout="prev, pager, next"
                  :small="false"
                />
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>

      <!-- 新增环境弹窗 -->
      <el-dialog v-model="showAddDialog" title="新增环境" width="350px" :close-on-click-modal="false">
        <el-input v-model="addEnvName" placeholder="请输入环境名称" style="margin-bottom: 10px;" />
        <el-input v-model="addEnvValue" placeholder="请输入环境值（如Base URL）" />
        <template #footer>
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="handleAddEnv">确定</el-button>
        </template>
      </el-dialog>

      <!-- 编辑环境弹窗 -->
      <el-dialog v-model="showEditDialog" title="编辑环境" width="350px" :close-on-click-modal="false">
        <el-input v-model="editEnvName" placeholder="请输入新的环境名称" style="margin-bottom: 10px;" />
        <el-input v-model="editEnvValue" placeholder="请输入新的环境值（如Base URL）" />
        <template #footer>
          <el-button @click="showEditDialog = false">取消</el-button>
          <el-button type="primary" @click="handleEditEnv">确定</el-button>
        </template>
      </el-dialog>

      <!-- 删除环境弹窗 -->
      <el-dialog v-model="showDeleteDialog" title="删除环境" width="350px" :close-on-click-modal="false">
        <div>确定要删除环境 "{{ deleteEnvRow?.name }}" 吗？</div>
        <template #footer>
          <el-button @click="showDeleteDialog = false">取消</el-button>
          <el-button type="danger" @click="handleDeleteEnvConfirm">确定</el-button>
        </template>
      </el-dialog>

      <!-- 新增环境变量对话框 -->
      <el-dialog
        v-model="showEnvVarDialog"
        title="新增环境变量"
        width="500px"
        :close-on-click-modal="false"
        destroy-on-close
      >
        <el-form
          ref="envVarFormRef"
          :model="envVarForm"
          :rules="envVarRules"
          label-width="100px"
        >
          <el-form-item label="所属环境" prop="env_id">
            <el-select v-model="envVarForm.env_id" placeholder="请选择环境" style="width: 100%">
              <el-option
                v-for="env in envs"
                :key="env.id"
                :label="env.name"
                :value="env.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="变量名" prop="key">
            <el-input v-model="envVarForm.key" placeholder="请输入变量名" />
          </el-form-item>
          <el-form-item label="变量值" prop="value">
            <el-input
              v-model="envVarForm.value"
              type="textarea"
              :rows="3"
              placeholder="请输入变量值"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="showEnvVarDialog = false">取 消</el-button>
            <el-button type="primary" @click="submitEnvVarForm">确 定</el-button>
          </div>
        </template>
      </el-dialog>

    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  getEnvironments, 
  getEnvironmentVariables, 
  addEnvironment, 
  updateEnvironment, 
  deleteEnvironment, 
  addEnvironmentVariable, 
  updateEnvironmentVariable, 
  deleteEnvironmentVariable 
} from '../api/environmentManage'

const loading = ref(false)
const searchEnv = ref('')
const searchEnvVar = ref('')
const showAddDialog = ref(false)
const showEnvVarDialog = ref(false)  // 新增变量对话框显示状态
const showEditDialog = ref(false)
const showDeleteDialog = ref(false)
const addEnvName = ref('')
const addEnvValue = ref('')
const editEnvName = ref('')
const editEnvValue = ref('')
const editEnvRow = ref(null)
const deleteEnvRow = ref(null)
const activeEnvTab = ref('env')

const envs = ref([])
const envVars = ref([])
const envPage = ref(1)
const envPageSize = ref(10)
const envVarPage = ref(1)
const envVarPageSize = ref(10)

const router = useRouter()
const goToDetailPage = (row) => {
  router.push({ name: 'EnvDetail', params: { id: row.id } })
}

const fetchEnvs = async () => {
  loading.value = true
  try {
    const res = await getEnvironments()
    console.log('Environment API response:', res)
    if (res?.data) {
      envs.value = Array.isArray(res.data) ? res.data : []
    } else {
      envs.value = []
      ElMessage.warning('获取到的环境数据格式不正确')
    }
  } catch (error) {
    console.error('获取环境列表失败:', error)
    envs.value = []
    ElMessage.error('获取环境列表失败')
  } finally {
    loading.value = false
  }
}

const fetchEnvVars = async () => {
  try {
    loading.value = true
    const res = await getEnvironmentVariables()
    envVars.value = res.data
  } catch (error) {
    console.error('获取环境变量失败:', error)
    ElMessage.error('获取环境变量失败')
  } finally {
    loading.value = false
  }
}

const handleAddEnv = async () => {
  if (!addEnvName.value.trim() || !addEnvValue.value.trim()) return
  await addEnvironment({ name: addEnvName.value.trim(), value: addEnvValue.value.trim() })
  showAddDialog.value = false
  addEnvName.value = ''
  addEnvValue.value = ''
  fetchEnvs()
}

const openEditDialog = (row) => {
  editEnvRow.value = row
  editEnvName.value = row.name
  editEnvValue.value = row.value
  showEditDialog.value = true
}
const handleEditEnv = async () => {
  if (!editEnvName.value.trim() || !editEnvValue.value.trim() || !editEnvRow.value) return
  if (editEnvName.value.trim() !== editEnvRow.value.name || editEnvValue.value.trim() !== editEnvRow.value.value) {
    await updateEnvironment(editEnvRow.value.id, { name: editEnvName.value.trim(), value: editEnvValue.value.trim() })
    fetchEnvs()
  }
  showEditDialog.value = false
  editEnvName.value = ''
  editEnvValue.value = ''
  editEnvRow.value = null
}

const openDeleteDialog = (row) => {
  deleteEnvRow.value = row
  showDeleteDialog.value = true
}
const handleDeleteEnvConfirm = async () => {
  if (deleteEnvRow.value) {
    await deleteEnvironment(deleteEnvRow.value.id)
    fetchEnvs()
  }
  showDeleteDialog.value = false
  deleteEnvRow.value = null
}

const handleSearch = async () => {
  envPage.value = 1
  await fetchEnvs()
}

const handleEnvVarSearch = () => {
  envVarPage.value = 1
}

const editEnvVar = (row) => {
  envVarForm.value = {
    ...row,
    env_id: row.env_id
  }
  showEnvVarDialog.value = true
}

const deleteEnvVar = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除此环境变量吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    loading.value = true
    await deleteEnvironmentVariable(id)
    ElMessage.success('删除成功')
    fetchEnvVars()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除环境变量失败:', error)
      ElMessage.error('删除失败')
    }
  } finally {
    loading.value = false
  }
}

const envVarForm = ref({
  env_id: '',
  key: '',
  value: ''
})

const envVarRules = {
  env_id: [{ required: true, message: '请选择所属环境', trigger: 'change' }],
  key: [{ required: true, message: '请输入变量名', trigger: 'blur' }],
  value: [{ required: true, message: '请输入变量值', trigger: 'blur' }]
}

const envVarFormRef = ref()

// 提交环境变量表单
const submitEnvVarForm = async () => {
  if (!envVarFormRef.value) return
  
  try {
    await envVarFormRef.value.validate()
    loading.value = true
    
    if (envVarForm.value.id) {
      // 更新已存在的环境变量
      await updateEnvironmentVariable(envVarForm.value.id, envVarForm.value)
      ElMessage.success('更新成功')
    } else {
      // 创建新的环境变量
      await addEnvironmentVariable(envVarForm.value)
      ElMessage.success('添加成功')
    }
    
    showEnvVarDialog.value = false
    // 重置表单
    envVarForm.value = {
      env_id: '',
      key: '',
      value: ''
    }
    // 重新加载环境变量列表
    fetchEnvVars()
  } catch (error) {
    console.error('操作环境变量失败:', error)
    ElMessage.error(error?.response?.data?.detail || '操作失败')
  } finally {
    loading.value = false
  }
}

// 初始化数据
onMounted(() => {
  fetchEnvs()
  fetchEnvVars()
})

const filteredEnvs = computed(() => {
  if (!envs.value || !Array.isArray(envs.value)) return []
  const searchText = searchEnv.value?.toLowerCase().trim() || ''
  return envs.value.filter(e => 
    (e?.name?.toLowerCase().includes(searchText)) || 
    (e?.value?.toLowerCase().includes(searchText))
  )
})

const pagedEnvs = computed(() => {
  const start = (envPage.value - 1) * envPageSize.value
  return filteredEnvs.value.slice(start, start + envPageSize.value)
})

// 计算筛选后的环境变量列表（用于分页和显示总数）
const filteredEnvVars = computed(() => {
  if (!searchEnvVar.value) return envVars.value
  
  const keyword = searchEnvVar.value.toLowerCase()
  return envVars.value.filter(v => 
    v.key.toLowerCase().includes(keyword) || 
    v.value.toLowerCase().includes(keyword)
  )
})

// 计算分页后的环境变量列表
const pagedEnvVars = computed(() => {
  const start = (envVarPage.value - 1) * envVarPageSize.value
  return filteredEnvVars.value.slice(start, start + envVarPageSize.value)
})

</script>

<style scoped>
.app-container {
  height: 100%;
  display: flex;
}

.main-content {
  flex: 1;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  position: relative;
  transition: all 0.3s ease-in-out;
}

.env-tabs {
  :deep(.el-tabs__header) {
    margin-bottom: 0;
    background-color: #f8fafc;
    border-bottom: 1px solid #e5e7eb;
    padding: 0 24px;
  }
  :deep(.el-tabs__nav-wrap::after) {
    display: none;
  }
  :deep(.el-tabs__item) {
    height: 48px;
    line-height: 48px;
    font-size: 14px;
    font-weight: 500;
    color: #4b5563;
    &.is-active {
      color: #1890ff;
      font-weight: 600;
    }
    &:hover {
      color: #1890ff;
    }
  }
  :deep(.el-tabs__active-bar) {
    background-color: #1890ff;
    height: 3px;
    border-radius: 3px 3px 0 0;
  }
}

.content-wrapper {
  background: #ffffff;
  width: 100%;
  padding: 24px;
  min-height: calc(100vh - 48px - 32px); /* 减去tabs高度和container padding */
}

/* 环境管理部分 */
.env-search-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 16px;
  background: #fff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.env-search-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.env-search-right {
  display: flex;
  align-items: center;
}

.env-name-link {
  color: #409EFF;
  cursor: pointer;
  text-decoration: none;
}

.env-name-link:hover {
  text-decoration: underline;
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
  border: 1px solid #e5e7eb;

  :deep(.el-table) {
    background: transparent;
    th.el-table__cell {
      background: #f8fafc;
      font-weight: 600;
      color: #111827;
    }
    .el-table__cell {
      padding: 12px;
    }
  }
}

.pagination-container {
  margin-top: 16px;
  padding: 16px 0;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid #e5e7eb;
}

/* 环境变量部分 */
.env-var-header-bar {
  background: #fff;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.env-var-search-left {
  display: flex;
  gap: 10px;
  align-items: center;
}

.env-var-search-right {
  display: flex;
  gap: 10px;
  align-items: center;
}

.env-var-table {
  background: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .app-container {
    padding: 8px;
  }

  .content-wrapper {
    padding: 16px;
  }

  .env-search-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .env-search-left {
    width: 100%;
  }

  .env-search-right {
    width: 100%;
  }

  .env-search-right .el-button {
    width: 100%;
  }

  .el-input {
    width: 100% !important;
  }

  .env-var-header-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .env-var-search-left {
    width: 100%;
  }

  .env-var-search-left .el-input {
    width: 100% !important;
  }

  .env-var-search-left .el-button {
    width: 100%;
  }
}
  
</style>
