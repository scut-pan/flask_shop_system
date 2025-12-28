# Flask 购物网站系统

基于 Flask + MySQL 的在线购物网站课程作业项目。

---

## 学生信息

- **学号**: 202330451431
- **姓名**: 潘兆斌

## 技术栈

- **后端框架**: Flask
- **数据库**: MySQL
- **ORM**: Flask-SQLAlchemy
- **用户认证**: Flask-Login
- **前端**: Bootstrap 5
- **包管理**: uv

## 主要功能

### 顾客功能
- 用户注册、登录、注销
- 商品浏览与搜索
- 购物车管理
- 订单创建与支付
- 订单历史查询
- 邮件确认发货

### 管理员功能
- 商品目录管理(增删改)
- 订单管理与发货
- 销售统计报表

## 快速开始

### Docker 部署(推荐)

```bash
# 1. 配置环境变量
cp .env.production .env
nano .env  # 修改 SECRET_KEY、数据库密码、邮箱配置

# 2. 一键部署
bash deploy.sh prod

# 访问应用
# HTTP: http://localhost 或 http://your-server-ip
```

### 本地开发

```bash
# 1. 安装依赖
pip install uv
uv sync

# 2. 配置环境变量
cp .env.example .env.local
nano .env.local  # 填入数据库等配置

# 3. 创建数据库
mysql -u root -p
CREATE DATABASE shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'shop_user'@'localhost' IDENTIFIED BY 'your-password';
GRANT ALL PRIVILEGES ON shop_db.* TO 'shop_user'@'localhost';
FLUSH PRIVILEGES;

# 4. 初始化并运行
uv run flask db upgrade
uv run python main.py

# 访问 http://localhost:5000
```

## 源代码文件说明

### 核心应用文件
- **`app/__init__.py`** - 应用工厂函数,初始化 Flask 应用和数据库
- **`app/extensions.py`** - Flask 扩展实例化(SQLAlchemy、Login、Mail)
- **`app/forms.py`** - WTForms 表单类定义
- **`config.py`** - 应用配置文件
- **`main.py`** - 应用入口文件

### 数据模型层 (`app/models/`)
- **`user.py`** - 用户模型(普通用户和管理员)
- **`product.py`** - 商品模型(商品信息、分类、库存)
- **`cart.py`** - 购物车模型
- **`order.py`** - 订单模型(订单、订单项、状态)

### 路由控制层 (`app/routes/`)
- **`main.py`** - 主页路由
- **`auth.py`** - 用户认证(注册、登录、注销)
- **`product.py`** - 商品展示与搜索
- **`cart.py`** - 购物车操作
- **`order.py`** - 订单创建、支付、历史查询
- **`admin.py`** - 管理员后台(商品、订单、统计)

### 视图模板 (`app/templates/`)
- **`base.html`** - 基础模板
- **`auth/`** - 登录注册页面
- **`products/`** - 商品列表和详情
- **`cart/`** - 购物车页面
- **`orders/`** - 订单相关页面
- **`admin/`** - 管理员后台页面

### 配置文件
- **`pyproject.toml`** - 项目依赖配置
- **`Dockerfile`** - Docker 镜像构建文件
- **`docker-compose.yml`** - Docker Compose 编排配置
- **`gunicorn_config.py`** - Gunicorn 服务器配置
- **`deploy.sh`** - 一键部署脚本

### 其他目录
- **`migrations/`** - 数据库迁移文件
- **`tests/`** - 单元测试
- **`docs/`** - 项目文档
- **`nginx/`** - Nginx 配置

## 测试账户

管理员账户:
- 用户名: `admin`
- 密码: `admin123`

## 项目结构

```
flask_shop_system/
├── app/                        # 应用主目录
│   ├── models/                 # 数据模型
│   ├── routes/                 # 路由控制
│   ├── templates/              # 视图模板
│   ├── static/                 # 静态资源
│   └── utils/                  # 工具函数
├── migrations/                 # 数据库迁移
├── tests/                      # 测试文件
├── docs/                       # 项目文档
├── nginx/                      # Nginx 配置
├── config.py                   # 配置文件
├── main.py                     # 入口文件
├── docker-compose.yml          # Docker 编排
└── README.md                   # 项目说明
```

## 开发文档

- [Docker 部署指南](docs/Docker部署指南.md)
- [项目概述](docs/project_overview.md)
- [配置说明](docs/configuration_guide.md)
