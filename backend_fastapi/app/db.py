from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1011%40@localhost/autotest"
# 数据库引擎对象，用于管理数据库连接
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# 创建会话工厂，用于生成数据库会话实例
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# 声明式模型基类，用于定义ORM模型
Base = declarative_base()


def get_db():
    """
    获取数据库会话
    
    该函数创建一个新的数据库会话，并确保在使用完成后正确关闭会话。
    使用yield实现上下文管理，保证资源释放。
    
    Returns:
        Session: 数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
