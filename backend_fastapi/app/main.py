from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="用户认证API",
)

# CORS 中间件配置
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- 配置 ----------------
SECRET_KEY = "your-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 初始化密码上下文和OAuth2方案
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ---------------- 数据库 ----------------
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1011%40@localhost/autotest"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# ---------------- 用户模型 ----------------
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)

# 创建所有表（如果不存在）
Base.metadata.create_all(bind=engine)

# ---------------- Pydantic ----------------
class UserCreate(BaseModel):
    """
    用户创建模型。

    属性:
    username (str): 用户名。
    password (str): 原始密码。
    """
    username: str
    password: str


class Token(BaseModel):
    """
    JWT令牌响应模型。

    属性:
    access_token (str): 编码后的JWT令牌。
    token_type (str): 令牌类型，通常是"bearer"。
    """
    access_token: str
    token_type: str

# ---------------- 工具函数 ----------------
def get_db():
    """
    获取数据库会话。

    该函数创建一个新的数据库会话，并在使用后确保正确关闭它。
    使用try-finally块来保证数据库会话始终会被关闭。

    返回:
    Session: 数据库会话对象。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    """
    对密码进行哈希处理。

    参数:
    password (str): 要哈希的原始密码。

    返回:
    str: 哈希后的密码。
    """
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """
    验证提供的密码是否与存储的哈希密码匹配。

    参数:
    plain (str): 要验证的明文密码。
    hashed (str): 存储的哈希密码。

    返回:
    bool: 如果密码匹配返回True，否则返回False。
    """
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    生成JWT访问令牌。

    参数:
    data (dict): 需要编码到令牌中的数据。
    expires_delta (timedelta, 可选): 令牌的过期时间间隔，默认为15分钟。

    返回:
    str: 编码后的JWT令牌。
    """
    to_encode = data.copy()
    # 计算过期时间
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    # 更新编码数据，加入过期时间
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    根据提供的JWT令牌获取当前用户。

    参数:
    token (str): 通过oauth2_scheme获取的JWT令牌。
    db (Session): 数据库会话对象。

    返回:
    UserDB: 解码令牌得到的当前用户。

    异常:
    HTTPException: 如果令牌无效或用户不存在时抛出401或404异常。
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token无效")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token验证失败")
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

# ---------------- FastAPI 应用 ----------------

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    print("收到注册请求", user.username)
    """
    用户注册接口。

    参数:
    user (UserCreate): 包含用户名和密码的用户创建模型。
    db (Session): 数据库会话对象。

    返回:
    dict: 注册成功时返回消息。

    异常:
    HTTPException: 如果用户名已存在时抛出400异常。
    """
    if db.query(UserDB).filter(UserDB.username == user.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    hashed_pwd = hash_password(user.password)
    new_user = UserDB(username=user.username, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    return {"msg": "注册成功"}

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def read_users_me(current_user: UserDB = Depends(get_current_user)):
    """
    获取当前登录用户信息。

    参数:
    current_user (UserDB): 通过get_current_user依赖注入获取的当前用户。

    返回:
    dict: 当前用户的用户名。
    """
    return {"username": current_user.username}
