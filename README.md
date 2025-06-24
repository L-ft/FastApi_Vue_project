# FastApi_projext

一：项目启动
1、后端项目
    cd backend
2、启动项目
    uvicorn main:app --reload --port 8000 --host 0.0.0.0
3、前端项目·
    cd frontend
    npm run dev  # 启动前端项目        
二：项目结构
backend/
    main.py  # 项目入口
    app/  # 项目核心代码
        __init__.py
        api/  # 接口模块
            __init__.py
            v1/  # 版本模块
                __init__.py
                user.py  # 用户接口模块
                ...
        core/  # 核心模块
            __init__.py
            config.py  # 项目配置模块
            db.py  # 数据库模块
            ...
        models/  # 数据模型模块
            __init__.py
            user.py  # 用户模型模块
            ...
        utils/  # 工具模块
            __init__.py
            jwt.py  # JWT模块
            ...
        ...
    tests/  # 测试模块
        __init__.py
        test_api.py  # 接口测试模块
        ...
    ...
frontend/
    public/  # 静态资源文件
    src/  # 前端代码
        assets/  # 静态资源文件
        components/  # 公共组件模块
        pages/  # 页面模块
            index.vue  # 首页模块
            ...
        router/  # 路由模块
            index.js  # 路由配置模块
            ...
        store/  # vuex状态管理模块
            index.js  # vuex配置模块
            ...
        App.vue  # 根组件
        main.js  # 入口文件
        ...
    ...
三：接口文档
http://127.0.0.1:8000/docs   # 接口文档  
四：接口测试
1、后端接口测试
    cd backend
    pytest tests/test_api.py
2、前端接口测试
    cd frontend
    npm run test  # 启动前端项目测试            
五：项目依赖包
1、后端依赖包
    fastapi==0.63.0
    uvicorn==0.13.4
    sqlalchemy==1.3.23
    passlib==1.7.2
    pydantic==1.7.3
    python-multipart==0.0.5
    pytest==6.2.2
    pytest-cov==2.11.1
    pytest-asyncio==0.14.0
    alembic==1.4.3
    python-jose==3.2.0
    cryptography==3.4.7
    ...
2、前端依赖包
    node.js
    npm
    vue.js
    vuex
    axios
    ... 
六：项目配置
1、后端项目配置
    cd backend/app/core/config.py
    修改配置项
2、前端项目配置
    cd frontend/src/assets/config.js
    修改配置项   
七：项目部署
1、后端项目部署
    参考FastApi官方文档
2、前端项目部署
    参考Vue官方文档   
八：项目问题
1、后端项目问题
    1、数据库连接问题
        修改app/core/db.py中的SQLALCHEMY_DATABASE_URL为正确的数据库连接字符串
    2、接口文档问题
        接口文档默认端口为8000，如需修改，请修改app/core/config.py中的DOCS_URL
    3、接口测试问题
        接口测试默认端口为8000，如需修改，请修改tests/test_api.py中的API_URL
2、前端项目问题
    1、接口测试问题
        接口测试默认端口为8000，如需修改，请修改tests/test_api.py中的API_URL    
