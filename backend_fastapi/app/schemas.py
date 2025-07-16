from pydantic import BaseModel
from typing import Optional


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
    description: Optional[str]
    class Config:
        orm_mode = True

class EnvironmentVariableCreate(BaseModel):
    name: str
    value: str

class EnvironmentVariable(EnvironmentVariableCreate):
    id: int

    class Config:
        orm_mode = True
