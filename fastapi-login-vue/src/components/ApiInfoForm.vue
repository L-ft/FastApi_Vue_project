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

          <!-- 环境选择 -->
          <el-form-item label="所属环境">
            <el-select v-model="debugEnvironment" placeholder="选择环境" style="width: 200px" clearable>
              <el-option
                v-for="env in environments"
                :key="env.id"
                :label="env.name"
                :value="env.id"
              >
                <div style="display: flex; justify-content: space-between;">
                  <span>{{ env.name }}</span>
                  <span style="color: #8492a6; font-size: 13px;">{{ env.value }}</span>
                </div>
              </el-option>
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
          <el-form-item label="请求Header">
            <HeaderInput 
              v-model="debugHeaders"
              @add-env-var="$emit('add-env-var')" />
          </el-form-item>

          <!-- 发送请求按钮 -->
          <el-form-item>
            <el-button type="primary" @click="doDebugRequest">发送请求</el-button>
            <el-button type="success" @click="testCustomHeaders" style="margin-left: 10px;">🧪 测试请求头</el-button>
            <el-button type="warning" @click="sendWithFetch" style="margin-left: 10px;">🚀 使用Fetch发送</el-button>
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
import { ref, computed, onMounted, onUnmounted, inject } from 'vue';
import { Search, Plus, Delete } from '@element-plus/icons-vue';
import { addCase as createCase } from '../api/caseManage';
import { ElMessage } from 'element-plus';
import { getApiList, deleteApi, addApi, updateApi } from '../api/apiManage';
import { getApiGroups } from '../api/apiManage';
import { getEnvironments } from '../api/environmentManage';
import axios from 'axios';
import request from '@/utils/request';
import HeaderInput from './HeaderInput.vue';

// 接口相关
const pagedApis = ref([]);
const selectedGroup = ref(null);
const search = ref('');
const activeTab = ref('body');
const responseViewType = ref('pretty');
const debugStatus = ref('');
const debugTime = ref('');
const debugSize = ref('');

// 注入环境变量相关功能
const envVariables = inject('envVariables', ref([]))
const replaceEnvVars = inject('replaceEnvVars', (text) => text)
const envUtils = inject('envUtils', null)

// 环境变量替换的后备函数
const safeReplaceEnvVars = (text) => {
  if (!text || typeof text !== 'string') {
    return text
  }
  
  console.log('🔍 环境变量替换调试:', {
    originalText: text,
    envUtils: envUtils ? '可用' : '不可用',
    replaceEnvVars: replaceEnvVars ? '可用' : '不可用',
    envVariablesCount: envVariables.value ? envVariables.value.length : 0
  })
  
  // 优先使用 envUtils
  if (envUtils && typeof envUtils.replaceVariables === 'function') {
    const result = envUtils.replaceVariables(text)
    console.log('✅ 使用envUtils替换:', text, '->', result)
    return result
  }
  
  // 后备使用注入的replaceEnvVars函数
  if (replaceEnvVars && typeof replaceEnvVars === 'function') {
    const result = replaceEnvVars(text)
    console.log('⚠️ 使用replaceEnvVars替换:', text, '->', result)
    return result
  }
  
  // 最后的后备：手动实现替换
  console.warn('❌ 环境变量替换功能不可用，使用手动实现')
  return manualReplaceEnvVars(text)
}

// 手动环境变量替换实现
const manualReplaceEnvVars = (text) => {
  if (!text || typeof text !== 'string') {
    return text
  }
  
  const placeholderRegex = /\{\{(\w+)\}\}/g
  return text.replace(placeholderRegex, (match, varName) => {
    // 在envVariables中查找对应的变量
    if (envVariables.value && Array.isArray(envVariables.value)) {
      const variable = envVariables.value.find(v => v.key === varName)
      if (variable) {
        console.log(`🔧 手动替换变量: ${match} -> ${variable.value}`)
        return variable.value
      }
    }
    
    console.warn(`⚠️ 未找到环境变量: ${varName}`)
    return match // 保留原占位符
  })
}

// 增强的JSON环境变量替换函数
const replaceEnvVarsInJson = (jsonString) => {
  if (!jsonString || typeof jsonString !== 'string') {
    return jsonString
  }
  
  console.log('🔄 JSON环境变量替换开始:', jsonString)
  
  try {
    // 先解析JSON以确保格式正确
    const jsonObj = JSON.parse(jsonString)
    
    // 递归替换JSON对象中的环境变量
    const replacedObj = replaceEnvVarsInObject(jsonObj)
    
    // 转回JSON字符串
    const result = JSON.stringify(replacedObj, null, 2)
    console.log('✅ JSON环境变量替换完成:', result)
    return result
  } catch (e) {
    // 如果JSON解析失败，直接进行字符串替换
    console.warn('⚠️ JSON解析失败，使用字符串替换:', e.message)
    return safeReplaceEnvVars(jsonString)
  }
}

// 递归替换对象中的环境变量
const replaceEnvVarsInObject = (obj) => {
  if (typeof obj === 'string') {
    return safeReplaceEnvVars(obj)
  } else if (Array.isArray(obj)) {
    return obj.map(item => replaceEnvVarsInObject(item))
  } else if (obj && typeof obj === 'object') {
    const result = {}
    for (const [key, value] of Object.entries(obj)) {
      // 替换键名中的环境变量
      const newKey = safeReplaceEnvVars(key)
      // 递归替换值中的环境变量
      result[newKey] = replaceEnvVarsInObject(value)
    }
    return result
  } else {
    return obj
  }
}

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

// 环境列表
const environments = ref([]);

// 调试相关
const debugDialogVisible = ref(false);
const debugMethod = ref('GET');
const debugUrl = ref('');
const debugEnvironment = ref(null);
const debugParamType = ref('params');
const debugParamsList = ref([]);
const debugJson = ref('');
const debugForm = ref('');
const debugHeaders = ref([]);  // 改为数组格式
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

const fetchEnvironments = async () => {
  try {
    const res = await getEnvironments();
    environments.value = res.data || [];
  } catch (error) {
    console.error('Failed to load environments:', error);
    ElMessage.error('加载环境列表失败');
    environments.value = [];
  }
};

// 页面初始化时调用 fetchGroups 和 fetchEnvironments
fetchGroups();
fetchEnvironments();

// 检测屏幕尺寸
const isSmallScreen = ref(window.innerWidth <= 768);

const handleResize = () => {
  isSmallScreen.value = window.innerWidth <= 768;
};

// 添加窗口大小监听和环境变量初始化
onMounted(async () => {
  window.addEventListener('resize', handleResize);
  
  // 初始化环境变量
  await initializeEnvironmentVariables();
});

// 初始化环境变量
const initializeEnvironmentVariables = async () => {
  try {
    console.log('🔄 初始化环境变量...')
    
    // 如果envUtils不可用，尝试手动加载环境变量
    if (!envUtils && envVariables.value.length === 0) {
      console.log('⚠️ envUtils不可用，尝试手动加载环境变量')
      
      // 导入环境变量API
      const { getEnvironmentVariables } = await import('../api/environmentManage')
      const response = await getEnvironmentVariables()
      const variables = response.data || []
      
      // 更新envVariables
      envVariables.value = variables
      console.log('✅ 手动加载环境变量成功:', variables.length, '个变量')
      variables.forEach(v => console.log(`  - ${v.key}: ${v.value}`))
    } else if (envUtils) {
      console.log('✅ envUtils可用，当前环境变量:', envUtils.getAllVariables().length, '个')
    }
    
    // 强制刷新环境变量（从API重新获取最新数据）
    console.log('🔄 强制刷新环境变量数据...')
    try {
      const { getEnvironmentVariables } = await import('../api/environmentManage')
      const response = await getEnvironmentVariables()
      const variables = response.data || []
      
      // 更新所有环境变量相关的数据
      envVariables.value = variables
      
      if (envUtils && typeof envUtils.setVariables === 'function') {
        envUtils.setVariables(variables)
        console.log('✅ envUtils环境变量已更新')
      }
      
      console.log('✅ 环境变量强制刷新完成:', variables.length, '个变量')
      variables.forEach(v => console.log(`  - ${v.key}: ${v.value.substring(0, 30)}...`))
      
    } catch (refreshError) {
      console.error('⚠️ 强制刷新环境变量失败:', refreshError)
    }
    
  } catch (error) {
    console.error('❌ 初始化环境变量失败:', error)
  }
}

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});

// 调试相关
const runApi = (row) => {
  console.log('runApi called with:', row);
  debugApi.value = row;
  debugMethod.value = row.method;
  // 确保 URL 是相对路径格式，方便 request 实例处理
  debugUrl.value = row.url.startsWith('/') ? row.url : `/${row.url}`;
  console.log('debugUrl set to:', debugUrl.value);
  
  // 如果API有关联的环境ID，则设置为默认环境
  debugEnvironment.value = row.env_id || null;
  
  debugParamType.value = 'params';
  debugParamsList.value = [{ key: '', value: '', type: 'string', desc: '' }];
  debugJson.value = '';
  debugForm.value = '';
  debugHeaders.value = []; // 重置为空数组
  debugResult.value = '';
  debugDialogVisible.value = true;
  console.log('debugDialogVisible set to:', debugDialogVisible.value);
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
  // 验证必需的数据
  if (!debugUrl.value.trim()) {
    ElMessage.error('请输入请求地址');
    return;
  }
  
  if (!debugMethod.value) {
    ElMessage.error('请选择请求方法');
    return;
  }

  console.log('🔄 开始保存用例，将环境变量转换为实际值...')

  // 组装用例数据
  // 组装 params - 替换环境变量为实际值
  let params = undefined, headers = {}, body = undefined;
  if (debugParamType.value === 'params') {
    params = {};
    debugParamsList.value.forEach(item => {
      if (item.key) {
        // 替换键和值中的环境变量
        const resolvedKey = safeReplaceEnvVars(item.key);
        const resolvedValue = safeReplaceEnvVars(item.value);
        params[resolvedKey] = resolvedValue;
        
        console.log(`📝 Params参数: ${item.key} -> ${resolvedKey}, ${item.value} -> ${resolvedValue}`);
      }
    });
  } else if (debugParamType.value === 'json') {
    try { 
      if (debugJson.value) {
        // 使用增强的JSON环境变量替换
        const resolvedJsonString = replaceEnvVarsInJson(debugJson.value);
        body = JSON.parse(resolvedJsonString);
        
        console.log('📝 JSON Body 原始:', debugJson.value);
        console.log('📝 JSON Body 替换后:', resolvedJsonString);
      } else {
        body = undefined;
      }
    } catch (e) { 
      ElMessage.error('JSON格式错误，请检查请求体格式');
      return;
    }
  } else if (debugParamType.value === 'form') {
    body = {};
    debugForm.value.split('\n').filter(Boolean).forEach(line => {
      const [k, v] = line.split('=');
      if (k && v !== undefined) {
        // 替换键和值中的环境变量
        const resolvedKey = safeReplaceEnvVars(k.trim());
        const resolvedValue = safeReplaceEnvVars(v.trim());
        body[resolvedKey] = resolvedValue;
        
        console.log(`📝 Form数据: ${k.trim()} -> ${resolvedKey}, ${v.trim()} -> ${resolvedValue}`);
      }
    });
  }
  
  // 处理headers - 从数组格式转换为对象格式，替换环境变量为实际值
  if (Array.isArray(debugHeaders.value)) {
    console.log('📝 开始处理Headers，替换环境变量...');
    debugHeaders.value.forEach((header, index) => {
      if (header.key && header.value) {
        const resolvedKey = safeReplaceEnvVars(header.key);
        const resolvedValue = safeReplaceEnvVars(header.value);
        headers[resolvedKey] = resolvedValue;
        
        console.log(`📝 Header ${index + 1}: ${header.key} -> ${resolvedKey}, ${header.value} -> ${resolvedValue}`);
      }
    });
  }

  // 构建完整的请求URL
  let fullUrl = debugUrl.value;
  if (debugEnvironment.value) {
    const selectedEnv = environments.value.find(env => env.id === debugEnvironment.value);
    if (selectedEnv) {
      const baseUrl = selectedEnv.value.endsWith('/') ? selectedEnv.value.slice(0, -1) : selectedEnv.value;
      const requestPath = debugUrl.value.startsWith('/') ? debugUrl.value : `/${debugUrl.value}`;
      fullUrl = `${baseUrl}${requestPath}`;
    }
  }

  // 确保必填字段有默认值
  const availableGroups = groups.value.filter(g => g.id);
  const availableApis = pagedApis.value.filter(a => a.id);
  
  if (availableGroups.length === 0) {
    ElMessage.error('没有可用的分组，请先创建分组');
    return;
  }
  
  if (availableApis.length === 0) {
    ElMessage.error('没有可用的API，请先创建API');
    return;
  }

  const caseData = {
    name: (debugApi.value?.name || `调试用例-${new Date().getTime()}`).slice(0, 100),
    description: debugApi.value?.description || `从接口调试自动生成的用例（环境变量已转换为实际值）`,
    group_id: debugApi.value?.group_id || availableGroups[0].id,
    api_id: debugApi.value?.id || availableApis[0].id,
    method: debugMethod.value,
    request_url: fullUrl,
    param_type: debugParamType.value,  // 添加参数类型字段
    params: params || {},
    headers: headers || {},
    body: body || {},
    expected_status: 200,
    expected_response: {},
  };
  
  // 显示环境变量替换总结
  console.log('✅ 环境变量替换完成，用例数据总结:');
  console.log('📋 请求头数量:', Object.keys(headers).length);
  console.log('📋 请求参数类型:', debugParamType.value);
  console.log('📋 请求参数:', params);
  console.log('📋 请求体:', body);
  console.log('📋 完整用例数据:', caseData);
  
  console.log('保存用例数据:', caseData);
  
  try {
    const response = await createCase(caseData);
    console.log('✅ 用例保存成功:', response);
    
    // 统计替换的环境变量数量
    let envVarCount = 0;
    const allText = JSON.stringify(caseData);
    const originalText = JSON.stringify({
      params: debugParamType.value === 'params' ? 
        debugParamsList.value.reduce((acc, item) => {
          if (item.key) acc[item.key] = item.value;
          return acc;
        }, {}) : {},
      headers: debugHeaders.value || [],
      body: debugParamType.value === 'json' ? debugJson.value : 
            debugParamType.value === 'form' ? debugForm.value : {}
    });
    
    // 简单统计占位符数量的差异
    const originalPlaceholders = (originalText.match(/\{\{\w+\}\}/g) || []).length;
    const savedPlaceholders = (allText.match(/\{\{\w+\}\}/g) || []).length;
    envVarCount = originalPlaceholders - savedPlaceholders;
    
    if (envVarCount > 0) {
      ElMessage.success(`用例保存成功！已将 ${envVarCount} 个环境变量转换为实际值`);
    } else {
      ElMessage.success('用例保存成功！');
    }
  } catch (e) {
    console.error('❌ 保存用例失败:', e);
    ElMessage.error(`用例保存失败: ${e.response?.data?.detail || e.message || '未知错误'}`);
  }
};

// 专用的请求发送函数，完全绕过拦截器
const sendCustomRequest = async (config) => {
  console.log('🚀 使用自定义请求函数，完全绕过所有拦截器');
  console.log('📋 请求配置:', JSON.stringify(config, null, 2));
  
  // 创建一个全新的axios实例，不使用任何全局配置
  const customAxios = axios.create({
    timeout: 30000,
    withCredentials: false
  });
  
  // 确保不会有任何拦截器干扰
  customAxios.interceptors.request.clear();
  customAxios.interceptors.response.clear();
  
  return customAxios.request(config);
};

// 测试请求头的专用函数
const testCustomHeaders = async () => {
  console.log('🧪 === 开始测试请求头 ===');
  
  // 构建测试用的headers
  let testHeaders = {};
  if (Array.isArray(debugHeaders.value) && debugHeaders.value.length > 0) {
    debugHeaders.value.forEach((header) => {
      if (header.key && header.value) {
        const resolvedKey = safeReplaceEnvVars(header.key);
        const resolvedValue = safeReplaceEnvVars(header.value);
        testHeaders[resolvedKey] = resolvedValue;
      }
    });
  }
  
  console.log('🔍 测试Headers:', JSON.stringify(testHeaders, null, 2));
  
  // 使用httpbin.org来测试请求头（这是一个测试HTTP请求的服务）
  const testUrl = 'https://httpbin.org/headers';
  
  try {
    console.log('🚀 发送测试请求到 httpbin.org...');
    
    // 创建完全独立的axios实例
    const testAxios = axios.create({
      timeout: 10000,
      withCredentials: false
    });
    
    const response = await testAxios.get(testUrl, {
      headers: testHeaders
    });
    
    console.log('✅ 测试请求成功！');
    console.log('📋 服务器接收到的请求头:', JSON.stringify(response.data, null, 2));
    
    // 检查Authorization头是否正确发送
    const receivedHeaders = response.data.headers;
    if (receivedHeaders.Authorization) {
      console.log('🎉 成功！服务器接收到的Authorization头:', receivedHeaders.Authorization);
      ElMessage.success(`测试成功！Authorization头: ${receivedHeaders.Authorization.substring(0, 30)}...`);
    } else {
      console.log('⚠️ 警告：服务器没有接收到Authorization头');
      ElMessage.warning('测试显示：服务器没有接收到Authorization头');
    }
    
    // 在调试结果中显示测试结果
    debugResult.value = JSON.stringify(response.data, null, 2);
    debugStatus.value = response.status;
    
  } catch (error) {
    console.error('❌ 测试请求失败:', error);
    ElMessage.error(`测试失败: ${error.message}`);
    debugResult.value = `测试失败: ${error.message}`;
  }
};

// 使用原生fetch API发送请求，完全绕过axios
const sendWithFetch = async () => {
  console.log('🚀 === 使用原生Fetch API发送请求 ===');
  
  // 验证必填字段
  if (!debugUrl.value.trim()) {
    ElMessage.error('请输入请求地址');
    return;
  }
  
  // 构建完整的请求URL
  let fullUrl = debugUrl.value;
  let selectedEnvironment = null;
  
  if (debugEnvironment.value) {
    selectedEnvironment = environments.value.find(env => env.id === debugEnvironment.value);
    if (selectedEnvironment) {
      const baseUrl = selectedEnvironment.value.endsWith('/') ? selectedEnvironment.value.slice(0, -1) : selectedEnvironment.value;
      const requestPath = debugUrl.value.startsWith('/') ? debugUrl.value : `/${debugUrl.value}`;
      fullUrl = `${baseUrl}${requestPath}`;
      console.log('使用环境:', selectedEnvironment.name, '- 完整URL:', fullUrl);
    }
  }
  
  // 处理请求头
  let headers = {};
  if (Array.isArray(debugHeaders.value) && debugHeaders.value.length > 0) {
    debugHeaders.value.forEach((header, index) => {
      if (header.key && header.value) {
        const resolvedKey = safeReplaceEnvVars(header.key);
        const resolvedValue = safeReplaceEnvVars(header.value);
        headers[resolvedKey] = resolvedValue;
        console.log(`Fetch Header ${index + 1}: ${resolvedKey} = ${resolvedValue}`);
        
        if (resolvedKey.toLowerCase() === 'authorization') {
          console.log('🔑 Fetch - 检测到Authorization头:', resolvedValue);
        }
      }
    });
  }
  
  // 处理请求参数和数据
  let fetchUrl = fullUrl;
  let body = undefined;
  
  if (debugParamType.value === 'params') {
    const params = new URLSearchParams();
    debugParamsList.value.forEach(item => {
      if (item.key) {
        params.append(item.key, item.value);
      }
    });
    if (params.toString()) {
      fetchUrl += (fullUrl.includes('?') ? '&' : '?') + params.toString();
    }
  } else if (debugParamType.value === 'json') {
    try {
      body = debugJson.value.trim() ? debugJson.value : undefined;
      if (body && !headers['Content-Type']) {
        headers['Content-Type'] = 'application/json';
      }
    } catch (e) {
      ElMessage.error('JSON格式不正确');
      return;
    }
  } else if (debugParamType.value === 'form') {
    const formData = new URLSearchParams();
    debugForm.value.split('\n').filter(Boolean).forEach(line => {
      const [k, v] = line.split('=');
      if (k && v) formData.append(k, v);
    });
    body = formData.toString();
    headers['Content-Type'] = 'application/x-www-form-urlencoded';
  }
  
  console.log('🔍 Fetch请求配置:');
  console.log('URL:', fetchUrl);
  console.log('Method:', debugMethod.value);
  console.log('Headers:', JSON.stringify(headers, null, 2));
  console.log('Body:', body);
  
  const start = Date.now();
  try {
    const response = await fetch(fetchUrl, {
      method: debugMethod.value,
      headers: headers,
      body: body,
      mode: 'cors'
    });
    
    const responseText = await response.text();
    const endTime = Date.now() - start;
    
    console.log('✅ Fetch请求成功!');
    console.log('状态:', response.status);
    console.log('响应头:', Object.fromEntries(response.headers.entries()));
    
    debugResult.value = formatJson(responseText);
    debugStatus.value = response.status;
    debugTime.value = endTime;
    debugSize.value = responseText.length + ' B';
    
    ElMessage.success(`Fetch请求成功 (${endTime}ms)`);
    
  } catch (error) {
    console.error('❌ Fetch请求失败:', error);
    const endTime = Date.now() - start;
    
    debugResult.value = `Fetch请求失败: ${error.message}`;
    debugStatus.value = '网络错误';
    debugTime.value = endTime;
    debugSize.value = '0 B';
    
    ElMessage.error(`Fetch请求失败: ${error.message}`);
  }
};

const doDebugRequest = async () => {
  console.log('=== 开始API调试请求 ===');
  console.log('请求方法:', debugMethod.value);
  console.log('请求地址:', debugUrl.value);
  console.log('所属环境:', debugEnvironment.value);
  console.log('请求头数量:', debugHeaders.value ? debugHeaders.value.length : 0);
  
  // 验证必填字段
  if (!debugUrl.value.trim()) {
    ElMessage.error('请输入请求地址');
    return;
  }
  
  // 构建完整的请求URL - 优先使用用户选择的环境
  let fullUrl = debugUrl.value;
  let selectedEnvironment = null;
  
  if (debugEnvironment.value) {
    selectedEnvironment = environments.value.find(env => env.id === debugEnvironment.value);
    if (selectedEnvironment) {
      // 拼接环境地址和请求地址
      const baseUrl = selectedEnvironment.value.endsWith('/') ? selectedEnvironment.value.slice(0, -1) : selectedEnvironment.value;
      const requestPath = debugUrl.value.startsWith('/') ? debugUrl.value : `/${debugUrl.value}`;
      fullUrl = `${baseUrl}${requestPath}`;
      console.log('使用环境:', selectedEnvironment.name, '- 完整URL:', fullUrl);
    }
  } else {
    console.log('未选择环境，使用原始URL:', fullUrl);
  }
  
  let params = {};
  let data = undefined;
  let headers = {};
  
  // 处理用户填写的请求头 - 优先使用用户输入的headers
  console.log('=== 处理请求头 ===');
  console.log('用户填写的debugHeaders:', debugHeaders.value);
  
  if (Array.isArray(debugHeaders.value) && debugHeaders.value.length > 0) {
    debugHeaders.value.forEach((header, index) => {
      if (header.key && header.value) {
        // 解析环境变量占位符
        const resolvedKey = safeReplaceEnvVars(header.key);
        const resolvedValue = safeReplaceEnvVars(header.value);
        headers[resolvedKey] = resolvedValue;
        console.log(`Header ${index + 1}: ${resolvedKey} = ${resolvedValue}`);
        
        // 特别记录Authorization头
        if (resolvedKey.toLowerCase() === 'authorization') {
          console.log('🔑 检测到用户设置的Authorization头:', resolvedValue);
        }
      }
    });
    console.log('最终请求头对象:', headers);
    
    // 验证Authorization头是否存在
    const authHeader = headers['Authorization'] || headers['authorization'];
    if (authHeader) {
      console.log('✅ 确认Authorization头已设置:', authHeader.substring(0, 20) + '...');
    } else {
      console.log('⚠️ 未检测到Authorization头');
    }
  } else {
    console.log('未设置请求头');
  }
  
  // 处理请求参数
  console.log('=== 处理请求参数 ===');
  console.log('参数类型:', debugParamType.value);
  
  if (debugParamType.value === 'params') {
    params = {};
    debugParamsList.value.forEach(item => {
      if (item.key) {
        // 环境变量替换
        const resolvedKey = safeReplaceEnvVars(item.key);
        let resolvedValue = safeReplaceEnvVars(item.value);
        
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
  } else if (debugParamType.value === 'json') {
    try {
      console.log('🔄 开始处理JSON参数类型')
      console.log('原始JSON:', debugJson.value)
      
      // 使用增强的JSON环境变量替换
      const resolvedJsonString = replaceEnvVarsInJson(debugJson.value);
      console.log('JSON环境变量替换前:', debugJson.value);
      console.log('JSON环境变量替换后:', resolvedJsonString);
      
      // 解析替换后的JSON
      data = resolvedJsonString.trim() ? JSON.parse(resolvedJsonString) : undefined;
      console.log('最终解析的JSON数据:', data);
    } catch (e) {
      console.error('JSON解析错误:', e);
      debugResult.value = 'JSON格式错误或环境变量替换失败';
      ElMessage.error('JSON格式不正确或包含无效的环境变量，请检查语法');
      return;
    }
  } else if (debugParamType.value === 'form') {
    data = new URLSearchParams();
    debugForm.value.split('\n').filter(Boolean).forEach(line => {
      const [k, v] = line.split('=');
      if (k && v !== undefined) {
        // 环境变量替换
        const resolvedKey = safeReplaceEnvVars(k.trim());
        const resolvedValue = safeReplaceEnvVars(v.trim());
        
        data.append(resolvedKey, resolvedValue);
        console.log(`Form数据: ${resolvedKey} = ${resolvedValue} [原始: ${k.trim()}=${v.trim()}]`);
      }
    });
    headers['Content-Type'] = 'application/x-www-form-urlencoded';
    console.log('添加Content-Type头: application/x-www-form-urlencoded');
  }
  
  console.log('=== 发送请求 ===');
  console.log('请求配置:', {
    url: fullUrl,
    method: debugMethod.value,
    headers: headers,
    params: Object.keys(params).length > 0 ? params : undefined,
    data: data,
    environment: selectedEnvironment ? selectedEnvironment.name : '无'
  });
  
  // 🔥 重要：完全绕过所有拦截器，使用原生axios
  console.log('🚀 使用原生axios发送请求，完全绕过拦截器');
  console.log('📋 最终请求头:', JSON.stringify(headers, null, 2));
  
  const start = Date.now();
  try {
    // 创建一个全新的axios实例，不继承任何配置和拦截器
    const freshAxios = axios.create();
    
    const requestConfig = {
      url: fullUrl,
      method: debugMethod.value.toLowerCase(),
      headers: { ...headers }, // 使用展开运算符创建新对象
      timeout: 30000,
      responseType: 'text'
    };
    
    // 根据参数类型添加对应的配置
    if (debugParamType.value === 'params' && Object.keys(params).length > 0) {
      requestConfig.params = params;
    }
    if (data !== undefined) {
      requestConfig.data = data;
    }
    
    console.log('🔍 即将发送的完整请求配置:', JSON.stringify(requestConfig, null, 2));
    
    // 使用自定义请求函数发送请求
    const res = await sendCustomRequest(requestConfig);
    
    console.log('✅ 请求发送成功!');
    console.log('📊 响应状态:', res.status);
    console.log('📋 响应头:', res.headers);
    
    console.log('=== 请求成功 ===');
    console.log('响应状态:', res.status);
    console.log('响应头:', res.headers);
    
    debugResult.value = formatJson(res.data);
    debugStatus.value = res.status;
    debugTime.value = Date.now() - start;
    debugSize.value = res.headers['content-length'] ? 
      res.headers['content-length'] + ' B' : 
      (typeof res.data === 'string' ? (new Blob([res.data]).size + ' B') : '未知大小');
      
    ElMessage.success(`请求成功 (${debugTime.value}ms)`);
    
  } catch (err) {
    console.log('=== 请求失败 ===');
    console.error('错误详情:', err);
    
    // 详细的错误处理
    let errorMessage = '请求失败';
    let errorDetail = '';
    
    if (err.code === 'ECONNREFUSED') {
      errorMessage = '连接被拒绝';
      errorDetail = '无法连接到目标服务器，请检查服务器是否运行正常';
    } else if (err.code === 'ETIMEDOUT') {
      errorMessage = '请求超时';
      errorDetail = '请检查网络连接或服务器响应速度';
    } else if (err.response) {
      errorMessage = `HTTP ${err.response.status}`;
      errorDetail = err.response.data ? (typeof err.response.data === 'string' ? err.response.data : JSON.stringify(err.response.data)) : '无响应内容';
    }
    
    debugResult.value = err?.response ? formatJson(err.response.data) : `${errorMessage}: ${errorDetail}`;
    debugStatus.value = err?.response?.status || '网络错误';
    debugTime.value = Date.now() - start;
    debugSize.value = err?.response?.headers?.['content-length'] ? 
      err.response.headers['content-length'] + ' B' : 
      (err?.response?.data ? (typeof err.response.data === 'string' ? (new Blob([err.response.data]).size + ' B') : '未知大小') : '0 B');
    
    ElMessage.error(`${errorMessage}: ${errorDetail}`);
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

/* 环境选择器样式 */
:deep(.el-select-dropdown__item) {
  padding: 8px 20px;
}

:deep(.el-select-dropdown__item div) {
  width: 100%;
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
