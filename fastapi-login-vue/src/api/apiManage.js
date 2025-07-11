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