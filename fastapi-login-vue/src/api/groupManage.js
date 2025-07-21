import request from '@/utils/request'

// 获取分组列表
export const getGroupList = () => {
  return request({
    url: '/api/groups',
    method: 'get'
  })
}

// 添加分组
export const addGroup = (data) => {
  return request({
    url: '/api/groups',
    method: 'post',
    data
  })
}

// 更新分组
export const updateGroup = (id, data) => {
  return request({
    url: `/api/groups/${id}`,
    method: 'put',
    data
  })
}

// 删除分组
export const deleteGroup = (id) => {
  return request({
    url: `/api/groups/${id}`,
    method: 'delete'
  })
}

// 获取单个分组详情
export const getGroupById = (id) => {
  return request({
    url: `/api/groups/${id}`,
    method: 'get'
  })
}
