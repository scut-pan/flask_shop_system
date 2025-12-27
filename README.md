# Flask 购物网站系统

基于 Flask + MySQL 的在线购物网站课程作业项目。

## 技术栈

- **后端框架**：Flask
- **数据库**：MySQL
- **ORM**：Flask-SQLAlchemy
- **用户认证**：Flask-Login
- **前端框架**：Bootstrap 5
- **包管理**：uv

## 快速开始

### 方式一：Docker 部署（推荐）

使用 Docker Compose 可以快速部署整个应用栈（包括 MySQL、Nginx）：

#### 1. 安装 Docker 和 Docker Compose

参考 [Docker 部署指南](docs/Docker部署指南.md#安装-docker-和-docker-compose)

#### 2. 配置环境变量

```bash
# 复制生产环境配置模板
cp .env.production .env

# 生成 SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# 编辑 .env 文件，设置必要的配置项
nano .env
```

必须修改的配置项：
- `SECRET_KEY`: Flask 密钥（使用上面的命令生成）
- `MYSQL_ROOT_PASSWORD`: MySQL root 密码
- `MYSQL_PASSWORD`: 应用数据库密码
- `MAIL_USERNAME`: 邮箱地址
- `MAIL_PASSWORD`: 邮箱授权码

#### 3. 一键部署

```bash
# 使用部署脚本（推荐）
chmod +x deploy.sh
bash deploy.sh prod

# 或手动部署
docker compose up -d --build
docker compose exec web flask db upgrade
```

#### 4. 访问应用

- HTTP: `http://localhost` 或 `http://your-server-ip`
- HTTPS: `https://your-domain.com`（需要配置 SSL 证书）

详细部署说明请查看 [Docker 部署指南](docs/Docker部署指南.md)

---

### 方式二：本地开发环境

#### 1. 克隆项目

```bash
git clone <your-repo-url>
cd flask_shop_system
```

#### 2. 安装依赖

使用 uv 包管理器（推荐）：

```bash
# 安装 uv（如果还没安装）
pip install uv

# 安装项目依赖
uv sync
```

#### 3. 配置环境变量

**重要**：创建 `.env.local` 文件存储敏感配置（该文件已在 `.gitignore` 中，不会被提交）：

```bash
# 复制本地开发配置模板
cp .env.example .env.local

# 编辑 .env.local 文件，填入真实配置
nano .env.local
```

`.env.local` 文件内容示例：

```env
SECRET_KEY=your-secret-key-here
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=shop_user
MYSQL_PASSWORD=your-database-password
MYSQL_DB=shop_db
MYSQL_CHARSET=utf8mb4
FLASK_ENV=development
FLASK_DEBUG=1
```

#### 4. 创建数据库

登录 MySQL 并创建数据库：

```sql
mysql -u root -p

CREATE DATABASE shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'shop_user'@'localhost' IDENTIFIED BY 'your-password';
GRANT ALL PRIVILEGES ON shop_db.* TO 'shop_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**注意**：将 `.env` 文件中的 `MYSQL_PASSWORD` 设置为这里创建的密码。

#### 5. 初始化数据库

```bash
# 使用 uv 运行 Flask 命令
uv run flask db upgrade
```

#### 6. 运行项目

```bash
uv run python main.py
```

访问 http://localhost:5000

## 项目结构

```
flask_shop_system/
├── app/                        # 应用主目录
│   ├── __init__.py            # 应用工厂函数与初始化
│   ├── extensions.py          # Flask扩展实例化
│   ├── forms.py               # WTForms表单定义
│   ├── models/                # 数据模型层
│   │   ├── __init__.py
│   │   ├── user.py           # 用户模型
│   │   ├── product.py        # 商品模型
│   │   ├── cart.py           # 购物车模型
│   │   └── order.py          # 订单模型
│   ├── routes/                # 路由控制层
│   │   ├── __init__.py
│   │   ├── main.py           # 主页路由
│   │   ├── auth.py           # 用户认证路由
│   │   ├── product.py        # 商品路由
│   │   ├── cart.py           # 购物车路由
│   │   ├── order.py          # 订单路由
│   │   └── admin.py          # 管理员路由
│   ├── templates/             # Jinja2模板
│   │   ├── base.html         # 基础模板
│   │   ├── auth/             # 认证相关模板
│   │   ├── products/         # 商品相关模板
│   │   ├── cart/             # 购物车模板
│   │   ├── orders/           # 订单模板
│   │   └── admin/            # 管理员模板
│   ├── static/                # 静态资源
│   │   ├── css/              # 样式文件
│   │   ├── js/               # JavaScript文件
│   │   ├── img/              # 图片资源
│   │   └── images/uploads/   # 用户上传的图片
│   └── utils/                 # 工具函数
│       ├── __init__.py
│       ├── decorators.py     # 自定义装饰器
│       └── helpers.py        # 辅助函数
├── tests/                     # 测试目录
│   ├── __init__.py
│   ├── test_models.py        # 模型测试
│   ├── test_routes.py        # 路由测试
│   └── test_utils.py         # 工具函数测试
├── docs/                      # 项目文档
│   ├── project_overview.md   # 项目概述
│   ├── configuration_guide.md # 配置指南
│   ├── Docker部署指南.md      # Docker部署详细文档
│   ├── Flask购物网站开发分步实施指南.md
│   ├── 订单系统实施总结.md
│   └── Flask购物网站功能测试指南.md
├── nginx/                     # Nginx配置文件
│   ├── nginx.conf            # Nginx主配置
│   ├── conf.d/               # 站点配置
│   ├── ssl/                  # SSL证书目录
│   └── logs/                 # Nginx日志
├── migrations/                # 数据库迁移文件
├── .env.production            # 生产环境配置模板
├── .gitignore                 # Git忽略规则
├── .dockerignore              # Docker构建忽略规则
├── .python-version            # Python版本配置
├── pyproject.toml             # 项目依赖配置
├── uv.lock                    # 依赖锁定文件
├── config.py                  # 应用配置文件
├── init_db.py                 # 数据库初始化脚本
├── main.py                    # 应用入口文件
├── deploy.sh                  # 一键部署脚本
├── docker-compose.yml         # Docker Compose配置
├── Dockerfile                 # 应用镜像构建文件
├── gunicorn_config.py         # Gunicorn WSGI服务器配置
├── CLAUDE.md                  # AI助手开发规则
└── README.md                  # 项目说明文档
```

## 主要功能

- ✅ 用户注册与登录
- ✅ 个人资料管理
- ✅ 修改密码
- ✅ 注销账号
- ✅ 商品展示与搜索
- ✅ 购物车管理
- ✅ 订单系统
- ✅ 管理员后台

## Docker 部署说明

### 快速部署

```bash
# 1. 配置环境变量
cp .env.production .env
nano .env  # 修改必要的配置项

# 2. 一键部署
chmod +x deploy.sh
bash deploy.sh prod
```

### 常用命令

```bash
# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f

# 停止服务
docker compose stop

# 重启服务
docker compose restart

# 更新应用
git pull
docker compose up -d --build
```

### 访问应用

- HTTP: `http://localhost` 或 `http://your-server-ip`
- HTTPS: `https://your-domain.com`（需要配置 SSL）

### 测试账户

部署后可使用的管理员账户:
- 用户名: `admin`
- 密码: `Admin@123`

⚠️ **请在生产环境中立即修改默认密码！**

详细部署文档请查看: [Docker 部署指南](docs/Docker部署指南.md)

## 开发文档

详细开发指南请查看：
- [Docker 部署指南](docs/Docker部署指南.md)
- [项目概述](docs/project_overview.md)
- [配置说明](docs/configuration_guide.md)

## 安全提示

⚠️ **重要**：
- `.env` 文件包含敏感信息，已在 `.gitignore` 中配置，不会被提交到 Git
- 提交代码前，请确认 `git status` 中没有出现 `.env` 文件
- 不要在代码中硬编码密码或密钥

## 常见问题

### Q: MySQL 命令不可用？

如果提示 `'mysql' 不是内部或外部命令`，需要将 MySQL 添加到系统环境变量。详细步骤请参考 [开发指南](docs/development_guide.md#步骤-11安装必要软件)。

### Q: 数据库连接失败？

检查 `.env` 文件中的配置是否正确，特别是：
- MySQL 服务是否已启动
- 用户名和密码是否正确
- 数据库是否已创建

## 许可证

MIT License
