<template>
  <el-container style="height: 100vh;">
    <el-main>
      <!-- 接口管理页面 -->
      <div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
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
          </div>
        </div>
        <el-table :data="pagedApis" style="width: 100%;">
          <el-table-column prop="name" label="名称" width="150" />
          <el-table-column prop="url" label="URL" width="200" />
          <el-table-column prop="method" label="方法" width="100" />
          <el-table-column prop="group_name" label="分组" width="100" />
          <el-table-column prop="desc" label="描述" />
          <el-table-column label="操作" width="160">
            <template #default="scope">
              <el-button size="mini" @click="editApi(scope.row)">编辑</el-button>
              <el-button size="mini" type="danger" @click="handleDeleteApi(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          v-model:current-page="apiPage"
          :page-size="apiPageSize"
          :total="pagedApis.length"
          layout="prev, pager, next"
          style="margin-top: 16px; text-align: right;"
        />
      </div>
      <el-dialog v-model="apiDialogVisible" title="新增接口" width="500px">
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
          <el-input v-model="apiForm.desc" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="apiDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitApiForm">提交</el-button>
      </template>
</el-dialog>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { getApiList, deleteApi, addApi, updateApi } from '../api/apiManage'
import { getApiGroups } from '../api/apiManage'
// import { fetchApis} from '../api/fetchApis'


// 接口相关
const pagedApis = ref([])
const selectedGroup = ref(null)
const search = ref('')

// 新增接口弹窗相关
const apiDialogVisible = ref(false)
const apiForm = ref({
  name: '',
  url: '',
  method: '',
  group_id: null,
  desc: ''
})

const groups = ref([]) // 确保 groups 有定义
// 更新接口
const isEdit = ref(false) // 标记是否为编辑状态

const openApiForm = (row = null) => {
  if (row) {
    apiForm.value = { ...row }
    isEdit.value = true
  } else {
    apiForm.value = { name: '', url: '', method: '', group_id: null, desc: '' }
    isEdit.value = false
  }
  apiDialogVisible.value = true
}

const submitApiForm = async () => {
  if (isEdit.value) {
    await updateApi(apiForm.value.id, apiForm.value)
  } else {
    await addApi(apiForm.value)
  }
  apiDialogVisible.value = false
  fetchApis()
}

const editApi = (row) => {
  openApiForm(row)
}

// 删除接口
const handleDeleteApi = async (id) => {
  await deleteApi(id)
  fetchApis()
}
// 接口分页
const apiPage = ref(1)
const apiPageSize = ref(10)

const pagedApiList = computed(() => {
  const start = (apiPage.value - 1) * apiPageSize.value
  return pagedApis.value.slice(start, start + apiPageSize.value)
})


const fetchApis = async () => {
  const res = await getApiList()
  let data = res.data
  if (selectedGroup.value) {
    data = data.filter(api => api.group_id === selectedGroup.value)
  }
  if (search.value) {
    data = data.filter(api => api.name.includes(search.value) || api.url.includes(search.value))
  }
  data = data.map(api => ({
    ...api,
    group_name: groups.value.find(g => g.id === api.group_id)?.name || ''
  }))
  pagedApis.value = data
}

const fetchGroups = async () => {
  const res = await getApiGroups()
  groups.value = res.data
  await fetchApis()
}

// 页面初始化时只调用 fetchGroups
fetchGroups()
</script>