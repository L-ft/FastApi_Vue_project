import request from '@/utils/request'

// 环境管理API
export function getEnvironments() {
  return request({
    url: '/api/environments',
    method: 'get'
  })
}

export function addEnvironment(data) {
  return request({
    url: '/api/environments',
    method: 'post',
    data
  })
}

export function updateEnvironment(env_id, data) {
  return request({
    url: `/api/environments/${env_id}`,
    method: 'put',
    data
  })
}

export function deleteEnvironment(env_id) {
  return request({
    url: `/api/environments/${env_id}`,
    method: 'delete'
  })
}

// 环境变量管理API
export function getEnvironmentVariables(env_id = null) {
  const url = env_id ? `/api/env-variables?env_id=${env_id}` : '/api/env-variables'
  return request({
    url,
    method: 'get'
  })
}

export function addEnvironmentVariable(data) {
  return request({
    url: '/api/env-variables',
    method: 'post',
    data
  })
}

export function updateEnvironmentVariable(var_id, data) {
  return request({
    url: `/api/env-variables/${var_id}`,
    method: 'put',
    data
  })
}

export function deleteEnvironmentVariable(var_id) {
  return request({
    url: `/api/env-variables/${var_id}`,
    method: 'delete'
  })
}

// 批量操作环境变量
export function batchUpdateEnvironmentVariables(data) {
  return request({
    url: '/api/env-variables/batch',
    method: 'put',
    data
  })
}

// 导入环境变量
export function importEnvironmentVariables(data) {
  return request({
    url: '/api/env-variables/import',
    method: 'post',
    data
  })
}

// 导出环境变量
export function exportEnvironmentVariables(env_id) {
  return request({
    url: `/api/env-variables/export?env_id=${env_id}`,
    method: 'get'
  })
}

// 复制环境变量到其他环境
export function copyEnvironmentVariables(from_env_id, to_env_id) {
  return request({
    url: '/api/env-variables/copy',
    method: 'post',
    data: { from_env_id, to_env_id }
  })
}
