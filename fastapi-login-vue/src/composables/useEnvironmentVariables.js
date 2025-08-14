import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { getEnvironmentVariables } from '@/api/environmentManage'
import { envUtils } from '@/utils/envUtils'
import { ElMessage } from 'element-plus'

/**
 * 环境变量管理的组合式函数
 * 提供环境变量的加载、缓存、更新等功能
 */
export function useEnvironmentVariables() {
  // 响应式数据
  const envVariables = ref([])
  const currentEnv = ref('dev')
  const loading = ref(false)
  const error = ref(null)
  const lastUpdated = ref(null)

  // 缓存配置
  const CACHE_KEY = 'env_variables_cache'
  const CACHE_EXPIRY = 5 * 60 * 1000 // 5分钟缓存

  /**11
   * 从本地存储获取缓存的环境变量
   */
  const getCachedVariables = () => {
    try {
      const cached = localStorage.getItem(CACHE_KEY)
      if (cached) {
        const data = JSON.parse(cached)
        const now = Date.now()
        if (data.timestamp && (now - data.timestamp) < CACHE_EXPIRY) {
          return data.variables
        }
      }
    } catch (e) {
      console.warn('读取环境变量缓存失败:', e)
    }
    return null
  }

  /**
   * 缓存环境变量到本地存储
   */
  const setCachedVariables = (variables) => {
    try {
      const data = {
        variables,
        timestamp: Date.now()
      }
      localStorage.setItem(CACHE_KEY, JSON.stringify(data))
    } catch (e) {
      console.warn('缓存环境变量失败:', e)
    }
  }

  /**
   * 加载环境变量
   */
  const loadEnvVariables = async (forceRefresh = false) => {
    // 如果不是强制刷新，先尝试从缓存获取
    if (!forceRefresh) {
      const cached = getCachedVariables()
      if (cached) {
        envVariables.value = cached
        envUtils.setVariables(cached)
        return
      }
    }

    loading.value = true
    error.value = null

    try {
      const response = await getEnvironmentVariables()
      const variables = response.data || []
      
      envVariables.value = variables
      envUtils.setVariables(variables)
      
      // 缓存到本地存储
      setCachedVariables(variables)
      
      lastUpdated.value = new Date()
      
    } catch (err) {
      error.value = err
      console.error('加载环境变量失败:', err)
      
      // 加载失败时使用默认环境变量
      const defaultVariables = [
        { key: 'base_url', value: 'http://localhost:8000', description: '基础URL' },
        { key: 'Authorization', value: 'Bearer token_placeholder', description: '认证令牌' },
        { key: 'Content-Type', value: 'application/json', description: '内容类型' },
        { key: 'X-API-Key', value: 'api-key-placeholder', description: 'API密钥' }
      ]
      
      envVariables.value = defaultVariables
      envUtils.setVariables(defaultVariables)
      
      ElMessage.warning('加载环境变量失败，使用默认配置')
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新环境变量
   */
  const updateEnvVariables = (newVariables) => {
    envVariables.value = newVariables
    envUtils.setVariables(newVariables)
    setCachedVariables(newVariables)
    lastUpdated.value = new Date()
  }

  /**
   * 获取环境变量值
   */
  const getEnvValue = (key) => {
    return envUtils.getValue(key)
  }

  /**
   * 替换字符串中的环境变量
   */
  const replaceEnvVars = (text) => {
    return envUtils.replaceVariables(text)
  }

  /**
   * 验证环境变量占位符
   */
  const validateEnvVars = (text) => {
    return envUtils.validatePlaceholders(text)
  }

  /**
   * 搜索环境变量
   */
  const searchEnvVars = (keyword) => {
    return envUtils.searchVariables(keyword)
  }

  /**
   * 预览替换结果
   */
  const previewReplacement = (text) => {
    return envUtils.previewReplacement(text)
  }

  /**
   * 转换Headers数组为对象
   */
  const convertHeadersToObject = (headersArray) => {
    return envUtils.convertHeadersArrayToObject(headersArray)
  }

  // 计算属性
  const envVariableNames = computed(() => {
    return envVariables.value.map(env => env.key)
  })

  const envVariableCount = computed(() => {
    return envVariables.value.length
  })

  const hasEnvVariables = computed(() => {
    return envVariables.value.length > 0
  })

  // 监听环境变化
  watch(currentEnv, async (newEnv) => {
    await loadEnvVariables(true) // 环境切换时强制刷新
  })

  // 组件挂载时自动加载
  onMounted(() => {
    loadEnvVariables()
  })

  // 定期刷新缓存
  let refreshTimer = null
  onMounted(() => {
    // 每5分钟检查一次是否需要刷新
    refreshTimer = setInterval(() => {
      const cached = getCachedVariables()
      if (!cached) {
        loadEnvVariables()
      }
    }, CACHE_EXPIRY)
  })

  onUnmounted(() => {
    if (refreshTimer) {
      clearInterval(refreshTimer)
    }
  })

  return {
    // 响应式数据
    envVariables,
    currentEnv,
    loading,
    error,
    lastUpdated,
    
    // 计算属性
    envVariableNames,
    envVariableCount,
    hasEnvVariables,
    
    // 方法
    loadEnvVariables,
    updateEnvVariables,
    getEnvValue,
    replaceEnvVars,
    validateEnvVars,
    searchEnvVars,
    previewReplacement,
    convertHeadersToObject,
    
    // 工具类实例
    envUtils
  }
}

/**
 * 用于API调试的组合式函数
 */
export function useApiDebug() {
  const debugDialogVisible = ref(false)
  const debugMethod = ref('GET')
  const debugUrl = ref('')
  const debugEnvironment = ref(null)
  const debugHeaders = ref([])
  const debugParams = ref([])
  const debugBody = ref('')
  const debugResult = ref(null)
  const debugLoading = ref(false)

  /**
   * 重置调试表单
   */
  const resetDebugForm = () => {
    debugMethod.value = 'GET'
    debugUrl.value = ''
    debugHeaders.value = []
    debugParams.value = []
    debugBody.value = ''
    debugResult.value = null
    debugLoading.value = false
  }

  /**
   * 打开调试对话框
   */
  const openDebugDialog = (api = null) => {
    if (api) {
      debugMethod.value = api.method || 'GET'
      debugUrl.value = api.url || ''
      debugEnvironment.value = api.env_id || null
    }
    debugDialogVisible.value = true
  }

  /**
   * 关闭调试对话框
   */
  const closeDebugDialog = () => {
    debugDialogVisible.value = false
    resetDebugForm()
  }

  return {
    // 响应式数据
    debugDialogVisible,
    debugMethod,
    debugUrl,
    debugEnvironment,
    debugHeaders,
    debugParams,
    debugBody,
    debugResult,
    debugLoading,
    
    // 方法
    resetDebugForm,
    openDebugDialog,
    closeDebugDialog
  }
}

/**
 * 用于表单验证的组合式函数
 */
export function useFormValidation() {
  const errors = ref({})
  const isValidating = ref(false)

  /**
   * 设置字段错误
   */
  const setFieldError = (field, message) => {
    errors.value[field] = message
  }

  /**
   * 清除字段错误
   */
  const clearFieldError = (field) => {
    delete errors.value[field]
  }

  /**
   * 清除所有错误
   */
  const clearAllErrors = () => {
    errors.value = {}
  }

  /**
   * 检查是否有错误
   */
  const hasErrors = computed(() => {
    return Object.keys(errors.value).length > 0
  })

  /**
   * 获取字段错误
   */
  const getFieldError = (field) => {
    return errors.value[field]
  }

  /**
   * 验证必填字段
   */
  const validateRequired = (value, fieldName) => {
    if (!value || (typeof value === 'string' && !value.trim())) {
      setFieldError(fieldName, `${fieldName}是必填项`)
      return false
    }
    clearFieldError(fieldName)
    return true
  }

  /**
   * 验证URL格式
   */
  const validateUrl = (url, fieldName = 'URL') => {
    if (!url) {
      setFieldError(fieldName, `${fieldName}不能为空`)
      return false
    }
    
    const urlPattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/
    if (!urlPattern.test(url) && !url.startsWith('/')) {
      setFieldError(fieldName, `${fieldName}格式不正确`)
      return false
    }
    
    clearFieldError(fieldName)
    return true
  }

  /**
   * 验证JSON格式
   */
  const validateJson = (jsonString, fieldName = 'JSON') => {
    if (!jsonString.trim()) {
      clearFieldError(fieldName)
      return true
    }
    
    try {
      JSON.parse(jsonString)
      clearFieldError(fieldName)
      return true
    } catch (e) {
      setFieldError(fieldName, `${fieldName}格式不正确`)
      return false
    }
  }

  return {
    errors,
    isValidating,
    hasErrors,
    setFieldError,
    clearFieldError,
    clearAllErrors,
    getFieldError,
    validateRequired,
    validateUrl,
    validateJson
  }
}
