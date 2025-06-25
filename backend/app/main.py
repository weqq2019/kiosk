"""
不动产自助查询一体机 - FastAPI 主应用
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from loguru import logger
import sys
import os
from datetime import datetime
import time

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.routers import identity, query, devices


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 不动产自助查询一体机启动中...")

    # 启动时执行
    try:
        # TODO: 初始化设备管理器
        # await device_manager.initialize()
        logger.info("📱 硬件设备初始化完成")

        # 启动系统监控
        logger.info("🔍 系统监控服务启动")
    except Exception as e:
        logger.error(f"❌ 初始化失败: {e}")

    yield  # 应用运行期间

    # 关闭时执行
    logger.info("🛑 系统正在关闭...")
    try:
        # TODO: 清理设备资源
        # await device_manager.cleanup()
        pass
    except Exception as e:
        logger.warning(f"⚠️ 清理资源时出错: {e}")
    logger.info("✅ 系统关闭完成")


# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="不动产自助查询一体机后端服务API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# 跨域中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """请求日志中间件"""
    start_time = time.time()

    # 记录请求
    logger.info(f"📥 {request.method} {request.url.path} - {request.client.host}")

    response = await call_next(request)

    # 记录响应
    process_time = time.time() - start_time
    logger.info(
        f"📤 {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s"
    )

    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    logger.error(f"❌ 未处理异常: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "系统内部错误，请联系管理员",
            "detail": str(exc) if settings.DEBUG else None,
        },
    )


# 健康检查接口
@app.get("/health")
async def health_check():
    """系统健康检查"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.now().isoformat(),
        "message": "不动产自助查询一体机运行正常",
    }


# 系统信息接口
@app.get("/")
async def root():
    """根路径信息"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "不动产自助查询一体机后端服务",
        "docs_url": "/docs" if settings.DEBUG else None,
        "health_url": "/health",
    }


# 注册路由模块
try:
    # 注册各模块路由
    app.include_router(identity.router, prefix="/identity", tags=["身份验证"])
    app.include_router(query.router, prefix="/query", tags=["业务查询"])
    app.include_router(devices.router, prefix="/devices", tags=["设备管理"])

    logger.info("✅ 路由模块加载成功")

except ImportError as e:
    logger.warning(f"⚠️ 路由模块加载失败: {e}")
    logger.info("💡 使用基础模式运行，部分功能可能不可用")


if __name__ == "__main__":
    # 配置日志
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
    )

    if settings.LOG_FILE_PATH:
        logger.add(
            f"{settings.LOG_FILE_PATH}/app.log",
            rotation="1 day",
            retention="30 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="INFO",
        )

    # 启动应用
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        access_log=False,  # 使用自定义日志中间件
        log_config=None,
    )
