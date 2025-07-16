from fastapi import APIRouter
from ..api import EnvironmentalManagement as env_vars_router  # 导入环境变量管理路由
from ..api import GroupManagement as group_router  # 导入API分组管理路由
from ..api import InterfaceManagement as io_router  # 导入接口管理路由

router = APIRouter(prefix="/api", tags=["API管理"])

router.include_router(env_vars_router.router)  # 注册环境变量管理路由
router.include_router(group_router.router)  # 注册API分组管理路由
router.include_router(io_router.router)  # 注册接口管理路由


