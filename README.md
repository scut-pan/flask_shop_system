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

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd flask_shop_system
```

### 2. 安装依赖

使用 uv 包管理器（推荐）：

```bash
# 安装 uv（如果还没安装）
pip install uv

# 安装项目依赖
uv sync
```

### 3. 配置环境变量

**重要**：创建 `.env` 文件存储敏感配置（该文件已在 `.gitignore` 中，不会被提交）：

```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件，填入真实配置
```

`.env` 文件内容示例：

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

### 4. 创建数据库

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

### 5. 初始化数据库

```bash
# 使用 uv 运行 Flask 命令
uv run flask init-db
```

### 6. 运行项目

```bash
uv run python main.py
```

访问 http://localhost:5000

## 项目结构

```
flask_shop_system/
├── app/
│   ├── models/         # 数据模型
│   ├── routes/         # 路由蓝图
│   ├── templates/      # HTML 模板
│   ├── static/         # 静态文件
│   └── utils/          # 工具函数
├── docs/               # 项目文档
├── .env.example        # 环境变量示例
├── .gitignore          # Git 忽略文件
└── pyproject.toml      # 项目配置
```

## 主要功能

- ✅ 用户注册与登录
- ✅ 商品展示与搜索
- ✅ 购物车管理
- ✅ 订单系统
- ✅ 管理员后台

## 开发文档

详细开发指南请查看：
- [开发指南](docs/development_guide.md)
- [配置说明](docs/configuration_guide.md)
- [项目概述](docs/project_overview.md)

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
