import request from '@/utils/request'

// 获取用例列表
export const getCases = () => {
  return request({
    url: '/api/cases',
    method: 'get'
  })
}

// 添加用例
export const addCase = (data) => {
  return request({
    url: '/api/cases',
    method: 'post',
    data
  })
}

// 更新用例
export const updateCase = (id, data) => {
  return request({
    url: `/api/cases/${id}`,
    method: 'put',
    data
  })
}

// 删除用例
export const deleteCaseById = (id) => {
  return request({
    url: `/api/cases/${id}`,
    method: 'delete'
  })
}

// 获取单个用例详情
export const getCaseById = (id) => {
  return request({
    url: `/api/cases/${id}`,
    method: 'get'
  })
}
