from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend_fastapi.app.routes import user
from backend_fastapi.app.db import Base, engine
from backend_fastapi.app.routes import api
from backend_fastapi.app.log import setup_logger
import logging

app = FastAPI(
    title="用户认证API",
    description="一个基于FastAPI和Vue.js的前后端分离项目",
    version="1.0.0"
)

# 设置日志
logger = setup_logger(app)

# CORS 中间件配置
origins = [
    # "http://localhost:5173",
    # "http://localhost:5174", 
    # "http://127.0.0.1:5173",
    # "http://127.0.0.1:5174",
    "http://localhost:8001",
    "http://127.0.0.1:8001",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
    expose_headers=["Content-Type"]
)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# --------------    路由注册--------------
# 注册用户认证路由
app.include_router(user.router)
# API管理路由
app.include_router(api.router)