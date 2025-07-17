.env-search-bar .el-button[type="primary"] {
  min-width: 120px;
}
@media (max-width: 768px) {
  .env-search-bar .el-button[type="primary"] {
    width: 100%;
    margin-top: 8px;
    display: block;
    text-align: center;
  }
}
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
                  @keyup.enter="handleSearch"
                />
                <el-button type="primary" @click="handleSearch">查询</el-button>
              </div>
              <div class="env-search-right">
                <el-button type="primary" @click="showAddDialog = true">新增环境</el-button>
              </div>
            </div>
            <div class="table-section" style="overflow-x:auto;">
              <el-table :data="pagedEnvs" :border="false" style="min-width: 400px; width: auto; table-layout: auto;">
                <el-table-column prop="name" label="环境名称" min-width="180">
                  <template #default="scope">
                    <span class="env-name-link" @click="goToDetailPage(scope.row)">{{ scope.row.name }}</span>
                  </template>
                </el-table-column>
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
          <div class="content-wrapper">
            <div class="env-var-header-bar">
              <div class="env-var-search-bar">
                <el-input
                  v-model="searchEnvVar"
                  placeholder="搜索环境变量名称"
                  style="width: 220px;"
                  clearable
                  @keyup.enter="handleSearchEnvVar"
                />
                <el-button type="primary" @click="handleSearchEnvVar">查询</el-button>
              </div>
              <div class="env-var-add-btn-bar">
                <el-button type="primary" @click="showAddVarDialog = true">新增变量</el-button>
              </div>
            </div>
            <EnvVarList :search-key="searchEnvVar" />
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

      <!-- 新增变量弹窗 -->
      <el-dialog v-model="showAddVarDialog" title="新增变量" width="350px" :close-on-click-modal="false">
        <el-input v-model="addVarName" placeholder="请输入变量名" style="margin-bottom: 10px;" />
        <el-input v-model="addVarValue" placeholder="请输入变量值" />
        <template #footer>
          <el-button @click="showAddVarDialog = false">取消</el-button>
          <el-button type="primary" @click="handleAddVar">确定</el-button>
        </template>
      </el-dialog>

<!-- 环境详情页面由路由控制，不再弹窗 -->
    </el-main>
  </el-container>
</template>

<script setup>
const showAddVarDialog = ref(false)
const addVarName = ref('')
const addVarValue = ref('')
const handleAddVar = () => {
  // TODO: 实际新增变量逻辑，调用API或EnvVarList方法
  showAddVarDialog.value = false
  addVarName.value = ''
  addVarValue.value = ''
}
import { ref, computed } from 'vue'
// EnvVarList import 只保留一处，避免重复声明

const searchEnvVar = ref('')
const handleSearchEnvVar = () => {
  // 这里可扩展实际搜索逻辑，当前仅传递给EnvVarList
}
import EnvVarList from './EnvVarList.vue'
import { useRouter } from 'vue-router'
import { getEnvironments, addEnvironment, updateEnvironment, deleteEnvironment } from '../api/environmentManage'

const envs = ref([])
const searchEnv = ref('')
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const showDeleteDialog = ref(false)
const addEnvName = ref('')
const addEnvValue = ref('')
const editEnvName = ref('')
const editEnvValue = ref('')
const editEnvRow = ref(null)
const deleteEnvRow = ref(null)
const activeEnvTab = ref('env')

const router = useRouter()
const goToDetailPage = (row) => {
  router.push({ name: 'EnvDetail', params: { id: row.id } })
}

const fetchEnvs = async () => {
  const res = await getEnvironments()
  envs.value = res.data
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

const handleSearch = () => {
  envPage.value = 1
}

const filteredEnvs = computed(() =>
  envs.value.filter(e => e.name.toLowerCase().includes(searchEnv.value.toLowerCase().trim()))
)

const envPage = ref(1)
const envPageSize = ref(10)
const pagedEnvs = computed(() => {
  const start = (envPage.value - 1) * envPageSize.value
  return filteredEnvs.value.slice(start, start + envPageSize.value)
})
fetchEnvs()
</script>

<style scoped>
/* 环境变量标签页头部布局 */
.env-var-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  gap: 10px;
}
.env-var-search-bar {
  display: flex;
  gap: 10px;
}
.env-var-add-btn-bar {
  display: flex;
  align-items: center;
}
@media (max-width: 768px) {
  .env-var-header-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  .env-var-search-bar {
    width: 100%;
    justify-content: stretch;
  }
  .env-var-add-btn-bar {
    width: 100%;
    justify-content: center;
    margin-top: 8px;
  }
  .env-var-add-btn-bar .el-button[type="primary"] {
    width: 100%;
    min-width: 120px;
    display: block;
    text-align: center;
  }
}
.app-container {
  min-height: 100vh;
  display: flex;
  width: 100%;
  background-color: #f5f7fa;
  padding: 16px;
  gap: 16px;
}
.env-search-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  gap: 10px;
}
.env-search-left {
  display: flex;
  gap: 10px;
}
.env-search-right {
  display: flex;
  align-items: center;
}
@media (max-width: 768px) {
  .env-search-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  .env-search-left {
    width: 100%;
    justify-content: stretch;
  }
  .env-search-right {
    width: 100%;
    justify-content: center;
    margin-top: 8px;
  }
  .env-search-right .el-button[type="primary"] {
    width: 100%;
    min-width: 120px;
    display: block;
    text-align: center;
  }
}

.env-search-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
.env-search-bar > div {
  display: flex;
  gap: 10px;
}
@media (max-width: 768px) {
  .env-search-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  .env-search-bar > div {
    width: 100%;
    justify-content: stretch;
  }
  .env-search-bar .el-button[type="primary"] {
    width: 100%;
    margin-top: 8px;
  }
}

.env-tabs {
  margin-bottom: 24px;
}

.env-name-link {
  color: #409EFF;
  cursor: pointer;
  text-decoration: underline;
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

.pagination-container {
  margin-top: 16px;
  padding: 16px 0;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid #e4e7ed;
}

@media (max-width: 768px) {
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
  
</style>
