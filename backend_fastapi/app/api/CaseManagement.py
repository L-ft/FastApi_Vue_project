from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import CaseInfo
from ..schemas import TestCaseOut, TestCaseUpdate,TestCaseCreate, TestCaseGroupCreate, TestCaseGroupUpdate,TestCaseGroupOut
from fastapi import Request
import logging

router = APIRouter()

# 获取模块日志记录器
logger = logging.getLogger(__name__)
import logging
# 用例管理
@router.get("/case_info", response_model=List[TestCaseOut])
async def get_case_info(db: Session = Depends(get_db)):
    """
    获取用例信息
    """
    import json
    def to_dict_safe(val):
        if isinstance(val, str):
            try:
                return json.loads(val)
            except Exception:
                return {}
        return val
    case_info = db.query(CaseInfo).all()
    for item in case_info:
        item.params = to_dict_safe(item.params)
        item.headers = to_dict_safe(item.headers)
        item.body = to_dict_safe(item.body)
        item.expected_response = to_dict_safe(item.expected_response)
    return case_info

@router.post("/case_info")
async def create_case_info(request: Request, db: Session = Depends(get_db)):
    """
    创建用例信息
    """
    import json
    body = await request.json()
    # 需要序列化的字段
    SERIALIZE_KEYS = ["params", "headers", "body", "expected_response", "response_data", "response_header"]
    for key in SERIALIZE_KEYS:
        if key in body:
            val = body[key]
            if val is None:
                body[key] = json.dumps({})
            elif not isinstance(val, str):
                body[key] = json.dumps(val)
            else:
                try:
                    json.loads(val)
                except Exception:
                    body[key] = json.dumps(val)
    db_case_info = CaseInfo(**body)
    db.add(db_case_info)
    db.commit()
    db.refresh(db_case_info)
    # 响应时反序列化
    def to_dict_safe(val):
        if isinstance(val, str):
            try:
                result = json.loads(val)
                if result is None or result == "" or result == {}:
                    return {}
                return result
            except Exception:
                return {}
        elif isinstance(val, dict):
            return val
        else:
            return {}
    for key in SERIALIZE_KEYS:
        if hasattr(db_case_info, key):
            value = getattr(db_case_info, key)
            dict_value = to_dict_safe(value)
            if not isinstance(dict_value, dict):
                dict_value = {}
            setattr(db_case_info, key, dict_value)
    # 额外字段直接返回
    for key in body:
        if hasattr(db_case_info, key):
            setattr(db_case_info, key, getattr(db_case_info, key))
    return db_case_info

@router.put("/case_info/{case_id}", response_model=TestCaseOut)
async def update_case_info(case_id: int, case_info: TestCaseUpdate, db: Session = Depends(get_db)):
    """
    更新用例信息
    """
    import json
    db_case_info = db.query(CaseInfo).filter(CaseInfo.id == case_id).first()
    if not db_case_info:
        raise HTTPException(status_code=404, detail="用例信息不存在")
    update_data = case_info.dict(exclude_unset=True)
    SERIALIZE_KEYS = ["params", "headers", "body", "expected_response", "response_data", "response_header"]
    for key, value in update_data.items():
        if key in SERIALIZE_KEYS:
            if value is None:
                value = json.dumps({})
            elif not isinstance(value, str):
                value = json.dumps(value)
            else:
                try:
                    json.loads(value)
                except Exception:
                    value = json.dumps(value)
        setattr(db_case_info, key, value)
    db.add(db_case_info)
    db.commit()
    db.refresh(db_case_info)
    # 响应时反序列化
    def to_dict_safe(val):
        if isinstance(val, str):
            try:
                return json.loads(val)
            except Exception:
                return {}
        return val
    for key in SERIALIZE_KEYS:
        if hasattr(db_case_info, key):
            setattr(db_case_info, key, to_dict_safe(getattr(db_case_info, key)))
    return db_case_info

@router.delete("/case_info/{case_id}", response_model=TestCaseOut)
async def delete_case_info(case_id: int, db: Session = Depends(get_db)):
    """
    删除用例信息
    """
    db_case_info = db.query(CaseInfo).filter(CaseInfo.id == case_id).first()
    if not db_case_info:
        raise HTTPException(status_code=404, detail="用例信息不存在")
    db.delete(db_case_info)
    db.commit()
    return db_case_info
