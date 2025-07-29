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

/* 运行结果对话框样式 */
.result-header {
  margin-bottom: 16px;
}

.result-header h4 {
  margin: 0 0 8px 0;
  color: #1f2937;
  font-size: 16px;
}

.result-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 8px;
  font-size: 13px;
}

.request-url {
  font-size: 13px;
  color: #6b7280;
  word-break: break-all;
}

.result-content h5 {
  margin: 0 0 8px 0;
  color: #374151;
  font-size: 14px;
  font-weight: 500;
}

.result-textarea :deep(.el-textarea__inner) {
  font-family: 'Courier New', monospace;
  font-size: 12px;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
}

.request-details {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 12px;
  margin: 8px 0;
  font-family: 'Courier New', monospace;
  font-size: 12px;
}

.request-details div {
  margin-bottom: 8px;
  word-break: break-all;
}

.request-details div:last-child {
  margin-bottom: 0;
}

/* 提取变量对话框样式 */
.extract-variable-dialog .el-form-item {
  margin-bottom: 18px;
}

.extract-variable-dialog .el-input__inner {
  font-family: 'Courier New', monospace;
}

.extract-variable-dialog .el-textarea__inner {
  font-family: 'Courier New', monospace;
  font-size: 12px;
}

.jsonpath-help {
  margin-top: 8px;
  padding: 8px;
  background: #f8f9fa;
  border-radius: 4px;
  border-left: 3px solid #409eff;
}

.jsonpath-help code {
  background: #e9ecef;
  padding: 2px 4px;
  border-radius: 2px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
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
                  <el-tag size="small" effect="plain" class="group-tag">
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
              <el-table-column label="参数类型" min-width="100">
                <template #default="scope">
                  <el-tag 
                    size="small" 
                    :type="scope.row.param_type === 'params' ? 'success' : 
                           scope.row.param_type === 'json' ? 'warning' : 'info'"
                  >
                    {{ scope.row.param_type === 'params' ? 'Params' : 
                       scope.row.param_type === 'json' ? 'JSON' : 
                       scope.row.param_type === 'form' ? 'Form' : 'Unknown' }}
                  </el-tag>
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
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
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
    
    <!-- 运行结果对话框 -->
    <el-dialog
      v-model="runResultDialog"
      title="用例运行结果"
      width="60%"
      :close-on-click-modal="false"
    >
      <div v-if="currentRunningCase">
        <div class="result-header">
          <h4>{{ currentRunningCase.name }}</h4>
          <div class="result-meta">
            <span>状态码: <el-tag :type="runStatus >= 200 && runStatus < 300 ? 'success' : 'danger'">{{ runStatus }}</el-tag></span>
            <span>耗时: {{ runTime }}</span>
            <span>方法: <el-tag>{{ currentRunningCase.method }}</el-tag></span>
          </div>
          <div class="request-url">
            <strong>请求地址:</strong> {{ currentRunningCase.request_url }}
          </div>
        </div>
        
        <el-divider />
        
        <div class="result-content">
          <h5>请求详情:</h5>
          <div class="request-details">
            <div><strong>请求方法:</strong> {{ currentRunningCase.method }}</div>
            <div><strong>请求地址:</strong> {{ currentRunningCase.request_url }}</div>
            <div v-if="currentRunningCase.params"><strong>请求参数:</strong> {{ JSON.stringify(currentRunningCase.params, null, 2) }}</div>
            <div v-if="currentRunningCase.headers"><strong>请求头:</strong> {{ JSON.stringify(currentRunningCase.headers, null, 2) }}</div>
            <div v-if="currentRunningCase.body"><strong>请求体:</strong> {{ JSON.stringify(currentRunningCase.body, null, 2) }}</div>
          </div>
          
          <h5 style="margin-top: 20px;">响应结果:</h5>
          <el-input
            v-model="runResult"
            type="textarea"
            :rows="15"
            readonly
            class="result-textarea"
          />
        </div>
      </div>
      
      <template #footer>
        <el-button type="primary" @click="openExtractVariableDialog">提取变量</el-button>
        <el-button @click="runResultDialog = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 提取变量对话框 -->
    <el-dialog
      v-model="extractVariableDialog"
      title="提取变量"
      width="50%"
      :close-on-click-modal="false"
      class="extract-variable-dialog"
    >
      <el-form :model="extractForm" label-width="100px">
        <el-form-item label="选择环境">
          <el-select v-model="extractForm.envId" placeholder="请选择环境" style="width: 100%">
            <el-option
              v-for="env in state.environmentList"
              :key="env.id"
              :label="env.name"
              :value="env.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="变量名">
          <el-input v-model="extractForm.key" placeholder="请输入变量名" />
        </el-form-item>
        
        <el-form-item label="JSONPath">
          <el-input v-model="extractForm.jsonPath" placeholder="例如: access_token 或 data.token 或 data[0].id">
            <template #prepend>$.</template>
          </el-input>
          <div class="jsonpath-help">
            <small>
              常用示例：<br/>
              • <code>access_token</code> - 提取根级别的access_token字段<br/>
              • <code>data.token</code> - 提取data对象中的token字段<br/>
              • <code>data[0].id</code> - 提取data数组第一个元素的id字段<br/>
              • <code>data[*].name</code> - 提取data数组中所有元素的name字段
            </small>
          </div>
        </el-form-item>
        
        <el-form-item label="提取结果">
          <el-input 
            v-model="extractForm.value" 
            type="textarea" 
            :rows="3" 
            readonly 
            placeholder="请输入JSONPath后预览提取结果"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="previewExtractValue">预览提取</el-button>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="extractVariableDialog = false">取消</el-button>
        <el-button type="primary" @click="saveExtractedVariable" :disabled="!extractForm.value">保存变量</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, reactive, toRefs } from 'vue'
import { Search, Plus, Edit, Delete, VideoPlay, RefreshRight, Check } from '@element-plus/icons-vue'
import { getCases, addCase, updateCase, deleteCaseById } from '@/api/caseManage'
import { getApiList } from '@/api/apiManage'
import { getGroupList } from '@/api/groupManage'
import { getEnvironments, addEnvironmentVariable } from '@/api/environmentManage'
import { ElMessageBox, ElMessage } from 'element-plus'
import request from '@/utils/request'
import axios from 'axios'
import jp from 'jsonpath'
import { useEnvironmentVariables } from '@/composables/useEnvironmentVariables'

// 环境变量处理
const { envUtils, replaceEnvVars } = useEnvironmentVariables()

// 状态管理
const state = reactive({
  caseList: [],
  groupList: [],
  apiList: [],
  environmentList: [],
  selectedGroup: null,
  search: '',
  loading: false,
  currentPage: 1,
  pageSize: 10,
  total: 0,
});

// 运行结果相关状态
const runResultDialog = ref(false);
const runResult = ref('');
const runStatus = ref('');
const runTime = ref('');
const currentRunningCase = ref(null);

// 提取变量相关状态
const extractVariableDialog = ref(false);
const extractForm = ref({
  envId: null,
  key: '',
  jsonPath: '',
  value: ''
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

// 环境相关方法
const getEnvironmentName = (envId) => {
  if (!envId) return '-';
  const env = state.environmentList.find(e => e.id === envId);
  return env ? env.name : '-';
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

const loadEnvironmentList = async () => {
  try {
    const response = await getEnvironments();
    state.environmentList = response.data || [];
    
    // 更新环境变量工具
    if (envUtils && state.environmentList.length > 0) {
      // 获取所有环境的变量
      const allVariables = [];
      state.environmentList.forEach(env => {
        if (env.variables && env.variables.length > 0) {
          allVariables.push(...env.variables);
        }
      });
      envUtils.setVariables(allVariables);
      console.log('CaseManagement: 环境变量已更新', allVariables.length, '个变量');
    }
  } catch (error) {
    console.error('Failed to load environment list:', error);
    ElMessage.error(error.response?.data?.detail || '加载环境列表失败');
    state.environmentList = [];
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
    
    console.log('Deleting case with ID:', row.id);
    const response = await deleteCaseById(row.id);
    console.log('Delete response:', response);
    
    ElMessage.success(response.data?.message || '删除成功');
    await loadCaseList();
  } catch (error) {
    if (error === 'cancel') {
      console.log('User canceled deletion');
      return;
    }
    
    console.error('Failed to delete case:', error);
    
    // 更详细的错误处理
    if (error.response) {
      const status = error.response.status;
      const message = error.response.data?.detail || error.response.data?.message || '删除失败';
      
      if (status === 404) {
        ElMessage.error('用例不存在或已被删除');
      } else if (status === 403) {
        ElMessage.error('没有权限删除此用例');
      } else if (status === 500) {
        ElMessage.error('服务器内部错误，删除失败');
      } else {
        ElMessage.error(`删除失败: ${message}`);
      }
    } else if (error.request) {
      ElMessage.error('网络错误，无法连接到服务器');
    } else {
      ElMessage.error('删除失败: ' + (error.message || '未知错误'));
    }
  }
};

// 辅助函数
function formatJson(data) {
  if (typeof data === 'string') {
    try {
      return JSON.stringify(JSON.parse(data), null, 2);
    } catch {
      return data;
    }
  }
  return JSON.stringify(data, null, 2);
}

const handleRun = async (row) => {
  console.log('doDebugRequest called (from case run)');
  console.log('Running case:', row);
  console.log('debugMethod:', row.method);
  
  currentRunningCase.value = row;
  
  // 从用例数据中提取参数，模拟调试界面的数据结构
  let debugUrl = row.request_url;
  let debugMethod = row.method;
  let debugEnvironment = null; // 用例暂时不支持环境选择，使用null
  let debugParamType = row.param_type || 'params'; // 使用保存的参数类型
  let debugParamsList = [];
  let debugJson = '';
  let debugForm = '';
  let debugHeaders = '';
  
  console.log('使用保存的参数类型:', debugParamType);
  
  // 根据保存的参数类型转换数据格式
  if (debugParamType === 'params' && row.params && Object.keys(row.params).length > 0) {
    // params类型：转换为参数列表格式
    Object.entries(row.params).forEach(([key, value]) => {
      debugParamsList.push({
        key: key,
        value: String(value),
        type: typeof value === 'number' ? 'number' : 
              typeof value === 'boolean' ? 'boolean' :
              Array.isArray(value) ? 'array' : 'string',
        desc: ''
      });
    });
  } else if (debugParamType === 'json' && row.body && Object.keys(row.body).length > 0) {
    // json类型：转换为JSON字符串
    debugJson = JSON.stringify(row.body, null, 2);
  } else if (debugParamType === 'form' && row.body && Object.keys(row.body).length > 0) {
    // form类型：转换为form格式
    debugForm = Object.entries(row.body)
      .map(([k, v]) => `${k}=${v}`)
      .join('\n');
  }
  
  // 处理headers
  if (row.headers && Object.keys(row.headers).length > 0) {
    debugHeaders = JSON.stringify(row.headers, null, 2);
  }
  
  console.log('智能识别的参数类型:', debugParamType);
  console.log('转换后的调试数据:', {
    debugUrl,
    debugMethod,
    debugParamType,
    debugParamsList,
    debugJson,
    debugForm,
    debugHeaders
  });
  
  // === 以下代码与ApiInfoForm.vue中doDebugRequest完全一致 ===
  
  // 构建完整的请求URL
  let fullUrl = debugUrl;
  if (debugEnvironment) {
    const selectedEnv = state.environmentList.find(env => env.id === debugEnvironment);
    if (selectedEnv) {
      // 拼接环境地址和请求地址
      const baseUrl = selectedEnv.value.endsWith('/') ? selectedEnv.value.slice(0, -1) : selectedEnv.value;
      const requestPath = debugUrl.startsWith('/') ? debugUrl : `/${debugUrl}`;
      fullUrl = `${baseUrl}${requestPath}`;
      console.log('Full URL with environment:', fullUrl);
    }
  }
  
  let params = {};
  let data = undefined;
  let headers = {};
  // 处理header
  try {
    if (debugHeaders.trim()) headers = JSON.parse(debugHeaders);
  } catch (e) {
    runResult.value = 'Header格式错误，需为JSON字符串';
    runResultDialog.value = true;
    return;
  }
  // 处理参数
  if (debugParamType === 'params') {
    params = {};
    debugParamsList.forEach(item => {
      if (item.key) {
        // 环境变量替换
        const resolvedKey = envUtils ? envUtils.replaceVariables(item.key) : replaceEnvVars(item.key);
        let resolvedValue = envUtils ? envUtils.replaceVariables(item.value) : replaceEnvVars(item.value);
        
        // 类型转换
        if (item.type === 'number') resolvedValue = Number(resolvedValue);
        else if (item.type === 'boolean') resolvedValue = resolvedValue === 'true' || resolvedValue === true;
        else if (item.type === 'array') {
          try { resolvedValue = JSON.parse(resolvedValue); } catch { resolvedValue = [resolvedValue]; }
        }
        
        params[resolvedKey] = resolvedValue;
        console.log(`参数: ${resolvedKey} = ${resolvedValue} (${item.type}) [原始: ${item.key}=${item.value}]`);
      }
    });
  } else if (debugParamType === 'json') {
    try {
      // 先进行环境变量替换，再解析JSON
      const resolvedJsonString = envUtils ? envUtils.replaceVariables(debugJson) : replaceEnvVars(debugJson);
      console.log('JSON环境变量替换前:', debugJson);
      console.log('JSON环境变量替换后:', resolvedJsonString);
      
      data = resolvedJsonString.trim() ? JSON.parse(resolvedJsonString) : undefined;
      console.log('解析后的JSON数据:', data);
    } catch (e) {
      runResult.value = 'JSON格式错误或环境变量替换失败';
      runResultDialog.value = true;
      return;
    }
  } else if (debugParamType === 'form') {
    data = new URLSearchParams();
    debugForm.split('\n').filter(Boolean).forEach(line => {
      const [k, v] = line.split('=');
      if (k && v !== undefined) {
        // 环境变量替换
        const resolvedKey = envUtils ? envUtils.replaceVariables(k.trim()) : replaceEnvVars(k.trim());
        const resolvedValue = envUtils ? envUtils.replaceVariables(v.trim()) : replaceEnvVars(v.trim());
        
        data.append(resolvedKey, resolvedValue);
        console.log(`Form数据: ${resolvedKey} = ${resolvedValue} [原始: ${k.trim()}=${v.trim()}]`);
      }
    });
    headers['Content-Type'] = 'application/x-www-form-urlencoded';
  }
  
  console.log('实际请求：', {
    url: fullUrl,
    method: debugMethod,
    headers,
    params,
    data
  });
  
  const start = Date.now();
  try {
    // 如果选择了环境，直接使用axios发送请求到完整URL
    // 否则使用配置好的 request 实例
    let res;
    if (debugEnvironment) {
      res = await axios({
        url: fullUrl,
        method: debugMethod.toLowerCase(),
        headers,
        params: debugParamType === 'params' ? params : undefined,
        data,
        responseType: 'text'
      });
    } else {
      res = await request({
        url: debugUrl,
        method: debugMethod.toLowerCase(),
        headers,
        params: debugParamType === 'params' ? params : undefined,
        data,
        responseType: 'text'
      });
    }
    
    runResult.value = formatJson(res.data);
    runStatus.value = res.status;
    runTime.value = Date.now() - start;
    runResultDialog.value = true;
    ElMessage.success('用例运行成功');
  } catch (err) {
    runResult.value = err?.response ? formatJson(err.response.data) : String(err);
    runStatus.value = err?.response?.status || '';
    runTime.value = Date.now() - start;
    runResultDialog.value = true;
    
    // 根据状态码显示不同的消息
    if (err?.response?.status === 401) {
      ElMessage.warning('用例运行完成，但返回401未授权状态。请检查认证信息是否正确。');
    } else if (err?.response?.status >= 400 && err?.response?.status < 500) {
      ElMessage.warning(`用例运行完成，返回${err.response.status}状态码`);
    } else {
      ElMessage.error('用例运行失败');
    }
  }
};

// 提取变量相关方法
const openExtractVariableDialog = () => {
  // 重置表单
  extractForm.value = {
    envId: null,
    key: '',
    jsonPath: '',
    value: ''
  };
  extractVariableDialog.value = true;
};

const previewExtractValue = () => {
  if (!extractForm.value.jsonPath) {
    ElMessage.warning('请输入JSONPath');
    return;
  }
  
  try {
    // 解析响应结果
    const responseData = JSON.parse(runResult.value);
    
    // 构建完整的JSONPath，如果不是以$开头就添加$
    let jsonPath = extractForm.value.jsonPath;
    if (!jsonPath.startsWith('$')) {
      jsonPath = '$.' + jsonPath;
    }
    
    // 使用JSONPath库进行提取
    const results = jp.query(responseData, jsonPath);
    
    if (results.length === 0) {
      throw new Error('未找到匹配的数据');
    }
    
    // 如果只有一个结果，直接使用；否则返回数组
    const result = results.length === 1 ? results[0] : results;
    
    extractForm.value.value = typeof result === 'string' ? result : JSON.stringify(result);
    ElMessage.success(`提取成功，找到 ${results.length} 个匹配项`);
  } catch (error) {
    console.error('JSONPath提取失败:', error);
    ElMessage.error(`提取失败: ${error.message || '无效的JSONPath'}`);
    extractForm.value.value = '';
  }
};

const saveExtractedVariable = async () => {
  if (!extractForm.value.envId) {
    ElMessage.warning('请选择环境');
    return;
  }
  
  if (!extractForm.value.key) {
    ElMessage.warning('请输入变量名');
    return;
  }
  
  if (!extractForm.value.value) {
    ElMessage.warning('请先预览提取结果');
    return;
  }
  
  try {
    const variableData = {
      env_id: extractForm.value.envId,
      key: extractForm.value.key,
      value: extractForm.value.value
    };
    
    await addEnvironmentVariable(variableData);
    
    // 获取环境名称用于提示
    const envName = getEnvironmentName(extractForm.value.envId);
    ElMessage.success(`变量 "${extractForm.value.key}" 已保存到环境 "${envName}"`);
    extractVariableDialog.value = false;
    
    // 重置表单
    extractForm.value = {
      envId: null,
      key: '',
      jsonPath: '',
      value: ''
    };
  } catch (error) {
    console.error('保存变量失败:', error);
    ElMessage.error(error.response?.data?.detail || '保存变量失败');
  }
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
      loadEnvironmentList(),
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
  getEnvironmentName,
  handleViewDetail,
  handleEdit,
  handleDelete,
  handleRun,
  handleCurrentChange,
  handleSizeChange,
  handleSearch,
  openCaseForm,
  runResultDialog,
  runResult,
  runStatus,
  runTime,
  currentRunningCase,
  extractVariableDialog,
  extractForm,
  openExtractVariableDialog,
  previewExtractValue,
  saveExtractedVariable,
});
</script>

