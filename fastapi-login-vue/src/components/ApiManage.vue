<template>
  <el-card>
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <div>
        <el-select v-model="selectedGroup" placeholder="选择分组" style="width: 180px" @change="fetchApis">
          <el-option label="全部分组" :value="null" />
          <el-option v-for="g in groups" :key="g.id" :label="g.name" :value="g.id" />
        </el-select>
        <el-input
          v-model="search"
          placeholder="搜索接口名称/URL"
          style="width: 220px; margin-left: 10px"
          clearable
          @input="fetchApis"
        />
      </div>
      <div>
        <el-button type="primary" @click="openApiForm()">新增接口</el-button>
        <el-button @click="openGroupForm()">新增分组</el-button>
      </div>
    </div>

    <el-table :data="pagedApis" style="width: 100%; margin-top: 20px">
      <el-table-column prop="name" label="名称" width="150" />
      <el-table-column prop="url" label="URL" width="220" />
      <el-table-column prop="method" label="方法" width="80" />
      <el-table-column prop="group_id" label="分组" width="120">
        <template #default="scope">
          {{ groupName(scope.row.group_id) }}
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" />
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" @click="openApiForm(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="confirmDelete(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div style="margin-top: 16px; text-align: right;">
      <el-pagination
        background
        layout="prev, pager, next, jumper"
        :total="filteredApis.length"
        :page-size="pageSize"
        v-model:current-page="currentPage"
      />
    </div>

    <!-- 新增/编辑接口弹窗 -->
    <el-dialog v-model="showApiDialog" :title="apiForm.id ? '编辑接口' : '新增接口'" width="500px">
      <el-form :model="apiForm" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="apiForm.name" />
        </el-form-item>
        <el-form-item label="URL">
          <el-input v-model="apiForm.url" />
        </el-form-item>
        <el-form-item label="方法">
          <el-select v-model="apiForm.method" placeholder="请选择">
            <el-option label="GET" value="GET" />
            <el-option label="POST" value="POST" />
            <el-option label="PUT" value="PUT" />
            <el-option label="DELETE" value="DELETE" />
          </el-select>
        </el-form-item>
        <el-form-item label="分组">
          <el-select v-model="apiForm.group_id" placeholder="请选择">
            <el-option v-for="g in groups" :key="g.id" :label="g.name" :value="g.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="apiForm.description" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showApiDialog = false">取消</el-button>
        <el-button type="primary" @click="submitApiForm">保存</el-button>
      </template>
    </el-dialog>

    <!-- 新增分组弹窗 -->
    <el-dialog v-model="showGroupDialog" title="新增分组" width="400px">
      <el-form :model="groupForm" label-width="80px">
        <el-form-item label="分组名称">
          <el-input v-model="groupForm.name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showGroupDialog = false">取消</el-button>
        <el-button type="primary" @click="submitGroupForm">保存</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import {
  getApiGroups, addApiGroup,
  getApiList, addApi, updateApi, deleteApi
} from '../api/apiManage'
import { ElMessage, ElMessageBox } from 'element-plus'

const groups = ref([])
const apis = ref([])
const selectedGroup = ref(null)
const search = ref('')
const currentPage = ref(1)
const pageSize = 8

const showApiDialog = ref(false)
const apiForm = ref({
  id: null, name: '', url: '', method: '', group_id: null, description: ''
})

const showGroupDialog = ref(false)
const groupForm = ref({ name: '' })

function fetchGroups() {
  getApiGroups().then(res => { groups.value = res.data })
}
function fetchApis() {
  getApiList().then(res => { apis.value = res.data })
}
function groupName(id) {
  const g = groups.value.find(x => x.id === id)
  return g ? g.name : ''
}
function openApiForm(api = null) {
  if (api) {
    apiForm.value = { ...api }
  } else {
    apiForm.value = { id: null, name: '', url: '', method: '', group_id: null, description: '' }
  }
  showApiDialog.value = true
}
function submitApiForm() {
  const data = { ...apiForm.value }
  if (!data.name || !data.url || !data.method) {
    ElMessage.warning('请填写完整信息')
    return
  }
  if (data.id) {
    updateApi(data.id, data).then(() => {
      ElMessage.success('更新成功')
      showApiDialog.value = false
      fetchApis()
    })
  } else {
    addApi(data).then(() => {
      ElMessage.success('新增成功')
      showApiDialog.value = false
      fetchApis()
    })
  }
}
function confirmDelete(id) {
  ElMessageBox.confirm('确定要删除该接口吗？', '提示', {
    type: 'warning'
  }).then(() => {
    deleteApi(id).then(() => {
      ElMessage.success('删除成功')
      fetchApis()
    })
  }).catch(() => {})
}
function openGroupForm() {
  groupForm.value = { name: '' }
  showGroupDialog.value = true
}
function submitGroupForm() {
  if (!groupForm.value.name) {
    ElMessage.warning('请输入分组名称')
    return
  }
  addApiGroup({ name: groupForm.value.name }).then(() => {
    ElMessage.success('新增分组成功')
    showGroupDialog.value = false
    fetchGroups()
  })
}

// 搜索和分组过滤
const filteredApis = computed(() => {
  let list = apis.value
  if (selectedGroup.value) {
    list = list.filter(api => api.group_id === selectedGroup.value)
  }
  if (search.value) {
    const s = search.value.toLowerCase()
    list = list.filter(api =>
      api.name.toLowerCase().includes(s) ||
      api.url.toLowerCase().includes(s)
    )
  }
  return list
})
const pagedApis = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredApis.value.slice(start, start + pageSize)
})

watch([selectedGroup, search], () => {
  currentPage.value = 1
})

onMounted(() => {
  fetchGroups()
  fetchApis()
})
</script>

<style scoped>
.el-card {
  max-width: 1100px;
  margin: 30px auto;
}
</style>