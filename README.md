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



# # ---------------- 配置 ----------------
# SECRET_KEY = "your-super-secret-key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
# # 初始化密码上下文和OAuth2方案
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
# # ---------------- 数据库 ----------------
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1011%40@localhost/autotest"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# Base = declarative_base()
#
# # ---------------- 用户模型 ----------------
# class UserDB(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True, index=True, nullable=False)
#     password = Column(String(100), nullable=False)
#
# # 创建所有表（如果不存在）
# Base.metadata.create_all(bind=engine)
#
# # ---------------- Pydantic ----------------
# class UserCreate(BaseModel):
#     """
#     用户创建模型。
#
#     属性:
#     username (str): 用户名。
#     password (str): 原始密码。
#     """
#     username: str
#     password: str
#
#
# class Token(BaseModel):
#     """
#     JWT令牌响应模型。
#
#     属性:
#     access_token (str): 编码后的JWT令牌。
#     token_type (str): 令牌类型，通常是"bearer"。
#     """
#     access_token: str
#     token_type: str
#
# # ---------------- 工具函数 ----------------
# def get_db():
#     """
#     获取数据库会话。
#
#     该函数创建一个新的数据库会话，并在使用后确保正确关闭它。
#     使用try-finally块来保证数据库会话始终会被关闭。
#
#     返回:
#     Session: 数据库会话对象。
#     """
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# def hash_password(password: str) -> str:
#     """
#     对密码进行哈希处理。
#
#     参数:
#     password (str): 要哈希的原始密码。
#
#     返回:
#     str: 哈希后的密码。
#     """
#     return pwd_context.hash(password)
#
# def verify_password(plain: str, hashed: str) -> bool:
#     """
#     验证提供的密码是否与存储的哈希密码匹配。
#
#     参数:
#     plain (str): 要验证的明文密码。
#     hashed (str): 存储的哈希密码。
#
#     返回:
#     bool: 如果密码匹配返回True，否则返回False。
#     """
#     return pwd_context.verify(plain, hashed)
#
# def create_access_token(data: dict, expires_delta: timedelta = None):
#     """
#     生成JWT访问令牌。
#
#     参数:
#     data (dict): 需要编码到令牌中的数据。
#     expires_delta (timedelta, 可选): 令牌的过期时间间隔，默认为15分钟。
#
#     返回:
#     str: 编码后的JWT令牌。
#     """
#     to_encode = data.copy()
#     # 计算过期时间
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
#     # 更新编码数据，加入过期时间
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     """
#     根据提供的JWT令牌获取当前用户。
#
#     参数:
#     token (str): 通过oauth2_scheme获取的JWT令牌。
#     db (Session): 数据库会话对象。
#
#     返回:
#     UserDB: 解码令牌得到的当前用户。
#
#     异常:
#     HTTPException: 如果令牌无效或用户不存在时抛出401或404异常。
#     """
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=401, detail="Token无效")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token验证失败")
#     user = db.query(UserDB).filter(UserDB.username == username).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="用户不存在")
#     return user
#
# # ---------------- FastAPI 应用 ----------------
#
# @app.post("/register")
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     print("收到注册请求", user.username)
#     """
#     用户注册接口。
#
#     参数:
#     user (UserCreate): 包含用户名和密码的用户创建模型。
#     db (Session): 数据库会话对象。
#
#     返回:
#     dict: 注册成功时返回消息。
#
#     异常:
#     HTTPException: 如果用户名已存在时抛出400异常。
#     """
#     if db.query(UserDB).filter(UserDB.username == user.username).first():
#         raise HTTPException(status_code=400, detail="用户名已存在")
#     hashed_pwd = hash_password(user.password)
#     new_user = UserDB(username=user.username, password=hashed_pwd)
#     db.add(new_user)
#     db.commit()
#     return {"msg": "注册成功"}
#
# @app.post("/token", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(UserDB).filter(UserDB.username == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.password):
#         raise HTTPException(status_code=401, detail="用户名或密码错误")
#     token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     return {"access_token": token, "token_type": "bearer"}
#
# @app.get("/me")
# def read_users_me(current_user: UserDB = Depends(get_current_user)):
#     """
#     获取当前登录用户信息。
#
#     参数:
#     current_user (UserDB): 通过get_current_user依赖注入获取的当前用户。
#
#     返回:
#     dict: 当前用户的用户名。
#     """
#     return {"username": current_user.username}
