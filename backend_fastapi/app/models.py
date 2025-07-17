from datetime import datetime
from sqlalchemy import DateTime

from .db import Base, engine  # 使用相对导入
from sqlalchemy import Column, Integer, String, ForeignKey


# ---------------- 用户模型 ----------------
# UserDB 类表示数据库中的用户表
# 属性:
#   id(int): 用户唯一标识，主键，自动递增
#   username(str): 用户名，最大长度50，唯一，不可为空
#   password(str): 密码，最大长度100，不可为空
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)

# 创建所有表（如果不存在）
# 参数:
#   bind(engine): 数据库引擎，用于连接数据库并执行创建表操作
Base.metadata.create_all(bind=engine)


# ---------------- API接口模型 ----------------
class ApiGroup(Base):
    """
      API分组模型

      Attributes:
          id (int): 分组唯一标识
          name (str): 分组名称，50字符内，唯一且非空
      """

    __tablename__ = "api_group"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

class ApiInfo(Base):
    """
    API信息模型

    Attributes:
        id (int): API唯一标识
        name (str): API名称，100字符内，非空
        url (str): API地址，255字符内，非空
        method (str): 请求方法，10字符内，非空
        group_id (int): 所属分组ID，关联api_group.id
        description (str): 描述信息，255字符内
    """

    __tablename__ = "api_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    url = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    group_id = Column(Integer, ForeignKey("api_group.id"))
    env_id = Column(Integer, ForeignKey("environment_variables.id"), nullable=True)
    description = Column(String(255))

# ---------------- 环境变量模型 ----------------
class EnvironmentVariable(Base):
    """
    环境变量模型

    Attributes:
        id (int): 环境变量唯一标识
        name (str): 环境变量名称，100字符内，非空且唯一
        value (str): 环境变量值，255字符内，非空
    """

    __tablename__ = "environment_variables"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    value = Column(String(255), nullable=False)

# ---------------- 用例管理模型 ----------------
class CaseInfo(Base):
    """
    用例信息模型

    Attributes:
        id (int): 用例唯一标识
        name (str): 用例名称，100字符内，非空
        description (str): 用例描述，255字符内
        group_id (int): 所属分组ID，关联api_group.id
        api_id (int): 所属APIID，关联api_info.id
        request_data (str): 请求数据，255字符内
        request_header (str): 请求头，255字符内
        request_method (str): 请求方法，10字符内
        request_url (str): 请求地址，255字符内
        response_data (str): 响应数据，255字符内
        response_header (str): 响应头，255字符内
        response_status (int): 响应状态码，10字符内
        creator (str): 创建人，100字符内
        create_time (datetime): 创建时间
        modifier (str): 修改人，100字符内
        modify_time (datetime): 修改时间
    """

    __tablename__ = "case_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    group_id = Column(Integer, ForeignKey("api_group.id"))
    api_id = Column(Integer, ForeignKey("api_info.id"))
    request_data = Column(String(255))
    params = Column(String(1000))  # 可根据实际需要调整长度
    request_header = Column(String(255))
    headers = Column(String(1000))  # 可根据实际需要调整长度
    body = Column(String(2000))  # 可根据实际需要调整长度
    method = Column(String(10))
    request_url = Column(String(255))
    response_data = Column(String(255))
    response_header = Column(String(255))
    response_status = Column(String(10))
    expected_status = Column(Integer)
    expected_response = Column(String(2000))  # 可根据实际需要调整长度
    creator = Column(String(100))
    create_time = Column(DateTime, default=datetime.now)
    modifier = Column(String(100))
    modify_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 注意：params, headers, body, expected_response, response_data, response_header 字段如存储 dict，必须在插入数据库前用 json.dumps 序列化为字符串，否则会报错。
# 创建所有表（如果不存在）
# 参数:
#   bind(engine): 数据库引擎，用于连接数据库并执行创建表操作
Base.metadata.create_all(bind=engine)
