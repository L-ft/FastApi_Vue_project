from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas import UserCreate, Token  # 使用相对导入
from ..db import get_db  # 使用相对导入
from ..auth import (  # 使用相对导入
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from ..models import UserDB  # 使用相对导入


# ---------------- FastAPI 应用 ----------------

router = APIRouter()
@router.post("/register")
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

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    用户登录接口，验证用户名和密码并生成访问令牌。

    参数:
    form_data (OAuth2PasswordRequestForm): 包含用户名和密码的表单数据。
    db (Session): 数据库会话对象，用于查询用户信息。

    返回值:
    dict: 包含访问令牌和令牌类型的字典。
    """
    # 验证用户是否存在以及密码是否正确
    user = db.query(UserDB).filter(UserDB.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 创建访问令牌并返回响应
    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(current_user: UserDB = Depends(get_current_user)):
    """
    获取当前登录用户信息。

    参数:
    current_user (UserDB): 通过get_current_user依赖注入获取的当前用户。

    返回:
    dict: 当前用户的用户名。
    """
    return {"username": current_user.username}