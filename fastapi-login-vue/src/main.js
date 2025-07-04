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
// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(ElementPlus)
app.mount('#app')