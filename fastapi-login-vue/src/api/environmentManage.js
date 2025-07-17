import axios from 'axios'

const base = '/api'

// 获取环境列表
export function getEnvironments() {
  return axios.get(`${base}/env-vars`)
}

// 新增环境
export function addEnvironment(data) {
  return axios.post(`${base}/env-vars`, data)
}

// 更新环境
export function updateEnvironment(env_id, data) {
  return axios.put(`${base}/env-vars/${env_id}`, data)
}

// 删除环境
export function deleteEnvironment(env_id) {
  return axios.delete(`${base}/env-vars/${env_id}`)
}
