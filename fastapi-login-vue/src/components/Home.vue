<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const username = ref('');

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/me');
    username.value = response.data.username;
  } catch (error) {
    username.value = '未登录';
  }
});

function logout() {
  localStorage.removeItem('token');
  window.location.href = '/login';
}
</script>

<template>
  <div class="main-layout sci-bg">
    <header class="sci-header">
      <div class="user-info">
        <span class="user-avatar">{{ username.charAt(0).toUpperCase() }}</span>
        <span class="user-name">{{ username }}</span>
        <button class="logout-btn" @click="logout">退出登录</button>
      </div>
    </header>
    <aside class="sidebar sci-sidebar">
      <div class="sidebar-title">接口自动化平台</div>
      <nav class="menu">
        <div class="menu-section">项目概览</div>
        <div class="menu-section">接口管理</div>
        <div class="menu-group">
          <div class="menu-item active"><span class="icon">📁</span> 接口目录</div>
          <div class="menu-item"><span class="icon">🔍</span> 快速开始</div>
          <div class="menu-item"><span class="icon">🔑</span> 认证 API</div>
          <div class="menu-item"><span class="icon">💳</span> 卡片 API</div>
          <div class="menu-item"><span class="icon">🔧</span> 设备 API</div>
          <div class="menu-item"><span class="icon">🎵</span> 套餐 API</div>
          <div class="menu-item"><span class="icon">🤝</span> 合约机组 API</div>
          <div class="menu-item"><span class="icon">🌐</span> 开放接口</div>
        </div>
        <div class="menu-section">数据模型</div>
        <div class="menu-section">组件库</div>
        <div class="menu-section">快速请求</div>
        <div class="menu-section">请求历史</div>
        <div class="menu-section">项目设置</div>
      </nav>
    </aside>
    <main class="content-area sci-content-area">
      <div class="welcome-card sci-card">
        <h2>欢迎，<span class="sci-username">{{ username }}</span></h2>
        <p class="sci-desc">请选择左侧功能进行接口管理或自动化测试。</p>
        <div class="desc-list">
          <div>· <span class="sci-blue">支持高效的接口目录管理</span></div>
          <div>· <span class="sci-blue">自动化测试用例执行与报告</span></div>
          <div>· <span class="sci-blue">数据模型与组件库复用</span></div>
          <div>· <span class="sci-blue">快速请求与历史追溯</span></div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.sci-bg {
  background: linear-gradient(120deg, #0a1a2f 0%, #1e3c72 100%);
}
.main-layout {
  display: flex;
  min-height: 100vh;
  align-items: stretch;
  padding-top: 64px;
}
.sci-sidebar {
  width: 250px;
  background: linear-gradient(160deg, #232b4d 0%, #1e90ff 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
  padding: 0 0 2em 0;
  box-shadow: 2px 0 18px 0 rgba(31, 38, 135, 0.18);
  border-right: 1.5px solid #1e90ff44;
}
.sidebar-title {
  font-size: 1.5em;
  font-weight: bold;
  letter-spacing: 2px;
  padding: 2.2em 0 1.5em 2em;
  text-shadow: 0 0 12px #1e90ff88;
}
.menu {
  flex: 1;
  padding-left: 2em;
}
.menu-section {
  font-size: 1.08em;
  margin: 1.2em 0 0.5em 0;
  font-weight: 500;
  opacity: 0.92;
  letter-spacing: 1px;
}
.menu-group {
  margin-bottom: 1.5em;
}
.menu-item {
  display: flex;
  align-items: center;
  font-size: 1em;
  padding: 0.45em 0;
  cursor: pointer;
  opacity: 0.92;
  border-radius: 8px 0 0 8px;
  transition: background 0.15s, color 0.15s;
  font-weight: 500;
}
.menu-item.active, .menu-item:hover {
  background: linear-gradient(90deg, #1e90ff44 0%, #1e90ff22 100%);
  opacity: 1;
  color: #00eaff;
}
.icon {
  margin-right: 0.7em;
  font-size: 1.1em;
}
.sci-content-area {
  flex: 1;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
.sci-card {
  background: rgba(20, 28, 48, 0.98);
  border-radius: 18px;
  box-shadow: 0 8px 40px 0 #1e90ff55, 0 1.5px 8px 0 #00eaff33;
  padding: 2.8em 3.5em 2.2em 3.5em;
  min-width: 420px;
  max-width: 520px;
  margin: 0;
  color: #fff;
  border: 1.5px solid #1e90ff33;
  backdrop-filter: blur(2px);
}
.sci-card h2 {
  font-size: 1.6em;
  font-weight: bold;
  color: #00eaff;
  margin-bottom: 0.7em;
  text-align: center;
  text-shadow: 0 0 12px #00eaff55;
}
.sci-username {
  color: #fff;
  font-weight: 600;
  text-shadow: 0 0 8px #1e90ff88;
}
.sci-desc {
  color: #b3c6e0;
  margin-bottom: 1.2em;
  text-align: center;
}
.desc-list {
  color: #00eaff;
  font-size: 1.08em;
  line-height: 2.2;
  margin-top: 1.2em;
}
.sci-blue {
  color: #00eaff;
  font-weight: 500;
  text-shadow: 0 0 8px #00eaff44;
}
.sci-header {
  position: fixed;
  top: 0;
  right: 0;
  left: 250px;
  height: 64px;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  z-index: 10;
  padding: 0 3vw 0 0;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 1em;
  background: rgba(30, 48, 80, 0.85);
  border-radius: 24px;
  padding: 0.4em 1.2em 0.4em 0.7em;
  box-shadow: 0 2px 8px #1e90ff33;
}
.user-avatar {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #1e90ff 0%, #00eaff 100%);
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2em;
  box-shadow: 0 0 8px #00eaff55;
}
.user-name {
  color: #fff;
  font-weight: 500;
  font-size: 1.08em;
  letter-spacing: 1px;
}
.logout-btn {
  background: linear-gradient(90deg, #00eaff 0%, #1e90ff 100%);
  color: #fff;
  border: none;
  border-radius: 16px;
  padding: 0.4em 1.2em;
  font-size: 1em;
  font-weight: 500;
  cursor: pointer;
  margin-left: 0.5em;
  box-shadow: 0 2px 8px #00eaff33;
  transition: background 0.2s, box-shadow 0.2s;
}
.logout-btn:hover {
  background: linear-gradient(90deg, #1e90ff 0%, #00eaff 100%);
  box-shadow: 0 4px 16px #00eaff88;
}
</style> 