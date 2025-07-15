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
            <el-table-column prop="description" label="描述" min-width="180" />
            <el-table-column label="操作" min-width="120" fixed="right">
              <template #default="scope">
                <el-button size="mini" @click="editApi(scope.row)">编辑</el-button>
                <el-button size="mini" type="danger" @click="handleDeleteApi(scope.row.id)">删除</el-button>
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
              <el-col :span="14">
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
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getApiList, deleteApi, addApi, updateApi } from '../api/apiManage'
import { getApiGroups } from '../api/apiManage'
// import { fetchApis} from '../api/fetchApis'


// 接口相关
const pagedApis = ref([])
const selectedGroup = ref(null)
const search = ref('')

// 新增接口弹窗相关
const apiDialogVisible = ref(false)
const apiForm = ref({
  name: '',
  url: '',
  method: '',
  group_id: null,
  description: ''
})

const groups = ref([]) // 确保 groups 有定义
// 更新接口
const isEdit = ref(false) // 标记是否为编辑状态

const openApiForm = (row = null) => {
  if (row) {
    apiForm.value = {
      ...row,
      description: row.description || ''
    }
    isEdit.value = true
  } else {
    apiForm.value = { name: '', url: '', method: '', group_id: null, description: '' }
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
    group_name: groups.value.find(g => g.id === api.group_id)?.name || ''
  }))
  pagedApis.value = data
}

const fetchGroups = async () => {
  const res = await getApiGroups()
  groups.value = res.data
  await fetchApis()
}

// 页面初始化时只调用 fetchGroups
fetchGroups()

// 检测屏幕尺寸
const isSmallScreen = ref(window.innerWidth <= 768)

const handleResize = () => {
  isSmallScreen.value = window.innerWidth <= 768
}

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
</script>

<style scoped>
/* 强制提升表单样式优先级，彻底覆盖 Element Plus 默认样式 */
.api-dialog :deep(.el-dialog),
.api-dialog >>> .el-dialog {
  border-radius: 6px !important;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
  overflow: hidden !important;
  margin-top: 15vh !important;
}
.api-dialog :deep(.el-dialog__header),
.api-dialog >>> .el-dialog__header {
  margin: 0 !important;
  padding: 14px 16px !important;
  background: #fff !important;
  border-bottom: 1px solid #f0f0f0 !important;
}
.api-dialog :deep(.el-dialog__title),
.api-dialog >>> .el-dialog__title {
  font-size: 14px !important;
  font-weight: 600 !important;
  color: #111827 !important;
}
.api-dialog :deep(.el-dialog__body),
.api-dialog >>> .el-dialog__body {
  padding: 0 !important;
}
.api-dialog :deep(.el-dialog__footer),
.api-dialog >>> .el-dialog__footer {
  margin: 0 !important;
  padding: 12px 16px !important;
  background: #f9fafb !important;
  border-top: 1px solid #f0f0f0 !important;
}
.api-dialog :deep(.dialog-footer),
.api-dialog >>> .dialog-footer {
  display: flex !important;
  justify-content: flex-end !important;
  gap: 8px !important;
}
.api-dialog :deep(.el-button),
.api-dialog >>> .el-button {
  min-width: 64px !important;
  height: 32px !important;
  padding: 0 12px !important;
  font-size: 13px !important;
  border-radius: 4px !important;
}
.api-dialog :deep(.el-button--primary),
.api-dialog >>> .el-button--primary {
  background-color: #1890ff !important;
  border-color: #1890ff !important;
}
.api-dialog :deep(.el-button--primary:hover),
.api-dialog >>> .el-button--primary:hover {
  background-color: #40a9ff !important;
  border-color: #40a9ff !important;
}
.api-dialog :deep(.el-button--primary:active),
.api-dialog >>> .el-button--primary:active {
  background-color: #096dd9 !important;
  border-color: #096dd9 !important;
}
.api-dialog :deep(.el-button:not(.el-button--primary)),
.api-dialog >>> .el-button:not(.el-button--primary) {
  border-color: #e5e7eb !important;
  color: #374151 !important;
}
.api-dialog :deep(.el-button:not(.el-button--primary):hover),
.api-dialog >>> .el-button:not(.el-button--primary):hover {
  color: #1890ff !important;
  border-color: #1890ff !important;
  background-color: #fff !important;
}

/* 表单内容样式提升优先级 */
.api-form :deep(.form-content),
.api-form >>> .form-content {
  background: #fff !important;
  padding: 20px !important;
}
.api-form :deep(.el-form-item),
.api-form >>> .el-form-item {
  margin-bottom: 20px !important;
}
.api-form :deep(.el-form-item__label),
.api-form >>> .el-form-item__label {
  padding: 0 0 6px !important;
  line-height: 1.4 !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  color: #374151 !important;
  height: auto !important;
}
.api-form :deep(.el-form-item__content),
.api-form >>> .el-form-item__content {
  line-height: 1 !important;
}
.api-form :deep(.el-input__wrapper),
.api-form >>> .el-input__wrapper {
  box-shadow: none !important;
  border: 1px solid #e5e7eb !important;
  border-radius: 4px !important;
  padding: 0 11px !important;
  height: 32px !important;
  background: #fff !important;
  transition: all 0.2s !important;
}
.api-form :deep(.el-input__wrapper:hover),
.api-form >>> .el-input__wrapper:hover {
  border-color: #40a9ff !important;
  background-color: #fff !important;
}
.api-form :deep(.el-input__wrapper.is-focus),
.api-form >>> .el-input__wrapper.is-focus {
  border-color: #1890ff !important;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2) !important;
}
.api-form :deep(.el-input__inner),
.api-form >>> .el-input__inner {
  height: 30px !important;
  font-size: 13px !important;
  color: #1f2937 !important;
  padding: 0 !important;
}
.api-form :deep(.el-input__inner::placeholder),
.api-form >>> .el-input__inner::placeholder {
  color: #9ca3af !important;
}
.api-form :deep(.el-select),
.api-form >>> .el-select {
  width: 100% !important;
}
.api-form :deep(.el-select.full-width),
.api-form >>> .el-select.full-width {
  display: block !important;
}
.api-form :deep(.el-select__caret),
.api-form >>> .el-select__caret {
  color: #9ca3af !important;
  font-size: 12px !important;
  transition: transform 0.2s !important;
}
.api-form :deep(.el-form-item__error),
.api-form >>> .el-form-item__error {
  font-size: 12px !important;
  padding-top: 4px !important;
  color: #dc2626 !important;
}
.api-form :deep(.el-textarea__inner),
.api-form >>> .el-textarea__inner {
  box-shadow: none !important;
  padding: 8px 11px !important;
  min-height: 72px !important;
  font-size: 13px !important;
  line-height: 1.6 !important;
  border: 1px solid #e5e7eb !important;
  border-radius: 4px !important;
  background-color: #f9fafb !important;
  transition: all 0.2s !important;
  resize: none !important;
}
.api-form :deep(.el-textarea__inner:hover),
.api-form >>> .el-textarea__inner:hover {
  border-color: #40a9ff !important;
  background-color: #fff !important;
}
.api-form :deep(.el-textarea__inner:focus),
.api-form >>> .el-textarea__inner:focus {
  border-color: #1890ff !important;
  background-color: #fff !important;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2) !important;
}
.api-form :deep(.el-textarea__inner::placeholder),
.api-form >>> .el-textarea__inner::placeholder {
  color: #9ca3af !important;
}
.api-form :deep(.monospace-input),
.api-form >>> .monospace-input {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace !important;
  letter-spacing: -0.2px !important;
}
.api-form :deep(.method-option),
.api-form >>> .method-option {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace !important;
  font-size: 12px !important;
  height: 32px !important;
  line-height: 32px !important;
}
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

@media (max-width: 768px) {
  .app-container {
    padding: 10px;
  }
  .main-content {
    border-radius: 4px;
  }
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
    background: #ffffff;
    padding: 20px;

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
</style>