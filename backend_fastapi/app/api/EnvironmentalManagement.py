from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..auth import get_current_user
from datetime import datetime

router = APIRouter()

# ---------------- 环境管理API ----------------

@router.get("/environments", response_model=List[schemas.Environment])
def get_environments(db: Session = Depends(get_db)):
    """获取所有环境（自动修正，手动构造 Environment，避免文档卡死）"""
    envs = db.query(models.Environment).all()
    result = [schemas.Environment(
        id=e.id,
        name=e.name,
        value=e.value,
        description=e.description,
        created_at=e.created_at,
        updated_at=e.updated_at
    ) for e in envs]
    return result

@router.post("/environments", response_model=schemas.Environment)
def create_environment(env: schemas.EnvironmentCreate, db: Session = Depends(get_db)):
    """创建新环境"""
    # 检查环境名是否已存在
    if db.query(models.Environment).filter(models.Environment.name == env.name).first():
        raise HTTPException(status_code=400, detail="环境名称已存在")
    
    db_env = models.Environment(**env.dict())
    db.add(db_env)
    db.commit()
    db.refresh(db_env)
    return db_env

@router.put("/environments/{env_id}", response_model=schemas.Environment)
def update_environment(env_id: int, env: schemas.EnvironmentUpdate, db: Session = Depends(get_db)):
    """更新环境信息"""
    db_env = db.query(models.Environment).filter(models.Environment.id == env_id).first()
    if not db_env:
        raise HTTPException(status_code=404, detail="环境不存在")
    
    # 如果更新名称，检查新名称是否与其他环境冲突
    if env.name and env.name != db_env.name:
        if db.query(models.Environment).filter(models.Environment.name == env.name).first():
            raise HTTPException(status_code=400, detail="环境名称已存在")
    
    for field, value in env.dict(exclude_unset=True).items():
        setattr(db_env, field, value)
    
    db_env.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_env)
    return db_env

@router.delete("/environments/{env_id}")
def delete_environment(env_id: int, db: Session = Depends(get_db)):
    """删除环境"""
    db_env = db.query(models.Environment).filter(models.Environment.id == env_id).first()
    if not db_env:
        raise HTTPException(status_code=404, detail="环境不存在")
    
    db.delete(db_env)
    db.commit()
    return {"status": "success", "message": "环境已删除"}

# ---------------- 环境变量管理API ----------------

@router.get("/env-variables", response_model=List[schemas.EnvironmentVariable])
def get_environment_variables(db: Session = Depends(get_db)):
    """获取所有环境变量（自动修正，手动构造 EnvironmentVariable，避免文档卡死）"""
    vars = db.query(models.EnvironmentVariable).all()
    result = [schemas.EnvironmentVariable(
        id=v.id,
        env_id=v.env_id,
        key=v.key,
        value=v.value,
        created_at=v.created_at,
        updated_at=v.updated_at
    ) for v in vars]
    return result

@router.post("/env-variables", response_model=schemas.EnvironmentVariable)
def create_environment_variable(variable: schemas.EnvironmentVariableCreate, db: Session = Depends(get_db)):
    """创建新环境变量"""
    # 检查环境是否存在
    if not db.query(models.Environment).filter(models.Environment.id == variable.env_id).first():
        raise HTTPException(status_code=404, detail="所选环境不存在")
    
    # 检查变量名是否在同一环境中重复
    if db.query(models.EnvironmentVariable).filter(
        models.EnvironmentVariable.env_id == variable.env_id,
        models.EnvironmentVariable.key == variable.key
    ).first():
        raise HTTPException(status_code=400, detail="变量名在该环境中已存在")
    
    db_var = models.EnvironmentVariable(**variable.dict())
    db.add(db_var)
    db.commit()
    db.refresh(db_var)
    return db_var

@router.put("/env-variables/{var_id}", response_model=schemas.EnvironmentVariable)
def update_environment_variable(var_id: int, variable: schemas.EnvironmentVariableUpdate, db: Session = Depends(get_db)):
    """更新环境变量"""
    db_var = db.query(models.EnvironmentVariable).filter(models.EnvironmentVariable.id == var_id).first()
    if not db_var:
        raise HTTPException(status_code=404, detail="环境变量不存在")
    
    # 如果更新环境ID，检查环境是否存在
    if variable.env_id is not None:
        if not db.query(models.Environment).filter(models.Environment.id == variable.env_id).first():
            raise HTTPException(status_code=404, detail="所选环境不存在")
    
    # 如果更新变量名，检查是否在同一环境中重复
    if variable.key is not None and variable.key != db_var.key:
        if db.query(models.EnvironmentVariable).filter(
            models.EnvironmentVariable.env_id == (variable.env_id or db_var.env_id),
            models.EnvironmentVariable.key == variable.key
        ).first():
            raise HTTPException(status_code=400, detail="变量名在该环境中已存在")
    
    for field, value in variable.dict(exclude_unset=True).items():
        setattr(db_var, field, value)
    
    db_var.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_var)
    return db_var

@router.delete("/env-variables/{var_id}")
def delete_environment_variable(var_id: int, db: Session = Depends(get_db)):
    """删除环境变量"""
    db_var = db.query(models.EnvironmentVariable).filter(models.EnvironmentVariable.id == var_id).first()
    if not db_var:
        raise HTTPException(status_code=404, detail="环境变量不存在")
    
    db.delete(db_var)
    db.commit()
    return {"status": "success", "message": "环境变量已删除"}
