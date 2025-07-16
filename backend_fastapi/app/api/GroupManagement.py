from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import ApiGroup
from ..schemas import ApiGroupOut, ApiGroupCreate, ApiGroupUpdate
import logging

router = APIRouter()

# 获取模块日志记录器
logger = logging.getLogger(__name__)

# API分组
@router.post("/group", response_model=ApiGroupOut)
def create_group(group: ApiGroupCreate, db: Session = Depends(get_db)):
    """
    创建一个新的API组

    参数:
    group (ApiGroupCreate): 包含新组数据的模型对象
    db (Session): 数据库会话对象，默认通过依赖注入获取

    返回:
    ApiGroupOut: 创建成功的组对象，包含数据库生成的信息
    """
    logger.info(f"Creating new API group: {group.name}")
    db_group = ApiGroup(name=group.name)  # 创建新的ApiGroup实例
    db.add(db_group)  # 将新实例添加到数据库会话
    db.commit()  # 提交事务，将更改保存到数据库
    db.refresh(db_group)  # 刷新实例，获取数据库中的最新数据（如ID等）
    logger.info(f"Created API group with ID: {db_group.id}")
    return db_group  # 返回创建的组对象

@router.get("/group", response_model=list[ApiGroupOut])
# 获取所有API分组信息
# 参数:
#   db: 数据库会话对象，默认通过get_db获取
# 返回:
#   ApiGroup对象列表
def list_groups(db: Session = Depends(get_db)):
    logger.info("Fetching all API groups")
    return db.query(ApiGroup).all()

# 添加更新和删除API分组的路由
@router.put("/group/{group_id}", response_model=ApiGroupOut)
def update_group(group_id: int, group: ApiGroupUpdate, db: Session = Depends(get_db)):
    """
    更新指定ID的API分组信息

    参数:
    group_id (int): 要更新的分组ID
    group (ApiGroupUpdate): 包含更新信息的对象
    db (Session): 数据库会话对象

    返回:
    ApiGroup: 更新后的分组对象
    """
    db_group = db.query(ApiGroup).filter(ApiGroup.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="分组不存在")
    if group.name is not None:
        db_group.name = group.name
    db.commit()
    db.refresh(db_group)
    return db_group

@router.delete("/group/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    """
    删除指定ID的API分组

    参数:
    group_id (int): 要删除的分组ID
    db (Session): 数据库会话对象

    返回:
    dict: 删除操作结果消息
    """
    db_group = db.query(ApiGroup).filter(ApiGroup.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="分组不存在")
    db.delete(db_group)
    db.commit()
    return {"msg": "分组删除成功"}