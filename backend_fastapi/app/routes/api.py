from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import ApiGroup, ApiInfo
from ..schemas import ApiGroupCreate, ApiGroupOut, ApiInfoCreate, ApiInfoOut

router = APIRouter(prefix="/api", tags=["API管理"])

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
    db_group = ApiGroup(name=group.name)  # 创建新的ApiGroup实例
    db.add(db_group)  # 将新实例添加到数据库会话
    db.commit()  # 提交事务，将更改保存到数据库
    db.refresh(db_group)  # 刷新实例，获取数据库中的最新数据（如ID等）
    return db_group  # 返回创建的组对象

@router.get("/group", response_model=list[ApiGroupOut])
# 获取所有API分组信息
# 参数:
#   db: 数据库会话对象，默认通过get_db获取
# 返回:
#   ApiGroup对象列表
def list_groups(db: Session = Depends(get_db)):
    return db.query(ApiGroup).all()
 
# API接口
# 新增接口
@router.post("/info", response_model=ApiInfoOut)
def create_api(api: ApiInfoCreate, db: Session = Depends(get_db)):
    """
    创建新的API接口

    参数:
    api (ApiInfoCreate): 包含新API信息的对象
    db (Session): 数据库会话对象

    返回:
    ApiInfo: 创建的API对象
    """
    db_api = ApiInfo(**api.dict())
    db.add(db_api)
    db.commit()
    db.refresh(db_api)
    return db_api

# 查询接口
@router.get("/info", response_model=list[ApiInfoOut])
def list_apis(db: Session = Depends(get_db)):
    """
    获取所有API接口列表

    参数:
    db (Session): 数据库会话对象

    返回:
    list[ApiInfo]: API对象列表
    """
    return db.query(ApiInfo).all()

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
