<template>
  <el-container style="height: 100vh;">
    <!-- 侧边栏 -->
    <el-aside width="180px" style="background: #fff; border-right: 1px solid #eee;">
      <el-menu :default-active="activeMenu" class="el-menu-vertical-demo" style="border: none;" @select="activeMenu = $event">
        <el-menu-item index="group">
          <span>分组管理</span>
        </el-menu-item>
        <el-menu-item index="api">
          <span>接口管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主体内容：动态组件 -->
    <el-container>
      <el-main>
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

<!-- <script setup>
import { ref, computed } from 'vue'
import { getApiGroups, getApiList, addApiGroup, deleteApi, update_group, delete_group } from '../api/apiManage'

// 页面切换
const activeMenu = ref('group')

// 分组相关
const groups = ref([])
const searchGroup = ref('')
const newGroupName = ref('')

// 接口相关
const pagedApis = ref([])
const selectedGroup = ref(null)
const search = ref('')

// // 获取分组
// const fetchGroups = async () => {
//   const res = await getApiGroups()
//   groups.value = res.data
// }

// // 新增分组
// const openGroupForm = async () => {
//   // 这里用 Element Plus 弹窗更好，简化为 prompt
//   const name = prompt('请输入分组名称')
//   if (name) {
//     await addApiGroup({ name })
//     fetchGroups()
//   }
// }

// // 查询分组
// const filteredGroups = computed(() =>
//   groups.value.filter(g => g.name.includes(searchGroup.value))
// )

// // 编辑分组
// const editGroup = async (row) => {
//   const newName = prompt('请输入新的分组名称', row.name)
//   if (newName && newName !== row.name) {
//     // 假设有 updateApiGroup 方法
//     await update_group(row.id, { name: newName })
//     fetchGroups()
//   }
// }

// // 删除分组
// const handleDeleteGroup = async (row) => {
//   if (confirm(`确定要删除分组 "${row.name}" 吗？`)) {
//     // 假设有 deleteApiGroup 方法
//     await delete_group(row.id)
//     fetchGroups()
//   }
// }
// // 分组分页
// const groupPage = ref(1)
// const groupPageSize = ref(10)

// const pagedGroups = computed(() => {
//   const start = (groupPage.value - 1) * groupPageSize.value
//   return filteredGroups.value.slice(start, start + groupPageSize.value)
// })
// // 接口相关
// const fetchApis = async () => {
//   const res = await getApiList()
//   let data = res.data
//   if (selectedGroup.value) {
//     data = data.filter(api => api.group_id === selectedGroup.value)
//   }
//   if (search.value) {
//     data = data.filter(api => api.name.includes(search.value) || api.url.includes(search.value))
//   }
//   pagedApis.value = data
// }

// const openApiForm = () => {
//   // 打开新增接口弹窗
// }
// const editApi = (row) => {
//   // 打开编辑接口弹窗
// }
// const handleDeleteApi = async (id) => {
//   await deleteApi(id)
//   fetchApis()
// }
// // 接口分页
// const apiPage = ref(1)
// const apiPageSize = ref(10)

// const pagedApiList = computed(() => {
//   const start = (apiPage.value - 1) * apiPageSize.value
//   return pagedApis.value.slice(start, start + apiPageSize.value)
// })
// 初始化
fetchGroups()
fetchApis()
</script> -->