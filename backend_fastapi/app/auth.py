from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .db import get_db  # 使用相对导入
from .models import UserDB  # 使用相对导入

# ---------------- 配置 ----------------
# 配置常量定义
# SECRET_KEY: 用于JWT签名的密钥
# ALGORITHM: JWT签名算法
# ACCESS_TOKEN_EXPIRE_MINUTES: 访问令牌过期时间（分钟）
SECRET_KEY = "your-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 初始化安全组件
# pwd_context: 密码加密上下文，使用bcrypt算法
# oauth2_scheme: OAuth2密码承载方案，用于获取token
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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