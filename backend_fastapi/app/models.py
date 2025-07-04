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
    description = Column(String(255))
