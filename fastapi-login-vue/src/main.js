import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './vue-router/index'

axios.interceptors.request.use(config => {
  if (
    !(config.url.endsWith('/register') || config.url.endsWith('/token'))
  ) {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

createApp(App).use(router).mount('#app')
