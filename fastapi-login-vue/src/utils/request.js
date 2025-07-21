import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例

// 设置默认的baseURL为8001端口（FastAPI新端口）
const defaultBase = 'http://127.0.0.1:8001';
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || defaultBase, // api的base_url
  timeout: 15000, // 请求超时时间
  withCredentials: true // 允许携带cookie
})

// request拦截器
service.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    // 对请求错误做些什么
    console.log(error)
    return Promise.reject(error)
  }
)

// response拦截器
service.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    console.error('Request error:', error);
    const message = error.response?.data?.detail || error.message || '请求失败';
    ElMessage({
      message: message,
      type: 'error',
      duration: 5 * 1000
    });
    return Promise.reject(error);
  }
)

export default service
