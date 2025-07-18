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
        <component :is="getActiveComponent" @add-env-var="handleAddEnvVar" />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import ApiGroupForm from './ApiGroupForm.vue'
import ApiInfoForm from './ApiInfoForm.vue'
import EnvironmentalManagement from './EnvironmentalManagement.vue'
import CaseManagement from './CaseManagement.vue'

const activeMenu = ref('group')

const getActiveComponent = computed(() => {
  if (activeMenu.value === 'group') return ApiGroupForm
  if (activeMenu.value === 'api') return ApiInfoForm
  if (activeMenu.value === 'env') return EnvironmentalManagement
  if (activeMenu.value === 'case') return CaseManagement
  return ApiGroupForm
})

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