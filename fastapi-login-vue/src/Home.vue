<template>
  <div class="home-container">
    <div class="navbar">
      <span class="title">🤖 AI 平台首页</span>
      <button @click="logout">退出登录</button>
    </div>
    <ApiManage />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import ApiManage from './components/ApiManage.vue'

const API = 'http://127.0.0.1:8000'
const router = useRouter()
const username = ref('')

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) return router.push('/')

  try {
    const res = await axios.get(`${API}/me`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    username.value = res.data.username
  } catch (e) {
    alert('登录信息失效，请重新登录')
    localStorage.removeItem('token')
    router.push('/')
  }
})

const logout = () => {
  localStorage.removeItem('token')
  router.push('/')
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5faff, #f0f9ff);
  font-family: "Segoe UI", sans-serif;
  color: #333;
  display: flex;
  flex-direction: column;
}

.navbar {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  background: #ffffffcc;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.title {
  font-size: 20px;
  font-weight: bold;
  color: #007bff;
}

button {
  background-color: #007bff;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
