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
      </el-menu>
    </el-aside>

    <!-- 主体内容：动态组件 -->
    <el-container style="height: 100vh; min-height: 100vh;">
      <el-main style="height: 100vh; min-height: 100vh; overflow: hidden;">
        <component :is="activeMenu === 'group' ? ApiGroupForm : ApiInfoForm" />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import ApiGroupForm from './ApiGroupForm.vue'
import ApiInfoForm from './ApiInfoForm.vue'

const activeMenu = ref('group')
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