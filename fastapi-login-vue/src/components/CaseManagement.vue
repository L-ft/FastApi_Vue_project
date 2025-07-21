<style scoped>
.app-container {
  min-height: 100vh;
  width: 100%;
  background-color: #f5f7fa;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.search-section {
  display: flex;
  gap: 12px;
}

.group-select {
  width: 200px;
}

.search-input {
  width: 240px;
}

.table-wrapper {
  background: #fff;
  border-radius: 4px;
  padding: 20px;
}

.case-name-link {
  text-decoration: none;
}

.api-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.api-name {
  font-size: 13px;
  color: #606266;
}

.no-api {
  color: #909399;
  font-size: 13px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
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
  width: 100%;
  max-width: 100%;
}
.content-wrapper {
  background: #f8fafc;
  width: 100%;
  padding: 24px;
  min-height: 100%;
}
.header-section {
  background: #fff;
  padding: clamp(12px, 3vw, 20px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: clamp(10px, 2vw, 16px);
  margin: 0 0 clamp(16px, 3vw, 24px) 0;
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
  gap: clamp(8px, 1.5vw, 10px);
  flex: 1;
  min-width: 0;
}

.right-section {
  display: flex;
  align-items: center;
  gap: clamp(8px, 1.5vw, 10px);
}

@media (max-width: 992px) {
  .header-section {
    flex-direction: column;
    align-items: stretch;
  }

  .left-section {
    width: 100%;
  }

  .right-section {
    width: 100%;
    justify-content: flex-end;
    margin-top: 10px;
  }

  .search-section {
    flex-wrap: wrap;
  }

  .el-select,
  .el-input {
    flex: 1;
    min-width: 150px;
  }
}

@media (max-width: 576px) {
  .app-container {
    padding: 8px;
  }

  .header-section {
    padding: 12px;
  }

  .left-section,
  .right-section {
    flex-direction: column;
    width: 100%;
  }

  .el-select,
  .el-input,
  .el-button {
    width: 100% !important;
  }

  .right-section {
    margin-top: 8px;
  }
}
.table-section {
  background: #ffffff;
  margin: 0;
  padding: clamp(12px, 3vw, 20px);
  position: relative;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(0, 0, 0, 0.05);
  width: 100%;
}

.table-wrapper {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin: 0 -8px;
  padding: 0 8px;
}

.table-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 20px;
  right: 20px;
  height: 1px;
}

:deep(.el-table) {
  width: 100% !important;
  
  .el-table__inner-wrapper {
    background-color: #fff;
    border: 1px solid #f0f0f0;
  }

  .el-table__header-wrapper {
    th {
      background-color: #fafafa;
      font-weight: 500;
      color: #1f2937;
      font-size: 13px;
      padding: 8px 12px;
      border-bottom: 1px solid #f0f0f0;
    }
  }

  .el-table__body-wrapper {
    td {
      padding: 8px 12px;
      font-size: 13px;
      color: #374151;
    }
  }

  @media (max-width: 768px) {
    .el-table__header-wrapper th,
    .el-table__body-wrapper td {
      padding: 6px 8px;
      font-size: 12px;
    }

    .el-button {
      padding: 6px 10px;
      font-size: 12px;
    }
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
.search-section {
  display: flex;
  gap: clamp(8px, 1.5vw, 12px);
  align-items: center;
  flex-wrap: wrap;
  width: 100%;
}

.search-select {
  min-width: 150px;
  max-width: 180px;
  flex: 1;
}

.search-input {
  min-width: 200px;
  max-width: 300px;
  flex: 2;
}

.search-button {
  white-space: nowrap;
}

.case-detail-dialog {
  :deep(.el-dialog) {
    max-width: 95vw;
    margin: 2.5vh auto !important;
    border-radius: 8px;
    overflow: hidden;
  }
}

.detail-card {
  :deep(.el-card__body) {
    padding: clamp(12px, 2vw, 20px);
  }
}

.detail-header {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: clamp(12px, 3vw, 20px);
}

.detail-title {
  font-size: clamp(16px, 2vw, 18px);
  font-weight: 600;
  color: #1f2937;
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.detail-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.request-info {
  margin-bottom: 16px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.request-method {
  font-family: monospace;
  color: #1f2937;
  margin-bottom: 8px;
}

.request-meta {
  display: flex;
  gap: 16px;
  color: #6b7280;
  font-size: 13px;
}

.success-status {
  color: #22c55e;
}

.body-textarea,
.response-textarea {
  :deep(.el-textarea__inner) {
    font-family: monospace;
    font-size: 13px;
    line-height: 1.5;
    background: #f9fafb;
    border-color: #e5e7eb;
  }
}

.case-name-link {
  text-decoration: none;
}

.api-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.api-name {
  font-size: 13px;
  color: #606266;
}

.no-api {
  color: #909399;
  font-size: 13px;
}

.group-tag {
  margin: 0;
}

@media (max-width: 992px) {
  .header-section {
    flex-direction: column;
    align-items: stretch;
  }

  .search-section {
    flex-wrap: wrap;
  }

  .search-select,
  .search-input {
    min-width: 0;
    max-width: none;
  }

  .right-section {
    justify-content: flex-end;
    margin-top: 8px;
  }
}

@media (max-width: 768px) {
  .app-container {
    padding: 8px;
  }

  .content-wrapper {
    padding: 12px;
  }

  .header-section {
    padding: 12px;
    margin-bottom: 16px;
  }

  .search-section,
  .detail-header {
    flex-direction: column;
  }

  .search-select,
  .search-input,
  .el-button {
    width: 100% !important;
  }

  .detail-actions {
    width: 100%;
    justify-content: center;
  }

  :deep(.el-table) {
    .el-table__header-wrapper th,
    .el-table__body-wrapper td {
      padding: 6px 8px;
      font-size: 12px;
    }

    .el-button {
      padding: 6px 10px;
      font-size: 12px;
    }
  }
}
</style>
<template>
  <div class="app-container">
    <el-container>
      <el-main>
        <div class="content-header">
          <div class="left-section">
            <div class="search-section">
              <el-select v-model="selectedGroup" placeholder="选择分组" clearable class="group-select">
                <el-option v-for="g in groupList" :key="g.id" :label="g.name" :value="g.id" />
              </el-select>
              <el-input
                v-model="search"
                placeholder="搜索用例名称"
                class="search-input"
                clearable
                @keyup.enter="handleSearch"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
              <el-button type="primary" class="search-button" @click="handleSearch">
                <el-icon><Search /></el-icon>
                <span>查询</span>
              </el-button>
            </div>
          </div>
          <div class="right-section">
            <el-button type="primary" @click="openCaseForm()">
              <el-icon><Plus /></el-icon>
              新增用例
            </el-button>
          </div>
        </div>
        
        <div class="table-section">
          <div class="table-wrapper">
            <el-table 
              :data="pagedCaseList" 
              :border="false" 
              style="min-width: 900px"
              v-loading="loading"
            >
              <el-table-column prop="name" label="用例名称" min-width="120">
                <template #default="scope">
                  <el-link type="primary" @click="handleViewDetail(scope.row)" class="case-name-link">
                    {{ scope.row.name }}
                  </el-link>
                </template>
              </el-table-column>
              <el-table-column prop="description" label="描述" min-width="180" show-overflow-tooltip />
              <el-table-column label="所属分组" min-width="120">
                <template #default="scope">
                  <el-tag size="small" effect="plain">
                    {{ getGroupName(scope.row.group_id) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="所属API" min-width="180">
                <template #default="scope">
                  <el-tooltip 
                    v-if="getApiInfo(scope.row.api_id)"
                    :content="getApiInfo(scope.row.api_id).url"
                    placement="top"
                  >
                    <div class="api-info">
                      <el-tag 
                        size="small" 
                        :type="getApiInfo(scope.row.api_id).method === 'GET' ? 'success' : 
                               getApiInfo(scope.row.api_id).method === 'POST' ? 'warning' :
                               getApiInfo(scope.row.api_id).method === 'PUT' ? 'info' : 'danger'"
                      >
                        {{ getApiInfo(scope.row.api_id).method }}
                      </el-tag>
                      <span class="api-name">{{ getApiInfo(scope.row.api_id).name }}</span>
                    </div>
                  </el-tooltip>
                  <span v-else class="no-api">-</span>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="scope">
                  <el-button-group>
                    <el-button size="small" type="primary" plain @click="handleEdit(scope.row)">
                      <el-icon><Edit /></el-icon>
                    </el-button>
                    <el-button size="small" type="danger" plain @click="handleDelete(scope.row)">
                      <el-icon><Delete /></el-icon>
                    </el-button>
                    <el-button size="small" type="success" plain @click="handleRun(scope.row)">
                      <el-icon><VideoPlay /></el-icon>
                    </el-button>
                  </el-button-group>
                </template>
              </el-table-column>
            </el-table>
            
            <!-- 分页 -->
            <div class="pagination-container">
              <el-pagination
                v-model:currentPage="currentPage"
                v-model:pageSize="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="total"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, reactive, toRefs } from 'vue'
import { Search, Plus, Edit, Delete, VideoPlay, RefreshRight, Check } from '@element-plus/icons-vue'
import { getCases, addCase, updateCase, deleteCaseById } from '@/api/caseManage'
import { getApiList } from '@/api/apiManage'
import { getGroupList } from '@/api/groupManage'
import { ElMessageBox, ElMessage } from 'element-plus'

// 状态管理
const state = reactive({
  caseList: [],
  groupList: [],
  apiList: [],
  selectedGroup: null,
  search: '',
  loading: false,
  currentPage: 1,
  pageSize: 10,
  total: 0,
});

// 分页的用例列表
const pagedCaseList = computed(() => {
  let filteredList = state.caseList;
  
  // 按分组筛选
  if (state.selectedGroup) {
    filteredList = filteredList.filter(item => item.group_id === state.selectedGroup);
  }
  
  // 按搜索关键字筛选
  if (state.search) {
    filteredList = filteredList.filter(item => 
      item.name.toLowerCase().includes(state.search.toLowerCase())
    );
  }
  
  // 更新总数
  state.total = filteredList.length;
  
  // 分页
  const start = (state.currentPage - 1) * state.pageSize;
  const end = start + state.pageSize;
  return filteredList.slice(start, end);
});

// API相关方法
const getApiInfo = (apiId) => {
  if (!apiId) return null;
  return state.apiList.find(api => api.id === apiId);
};

// 分组相关方法
const getGroupName = (groupId) => {
  if (!groupId) return '-';
  const group = state.groupList.find(g => g.id === groupId);
  return group ? group.name : '-';
};

// 加载数据方法
const loadApiList = async () => {
  try {
    const response = await getApiList();
    state.apiList = response.data || [];
  } catch (error) {
    console.error('Failed to load API list:', error);
    ElMessage.error(error.response?.data?.detail || '加载API列表失败');
    state.apiList = [];
  }
};

const loadGroupList = async () => {
  try {
    const response = await getGroupList();
    state.groupList = response.data || [];
  } catch (error) {
    console.error('Failed to load group list:', error);
    ElMessage.error(error.response?.data?.detail || '加载分组列表失败');
    state.groupList = [];
  }
};

const loadCaseList = async () => {
  try {
    state.loading = true;
    const response = await getCases();
    state.caseList = response.data || [];
    state.total = state.caseList.length;
  } catch (error) {
    console.error('Failed to load case list:', error);
    ElMessage.error(error.response?.data?.detail || '加载用例列表失败');
    state.caseList = [];
    state.total = 0;
  } finally {
    state.loading = false;
  }
};

// 操作处理方法
const handleViewDetail = (row) => {
  // TODO: 实现跳转到详情页的逻辑
  console.log('View detail:', row);
};

const handleEdit = (row) => {
  // TODO: 实现编辑功能
  console.log('Edit:', row);
};

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确认删除用例 "${row.name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );
    
    await deleteCaseById(row.id);
    ElMessage.success('删除成功');
    await loadCaseList();
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete case:', error);
      ElMessage.error('删除失败');
    }
  }
};

const handleRun = (row) => {
  // TODO: 实现运行功能
  console.log('Run:', row);
};

// 分页处理
const handleCurrentChange = (val) => {
  state.currentPage = val;
};

const handleSizeChange = (val) => {
  state.pageSize = val;
  state.currentPage = 1;
};

// 搜索处理
const handleSearch = () => {
  state.currentPage = 1;
};

// 表单处理
const openCaseForm = () => {
  // TODO: 实现新增用例功能
  console.log('Open case form');
};

// 生命周期钩子
onMounted(async () => {
  try {
    state.loading = true;
    await Promise.all([
      loadApiList(),
      loadGroupList(),
      loadCaseList(),
    ]);
  } catch (error) {
    console.error('Failed to initialize data:', error);
    ElMessage.error('初始化数据失败');
  } finally {
    state.loading = false;
  }
});

// 导出状态和方法
const { 
  caseList, 
  groupList, 
  apiList, 
  loading, 
  currentPage, 
  pageSize, 
  total,
  selectedGroup,
  search,
} = toRefs(state);

defineExpose({
  caseList,
  groupList,
  apiList,
  loading,
  currentPage,
  pageSize,
  total,
  selectedGroup,
  search,
  pagedCaseList,
  getApiInfo,
  getGroupName,
  handleViewDetail,
  handleEdit,
  handleDelete,
  handleRun,
  handleCurrentChange,
  handleSizeChange,
  handleSearch,
  openCaseForm,
});
</script>

