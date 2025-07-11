const fetchApis = async () => {
  const res = await getApiList()
  let data = res.data
  if (selectedGroup.value) {
    data = data.filter(api => api.group_id === selectedGroup.value)
  }
  if (search.value) {
    data = data.filter(api => api.name.includes(search.value) || api.url.includes(search.value))
  }
  // 关键：为每条数据加上 group_name
  data = data.map(api => ({
    ...api,
    group_name: groups.value.find(g => g.id === api.group_id)?.name || ''
  }))
  pagedApis.value = data
}