from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


# ---------------- 认证Pydantic ----------------
class UserCreate(BaseModel):
    """
    用户创建模型。

    属性:
    username (str): 用户名。
    password (str): 原始密码。
    """
    username: str
    password: str


class Token(BaseModel):
    """
    JWT令牌响应模型。

    属性:
    access_token (str): 编码后的JWT令牌。
    token_type (str): 令牌类型，通常是"bearer"。
    """
    access_token: str
    token_type: str

# ---------------- 接口管理Pydantic ----------------
class ApiGroupCreate(BaseModel):
    """
    创建API组的请求数据模型

    Attributes:
        name (str): API组名称，必填字段
    """
    name: str

class ApiGroupOut(BaseModel):
    """
    API组响应数据模型

    Attributes:
        id (int): API组唯一标识
        name (str): API组名称
    """
    id: int
    name: str
    model_config = {"from_attributes": True}

class ApiGroupUpdate(BaseModel):
    """
    更新API组的请求数据模型

    Attributes:
        name (Optional[str]): API组名称，可选字段
    """
    name: Optional[str] = None

class ApiInfoCreate(BaseModel):
    """
    创建API信息的请求数据模型

    Attributes:
        name (str): API名称，必填字段
        url (str): API地址，必填字段
        method (str): HTTP方法类型，必填字段
        group_id (Optional[int]): 所属API组ID，可选字段，默认为None
        description (Optional[str]): API描述信息，可选字段，默认为None
    """
    name: str
    url: str
    method: str
    group_id: Optional[int] = None
    env_id: Optional[int] = None
    description: Optional[str] = None

class ApiInfoOut(BaseModel):
    """
    API信息响应数据模型

    Attributes:
        id (int): API唯一标识
        name (str): API名称
        url (str): API地址
        method (str): HTTP方法类型
        group_id (Optional[int]): 所属API组ID
        env_id (Optional[int]): 关联的环境ID
        env_name: Optional[str] = None  # 环境名称（非数据库字段）
        description (Optional[str]): API描述信息
    """
    id: int
    name: str
    url: str
    method: str
    group_id: Optional[int]
    env_id: Optional[int]
    env_name: Optional[str] = None
    description: Optional[str]
    model_config = {"from_attributes": True}


# ---------------- 环境管理Pydantic ----------------
class EnvironmentBase(BaseModel):
    """环境基础模型"""
    name: str
    value: str
    description: Optional[str] = None

class EnvironmentCreate(EnvironmentBase):
    """用于创建环境的请求模型"""
    pass

class EnvironmentUpdate(BaseModel):
    """用于更新环境的请求模型"""
    name: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None

class Environment(EnvironmentBase):
    """环境的响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# ---------------- 环境变量Pydantic ----------------
class EnvironmentVariableBase(BaseModel):
    """环境变量的基础模型"""
    env_id: int
    key: str
    value: str

class EnvironmentVariableCreate(EnvironmentVariableBase):
    """用于创建环境变量的请求模型"""
    pass

class EnvironmentVariableUpdate(BaseModel):
    """用于更新环境变量的请求模型"""
    env_id: Optional[int] = None
    key: Optional[str] = None
    value: Optional[str] = None

class EnvironmentVariable(EnvironmentVariableBase):
    """环境变量的响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# ---------------- 用例管理Pydantic ----------------
class TestCaseCreate(BaseModel):
    """
    用例创建模型

    属性:
        name (str): 用例名称
        description (Optional[str]): 用例描述
        group_id (int): 所属用例组ID
        api_id (int): 所属APIID
        method (str): HTTP方法类型
        url (str): API地址
        params (Optional[Dict[str, Any]]): 请求参数
        headers (Optional[Dict[str, Any]]): 请求头
        body (Optional[Dict[str, Any]]): 请求体
        expected_status (int): 期望HTTP状态码
        expected_response (Optional[Dict[str, Any]]): 期望响应体
    """
    name: str
    description: Optional[str]
    group_id: int
    api_id: int
    method: str
    request_url: str
    params: Optional[Dict[str, Any]]
    headers: Optional[Dict[str, Any]]
    body: Optional[Dict[str, Any]]
    expected_status: int
    expected_response: Optional[Dict[str, Any]]

class TestCaseOut(BaseModel):
    """
    用例响应模型

    属性:
        id (int): 用例ID
        name (str): 用例名称
        description (Optional[str]): 用例描述
        group_id (int): 所属用例组ID
        api_id (int): 所属APIID
        method (str): HTTP方法类型
        url (str): API地址
        params (Optional[Dict[str, Any]]): 请求参数
        headers (Optional[Dict[str, Any]]): 请求头
        body (Optional[Dict[str, Any]]): 请求体
        expected_status (int): 期望HTTP状态码
        expected_response (Optional[Dict[str, Any]]): 期望响应体
    """
    id: int
    name: str
    description: Optional[str]
    group_id: int
    api_id: int
    method: str
    request_url: str
    params: Optional[Dict[str, Any]]
    headers: Optional[Dict[str, Any]]
    body: Optional[Dict[str, Any]]
    expected_status: int
    expected_response: Optional[Dict[str, Any]]
    model_config = {"from_attributes": True}

class TestCaseUpdate(BaseModel):
    """
    用例更新模型

    属性:
        name (Optional[str]): 用例名称
        description (Optional[str]): 用例描述
        group_id (Optional[int]): 所属用例组ID
        api_id (Optional[int]): 所属APIID
        method (Optional[str]): HTTP方法类型
        url (Optional[str]): API地址
        params (Optional[Dict[str, Any]]): 请求参数
        headers (Optional[Dict[str, Any]]): 请求头
        body (Optional[Dict[str, Any]]): 请求体
        expected_status (Optional[int]): 期望HTTP状态码
        expected_response (Optional[Dict[str, Any]]): 期望响应体
    """
    name: Optional[str] = None
    description: Optional[str] = None
    group_id: Optional[int] = None
    api_id: Optional[int] = None
    method: Optional[str] = None
    request_url: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None
    expected_status: Optional[int] = None
    expected_response: Optional[Dict[str, Any]] = None

# ---------------- 用例组管理Pydantic ----------------
class TestCaseGroupCreate(BaseModel):
    """
    用例组创建模型

    属性:
        name (str): 用例组名称
        description (Optional[str]): 用例组描述
    """
    name: str
    description: Optional[str]

class TestCaseGroupOut(BaseModel):
    """
    用例组响应模型

    属性:
        id (int): 用例组ID
        name (str): 用例组名称
        description (Optional[str]): 用例组描述
    """
    id: int
    name: str
    description: Optional[str]
    model_config = {"from_attributes": True}

class TestCaseGroupUpdate(BaseModel):
    """
    用例组更新模型

    属性:
        name (Optional[str]): 用例组名称
        description (Optional[str]): 用例组描述
    """
    name: Optional[str] = None
    description: Optional[str] = None