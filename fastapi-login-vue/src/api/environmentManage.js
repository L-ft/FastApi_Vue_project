import axios from 'axios'

const base = '/api'

// 环境管理API
export function getEnvironments() {
  return axios.get(`${base}/environments`)
}

export function addEnvironment(data) {
  return axios.post(`${base}/environments`, data)
}

export function updateEnvironment(env_id, data) {
  return axios.put(`${base}/environments/${env_id}`, data)
}

export function deleteEnvironment(env_id) {
  return axios.delete(`${base}/environments/${env_id}`)
}

// 环境变量管理API
export function getEnvironmentVariables() {
  return axios.get(`${base}/env-variables`)
}

export function addEnvironmentVariable(data) {
  return axios.post(`${base}/env-variables`, data)
}

export function updateEnvironmentVariable(var_id, data) {
  return axios.put(`${base}/env-variables/${var_id}`, data)
}

export function deleteEnvironmentVariable(var_id) {
  return axios.delete(`${base}/env-variables/${var_id}`)
}
