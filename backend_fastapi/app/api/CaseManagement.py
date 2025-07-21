from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import CaseInfo
from ..schemas import TestCaseOut, TestCaseUpdate, TestCaseCreate
import logging
import json

router = APIRouter()
logger = logging.getLogger(__name__)

SERIALIZE_KEYS = ["params", "headers", "body", "expected_response", "response_data", "response_header"]

def to_dict_safe(val: str) -> Dict[str, Any]:
    """安全地将字符串转换为字典"""
    if isinstance(val, str):
        try:
            return json.loads(val)
        except Exception:
            return {}
    elif isinstance(val, dict):
        return val
    return {}
# 用例管理

@router.get("/cases", response_model=List[TestCaseOut])
async def get_case_info(db: Session = Depends(get_db)):
    """
    获取用例信息列表（自动修正，手动构造 TestCaseOut，避免文档卡死）
    """
    try:
        logger.info("Fetching all test cases")
        case_info = db.query(CaseInfo).all()
        result = []
        for item in case_info:
            result.append(TestCaseOut(
                id=item.id,
                name=item.name,
                description=item.description,
                group_id=item.group_id,
                api_id=item.api_id,
                method=item.method,
                request_url=item.request_url,
                params=to_dict_safe(item.params),
                headers=to_dict_safe(item.headers),
                body=to_dict_safe(item.body),
                expected_status=item.expected_status,
                expected_response=to_dict_safe(item.expected_response)
            ))
        logger.info(f"Successfully fetched {len(result)} test cases")
        return result
    except Exception as e:
        logger.error(f"Error fetching test cases: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cases", response_model=TestCaseOut)
async def create_case_info(case: TestCaseCreate, db: Session = Depends(get_db)):
    """
    创建新的用例
    
    参数:
        case (TestCaseCreate): 用例创建模型
        db (Session): 数据库会话对象
    返回:
        TestCaseOut: 创建的用例信息
    """
    try:
        logger.info(f"Creating new test case: {case.name}")
        case_dict = case.dict()
        
        # 序列化JSON字段
        for key in SERIALIZE_KEYS:
            if key in case_dict and case_dict[key] is not None:
                case_dict[key] = json.dumps(case_dict[key])
        
        db_case = CaseInfo(**case_dict)
        db.add(db_case)
        db.commit()
        db.refresh(db_case)
        
        # 反序列化JSON字段
        for key in SERIALIZE_KEYS:
            if hasattr(db_case, key):
                setattr(db_case, key, to_dict_safe(getattr(db_case, key)))
        
        logger.info(f"Successfully created test case with ID: {db_case.id}")
        return db_case
    except Exception as e:
        logger.error(f"Error creating test case: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/cases/{case_id}", response_model=TestCaseOut)
async def update_case_info(case_id: int, case: TestCaseUpdate, db: Session = Depends(get_db)):
    """
    更新用例信息
    
    参数:
        case_id (int): 用例ID
        case (TestCaseUpdate): 用例更新模型
        db (Session): 数据库会话对象
    返回:
        TestCaseOut: 更新后的用例信息
    """
    try:
        logger.info(f"Updating test case with ID: {case_id}")
        db_case = db.query(CaseInfo).filter(CaseInfo.id == case_id).first()
        if not db_case:
            raise HTTPException(status_code=404, detail="Test case not found")
        
        # 更新非None字段
        update_data = case.dict(exclude_unset=True)
        for key in SERIALIZE_KEYS:
            if key in update_data and update_data[key] is not None:
                update_data[key] = json.dumps(update_data[key])
        
        for key, value in update_data.items():
            setattr(db_case, key, value)
        
        db.commit()
        db.refresh(db_case)
        
        # 反序列化JSON字段
        for key in SERIALIZE_KEYS:
            if hasattr(db_case, key):
                setattr(db_case, key, to_dict_safe(getattr(db_case, key)))
        
        logger.info(f"Successfully updated test case with ID: {case_id}")
        return db_case
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating test case: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cases/{case_id}", response_model=TestCaseOut)
async def delete_case_info(case_id: int, db: Session = Depends(get_db)):
    """
    删除用例信息
    
    参数:
        case_id (int): 用例ID
        db (Session): 数据库会话对象
    返回:
        TestCaseOut: 删除的用例信息
    """
    try:
        logger.info(f"Deleting test case with ID: {case_id}")
        db_case = db.query(CaseInfo).filter(CaseInfo.id == case_id).first()
        if not db_case:
            raise HTTPException(status_code=404, detail="Test case not found")
        
        db.delete(db_case)
        db.commit()
        
        logger.info(f"Successfully deleted test case with ID: {case_id}")
        return db_case
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting test case: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
