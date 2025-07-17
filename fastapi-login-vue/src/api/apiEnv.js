import axios from 'axios'

const base = '/api'

// 获取接口分组列表
export function getApiGroups() {
  return axios.get(`${base}/group`)
}

// 获取环境列表
export function getEnvironments() {
  return axios.get(`${base}/env-vars`)
}

// ...existing code...
