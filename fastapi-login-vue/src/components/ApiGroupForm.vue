<template>
    <!-- 主体内容 -->
    <el-container style="height: 100vh;">
      <el-main>
        <!-- 分组管理页面 -->
          <div v-if="activeMenu === 'group'">
            <div style="margin-bottom: 20px; display: flex; align-items: center;">
              <el-button type="primary" @click="openGroupForm" style="margin-right: 10px;">新增分组</el-button>
              <el-input
                v-model="searchGroup"
                placeholder="查询分组"
                style="width: 200px;"
                clearable
              />
            </div>
            <el-table :data="filteredGroups" style="width: 100%;">
              <el-table-column prop="name" label="分组名称" />
              <el-table-column label="操作" width="160">
                <template #default="scope">
                  <el-button size="mini" @click="editGroup(scope.row)">编辑</el-button>
                  <el-button size="mini" type="danger" @click="handleDeleteGroup(scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
             <el-pagination
                v-model:current-page="groupPage"
                :page-size="groupPageSize"
                :total="filteredGroups.length"
                layout="prev, pager, next"
                style="margin-top: 16px; text-align: right;"
              />
          </div>
      </el-main>
    </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { getApiGroups, getApiList, addApiGroup, deleteApi, update_group, delete_group } from '../api/apiManage'

// 页面切换
const activeMenu = ref('group')

// 分组相关
const groups = ref([])
const searchGroup = ref('')
const newGroupName = ref('')

// 获取分组
const fetchGroups = async () => {
  const res = await getApiGroups()
  groups.value = res.data
}

// 新增分组
const openGroupForm = async () => {
  // 这里用 Element Plus 弹窗更好，简化为 prompt
  const name = prompt('请输入分组名称')
  if (name) {
    await addApiGroup({ name })
    fetchGroups()
  }
}

// 查询分组
const filteredGroups = computed(() =>
  groups.value.filter(g => g.name.includes(searchGroup.value))
)

// 编辑分组
const editGroup = async (row) => {
  const newName = prompt('请输入新的分组名称', row.name)
  if (newName && newName !== row.name) {
    // 假设有 updateApiGroup 方法
    await update_group(row.id, { name: newName })
    fetchGroups()
  }
}

// 删除分组
const handleDeleteGroup = async (row) => {
  if (confirm(`确定要删除分组 "${row.name}" 吗？`)) {
    // 假设有 deleteApiGroup 方法
    await delete_group(row.id)
    fetchGroups()
  }
}
// 分组分页
const groupPage = ref(1)
const groupPageSize = ref(10)

const pagedGroups = computed(() => {
  const start = (groupPage.value - 1) * groupPageSize.value
  return filteredGroups.value.slice(start, start + groupPageSize.value)
})
// 初始化
fetchGroups()

</script>