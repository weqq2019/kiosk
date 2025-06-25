# 不动产自助查询一体机

## 项目简介

不动产自助查询一体机是一个集成身份验证、信息查询、文档打印和电子盖章功能的政务服务终端设备软件系统。

## 技术架构

- **前端**: Vue3 + Electron + TypeScript
- **后端**: FastAPI + Python 3.11.0
- **数据库**: MySQL 8.0 + Redis
- **硬件**: 7类专业设备集成

## 硬件清单

1. **主机**: 新华三 H3C X500ZG2（兆芯CPU + 银河麒麟V10）
2. **身份证读卡器**: 新中新 F200
3. **双目摄像头**: 健德源 JDY-K2002R
4. **激光打印机**: 惠普 HP454DW
5. **盖章机**: 汉威信 GZ820
6. **二维码扫描仪**: 新大陆 NLS-FM25-EX
7. **UPS电源**: 山特 MT-500Pro
8. **补光灯**: LED红色高亮灯

## 核心功能

### 1. 身份验证
- 身份证真伪验证
- 人脸识别比对
- 人证一致性验证

### 2. 业务查询
- 有房无房查询
- 产权详情查询
- 登记进度查询

### 3. 文档处理
- PDF/WPS文档生成
- 自动打印
- 电子盖章

### 4. 系统管理
- 设备状态监控
- 操作日志记录
- 故障自动处理

## 安全特性

- RSA/SM2双重加密
- 数据脱敏处理
- 操作全程审计
- 临时数据自动清理

## 项目结构

```
不动产自助查询一体机/
├── backend/                 # 后端服务
│   ├── app/                # 应用主体
│   │   ├── routers/       # 路由模块（身份验证、查询、设备）
│   │   ├── services/      # 业务服务逻辑
│   │   ├── models/        # 数据模型
│   │   ├── utils/         # 工具函数
│   │   ├── core/          # 核心配置
│   │   └── main.py        # 应用入口
│   ├── tests/             # 测试用例
│   ├── requirements.txt   # Python依赖
│   └── start.py           # 启动脚本
├── frontend/               # 前端应用（Vue3 + Electron）
│   ├── src/               # 源代码
│   ├── public/            # 静态资源
│   └── package.json       # Node.js依赖
├── mock/                   # 模拟设备响应（开发调试）
├── docs/                   # 项目文档
│   ├── api.md             # API接口文档
│   ├── deployment.md      # 部署指南
│   └── hardware.md        # 硬件配置说明
└── hardware/              # 硬件驱动和SDK
    ├── drivers/           # 设备驱动
    └── sdk/               # SDK文件
```

## 快速开始

### 环境要求

- Python 3.11.0+
- Node.js 22.15.0+
- Docker & Docker Compose
- MySQL 8.0+
- Redis 7+

### 1. 克隆项目

```bash
git clone <repository-url>
cd 不动产自助查询一体机
```

### 2. 数据库环境搭建

#### 使用 Docker 快速启动（推荐）

```bash
# Linux/macOS
./scripts/start-database.sh dev

# Windows PowerShell
.\scripts\start-database.ps1 dev

# 或启动生产环境
./scripts/start-database.sh prod    # Linux/macOS
.\scripts\start-database.ps1 prod   # Windows
```

#### 手动启动 Docker

```bash
# 开发环境（包含 phpMyAdmin）
docker-compose --profile dev up -d

# 生产环境
docker-compose up -d mysql redis
```

#### 数据库连接信息

- **MySQL 数据库**: localhost:3306
- **数据库名**: real_estate_kiosk
- **用户名**: kiosk_user
- **密码**: kiosk_password
- **Root密码**: root_password_123
- **phpMyAdmin**: http://localhost:8080 （仅开发环境）

#### Redis 连接信息

- **Redis 服务**: localhost:6379
- **密码**: redis_password_123

### 3. 后端环境配置

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量配置
cp ../env.example .env
# 根据需要修改 .env 文件中的配置

# 启动后端服务
python start.py
```

### 4. 前端环境配置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 启动 Electron 应用
npm run electron:dev
```

### 5. 验证安装

- 后端 API 文档: http://localhost:8000/docs
- 前端开发服务器: http://localhost:5173
- 数据库管理: http://localhost:8080 （开发环境）

## 开发指南

### 项目结构

```
不动产自助查询一体机/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── routers/        # API 路由
│   │   ├── services/       # 业务服务
│   │   ├── models/         # 数据模型
│   │   ├── utils/          # 工具函数
│   │   └── core/           # 核心配置
│   ├── requirements.txt    # Python 依赖
│   └── start.py           # 启动脚本
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/    # Vue 组件
│   │   ├── views/         # 页面视图
│   │   └── stores/        # 状态管理
│   ├── electron/          # Electron 主进程
│   └── package.json       # Node.js 依赖
├── database/              # 数据库配置
│   ├── init/             # 初始化脚本
│   └── conf/             # MySQL 配置
├── hardware/              # 硬件驱动
├── scripts/               # 部署脚本
├── docker-compose.yml     # Docker 配置
└── env.example           # 环境变量示例
```

### 数据库管理

#### 常用命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f mysql

# 进入数据库
docker-compose exec mysql mysql -u kiosk_user -p real_estate_kiosk

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 清理数据（谨慎使用）
docker-compose down -v
```

#### 数据库结构

主要数据表：
- `user_operations` - 用户操作记录
- `device_status` - 设备状态
- `query_records` - 查询记录
- `print_records` - 打印记录
- `system_logs` - 系统日志
- `system_config` - 系统配置

### 开发模式

#### 模拟设备模式

在开发环境中，可以启用模拟设备模式：

```bash
# 在 .env 文件中设置
MOCK_DEVICES=true
MOCK_GOVERNMENT_API=true
```

#### API 调试

- Swagger 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

### 硬件集成

硬件驱动位于 `hardware/` 目录：

```
hardware/
├── drivers/              # 设备驱动
│   ├── camera/          # 摄像头驱动
│   ├── id_card_reader/  # 身份证读卡器
│   ├── printer/         # 打印机驱动
│   └── ...
└── sdk/                 # 厂商 SDK
    ├── arcsoft/         # 虹软人脸识别
    ├── xinzhongxin/     # 新中新身份证读卡器
    └── ...
```

## 部署指南

### 生产环境部署

1. **环境准备**
   ```bash
   # 安装 Docker
   curl -fsSL https://get.docker.com | sh
   
   # 启动数据库服务
   ./scripts/start-database.sh prod
   ```

2. **后端部署**
   ```bash
   cd backend
   pip install -r requirements.txt
   python start.py
   ```

3. **前端打包**
   ```bash
   cd frontend
   npm run build
   npm run electron:build
   ```

### 系统配置

主要配置文件：
- `backend/app/core/config.py` - 后端配置
- `frontend/vite.config.ts` - 前端构建配置
- `docker-compose.yml` - 数据库服务配置
- `.env` - 环境变量配置

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查 Docker 服务是否启动
   - 确认端口 3306 未被占用
   - 验证数据库连接配置

2. **硬件设备无法识别**
   - 检查设备驱动是否正确安装
   - 确认设备权限配置
   - 查看设备状态日志

3. **前端页面无法加载**
   - 检查 Node.js 版本是否正确
   - 清除 npm 缓存：`npm cache clean --force`
   - 重新安装依赖：`rm -rf node_modules && npm install`

### 日志查看

```bash
# 应用日志
tail -f /var/log/kiosk/app.log

# 数据库日志
docker-compose logs -f mysql

# 系统日志
journalctl -u kiosk-service -f
```

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目为商业项目，版权所有。

## 联系方式

- 项目经理: 刘泉
- 邮箱: 1515817@qq.com
- 项目状态: 开发中

---

**注意**: 本项目包含敏感的政务数据处理功能，请确保在合规的环境中使用。 