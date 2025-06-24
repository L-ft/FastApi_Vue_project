::D:\FastApi_project\FastAPIProject\fastapi-login-vue\src\components\Login.vue
<template>
  <div class="auth-bg">
    <div class="auth-left">
      <div class="logo-circle"></div>
      <div class="platform-title">接口自动化平台</div>
      <div class="platform-desc">高效、智能的API测试解决方案</div>
      <ul class="feature-list">
        <li>高效的接口管理</li>
        <li>自动化测试能力</li>
        <li>直观的数据展示</li>
      </ul>
    </div>
    <div class="auth-right">
      <div class="auth-card">
        <div class="auth-title">欢迎登录</div>
        <div class="auth-subtitle">请输入您的账号信息</div>
        <form @submit.prevent="submitLogin">
          <input v-model="loginData.username" class="auth-input" placeholder="账号" autocomplete="username" />
          <input type="password" v-model="loginData.password" class="auth-input" placeholder="密码" autocomplete="current-password" />
          <div class="auth-row">
            <label class="remember-me"><input type="checkbox" v-model="rememberMe" /> 记住我</label>
            <a class="forgot-link" href="#">忘记密码？</a>
            <button type="submit" class="register-link">注册</button>
          </div>
          <button type="submit" class="auth-btn">登录系统</button>
        </form>
        <div class="test-account">测试账号：admin / admin</div>
      </div>
      <div class="copyright">© 2025 接口自动化平台 - 版权所有</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const loginData = ref({
  username: '',
  password: ''
});
const rememberMe = ref(true);

const submitLogin = async () => {
  try {
    const response = await axios.post('http://localhost:8000/token', new URLSearchParams({
      username: loginData.value.username,
      password: loginData.value.password
    }));
    localStorage.setItem('token', response.data.access_token);
    alert('登录成功');
    window.location.href = '/home';
  } catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      alert('登录失败: ' + error.response.data.detail);
    } else {
      alert('登录失败，请检查用户名和密码');
    }
  }
};
</script>

<style scoped>
.auth-bg {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(120deg, #4f8cff 0%, #3bb2f9 100%);
  align-items: stretch;
}
.auth-left {
  flex: 1.2;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-left: 8vw;
}
.logo-circle {
  width: 80px;
  height: 80px;
  background: #fff;
  border-radius: 50%;
  margin-bottom: 2.5em;
}
.platform-title {
  font-size: 2.5em;
  font-weight: bold;
  margin-bottom: 0.7em;
  letter-spacing: 2px;
}
.platform-desc {
  font-size: 1.2em;
  margin-bottom: 2em;
  opacity: 0.95;
}
.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.feature-list li {
  font-size: 1.1em;
  margin-bottom: 1em;
  padding-left: 1.5em;
  position: relative;
}
.feature-list li::before {
  content: '';
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #fff;
  opacity: 0.3;
  position: absolute;
  left: 0;
  top: 0.3em;
}
.auth-right {
  flex: 1;
  background: #f7f8fa;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 420px;
  height: 100vh;
}
.auth-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 32px 0 rgba(31, 38, 135, 0.10);
  padding: 2.5em 2.5em 1.5em 2.5em;
  min-width: 350px;
  max-width: 380px;
  margin-bottom: 1.5em;
}
.auth-title {
  font-size: 1.6em;
  font-weight: bold;
  color: #222;
  text-align: center;
  margin-bottom: 0.5em;
}
.auth-subtitle {
  color: #888;
  text-align: center;
  margin-bottom: 1.5em;
  font-size: 1em;
}
.auth-input {
  width: 100%;
  padding: 0.9em 1em;
  border-radius: 8px;
  border: 1px solid #e0e6ed;
  background: #f7f8fa;
  margin-bottom: 1.2em;
  font-size: 1em;
  outline: none;
  transition: border 0.2s;
}
.auth-input:focus {
  border: 1.5px solid #4f8cff;
}
.auth-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.2em;
}
.remember-me {
  font-size: 0.98em;
  color: #666;
}
.forgot-link {
  color: #4f8cff;
  font-size: 0.98em;
  text-decoration: none;
}
.register-link {
  color: #4f8cff;
  font-size: 0.98em;
  text-decoration: none;
  cursor: pointer;
}
.auth-btn {
  width: 100%;
  padding: 0.9em 0;
  border: none;
  border-radius: 24px;
  background: linear-gradient(90deg, #4f8cff 0%, #3bb2f9 100%);
  color: #fff;
  font-size: 1.1em;
  font-weight: bold;
  box-shadow: 0 2px 8px #4f8cff22;
  cursor: pointer;
  margin-bottom: 1.2em;
  transition: background 0.2s, box-shadow 0.2s;
}
.auth-btn:hover {
  background: linear-gradient(90deg, #3bb2f9 0%, #4f8cff 100%);
  box-shadow: 0 4px 16px #4f8cff44;
}
.test-account {
  color: #888;
  font-size: 0.98em;
  text-align: center;
  margin-bottom: 0.5em;
}
.copyright {
  color: #bbb;
  font-size: 0.95em;
  text-align: center;
}
</style>
