from pydantic import BaseModel
from typing import Optional, List, Dict, Any


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
    class Config:
        orm_mode = True

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
        description (Optional[str]): API描述信息
    """
    id: int
    name: str
    url: str
    method: str
    group_id: Optional[int]
    env_id: Optional[int]
    description: Optional[str]
    class Config:
        orm_mode = True


# ---------------- 环境变量管理 ----------------

class EnvironmentVariableCreate(BaseModel):
    """
    环境变量创建模型

    属性:
        name (str): 环境变量名称
        value (str): 环境变量值
    """
    name: str
    value: str


class EnvironmentVariable(EnvironmentVariableCreate):
    """
    环境变量数据库模型

    属性:
        id (Optional[int]): 主键ID（可选）
        name (str): 继承自父类的环境变量名称
        value (str): 继承自父类的环境变量值

    嵌套类:
        Config: ORM配置类
            orm_mode (bool): 启用ORM模式
    """
    id: Optional[int] = None

    class Config:
        orm_mode = True

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
    class Config:
        orm_mode = True

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
    class Config:
        orm_mode = True

class TestCaseGroupUpdate(BaseModel):
    """
    用例组更新模型

    属性:
        name (Optional[str]): 用例组名称
        description (Optional[str]): 用例组描述
    """
    name: Optional[str] = None
    description: Optional[str] = None