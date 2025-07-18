from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..auth import get_current_user
from datetime import datetime
from ..models import Environment, EnvironmentVariable as ORMEnvironmentVariable
from ..schemas import EnvironmentVariable, EnvironmentVariableCreate, EnvironmentVariableUpdate
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
    env_vars = db.query(ORMEnvironmentVariable).all()
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
    env_var = db.query(ORMEnvironmentVariable).filter(ORMEnvironmentVariable.id == env_var_id).first()
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
    db_env_var = ORMEnvironmentVariable(**env_var.dict())
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
    db_env_var = db.query(ORMEnvironmentVariable).filter(ORMEnvironmentVariable.id == env_var_id).first()
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
    db_env_var = db.query(ORMEnvironmentVariable).filter(ORMEnvironmentVariable.id == env_var_id).first()
    if not db_env_var:
        raise HTTPException(status_code=404, detail="环境变量不存在")
    db.delete(db_env_var)
    db.commit()
    return {"msg": "环境变量删除成功"}

# 获取所有环境变量
@router.get("/env-variables", response_model=List[EnvironmentVariable])
def get_environment_variables(
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(get_current_user)
):
    variables = db.query(ORMEnvironmentVariable).all()
    return variables

# 创建新环境变量
@router.post("/env-variables", response_model=EnvironmentVariable)
def create_environment_variable(
    variable: EnvironmentVariableCreate,
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(get_current_user)
):
    # 检查环境是否存在
    env = db.query(Environment).filter(Environment.id == variable.env_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")
    
    # 检查变量名是否已存在于同一环境中
    existing = db.query(ORMEnvironmentVariable).filter(
        ORMEnvironmentVariable.env_id == variable.env_id,
        ORMEnvironmentVariable.key == variable.key
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Variable key already exists in this environment")
    
    db_var = ORMEnvironmentVariable(**variable.dict())
    db.add(db_var)
    db.commit()
    db.refresh(db_var)
    return db_var

# 更新环境变量
@router.put("/env-variables/{var_id}", response_model=schemas.EnvironmentVariable)
def update_environment_variable(
    var_id: int,
    variable: schemas.EnvironmentVariableUpdate,
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(get_current_user)
):
    db_var = db.query(models.EnvironmentVariable).filter(models.EnvironmentVariable.id == var_id).first()
    if not db_var:
        raise HTTPException(status_code=404, detail="Environment variable not found")
    
    # 如果要更新key，检查新key是否与其他变量冲突
    if variable.key and variable.key != db_var.key:
        existing = db.query(models.EnvironmentVariable).filter(
            models.EnvironmentVariable.env_id == db_var.env_id,
            models.EnvironmentVariable.key == variable.key
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Variable key already exists in this environment")
    
    for field, value in variable.dict(exclude_unset=True).items():
        setattr(db_var, field, value)
    
    db_var.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_var)
    return db_var

# 删除环境变量
@router.delete("/env-variables/{var_id}")
def delete_environment_variable(
    var_id: int,
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(get_current_user)
):
    db_var = db.query(models.EnvironmentVariable).filter(models.EnvironmentVariable.id == var_id).first()
    if not db_var:
        raise HTTPException(status_code=404, detail="Environment variable not found")
    
    db.delete(db_var)
    db.commit()
    return {"status": "success", "message": "Environment variable deleted"}
