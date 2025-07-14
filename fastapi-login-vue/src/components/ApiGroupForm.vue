<template>
    <!-- 主体内容 -->
    <el-container style="height: 100vh;">
      <el-main>
        <!-- 分组管理页面 -->
          <div v-if="activeMenu === 'group'">
            <div style="margin-bottom: 20px; display: flex; align-items: center;">
              <el-button type="primary" @click="showAddDialog = true" style="margin-right: 10px;">新增分组</el-button>
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
                  <el-button size="mini" @click="openEditDialog(scope.row)">编辑</el-button>
                  <el-button size="mini" type="danger" @click="openDeleteDialog(scope.row)">删除</el-button>
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

          <!-- 新增分组弹窗 -->
          <el-dialog v-model="showAddDialog" title="新增分组" width="350px" :close-on-click-modal="false">
            <el-input v-model="addGroupName" placeholder="请输入分组名称" />
            <template #footer>
              <el-button @click="showAddDialog = false">取消</el-button>
              <el-button type="primary" @click="handleAddGroup">确定</el-button>
            </template>
          </el-dialog>

          <!-- 编辑分组弹窗 -->
          <el-dialog v-model="showEditDialog" title="编辑分组" width="350px" :close-on-click-modal="false">
            <el-input v-model="editGroupName" placeholder="请输入新的分组名称" />
            <template #footer>
              <el-button @click="showEditDialog = false">取消</el-button>
              <el-button type="primary" @click="handleEditGroup">确定</el-button>
            </template>
          </el-dialog>

          <!-- 删除分组弹窗 -->
          <el-dialog v-model="showDeleteDialog" title="删除分组" width="350px" :close-on-click-modal="false">
            <div>确定要删除分组 "{{ deleteGroupRow?.name }}" 吗？</div>
            <template #footer>
              <el-button @click="showDeleteDialog = false">取消</el-button>
              <el-button type="danger" @click="handleDeleteGroupConfirm">确定</el-button>
            </template>
          </el-dialog>
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

// 弹窗相关
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const showDeleteDialog = ref(false)
const addGroupName = ref('')
const editGroupName = ref('')
const editGroupRow = ref(null)
const deleteGroupRow = ref(null)

// 获取分组
const fetchGroups = async () => {
  const res = await getApiGroups()
  groups.value = res.data
}

// 新增分组
const handleAddGroup = async () => {
  if (!addGroupName.value.trim()) return
  await addApiGroup({ name: addGroupName.value.trim() })
  showAddDialog.value = false
  addGroupName.value = ''
  fetchGroups()
}

// 打开编辑弹窗
const openEditDialog = (row) => {
  editGroupRow.value = row
  editGroupName.value = row.name
  showEditDialog.value = true
}
// 编辑分组
const handleEditGroup = async () => {
  if (!editGroupName.value.trim() || !editGroupRow.value) return
  if (editGroupName.value.trim() !== editGroupRow.value.name) {
    await update_group(editGroupRow.value.id, { name: editGroupName.value.trim() })
    fetchGroups()
  }
  showEditDialog.value = false
  editGroupName.value = ''
  editGroupRow.value = null
}

// 打开删除弹窗
const openDeleteDialog = (row) => {
  deleteGroupRow.value = row
  showDeleteDialog.value = true
}
// 删除分组
const handleDeleteGroupConfirm = async () => {
  if (deleteGroupRow.value) {
    await delete_group(deleteGroupRow.value.id)
    fetchGroups()
  }
  showDeleteDialog.value = false
  deleteGroupRow.value = null
}

// 查询分组
const filteredGroups = computed(() =>
  groups.value.filter(g => g.name.includes(searchGroup.value))
)

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