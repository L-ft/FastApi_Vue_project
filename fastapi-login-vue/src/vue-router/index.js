// ::D:\FastApi_project\FastAPIProject\fastapi-login-vue\src\vue-router\index.js
import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import Home from '../components/Home.vue';
// import EnvDetail from '../components/EnvDetail.vue';

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  // 环境变量详情页面已移至环境管理-环境变量列表，不再单独路由
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
