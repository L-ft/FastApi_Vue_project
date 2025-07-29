import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例

// 设置默认的baseURL为8000端口（FastAPI端口）
const defaultBase = 'http://127.0.0.1:8001';
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || defaultBase, // api的base_url
  timeout: 15000, // 请求超时时间
  withCredentials: false // 暂时禁用 credentials 避免 CORS 问题
})

// request拦截器
service.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    console.log('Request拦截器 - 检查Authorization头:', config.headers);
    
    // 检查是否已经手动设置了Authorization头
    const hasManualAuth = config.headers && 
      (config.headers['Authorization'] || config.headers['authorization']);
    
    if (!hasManualAuth) {
      // 只有在没有手动设置Authorization头时，才从localStorage获取token
      const token = localStorage.getItem('token');
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
        console.log('Request拦截器 - 自动添加Authorization头:', `Bearer ${token.substring(0, 20)}...`);
      }
    } else {
      console.log('Request拦截器 - 检测到手动设置的Authorization头，跳过自动添加');
    }
    
    console.log('Request拦截器 - 最终请求头:', config.headers);
    return config;
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
