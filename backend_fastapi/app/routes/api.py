from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import ApiGroup, ApiInfo
from ..schemas import ApiGroupCreate, ApiGroupOut, ApiInfoCreate, ApiInfoOut

router = APIRouter(prefix="/api", tags=["API管理"])

# API分组
@router.post("/group", response_model=ApiGroupOut)
def create_group(group: ApiGroupCreate, db: Session = Depends(get_db)):
    db_group = ApiGroup(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.get("/group", response_model=list[ApiGroupOut])
def list_groups(db: Session = Depends(get_db)):
    return db.query(ApiGroup).all()

# API接口
# 新增接口
@router.post("/info", response_model=ApiInfoOut)
def create_api(api: ApiInfoCreate, db: Session = Depends(get_db)):
    db_api = ApiInfo(**api.dict())
    db.add(db_api)
    db.commit()
    db.refresh(db_api)
    return db_api

# 查询接口
@router.get("/info", response_model=list[ApiInfoOut])
def list_apis(db: Session = Depends(get_db)):
    return db.query(ApiInfo).all()

# 修改接口
@router.put("/info/{api_id}", response_model=ApiInfoOut)
def update_api(api_id: int, api: ApiInfoCreate, db: Session = Depends(get_db)):
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
    db_api = db.query(ApiInfo).filter(ApiInfo.id == api_id).first()
    if not db_api:
        raise HTTPException(status_code=404, detail="接口不存在")
    db.delete(db_api)
    db.commit()
    return {"msg": "删除成功"}