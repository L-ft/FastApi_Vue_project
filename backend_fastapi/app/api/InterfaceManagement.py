from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import ApiInfo
from ..schemas import ApiInfoOut, ApiInfoCreate
from ..models import EnvironmentVariable
import logging

router = APIRouter()

# 获取模块日志记录器
logger = logging.getLogger(__name__)

# API接口
# 新增接口
@router.post("/apis", response_model=ApiInfoOut)
def create_api(api: ApiInfoCreate, db: Session = Depends(get_db)):
    """
    创建新的API接口

    参数:
    api (ApiInfoCreate): 包含新API信息的对象
    db (Session): 数据库会话对象

    返回:
    ApiInfo: 创建的API对象
    """
    logger.info(f"Creating new API: {api.name}")
    db_api = ApiInfo(**api.dict())
    db.add(db_api)
    db.commit()
    db.refresh(db_api)
    logger.info(f"Created API with ID: {db_api.id}")
    return db_api

# 查询接口

@router.get("/apis", response_model=list[ApiInfoOut])
def list_apis(db: Session = Depends(get_db)):
    """
    获取所有API接口列表（自动修正，手动构造 ApiInfoOut，避免文档卡死）
    """
    logger.info("Fetching all APIs")
    from ..models import Environment
    apis = db.query(ApiInfo).all()
    envs = {e.id: e.name for e in db.query(Environment).all()}
    result = []
    for api in apis:
        result.append(ApiInfoOut(
            id=api.id,
            name=api.name,
            url=api.url,
            method=api.method,
            group_id=api.group_id,
            env_id=api.env_id,
            env_name=envs.get(api.env_id) if api.env_id else None,
            description=api.description
        ))
    logger.info(f"Successfully fetched {len(result)} apis")
    return result

# 修改接口
@router.put("/info/{api_id}", response_model=ApiInfoOut)
def update_api(api_id: int, api: ApiInfoCreate, db: Session = Depends(get_db)):
    """
    更新指定ID的API接口信息

    参数:
    api_id (int): 要更新的API的ID
    api (ApiInfoCreate): 包含更新信息的对象
    db (Session): 数据库会话对象

    返回:
    ApiInfo: 更新后的API对象
    """
    db_api = db.query(ApiInfo).filter(ApiInfo.id == api_id).first()
    if not db_api:
        raise HTTPException(status_code=404, detail="接口不存在")
    for k, v in api.dict().items():
        setattr(db_api, k, v)
    db.commit()
    db.refresh(db_api)
    return db_api

# 删除接口
@router.delete("/info/{api_id}")
def delete_api(api_id: int, db: Session = Depends(get_db)):
    """
    删除指定ID的API接口

    参数:
    api_id (int): 要删除的API的ID
    db (Session): 数据库会话对象

    返回:
    dict: 删除操作结果消息
    """
    db_api = db.query(ApiInfo).filter(ApiInfo.id == api_id).first()
    if not db_api:
        raise HTTPException(status_code=404, detail="接口不存在")
    db.delete(db_api)
    db.commit()
    return {"msg": "删除成功"}
