<template>
  <div>
    <h3>新增分组</h3>
    <input v-model="name" placeholder="分组名称" />
    <button @click="submit">提交</button>
    <button @click="$emit('close')">取消</button>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { addApiGroup } from '../api/apiManage'
const name = ref('')
function submit() {
  addApiGroup({ name: name.value }).then(() => {
    name.value = ''
    // 通知父组件刷新
    emit('success')
    emit('close')
  })
}
const emit = defineEmits(['success', 'close'])
</script>