# 配置文件说明

## 文件说明

### 配置模板文件(✅ 可提交到 Git)

#### .env.example
- **作用**: 本地开发环境变量配置模板
- **内容**: 展示本地开发需要配置哪些环境变量
- **用途**: 用于创建本地开发的 `.env.local` 文件

#### .env.production
- **作用**: Docker 生产环境配置模板
- **内容**: 包含 Docker 部署所需的完整配置
- **用途**: 用于创建 Docker 部署的 `.env` 文件

### 实际配置文件(❌ 不可提交到 Git)

#### .env
- **作用**: Docker 部署的实际环境变量配置文件
- **内容**: 包含 Docker 环境的真实数据库密码等敏感信息
- **配置**: `MYSQL_HOST=mysql` (Docker 容器名称)
- **安全性**: 已在 `.gitignore` 中，不会被提交

#### .env.local
- **作用**: 本地开发的实际环境变量配置文件
- **内容**: 包含本地开发的真实数据库密码等敏感信息
- **配置**: `MYSQL_HOST=localhost` (本地数据库)
- **安全性**: 已在 `.gitignore` 中，不会被提交

## 使用步骤

### 方式一: 本地开发

#### 1. 创建 .env.local 文件

```bash
cp .env.example .env.local
```

#### 2. 编辑 .env.local 文件，填入真实配置

```env
# Flask 安全密钥
SECRET_KEY=your-secret-key-here

# MySQL 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=shop_user
MYSQL_PASSWORD=your-database-password
MYSQL_DB=shop_db
MYSQL_CHARSET=utf8mb4

# 环境标识
FLASK_ENV=development
FLASK_DEBUG=1
```

#### 3. 运行应用

```bash
# 应用会自动优先加载 .env.local
uv run python main.py
```

### 方式二: Docker 部署

#### 1. 创建 .env 文件

```bash
cp .env.production .env
```

#### 2. 编辑 .env 文件，填入真实配置

```env
# Flask 安全密钥
SECRET_KEY=your-secret-key-here

# MySQL 数据库配置
MYSQL_ROOT_PASSWORD=Root@123456
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_USER=shop_user
MYSQL_PASSWORD=Shop@2025
MYSQL_DB=shop_db
MYSQL_CHARSET=utf8mb4

# 环境标识
FLASK_ENV=production
FLASK_DEBUG=0
```

#### 3. 启动 Docker 服务

```bash
docker compose up -d --build
```

## 配置加载逻辑

应用启动时会按以下优先级加载配置:

1. **优先加载** `.env.local` (如果存在) - 用于本地开发
2. **否则加载** `.env` (如果存在) - 用于 Docker 部署
3. 两者都存在时,`.env.local` 会覆盖 `.env` 的配置

代码实现见 `app/__init__.py`:
```python
from dotenv import load_dotenv
from pathlib import Path

# 优先加载 .env.local (本地开发)
env_path = Path(__file__).parent.parent / '.env.local'
load_dotenv(env_path, override=True)
# 如果 .env.local 不存在,加载 .env (Docker部署)
load_dotenv()
```

## 安全检查清单

### 提交代码前，务必确认：

- [ ] `.gitignore` 文件中已包含 `.env` 和 `.env.local`
- [ ] `.env` 和 `.env.local` 文件不存在于 Git 仓库中
- [ ] 代码中不要硬编码真实密码
- [ ] 只有 `.env.example` 和 `.env.production` 被提交

### 检查命令：

```bash
# 检查哪些文件会被 Git 跟踪
git status

# 检查 .gitignore 是否生效
git check-ignore -v .env
git check-ignore -v .env.local

# 应该输出类似：
# .gitignore:19:.env    .env
# .gitignore:20:.env.local    .env.local
```

## 常见问题

### Q: 如果不小心提交了 .env 怎么办？

1. **立即更改密码**
2. **从 Git 历史中移除**（如果是课程作业，重新创建数据库即可）
3. **将 .env 添加到 .gitignore**

### Q: 如何验证 .env 不会被提交？

```bash
# 测试 gitignore 规则
git check-ignore -v .env
git check-ignore -v .env.local

# 查看会被提交的文件
git ls-files | grep "\.env"
```

### Q: 本地开发和 Docker 部署如何切换？

- **本地开发**: 使用 `.env.local` (从 `.env.example` 复制)
- **Docker 部署**: 使用 `.env` (从 `.env.production` 复制)
- **两者可以共存**: 应用会优先加载 `.env.local`
