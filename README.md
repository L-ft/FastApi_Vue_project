# FastAPI + Vue3 接口管理系统

一个基于 FastAPI 和 Vue3 的前后端分离接口管理平台，提供用户认证、接口管理、环境管理、用例管理等功能。

## 🚀 项目启动

### 后端启动
```bash
# 进入后端目录
cd backend_fastapi

# 安装依赖
pip install -r requirements.txt

# 启动后端服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动
```bash
# 进入前端目录
cd fastapi-login-vue

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 📁 项目架构### 后端架构 (FastAPI)
```
backend_fastapi/
├── main.py                    # 应用入口，包含CORS配置和路由注册
├── requirements.txt           # Python依赖包列表
├── backup.sql                 # 数据库备份文件
└── app/                       # 核心应用代码
    ├── __init__.py
    ├── auth.py                # JWT认证模块
    ├── db.py                  # 数据库连接和会话管理
    ├── log.py                 # 日志配置模块
    ├── models.py              # SQLAlchemy数据模型
    ├── schemas.py             # Pydantic数据验证模型
    ├── api/                   # API业务逻辑模块
    │   ├── __init__.py
    │   ├── CaseManagement.py          # 用例管理API
    │   ├── EnvironmentalManagement.py # 环境管理API
    │   ├── GroupManagement.py         # 分组管理API
    │   └── InterfaceManagement.py     # 接口管理API
    └── routes/                # 路由配置
        ├── __init__.py
        ├── api.py             # API路由注册
        └── user.py            # 用户路由注册
```

### 前端架构 (Vue3 + Vite)
```
fastapi-login-vue/
├── index.html                 # HTML入口文件
├── package.json               # 项目依赖和脚本配置
├── vite.config.js             # Vite构建配置
└── src/                       # 源代码目录
    ├── App.vue                # 根组件
    ├── main.js                # 应用入口
    ├── Home.vue               # 首页组件
    ├── style.css              # 全局样式
    ├── api/                   # API接口模块
    │   ├── apiEnv.js          # 环境相关API
    │   ├── apiManage.js       # API管理相关接口
    │   ├── caseManage.js      # 用例管理接口
    │   ├── environmentManage.js # 环境管理接口
    │   ├── fetchApis.js       # 通用请求封装
    │   └── groupManage.js     # 分组管理接口
    ├── components/            # Vue组件
    │   ├── ApiGroupForm.vue   # 接口分组表单
    │   ├── ApiInfoForm.vue    # 接口信息表单
    │   ├── ApiManage.vue      # API管理主页面
    │   ├── CaseDetail.vue     # 用例详情
    │   ├── CaseManagement.vue # 用例管理
    │   ├── EnvDetail.vue      # 环境详情
    │   ├── EnvironmentalManagement.vue # 环境管理
    │   ├── EnvTestPage.vue    # 环境测试页面
    │   ├── EnvVarList.vue     # 环境变量列表
    │   ├── HeaderInput.vue    # Header输入组件
    │   ├── Login.vue          # 登录页面
    │   ├── Register.vue       # 注册页面
    │   └── Home.vue           # 主页
    ├── composables/           # 组合式函数
    │   └── useEnvironmentVariables.js # 环境变量逻辑
    ├── utils/                 # 工具类
    │   ├── envUtils.js        # 环境变量工具
    │   └── request.js         # HTTP请求封装
    └── vue-router/            # 路由配置
        └── index.js
```
## 🔧 核心功能

### 1. 用户管理模块
- **用户注册/登录**：基于JWT的安全认证
- **密码加密**：使用Bcrypt进行密码哈希
- **Token管理**：自动刷新和过期管理

### 2. 接口管理模块
- **接口分组管理**：支持多级分组组织
- **接口信息管理**：请求方法、URL、参数等完整配置
- **API调试功能**：内置HTTP客户端，支持实时测试
- **Header管理**：智能Header编辑，支持环境变量占位符

### 3. 环境管理模块 🌟
- **多环境配置**：开发、测试、生产环境隔离
- **环境变量管理**：支持变量的增删改查
- **占位符解析**：`{{变量名}}` 格式自动替换
- **环境切换**：一键切换不同环境配置

### 4. 用例管理模块
- **测试用例创建**：完整的用例信息管理
- **用例执行**：自动化用例执行和结果记录
- **用例分组**：按功能模块组织测试用例

### 5. 系统特性
- **响应式设计**：支持PC和移动端访问
- **实时预览**：环境变量解析实时预览
- **操作日志**：详细的操作和调试日志
- **数据持久化**：MySQL数据库存储

## 🛠️ 技术栈

### 后端技术
- **FastAPI 0.63.0**：现代化的Python Web框架
- **SQLAlchemy 1.3.23**：Python ORM框架
- **PyMySQL**：MySQL数据库连接器
- **Pydantic**：数据验证和序列化
- **Python-Jose**：JWT Token处理
- **Passlib**：密码加密库
- **Uvicorn**：ASGI服务器

### 前端技术
- **Vue 3**：渐进式JavaScript框架
- **Vite**：下一代前端构建工具
- **Element Plus**：Vue3组件库
- **Vue Router 4**：官方路由管理器
- **Axios**：HTTP客户端库
- **Composition API**：Vue3组合式API

### 数据库
- **MySQL**：关系型数据库
- **数据库表结构**：
  - `users`：用户信息表
  - `api_groups`：接口分组表
  - `api_infos`：接口信息表
  - `environments`：环境配置表
  - `environment_variables`：环境变量表
  - `case_infos`：用例信息表
## 🌐 API文档和测试

### Swagger文档
访问地址：http://127.0.0.1:8000/docs

### API接口概览

#### 用户认证接口
- `POST /register`：用户注册
- `POST /token`：用户登录获取Token
- `GET /me`：获取当前用户信息

#### 接口管理接口
- `GET /api/groups`：获取接口分组列表
- `POST /api/groups`：创建新的接口分组
- `PUT /api/group/{group_id}`：更新接口分组
- `DELETE /api/group/{group_id}`：删除接口分组
- `GET /api/apis`：获取接口列表
- `POST /api/apis`：创建新接口
- `PUT /api/apis/{api_id}`：更新接口信息
- `DELETE /api/apis/{api_id}`：删除接口

#### 环境管理接口
- `GET /api/environments`：获取环境列表
- `POST /api/environments`：创建新环境
- `PUT /api/environments/{env_id}`：更新环境信息
- `DELETE /api/environments/{env_id}`：删除环境
- `GET /api/env-variables`：获取环境变量列表
- `POST /api/env-variables`：创建环境变量
- `PUT /api/env-variables/{var_id}`：更新环境变量
- `DELETE /api/env-variables/{var_id}`：删除环境变量

#### 用例管理接口
- `GET /api/cases`：获取用例列表
- `POST /api/cases`：创建新用例
- `PUT /api/cases/{case_id}`：更新用例信息
- `DELETE /api/cases/{case_id}`：删除用例

## 📋 使用指南

### 环境变量配置示例
```json
{
  "key": "Authorization",
  "value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "description": "认证令牌"
}

{
  "key": "base_url",
  "value": "http://localhost:8000",
  "description": "API基础地址"
}
```

### Header占位符使用
在接口调试中，Header值支持环境变量占位符：
```
Authorization: {{Authorization}}
Content-Type: application/json
X-API-Key: {{api_key}}
```

### API调试流程
1. 在环境管理中配置环境变量
2. 在接口管理中创建或编辑接口
3. 点击"运行"进入调试页面
4. 选择环境、配置Header
5. 发送请求查看响应结果## 📦 依赖包列表

### 后端依赖 (requirements.txt)
```
fastapi==0.63.0          # Web框架
uvicorn==0.13.4          # ASGI服务器
sqlalchemy==1.3.23       # ORM框架
pydantic==1.7.3          # 数据验证
python-jose==3.2.0       # JWT处理
passlib==1.7.2           # 密码加密
pytest==6.2.2           # 测试框架
mysql-connector-python   # MySQL驱动
python-dotenv            # 环境变量管理
alembic                  # 数据库迁移
```

### 前端依赖 (package.json)
```json
{
  "dependencies": {
    "vue": "^3.5.13",           // Vue3框架
    "vue-router": "^4.0.13",    // 路由管理
    "axios": "^1.9.0",          // HTTP客户端
    "element-plus": "^2.10.3",  // UI组件库
    "jsonpath": "^1.1.1"        // JSON路径解析
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.2.3",  // Vue插件
    "vite": "^6.3.5"                  // 构建工具
  }
}
```## ⚙️ 项目配置

### 数据库配置
在 `backend_fastapi/app/db.py` 中修改数据库连接：
```python
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost/autotest"
```

### CORS配置
在 `backend_fastapi/main.py` 中配置允许的前端域名：
```python
origins = [
    "http://localhost:5173",    # Vite开发服务器
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### JWT配置
在认证模块中配置JWT密钥和过期时间：
```python
SECRET_KEY = "your-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

## 🚀 部署说明

### 开发环境
1. 确保MySQL服务运行
2. 创建数据库 `autotest`
3. 后端启动：`uvicorn main:app --reload --host 0.0.0.0 --port 8000`
4. 前端启动：`npm run dev`

### 生产环境
- **后端部署**：使用Gunicorn + Nginx
- **前端部署**：`npm run build` 生成静态文件，部署到Web服务器
- **数据库**：配置MySQL主从复制和备份策略
- **反向代理**：使用Nginx进行负载均衡和SSL配置

## 🔍 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查MySQL服务是否启动
   - 验证数据库连接字符串中的用户名、密码、主机地址
   - 确保数据库 `autotest` 已创建

2. **CORS错误**
   - 检查前端请求地址是否在后端CORS配置中
   - 确认前后端端口配置正确

3. **Token验证失败**
   - 检查JWT密钥配置
   - 验证Token是否过期
   - 确认请求头中Authorization格式正确

4. **接口文档访问异常**
   - 访问 http://127.0.0.1:8000/docs
   - 如端口被占用，修改启动端口

5. **环境变量不生效**
   - 检查占位符格式是否为 `{{变量名}}`
   - 确认环境变量已保存
   - 清理浏览器缓存重新加载

## 🔄 版本更新

### 最新优化 (v1.1.0)
- ✅ 新增环境变量占位符支持
- ✅ Header输入组件重构
- ✅ API调试功能增强
- ✅ 性能优化和缓存机制
- ✅ 用户体验改进

### 后续规划
- [ ] 添加接口文档导入/导出功能
- [ ] 支持接口Mock数据生成
- [ ] 增加API测试报告生成
- [ ] 集成CI/CD自动化测试
- [ ] 支持GraphQL接口测试

## 📞 技术支持

如有问题或建议，请通过以下方式联系：
- 📧 邮箱：tech-support@example.com
- 🐛 问题反馈：项目Issues
- 📖 文档：项目Wiki

---

⭐ 如果这个项目对您有帮助，请给个Star支持一下！
