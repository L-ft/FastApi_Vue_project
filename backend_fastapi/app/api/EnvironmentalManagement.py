from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..auth import get_current_user
from datetime import datetime
from ..models import Environment, EnvironmentVariable as ORMEnvironmentVariable
from ..schemas import EnvironmentVariable, EnvironmentVariableCreate, EnvironmentVariableUpdate, EnvironmentCreate, EnvironmentUpdate
import logging

router = APIRouter()

# 获取模块日志记录器
logger = logging.getLogger(__name__)

# 环境管理
@router.get("/env-vars", response_model=List[schemas.Environment])
def read_environments(db: Session = Depends(get_db)):
    """
    获取所有环境

    参数:
    db (Session): 数据库会话对象

    返回:
    List[Environment]: 环境对象列表
    """
    logger.info("Fetching all environments")
    environments = db.query(Environment).all()
    return environments

@router.get("/env-vars/{env_id}", response_model=schemas.Environment)
def read_environment(env_id: int, db: Session = Depends(get_db)):
    """
    根据ID获取特定环境

    参数:
    env_id (int): 环境的唯一标识
    db (Session): 数据库会话对象

    返回:
    Environment: 请求的环境对象

    异常:
    HTTPException: 如果未找到对应ID的环境，则抛出404错误
    """
    logger.info(f"Fetching environment with ID: {env_id}")
    environment = db.query(Environment).filter(Environment.id == env_id).first()
    if not environment:
        logger.warning(f"Environment not found: {env_id}")
        raise HTTPException(status_code=404, detail="环境不存在")
    return environment

@router.post("/env-vars", response_model=schemas.Environment)
def create_environment(env: EnvironmentCreate, db: Session = Depends(get_db)):
    """
    创建新的环境

    参数:
    env (EnvironmentCreate): 包含新环境信息的对象
    db (Session): 数据库会话对象

    返回:
    Environment: 创建成功的环境对象
    """
    db_env = Environment(**env.dict())
    db.add(db_env)
    db.commit()
    db.refresh(db_env)
    return db_env

@router.put("/env-vars/{env_id}", response_model=schemas.Environment)
def update_environment(env_id: int, env: EnvironmentUpdate, db: Session = Depends(get_db)):
    """
    更新指定ID的环境信息

    参数:
    env_id (int): 环境的唯一标识
    env (EnvironmentUpdate): 包含更新信息的对象
    db (Session): 数据库会话对象

    返回:
    Environment: 更新后的环境对象

    异常:
    HTTPException: 如果未找到对应ID的环境，则抛出404错误
    """
    db_env = db.query(Environment).filter(Environment.id == env_id).first()
    if not db_env:
        raise HTTPException(status_code=404, detail="环境不存在")
    for key, value in env.dict(exclude_unset=True).items():
        setattr(db_env, key, value)
    db_env.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_env)
    return db_env

@router.delete("/env-vars/{env_id}")
def delete_environment(env_id: int, db: Session = Depends(get_db)):
    """
    删除指定ID的环境

    参数:
    env_id (int): 环境的唯一标识
    db (Session): 数据库会话对象

    返回:
    dict: 删除操作结果消息

    异常:
    HTTPException: 如果未找到对应ID的环境，则抛出404错误
    """
    db_env = db.query(Environment).filter(Environment.id == env_id).first()
    if not db_env:
        raise HTTPException(status_code=404, detail="环境不存在")
    db.delete(db_env)
    db.commit()
    return {"msg": "环境删除成功"}

# 获取所有环境变量
@router.get("/env-variables", response_model=List[EnvironmentVariable])
def get_environment_variables(
    db: Session = Depends(get_db)
    # current_user: models.UserDB = Depends(get_current_user)  # 暂时移除认证
):
    variables = db.query(ORMEnvironmentVariable).all()
    return variables

# 创建新环境变量
@router.post("/env-variables", response_model=EnvironmentVariable)
def create_environment_variable(
    variable: EnvironmentVariableCreate,
    db: Session = Depends(get_db)
    # current_user: models.UserDB = Depends(get_current_user)  # 暂时移除认证
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
    db: Session = Depends(get_db)
    # current_user: models.UserDB = Depends(get_current_user)  # 暂时移除认证
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
    db: Session = Depends(get_db)
    # current_user: models.UserDB = Depends(get_current_user)  # 暂时移除认证
):
    db_var = db.query(models.EnvironmentVariable).filter(models.EnvironmentVariable.id == var_id).first()
    if not db_var:
        raise HTTPException(status_code=404, detail="Environment variable not found")
    
    db.delete(db_var)
    db.commit()
    return {"status": "success", "message": "Environment variable deleted"}
