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
export function getEnvironmentVariables() {
  return request({
    url: '/api/env-variables',
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
