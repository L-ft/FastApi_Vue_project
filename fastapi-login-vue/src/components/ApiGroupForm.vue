<template>
  <el-container class="app-container">
    <el-main class="main-content">
      <div class="content-wrapper">
        <div class="header-section">
          <div>
            <el-button type="primary" @click="showAddDialog = true" style="margin-right: 10px;">新增分组</el-button>
            <el-input
              v-model="searchGroup"
              placeholder="查询分组"
              style="width: 200px;"
              clearable
            />
          </div>
        </div>
        <div class="table-section" style="overflow-x:auto;">
          <el-table :data="pagedGroups" :border="false" style="min-width: 400px; width: auto; table-layout: auto;">
            <el-table-column prop="name" label="分组名称" min-width="180" />
            <el-table-column label="操作" min-width="120" fixed="right">
              <template #default="scope">
                <el-button size="mini" @click="openEditDialog(scope.row)">编辑</el-button>
                <el-button size="mini" type="danger" @click="openDeleteDialog(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="groupPage"
              :page-size="groupPageSize"
              :total="filteredGroups.length"
              layout="prev, pager, next"
              :small="false"
            />
          </div>
        </div>
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
import { getApiGroups, addApiGroup, update_group, delete_group } from '../api/apiManage'

const groups = ref([])
const searchGroup = ref('')
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const showDeleteDialog = ref(false)
const addGroupName = ref('')
const editGroupName = ref('')
const editGroupRow = ref(null)
const deleteGroupRow = ref(null)

const fetchGroups = async () => {
  const res = await getApiGroups()
  groups.value = res.data
}

const handleAddGroup = async () => {
  if (!addGroupName.value.trim()) return
  await addApiGroup({ name: addGroupName.value.trim() })
  showAddDialog.value = false
  addGroupName.value = ''
  fetchGroups()
}

const openEditDialog = (row) => {
  editGroupRow.value = row
  editGroupName.value = row.name
  showEditDialog.value = true
}
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

const openDeleteDialog = (row) => {
  deleteGroupRow.value = row
  showDeleteDialog.value = true
}
const handleDeleteGroupConfirm = async () => {
  if (deleteGroupRow.value) {
    await delete_group(deleteGroupRow.value.id)
    fetchGroups()
  }
  showDeleteDialog.value = false
  deleteGroupRow.value = null
}

const filteredGroups = computed(() =>
  groups.value.filter(g => g.name.includes(searchGroup.value))
)

const groupPage = ref(1)
const groupPageSize = ref(10)
const pagedGroups = computed(() => {
  const start = (groupPage.value - 1) * groupPageSize.value
  return filteredGroups.value.slice(start, start + groupPageSize.value)
})
fetchGroups()
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
  justify-content: flex-start;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  margin: 0 0 24px 0;
  position: relative;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05),
              0 4px 6px -1px rgba(0, 0, 0, 0.03);
  background: linear-gradient(to bottom, #ffffff, #fafafa);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.table-section {
  background: #ffffff;
  margin: 0;
  padding: 20px;
  overflow-x: auto;
  position: relative;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.pagination-container {
  margin-top: 16px;
  padding: 16px 0;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid #e4e7ed;
}
  
</style>