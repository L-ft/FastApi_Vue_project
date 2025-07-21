import axios from 'axios'
import { ElMessage } from 'element-plus'

// API错误处理函数
const handleApiError = (error) => {
  let message = 'An error occurred'
  if (error.response) {
    // 服务器返回错误响应
    message = error.response.data.detail || error.response.data.message || error.response.statusText
  } else if (error.request) {
    // 请求发送但未收到响应
    message = 'No response received from server'
  } else {
    // 请求设置时发生错误
    message = error.message
  }
  ElMessage.error(message)
  return Promise.reject(error)
}

const base = '/api'

// 获取接口分组列表
export function getApiGroups() {
  return axios.get(`${base}/groups`)
}

// 新增接口分组
export function addApiGroup(data) {
  return axios.post(`${base}/groups`, data)
}

// 更新接口分组
export function update_group(group_id, data) {
  return axios.put(`${base}/group/${group_id}`, data)
}
// 删除接口分组
export function delete_group(group_id) {
  return axios.delete(`${base}/group/${group_id}`)
}

// 用例管理相关接口
export async function getCases() {
  try {
    const response = await axios.get('/api/cases')
    return response.data
  } catch (error) {
    return handleApiError(error)
  }
}

export async function addCase(data) {
  try {
    const response = await axios.post('/api/cases', data)
    ElMessage.success('Test case created successfully')
    return response.data
  } catch (error) {
    return handleApiError(error)
  }
}

export async function updateCase(data) {
  try {
    const response = await axios.put(`/api/cases/${data.id}`, data)
    ElMessage.success('Test case updated successfully')
    return response.data
  } catch (error) {
    return handleApiError(error)
  }
}

export async function deleteCaseById(id) {
  try {
    const response = await axios.delete(`/api/cases/${id}`)
    ElMessage.success('Test case deleted successfully')
    return response.data
  } catch (error) {
    return handleApiError(error)
  }
}

// 获取分组列表
export function getGroups() {
  return axios.get('/api/group')
}

// 获取API列表
export function getApis() {
  return axios.get('/api/info')
}

// 获取接口列表
export function getApiList() {
  return axios.get(`${base}/info`)
}

// 新增接口
export function addApi(data) {
  return axios.post(`${base}/info`, data)
}

// 更新接口
export function updateApi(id, data) {
  return axios.put(`${base}/info/${id}`, data)
}

// 删除接口
export function deleteApi(id) {
  return axios.delete(`${base}/info/${id}`)
}