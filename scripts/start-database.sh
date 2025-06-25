#!/bin/bash

# 不动产自助查询一体机 - 数据库启动脚本
# 使用方法: ./scripts/start-database.sh [dev|prod]

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 切换到项目根目录
cd "$PROJECT_ROOT"

# 检查参数
MODE=${1:-dev}

echo "🚀 启动不动产自助查询一体机数据库服务..."
echo "📁 项目目录: $PROJECT_ROOT"
echo "🔧 运行模式: $MODE"

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ 错误: Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 创建必要的目录
echo "📂 创建必要的目录..."
mkdir -p database/init
mkdir -p database/conf
mkdir -p logs
mkdir -p data

# 检查配置文件
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ 错误: docker-compose.yml 文件不存在"
    exit 1
fi

# 根据模式启动服务
if [ "$MODE" = "dev" ]; then
    echo "🔧 启动开发环境数据库服务（包含 phpMyAdmin）..."
    docker-compose --profile dev up -d
    
    echo ""
    echo "✅ 开发环境数据库服务启动成功！"
    echo ""
    echo "📊 服务信息:"
    echo "   MySQL 数据库: localhost:3306"
    echo "   phpMyAdmin:   http://localhost:8080"
    echo "   Redis 缓存:   localhost:6379"
    echo ""
    echo "🔑 数据库连接信息:"
    echo "   数据库名: real_estate_kiosk"
    echo "   用户名:   kiosk_user"
    echo "   密码:     kiosk_password"
    echo "   Root密码: root_password_123"
    echo ""
    echo "🔑 Redis连接信息:"
    echo "   密码:     redis_password_123"
    
elif [ "$MODE" = "prod" ]; then
    echo "🚀 启动生产环境数据库服务..."
    docker-compose up -d mysql redis
    
    echo ""
    echo "✅ 生产环境数据库服务启动成功！"
    echo ""
    echo "📊 服务信息:"
    echo "   MySQL 数据库: localhost:3306"
    echo "   Redis 缓存:   localhost:6379"
    
else
    echo "❌ 错误: 无效的运行模式 '$MODE'，请使用 'dev' 或 'prod'"
    exit 1
fi

echo ""
echo "🔍 检查服务状态..."
docker-compose ps

echo ""
echo "📋 常用命令:"
echo "   查看日志:     docker-compose logs -f"
echo "   停止服务:     docker-compose down"
echo "   重启服务:     docker-compose restart"
echo "   进入数据库:   docker-compose exec mysql mysql -u kiosk_user -p real_estate_kiosk"
echo ""
echo "🎉 数据库服务启动完成！" 