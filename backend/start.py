#!/usr/bin/env python3
"""
不动产自助查询一体机 - 启动脚本
"""
import os
import sys
import asyncio
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))


def check_dependencies():
    """检查依赖包是否安装"""
    required_packages = ["fastapi", "uvicorn", "pydantic", "loguru"]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ 缺少以下依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False

    return True


def create_directories():
    """创建必要的目录"""
    directories = ["data", "logs", "temp", "output", "backup"]

    for dir_name in directories:
        dir_path = current_dir / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"📁 创建目录: {dir_path}")


def main():
    """主启动函数"""
    print("🚀 不动产自助查询一体机启动中...")

    # 检查依赖
    if not check_dependencies():
        sys.exit(1)

    # 创建必要目录
    create_directories()

    # 设置环境变量
    os.environ.setdefault("PYTHONPATH", str(current_dir))

    try:
        # 导入应用
        from app.main import app
        import uvicorn

        print("✅ 依赖检查通过")
        print("🔧 正在启动服务...")

        # 启动服务
        uvicorn.run(
            "app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
        )

    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("请检查项目结构和依赖包安装")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
