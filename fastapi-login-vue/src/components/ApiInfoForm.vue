<template>
  <el-container class="app-container">
    <el-main class="main-content">
      <!-- 接口管理页面 -->
      <div class="content-wrapper">
        <div class="header-section">
          <div class="left-section">
            <div class="search-section">
              <el-select 
                v-model="selectedGroup" 
                placeholder="选择分组" 
                style="width: 180px" 
                @change="fetchApis"
                size="default"
              >
                <el-option label="全部分组" :value="null" />
                <el-option v-for="g in groups" :key="g.id" :label="g.name" :value="g.id" />
              </el-select>
              <el-input
                v-model="search"
                placeholder="搜索接口名称/URL"
                style="width: 220px"
                clearable
                @keyup.enter="handleSearch"
                size="default"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
              <el-button type="primary" @click="handleSearch" size="default">
                <el-icon><Search /></el-icon>
                查询
              </el-button>
            </div>
          </div>
          <div class="right-section">
            <el-button type="primary" @click="openApiForm()" size="default">
              <el-icon><Plus /></el-icon>
              新增接口
            </el-button>
          </div>
        </div>
        <div class="table-section" style="overflow-x:auto;">
          <el-table :data="pagedApiList" :border="false" style="min-width: 900px; width: auto; table-layout: auto;">
            <el-table-column prop="name" label="名称" min-width="120" />
            <el-table-column prop="url" label="URL" min-width="180" />
            <el-table-column prop="method" label="方法" min-width="80" />
            <el-table-column prop="group_name" label="分组" min-width="100" />
            <el-table-column prop="description" label="描述" min-width="180" />
            <el-table-column label="操作" min-width="180" fixed="right">
              <template #default="scope">
                <el-button size="small" @click="editApi(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="handleDeleteApi(scope.row.id)">删除</el-button>
                <el-button size="small" type="success" @click="runApi(scope.row)">运行</el-button>
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
              <el-col :span="12">
                <el-form-item label="所属分组" prop="group_id">
                  <el-select v-model="apiForm.group_id" placeholder="请选择分组" style="width: 100%">
                    <el-option
                      v-for="group in groups"
                      :key="group.id"
                      :label="group.name"
                      :value="group.id"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="请求方法" prop="method">
                  <el-select v-model="apiForm.method" placeholder="请选择方法" style="width: 100%">
                    <el-option label="GET" value="GET" />
                    <el-option label="POST" value="POST" />
                    <el-option label="PUT" value="PUT" />
                    <el-option label="DELETE" value="DELETE" />
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
          <el-form-item v-if="debugParamType === 'params'" label="请求参数">
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
            <el-button @click="saveDebugAsCase" style="margin-left: 10px;">保存用例</el-button>
          </el-form-item>

          <!-- 响应结果部分 -->
          <el-form-item label="响应结果" class="response-form-item">
            <div class="response-panel">
              <div class="response-header">
                <div class="response-header-top">
                  <el-tabs v-model="activeTab">
                    <el-tab-pane label="Body" name="body">
                      <template #label>
                        <el-icon><Document /></el-icon>
                        <span>Body</span>
                      </template>
                    </el-tab-pane>
                    <el-tab-pane label="Cookie" name="cookie">
                      <template #label>
                        <el-icon><Connection /></el-icon>
                        <span>Cookie</span>
                      </template>
                    </el-tab-pane>
                    <el-tab-pane label="Header" name="header">
                      <template #label>
                        <el-icon><List /></el-icon>
                        <span>Header</span>
                      </template>
                    </el-tab-pane>
                  </el-tabs>
                </div>

                <div class="body-tab-content" v-if="activeTab === 'body'">
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
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { Search, Plus, Delete } from '@element-plus/icons-vue';
import { addCase } from '../api/apiManage';
import { ElMessage } from 'element-plus';
import { getApiList, deleteApi, addApi, updateApi } from '../api/apiManage';
import { getApiGroups } from '../api/apiManage';
import axios from 'axios';

// 接口相关
const pagedApis = ref([]);
const selectedGroup = ref(null);
const search = ref('');
const activeTab = ref('body');
const responseViewType = ref('pretty');
const debugStatus = ref('');
const debugTime = ref('');
const debugSize = ref('');

// 新增接口弹窗相关
const apiDialogVisible = ref(false);
const apiForm = ref({
  name: '',
  url: '',
  method: '',
  group_id: null,
  description: ''
});

// 分组列表
const groups = ref([]);

// 调试相关
const debugDialogVisible = ref(false);
const debugMethod = ref('GET');
const debugUrl = ref('');
const debugParamType = ref('params');
const debugParamsList = ref([]);
const debugJson = ref('');
const debugForm = ref('');
const debugHeaders = ref('');
const debugResult = ref(null);
const debugApi = ref(null);
const isEdit = ref(false);
const dialogWidth = computed(() => {
  return window.innerWidth <= 768 ? '98%' : '900px';
});

// Methods
const openApiForm = (row = null) => {
  if (row) {
    apiForm.value = {
      ...row,
      description: row.description || ''
    };
    isEdit.value = true;
  } else {
    apiForm.value = {
      name: '',
      url: '',
      method: '',
      group_id: null,
      description: ''
    };
    isEdit.value = false;
  }
  apiDialogVisible.value = true;
};

const submitApiForm = async () => {
  if (isEdit.value) {
    await updateApi(apiForm.value.id, apiForm.value);
  } else {
    await addApi(apiForm.value);
  }
  apiDialogVisible.value = false;
  fetchApis();
};

const editApi = (row) => {
  openApiForm(row);
};

// 删除接口
const handleDeleteApi = async (id) => {
  await deleteApi(id);
  fetchApis();
};

// 接口分页
const apiPage = ref(1);
const apiPageSize = ref(10);

const pagedApiList = computed(() => {
  const start = (apiPage.value - 1) * apiPageSize.value;
  return pagedApis.value.slice(start, start + apiPageSize.value);
});

const handleSearch = async () => {
  apiPage.value = 1;
  await fetchApis();
};

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
  }));
  pagedApis.value = data;
};

const fetchGroups = async () => {
  const res = await getApiGroups();
  groups.value = res.data;
  await fetchApis();
};

// 页面初始化时调用 fetchGroups
fetchGroups();

// 检测屏幕尺寸
const isSmallScreen = ref(window.innerWidth <= 768);

const handleResize = () => {
  isSmallScreen.value = window.innerWidth <= 768;
};

// 添加窗口大小监听
onMounted(() => {
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});

// 调试相关
const runApi = (row) => {
  debugApi.value = row;
  debugMethod.value = row.method;
  debugUrl.value = row.url;
  debugParamType.value = 'params';
  debugParamsList.value = [{ key: '', value: '', type: 'string', desc: '' }];
  debugJson.value = '';
  debugForm.value = '';
  debugHeaders.value = '';
  debugResult.value = '';
  debugDialogVisible.value = true;
};

const addParam = () => {
  debugParamsList.value.push({ key: '', value: '', type: 'string', desc: '' });
};

const removeParam = (idx) => {
  if (debugParamsList.value.length === 1) {
    debugParamsList.value[0] = { key: '', value: '' };
  } else {
    debugParamsList.value.splice(idx, 1);
  }
};

// 保存调试内容为用例
const saveDebugAsCase = async () => {
  // 组装用例数据
  // 组装 params
  let params = undefined, headers = undefined, body = undefined;
  if (debugParamType.value === 'params') {
    params = {};
    debugParamsList.value.forEach(item => {
      if (item.key) params[item.key] = item.value;
    });
  } else if (debugParamType.value === 'json') {
    try { body = debugJson.value ? JSON.parse(debugJson.value) : undefined; } catch { body = undefined; }
  } else if (debugParamType.value === 'form') {
    body = {};
    debugForm.value.split('\n').filter(Boolean).forEach(line => {
      const [k, v] = line.split('=');
      body[k] = v;
    });
  }
  // headers
  try { headers = debugHeaders.value ? JSON.parse(debugHeaders.value) : undefined; } catch { headers = undefined; }

  const caseData = {
    name: debugApi.value?.name || debugUrl.value || '新用例',
    description: debugApi.value?.description || '',
    group_id: debugApi.value?.group_id || 1,
    api_id: debugApi.value?.id || 1,
    method: debugMethod.value,
    request_url: debugUrl.value,
    params,
    headers,
    body,
    expected_status: 200,
    expected_response: {},
  };
  
  try {
    await addCase(caseData);
    ElMessage.success('用例保存成功！');
  } catch (e) {
    ElMessage.error('用例保存失败');
  }
};

const doDebugRequest = async () => {
  let params = {};
  let data = undefined;
  let headers = {};
  // 处理header
  try {
    if (debugHeaders.value.trim()) headers = JSON.parse(debugHeaders.value);
  } catch (e) {
    debugResult.value = 'Header格式错误，需为JSON字符串';
    return;
  }
  // 处理参数
  if (debugParamType.value === 'params') {
    params = {};
    debugParamsList.value.forEach(item => {
      if (item.key) {
        // 类型转换
        let v = item.value;
        if (item.type === 'number') v = Number(item.value);
        else if (item.type === 'boolean') v = item.value === 'true' || item.value === true;
        else if (item.type === 'array') {
          try { v = JSON.parse(item.value); } catch { v = [item.value]; }
        }
        params[item.key] = v;
      }
    });
  } else if (debugParamType.value === 'json') {
    try {
      data = debugJson.value.trim() ? JSON.parse(debugJson.value) : undefined;
    } catch (e) {
      debugResult.value = 'JSON格式错误';
      return;
    }
  } else if (debugParamType.value === 'form') {
    data = new URLSearchParams();
    debugForm.value.split('\n').filter(Boolean).forEach(line => {
      const [k, v] = line.split('=');
      data.append(k, v);
    });
    headers['Content-Type'] = 'application/x-www-form-urlencoded';
  }
  
  console.log('实际请求：', {
    url: debugUrl.value,
    method: debugMethod.value,
    headers,
    params,
    data
  });
  
  const start = Date.now();
  try {
    const res = await axios({
      url: debugUrl.value,
      method: debugMethod.value.toLowerCase(),
      headers,
      params: debugParamType.value === 'params' ? params : undefined,
      data,
      responseType: 'text'
    });
    debugResult.value = formatJson(res.data);
    debugStatus.value = res.status;
    debugTime.value = Date.now() - start;
    debugSize.value = res.headers['content-length'] ? res.headers['content-length'] + ' B' : (typeof res.data === 'string' ? (new Blob([res.data]).size + ' B') : '');
  } catch (err) {
    debugResult.value = err?.response ? formatJson(err.response.data) : String(err);
    debugStatus.value = err?.response?.status || '';
    debugTime.value = Date.now() - start;
    debugSize.value = err?.response?.headers?.['content-length'] ? err.response.headers['content-length'] + ' B' : (err?.response?.data ? (typeof err.response.data === 'string' ? (new Blob([err.response.data]).size + ' B') : '') : '');
  }
};

function highlightedJson(jsonStr) {
  if (!jsonStr) return '';
  let html = jsonStr;
  try {
    const obj = JSON.parse(jsonStr);
    html = JSON.stringify(obj, null, 2);
    html = html.replace(/(&)/g, '&amp;').replace(/(<)/g, '&lt;').replace(/(>)/g, '&gt;');
    html = html.replace(/("[^"]+": )/g, '<span class="key">$1</span>')
      .replace(/(:\s?"[^"]+")/g, '<span class="string">$1</span>')
      .replace(/(:\s?\d+)/g, '<span class="number">$1</span>')
      .replace(/(:\s?true|false)/g, '<span class="boolean">$1</span>')
      .replace(/(:\s?null)/g, '<span class="null">$1</span>');
  } catch {}
  return html;
}

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
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.left-section {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.right-section {
  margin-left: 20px;
}

.search-section {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.table-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.param-table {
  border: 1px solid #ebeef5;
  border-radius: 4px;
}

.param-table-header {
  display: flex;
  background-color: #f5f7fa;
  padding: 12px;
  font-weight: bold;
}

.param-table-body {
  padding: 8px 12px;
}

.param-row {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.param-col {
  padding: 0 8px;
}

.param-name { width: 20%; }
.param-value { width: 30%; }
.param-type { width: 15%; }
.param-desc { width: 25%; }
.param-action { width: 10%; }

.param-add-btn {
  padding: 12px;
  display: flex;
  justify-content: center;
}

.response-panel {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  margin-top: 0;
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 400px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.response-header {
  border-bottom: 1px solid #dcdfe6;
  background-color: #f5f7fa;
  padding: 0;
}

.response-header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.body-tab-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-top: 1px solid #dcdfe6;
}

.response-content {
  flex: 1;
  overflow: auto;
  background-color: #ffffff;
  position: relative;
}

.response-view {
  height: 100%;
  overflow: auto;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.json-content {
  word-wrap: break-word;
  font-family: monaco, menlo, consolas, 'courier new', monospace;
  font-size: 13px;
  line-height: 1.5;
  padding: 8px;
}

.empty-content {
  color: #909399;
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.response-status {
  margin-top: 8px;
  color: #606266;
  border-top: 1px solid #ebeef5;
  padding-top: 8px;
}

.success-status {
  color: #67c23a;
}

.view-options {
  margin-bottom: 12px;
}

@media screen and (max-width: 768px) {
  .header-section {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }
  
  .left-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .right-section {
    margin-left: 0;
    display: flex;
    justify-content: flex-end;
  }
  
  .search-section {
    flex-direction: column;
  }
}
</style>
