/**
 * 环境变量工具类
 * 提供环境变量的解析、替换、验证等功能
 */

class EnvVariableUtils {
  constructor() {
    this.envVariables = new Map()
    this.placeholderRegex = /\{\{(\w+)\}\}/g
  }

  /**
   * 设置环境变量
   * @param {Array} variables - 环境变量数组
   */
  setVariables(variables) {
    this.envVariables.clear()
    if (Array.isArray(variables)) {
      variables.forEach(variable => {
        if (variable.key) {
          this.envVariables.set(variable.key, variable)
        }
      })
    }
  }

  /**
   * 获取环境变量值
   * @param {string} key - 变量名
   * @returns {string} 变量值
   */
  getValue(key) {
    const variable = this.envVariables.get(key)
    return variable ? variable.value : ''
  }

  /**
   * 获取环境变量描述
   * @param {string} key - 变量名
   * @returns {string} 变量描述
   */
  getDescription(key) {
    const variable = this.envVariables.get(key)
    return variable ? variable.description : ''
  }

  /**
   * 替换字符串中的环境变量占位符
   * @param {string} text - 待替换的文本
   * @param {boolean} keepUnmatched - 是否保留未匹配的占位符
   * @returns {string} 替换后的文本
   */
  replaceVariables(text, keepUnmatched = true) {
    if (!text || typeof text !== 'string') {
      return text
    }

    return text.replace(this.placeholderRegex, (match, varName) => {
      const value = this.getValue(varName)
      if (value !== '') {
        return value
      }
      return keepUnmatched ? match : ''
    })
  }

  /**
   * 检查文本中是否包含环境变量占位符
   * @param {string} text - 待检查的文本
   * @returns {boolean} 是否包含占位符
   */
  hasPlaceholders(text) {
    if (!text || typeof text !== 'string') {
      return false
    }
    return this.placeholderRegex.test(text)
  }

  /**
   * 提取文本中的所有环境变量占位符
   * @param {string} text - 待提取的文本
   * @returns {Array} 占位符数组
   */
  extractPlaceholders(text) {
    if (!text || typeof text !== 'string') {
      return []
    }

    const matches = []
    let match
    const regex = new RegExp(this.placeholderRegex)
    
    while ((match = regex.exec(text)) !== null) {
      matches.push({
        full: match[0],
        varName: match[1],
        index: match.index
      })
    }
    
    return matches
  }

  /**
   * 验证环境变量占位符是否有效
   * @param {string} text - 待验证的文本
   * @returns {Object} 验证结果
   */
  validatePlaceholders(text) {
    const placeholders = this.extractPlaceholders(text)
    const result = {
      isValid: true,
      invalidPlaceholders: [],
      validPlaceholders: []
    }

    placeholders.forEach(placeholder => {
      const hasValue = this.envVariables.has(placeholder.varName)
      if (hasValue) {
        result.validPlaceholders.push(placeholder)
      } else {
        result.invalidPlaceholders.push(placeholder)
        result.isValid = false
      }
    })

    return result
  }

  /**
   * 获取所有环境变量列表
   * @returns {Array} 环境变量数组
   */
  getAllVariables() {
    return Array.from(this.envVariables.values())
  }

  /**
   * 获取变量名列表
   * @returns {Array} 变量名数组
   */
  getVariableNames() {
    return Array.from(this.envVariables.keys())
  }

  /**
   * 搜索环境变量
   * @param {string} keyword - 搜索关键词
   * @returns {Array} 匹配的环境变量
   */
  searchVariables(keyword) {
    if (!keyword) {
      return this.getAllVariables()
    }

    const lowerKeyword = keyword.toLowerCase()
    return this.getAllVariables().filter(variable => {
      return variable.key.toLowerCase().includes(lowerKeyword) ||
             (variable.description && variable.description.toLowerCase().includes(lowerKeyword)) ||
             (variable.value && variable.value.toLowerCase().includes(lowerKeyword))
    })
  }

  /**
   * 生成占位符格式的变量名
   * @param {string} varName - 变量名
   * @returns {string} 占位符格式
   */
  generatePlaceholder(varName) {
    return `{{${varName}}}`
  }

  /**
   * 批量替换对象中的环境变量
   * @param {Object} obj - 待替换的对象
   * @returns {Object} 替换后的对象
   */
  replaceObjectVariables(obj) {
    if (!obj || typeof obj !== 'object') {
      return obj
    }

    const result = Array.isArray(obj) ? [] : {}

    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        const value = obj[key]
        if (typeof value === 'string') {
          result[key] = this.replaceVariables(value)
        } else if (typeof value === 'object' && value !== null) {
          result[key] = this.replaceObjectVariables(value)
        } else {
          result[key] = value
        }
      }
    }

    return result
  }

  /**
   * 转换Headers数组为对象格式，并替换环境变量
   * @param {Array} headersArray - Headers数组
   * @returns {Object} Headers对象
   */
  convertHeadersArrayToObject(headersArray) {
    const headers = {}
    
    if (Array.isArray(headersArray)) {
      headersArray.forEach(header => {
        if (header.key && header.value) {
          const resolvedKey = this.replaceVariables(header.key)
          const resolvedValue = this.replaceVariables(header.value)
          headers[resolvedKey] = resolvedValue
        }
      })
    }
    
    return headers
  }

  /**
   * 预览替换结果
   * @param {string} text - 原始文本
   * @returns {Object} 预览结果
   */
  previewReplacement(text) {
    if (!text || typeof text !== 'string') {
      return {
        original: text,
        resolved: text,
        hasChanges: false,
        placeholders: []
      }
    }

    const placeholders = this.extractPlaceholders(text)
    const resolved = this.replaceVariables(text)
    
    return {
      original: text,
      resolved: resolved,
      hasChanges: text !== resolved,
      placeholders: placeholders.map(placeholder => ({
        ...placeholder,
        resolvedValue: this.getValue(placeholder.varName),
        hasValue: this.envVariables.has(placeholder.varName)
      }))
    }
  }
}

// 创建全局实例
export const envUtils = new EnvVariableUtils()

// 导出类以便创建新实例
export default EnvVariableUtils
