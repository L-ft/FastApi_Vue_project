from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import EnvironmentVariable
from ..schemas import EnvironmentVariableCreate, EnvironmentVariable
import logging

router = APIRouter()

# 获取模块日志记录器
logger = logging.getLogger(__name__)

# 环境变量
@router.get("/env-vars", response_model=list[EnvironmentVariable])
def read_env_vars(db: Session = Depends(get_db)):
    """
    获取所有环境变量

    参数:
    db (Session): 数据库会话对象

    返回:
    list[EnvironmentVariable]: 环境变量对象列表
    """
    logger.info("Fetching all environment variables")
    env_vars = db.query(EnvironmentVariable).all()
    return env_vars

@router.get("/env-vars/{env_var_id}", response_model=EnvironmentVariable)
def read_env_var(env_var_id: int, db: Session = Depends(get_db)):
    """
    根据ID获取特定环境变量

    参数:
    env_var_id (int): 环境变量的唯一标识
    db (Session): 数据库会话对象

    返回:
    EnvironmentVariable: 请求的环境变量对象

    异常:
    HTTPException: 如果未找到对应ID的环境变量，则抛出404错误
    """
    logger.info(f"Fetching environment variable with ID: {env_var_id}")
    env_var = db.query(EnvironmentVariable).filter(EnvironmentVariable.id == env_var_id).first()
    if not env_var:
        logger.warning(f"Environment variable not found: {env_var_id}")
        raise HTTPException(status_code=404, detail="环境变量不存在")
    return env_var

@router.post("/env-vars", response_model=EnvironmentVariable)
def create_env_var(env_var: EnvironmentVariableCreate, db: Session = Depends(get_db)):
    """
    创建新的环境变量

    参数:
    env_var (EnvironmentVariableCreate): 包含新环境变量信息的对象
    db (Session): 数据库会话对象

    返回:
    EnvironmentVariable: 创建成功的环境变量对象
    """
    db_env_var = EnvironmentVariable(**env_var.dict())
    db.add(db_env_var)
    db.commit()
    db.refresh(db_env_var)
    return db_env_var

@router.put("/env-vars/{env_var_id}", response_model=EnvironmentVariable)
def update_env_var(env_var_id: int, env_var: EnvironmentVariableCreate, db: Session = Depends(get_db)):
    """
    更新指定ID的环境变量信息

    参数:
    env_var_id (int): 环境变量的唯一标识
    env_var (EnvironmentVariableCreate): 包含更新信息的对象
    db (Session): 数据库会话对象

    返回:
    EnvironmentVariable: 更新后的环境变量对象

    异常:
    HTTPException: 如果未找到对应ID的环境变量，则抛出404错误
    """
    db_env_var = db.query(EnvironmentVariable).filter(EnvironmentVariable.id == env_var_id).first()
    if not db_env_var:
        raise HTTPException(status_code=404, detail="环境变量不存在")
    for key, value in env_var.dict().items():
        setattr(db_env_var, key, value)
    db.commit()
    db.refresh(db_env_var)
    return db_env_var

@router.delete("/env-vars/{env_var_id}")
def delete_env_var(env_var_id: int, db: Session = Depends(get_db)):
    """
    删除指定ID的环境变量

    参数:
    env_var_id (int): 环境变量的唯一标识
    db (Session): 数据库会话对象

    返回:
    dict: 删除操作结果消息

    异常:
    HTTPException: 如果未找到对应ID的环境变量，则抛出404错误
    """
    db_env_var = db.query(EnvironmentVariable).filter(EnvironmentVariable.id == env_var_id).first()
    if not db_env_var:
        raise HTTPException(status_code=404, detail="环境变量不存在")
    db.delete(db_env_var)
    db.commit()
    return {"msg": "环境变量删除成功"}
