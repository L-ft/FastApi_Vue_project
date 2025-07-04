from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend_fastapi.app.routes import user
from backend_fastapi.app.db import Base, engine
from backend_fastapi.app.routes import api

app = FastAPI(
    title="用户认证API",
)

# CORS 中间件配置
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
# --------------    路由注册--------------
# 注册用户认证路由
app.include_router(user.router)
# API管理路由
app.include_router(api.router)

