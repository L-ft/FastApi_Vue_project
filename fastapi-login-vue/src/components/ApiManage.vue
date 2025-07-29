<template>
  <el-container style="height: 100vh; min-height: 100vh;">
    <!-- 侧边栏 -->
    <el-aside width="180px" style="background: #f4f6fa; border-right: 1px solid #e6e6e6; height: 100vh; min-height: 100vh; overflow: hidden;">
      <el-menu :default-active="activeMenu" 
               class="el-menu-vertical-demo" 
               style="border: none; text-align: center; background: #f4f6fa; height: 100%;" 
               @select="activeMenu = $event">
        <el-menu-item index="group" style="display: flex; justify-content: center;">
          <span>分组管理</span>
        </el-menu-item>
        <el-menu-item index="api" style="display: flex; justify-content: center;">
          <span>接口管理</span>
        </el-menu-item>
        <el-menu-item index="env" style="display: flex; justify-content: center;">
          <span>环境管理</span>
        </el-menu-item>
        <el-menu-item index="case" style="display: flex; justify-content: center;">
          <span>用例管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主体内容：动态组件 -->
    <el-container style="height: 100vh; min-height: 100vh;">
      <el-main style="height: 100vh; min-height: 100vh; overflow: hidden;">
        <component 
          :is="getActiveComponent" 
          :envVariables="envVariables"
          :currentEnv="currentEnv"
          @add-env-var="handleAddEnvVar"
          @update-env-vars="handleUpdateEnvVars"
          @env-change="handleEnvChange" />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted, provide } from 'vue'
import ApiGroupForm from './ApiGroupForm.vue'
import ApiInfoForm from './ApiInfoForm.vue'
import EnvironmentalManagement from './EnvironmentalManagement.vue'
import CaseManagement from './CaseManagement.vue'
import { getEnvironmentVariables } from '../api/environmentManage'
import { envUtils } from '../utils/envUtils'

const activeMenu = ref('group')
const envVariables = ref([])
const currentEnv = ref('dev')

const getActiveComponent = computed(() => {
  if (activeMenu.value === 'group') return ApiGroupForm
  if (activeMenu.value === 'api') return ApiInfoForm
  if (activeMenu.value === 'env') return EnvironmentalManagement
  if (activeMenu.value === 'case') return CaseManagement
  return ApiGroupForm
})

// 获取环境变量值的工具函数
const getEnvValue = (key) => {
  return envUtils.getValue(key)
}

// 替换字符串中的环境变量占位符
const replaceEnvVars = (text) => {
  return envUtils.replaceVariables(text)
}

// 提供环境变量给所有子组件
provide('envVariables', envVariables)
provide('currentEnv', currentEnv)
provide('getEnvValue', getEnvValue)
provide('replaceEnvVars', replaceEnvVars)
provide('envUtils', envUtils)

// 初始化时加载环境变量
onMounted(async () => {
  await loadEnvVariables()
})

// 加载环境变量
const loadEnvVariables = async () => {
  try {
    // 调用API获取环境变量
    const response = await getEnvironmentVariables()
    const variables = response.data || []
    envVariables.value = variables
    
    // 更新环境变量工具类
    envUtils.setVariables(variables)
  } catch (error) {
    console.error('加载环境变量失败:', error)
    // 设置默认环境变量作为备用
    const defaultVariables = [
      { key: 'base_url', value: 'http://localhost:8000', description: '基础URL' },
      { key: 'Authorization', value: 'Bearer token_placeholder', description: '认证令牌' },
      { key: 'Content-Type', value: 'application/json', description: '内容类型' },
      { key: 'X-API-Key', value: 'api-key-placeholder', description: 'API密钥' }
    ]
    envVariables.value = defaultVariables
    envUtils.setVariables(defaultVariables)
  }
}

// 处理添加环境变量的事件
const handleAddEnvVar = () => {
  // 切换到环境管理页面
  activeMenu.value = 'env'
  // 给环境管理组件一点时间加载
  setTimeout(() => {
    // 获取环境管理组件的实例
    const envComponent = document.querySelector('.main-content')
    if (envComponent) {
      // 触发新增变量的动作
      const addVarButton = envComponent.querySelector('.env-search-right button')
      if (addVarButton) {
        addVarButton.click()
      }
    }
  }, 100)
}

// 处理环境变量更新事件
const handleUpdateEnvVars = (newEnvVars) => {
  envVariables.value = newEnvVars
  envUtils.setVariables(newEnvVars)
}

// 处理环境切换事件
const handleEnvChange = async (newEnv) => {
  currentEnv.value = newEnv
  await loadEnvVariables()
}
</script>

<style scoped>
.el-menu-item {
  margin: 4px 0;
}

.el-menu-item:hover {
  background-color: #e6f3ff !important;
}

.el-menu-item.is-active {
  background-color: #e6f3ff !important;
  color: #409EFF !important;
}
</style>