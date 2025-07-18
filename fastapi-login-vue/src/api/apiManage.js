import axios from 'axios'

const base = '/api'

// 获取接口分组列表
export function getApiGroups() {
  return axios.get(`${base}/group`)
}

// 新增接口分组
export function addApiGroup(data) {
  return axios.post(`${base}/group`, data)
}

// 更新接口分组
export function update_group(group_id, data) {
  return axios.put(`/api/group/${group_id}`, data)
}
// 删除接口分组
export function delete_group(group_id) {
  return axios.delete(`/api/group/${group_id}`)
}

// 用例管理相关接口
export function getCases() {
  return axios.get('/api/case_info')
}

export function addCase(data) {
  return axios.post('/api/case_info', data)
}

export function updateCase(data) {
  return axios.put(`/api/case_info/${data.id}`, data)
}

export function deleteCaseById(id) {
  return axios.delete(`/api/case_info/${id}`)
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