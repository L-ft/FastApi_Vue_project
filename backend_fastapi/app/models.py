from sqlalchemy import Column, Integer, String
from .db import Base, engine  # 使用相对导入


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