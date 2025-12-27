# Flask 商城系统 Docker 部署指南

## 目录

- [部署架构](#部署架构)
- [前置要求](#前置要求)
- [本地部署测试](#本地部署测试)
- [云服务器部署](#云服务器部署)
- [常用运维命令](#常用运维命令)
- [故障排查](#故障排查)
- [安全建议](#安全建议)

---

## 部署架构

本项目采用 Docker 容器化部署方案,包含以下服务:

```
┌─────────────────────────────────────────────────────┐
│                   Nginx (反向代理)                    │
│              端口: 80 (HTTP), 443 (HTTPS)            │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│              Flask Web 应用                           │
│              端口: 5000                              │
│              Gunicorn WSGI 服务器                    │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│              MySQL 8.0 数据库                        │
│              端口: 3306                              │
└─────────────────────────────────────────────────────┘
```

### 服务说明

- **Nginx**: 反向代理服务器,处理静态文件和负载均衡
- **Flask Web**: 核心应用,使用 Gunicorn 作为 WSGI 服务器
- **MySQL**: 数据库服务,存储应用数据

---

## 前置要求

### 1. 本地环境

- Docker Engine 20.10+
- Docker Compose 2.0+

### 2. 云服务器要求

推荐配置:
- **CPU**: 2 核心或以上
- **内存**: 4GB 或以上
- **存储**: 40GB 或以上
- **操作系统**: Ubuntu 20.04/22.04 或 CentOS 7/8

### 3. 安装 Docker 和 Docker Compose

#### Ubuntu/Debian

```bash
# 更新包索引
sudo apt-get update

# 安装依赖
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# 添加 Docker 官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 添加 Docker 仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 验证安装
docker --version
docker compose version
```

#### CentOS/RHEL

```bash
# 安装依赖
sudo yum install -y yum-utils

# 添加 Docker 仓库
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装 Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 验证安装
docker --version
docker compose version
```

#### Windows 11

**安装 Docker Desktop:**

1. 访问 [Docker Desktop 官网](https://www.docker.com/products/docker-desktop/) 下载 Windows 版本
2. 运行安装程序,安装时确保启用 **WSL 2 后端**
3. 安装完成后重启计算机
4. 启动 Docker Desktop,等待 Docker 引擎启动完成
5. 验证安装:

```powershell
# 打开 PowerShell 或 Windows Terminal
docker --version
docker compose version
```

**注意事项:**
- Windows 11 需要 WSL 2 支持,确保系统已启用虚拟化
- 首次运行 Docker Desktop 可能需要管理员权限
- 建议分配至少 4GB 内存给 Docker Desktop

---

## 本地部署测试

### Windows 11 本地部署测试步骤

#### 步骤 1: 准备配置文件

```powershell
# 在项目根目录打开 PowerShell
# 复制生产环境配置模板为 .env(如果本地已有 .env,请先备份为 .env.local)
cp .env.production .env

# 使用记事本编辑 .env 文件
notepad .env
```

**必须修改的配置项:**

```bash
# 生成强密钥 (见步骤 2)
SECRET_KEY=你生成的密钥

# MySQL 配置
MYSQL_ROOT_PASSWORD=设置root密码(例如: Root@123456)
MYSQL_PASSWORD=设置数据库密码(例如: Shop@2025)

# 邮件配置 (可选,测试阶段可以先不配置)
MAIL_USERNAME=你的邮箱@qq.com
MAIL_PASSWORD=邮箱授权码
```

**⚠️ 注意事项:**
- `.env` 文件会被 git 忽略,不会提交到仓库
- `.env.production` 是配置模板,包含了 Docker 部署所需的所有配置
- `.env` 中的 `MYSQL_HOST=mysql` 专用于 Docker 环境
- **本地开发**请使用 `.env.local` 文件(从 `.env.example` 复制,`MYSQL_HOST=localhost`)
- 如果之前有本地开发的 `.env` 文件,请先将其重命名为 `.env.local` 保存

#### 步骤 2: 生成 SECRET_KEY

```powershell
# 运行 Python 生成随机密钥
python -c "import secrets; print(secrets.token_hex(32))"
```

将生成的密钥(类似 `a1b2c3d4e5f6...` 这样的64位十六进制字符串)复制到 `.env` 文件的 `SECRET_KEY` 中。

#### 步骤 3: 创建必要的目录

```powershell
# 创建所有需要的目录
mkdir nginx\ssl
mkdir nginx\logs
mkdir logs
mkdir app\static\images\uploads
```

#### 步骤 4: 启动所有服务

```powershell
# 构建镜像并启动所有服务(首次运行会下载镜像,需要几分钟)
docker compose up -d --build

# 查看服务状态
docker compose ps

# 查看日志(可选)
docker compose logs -f
```

**预期输出:**
- 3 个容器都在运行: `flask_shop_mysql`, `flask_shop_web`, `flask_shop_nginx`
- 状态显示为 `Up` 或 `healthy`

#### 步骤 5: 初始化数据库

**⚠️ 重要提示:**
- 确保 `migrations` 目录存在并已提交到 Git 仓库
- 如果 `migrations` 目录不存在,需要在本地先运行 `flask db init` 和 `flask db migrate`
- 详见"故障排查 > 问题 6: 迁移文件缺失"

```powershell
# 等待 MySQL 完全启动后(约 30 秒),运行数据库迁移
docker compose exec web uv run flask db upgrade

# 创建管理员账户
docker compose exec web uv run python -c "from app.extensions import db; from app.models import User; from werkzeug.security import generate_password_hash; admin = User(username='admin', email='admin@example.com', password_hash=generate_password_hash('Admin@123'), is_admin=True); db.session.add(admin); db.session.commit(); print('管理员账户创建成功!')"
```

**预期输出:**
```
管理员账户创建成功!
用户名: admin
密码: Admin@123
```

#### 步骤 6: 访问应用

打开浏览器访问: **http://localhost**

使用以下账户登录:
- 用户名: `admin`
- 密码: `Admin@123`

#### 常用命令

```powershell
# 查看所有服务状态
docker compose ps

# 查看日志
docker compose logs -f

# 停止所有服务
docker compose stop

# 启动所有服务
docker compose start

# 重启所有服务
docker compose restart

# 停止并删除所有服务
docker compose down

# 停止并删除所有服务及数据(⚠️ 会删除数据库数据)
docker compose down -v
```

---

### Linux/macOS 本地部署测试步骤

#### 步骤 1: 准备配置文件

```bash
# 复制生产环境配置文件
cp .env.production .env

# 编辑 .env 文件,修改关键配置
nano .env
```

**必须修改的配置项:**

```bash
# 生成强密钥 (运行以下命令生成)
SECRET_KEY=生成的密钥

# MySQL 配置
MYSQL_ROOT_PASSWORD=设置root密码
MYSQL_PASSWORD=设置数据库密码

# 邮件配置
MAIL_USERNAME=你的邮箱@qq.com
MAIL_PASSWORD=邮箱授权码
```

### 步骤 2: 生成 SECRET_KEY

```bash
# 运行以下 Python 命令生成密钥
python3 -c "import secrets; print(secrets.token_hex(32))"
```

将生成的密钥复制到 `.env` 文件的 `SECRET_KEY` 中。

### 步骤 3: 构建并启动服务

```bash
# 构建镜像并启动所有服务
docker compose up -d --build

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f
```

### 步骤 4: 初始化数据库

**⚠️ 重要提示:**
- 确保 `migrations` 目录存在并已提交到 Git 仓库
- 如果 `migrations` 目录不存在,需要在本地先运行 `flask db init` 和 `flask db migrate`

```bash
# 等待 MySQL 完全启动后,运行数据库迁移
docker compose exec web uv run flask db upgrade

# 创建管理员账户
docker compose exec web uv run python -c "
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash

admin = User(
    username='admin',
    email='admin@example.com',
    password_hash=generate_password_hash('Admin@123'),
    is_admin=True
)
db.session.add(admin)
db.session.commit()
print('管理员账户创建成功!')
print('用户名: admin')
print('密码: Admin@123')
"
```

### 步骤 5: 访问应用

打开浏览器访问: `http://localhost`

---

## 云服务器部署

### 步骤 1: 连接到服务器

```bash
# 使用 SSH 连接到服务器
ssh root@your-server-ip

# 或使用密钥
ssh -i /path/to/key.pem root@your-server-ip
```

### 步骤 2: 安装 Docker

按照上面的 "安装 Docker 和 Docker Compose" 步骤安装。

### 步骤 3: 部署项目

```bash
# 安装 Git
sudo apt-get install -y git  # Ubuntu/Debian
sudo yum install -y git      # CentOS/RHEL

# 克隆项目代码
git clone https://github.com/your-username/flask_shop_system.git
cd flask_shop_system

# 或者上传代码到服务器
# scp -r /local/path/to/project root@your-server-ip:/root/flask_shop_system

# 复制并编辑配置文件
cp .env.production .env
nano .env

# 修改配置后,启动服务
docker compose up -d --build
```

### 步骤 4: 配置防火墙

```bash
# Ubuntu/Debian (UFW)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 步骤 5: (可选) 配置域名和 HTTPS

#### 5.1 购买域名并配置 DNS

购买域名后,在域名注册商处添加 A 记录:
```
类型: A
主机记录: @
记录值: 你的服务器公网IP
```

#### 5.2 修改 Nginx 配置

编辑 `nginx/conf.d/flask_shop.conf`,将 `server_name` 改为你的域名:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 修改为你的域名
    # ... 其他配置
}
```

#### 5.3 申请 SSL 证书 (使用 Let's Encrypt)

```bash
# 安装 Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# 申请证书并自动配置 Nginx
sudo certbot --nginx -d your-domain.com

# 重启 Nginx 容器
docker compose restart nginx
```

或者使用 OpenSSL 生成自签名证书(仅用于测试):

```bash
# 创建 SSL 目录
mkdir -p nginx/ssl

# 生成自签名证书
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem \
  -subj "/CN=your-domain.com"

# 修改 nginx/conf.d/flask_shop.conf,启用 HTTPS 配置
```

### 步骤 6: 初始化数据库

```bash
# 运行数据库迁移
docker compose exec web uv run flask db upgrade

# 创建管理员账户
docker compose exec web uv run python -c "
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash

admin = User(
    username='admin',
    email='admin@example.com',
    password_hash=generate_password_hash('Admin@123'),
    is_admin=True
)
db.session.add(admin)
db.session.commit()
print('管理员账户创建成功!')
"
```

### 步骤 7: 访问应用

在浏览器中访问:
- HTTP: `http://your-server-ip` 或 `http://your-domain.com`
- HTTPS: `https://your-domain.com` (如果配置了 SSL)

---

## 常用运维命令

### 服务管理

```bash
# 启动所有服务
docker compose up -d

# 停止所有服务
docker compose stop

# 重启所有服务
docker compose restart

# 重启指定服务
docker compose restart web
docker compose restart nginx

# 停止并删除所有服务
docker compose down

# 停止并删除所有服务及数据卷
docker compose down -v
```

### 日志查看

```bash
# 查看所有服务日志
docker compose logs

# 查看指定服务日志
docker compose logs web
docker compose logs mysql
docker compose logs nginx

# 实时查看日志
docker compose logs -f web

# 查看最近 100 行日志
docker compose logs --tail=100 web
```

### 数据库管理

```bash
# 进入 MySQL 容器
docker compose exec mysql bash

# 登录 MySQL
mysql -u shop_user -p

# 备份数据库
docker compose exec mysql mysqldump -u root -p shop_db > backup_$(date +%Y%m%d).sql

# 恢复数据库
docker compose exec -T mysql mysql -u root -p shop_db < backup_20250127.sql
```

### 应用管理

```bash
# 进入 Flask 应用容器
docker compose exec web bash

# 在容器中运行 Flask 命令
docker compose exec web uv run flask --help

# 查看数据库迁移状态
docker compose exec web uv run flask db current

# 升级数据库
docker compose exec web uv run flask db upgrade

# 创建新的迁移
docker compose exec web uv run flask db migrate -m "描述"
```

### 更新应用

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker compose up -d --build

# 清理旧的镜像
docker image prune -f
```

### 监控资源使用

```bash
# 查看容器资源使用情况
docker stats

# 查看磁盘使用
docker system df

# 清理未使用的资源
docker system prune -a
```

---

## 故障排查

### 问题 1: 容器无法启动

**症状**: `docker compose up` 失败

**解决方法**:

```bash
# 查看详细错误日志
docker compose logs

# 检查端口占用
sudo netstat -tulpn | grep :5000
sudo netstat -tulpn | grep :3306

# 检查磁盘空间
df -h

# 检查 Docker 服务状态
sudo systemctl status docker
```

### 问题 2: 数据库连接失败

**症状**: 应用日志显示 "Can't connect to MySQL server"

**解决方法**:

```bash
# 检查 MySQL 容器是否运行
docker compose ps mysql

# 检查 MySQL 日志
docker compose logs mysql

# 测试数据库连接
docker compose exec web uv run python -c "
from app import create_app
app = create_app()
with app.app_context():
    from app.extensions import db
    db.session.execute(db.text('SELECT 1'))
    print('数据库连接成功!')
"

# 确认环境变量配置
docker compose exec web env | grep MYSQL
```

### 问题 3: 静态文件无法加载

**症状**: 页面样式丢失,图片无法显示

**解决方法**:

```bash
# 检查静态文件挂载
docker compose exec web ls -la /app/app/static

# 检查 Nginx 静态文件配置
docker compose exec nginx ls -la /usr/share/nginx/html/static

# 重新构建并启动
docker compose up -d --build
```

### 问题 4: 502 Bad Gateway

**症状**: Nginx 返回 502 错误

**解决方法**:

```bash
# 检查 Web 服务是否运行
docker compose ps web

# 检查 Gunicorn 日志
docker compose exec web cat /app/logs/error.log

# 手动重启 Web 服务
docker compose restart web

# 检查 Nginx 配置
docker compose exec nginx nginx -t
```

### 问题 5: 内存不足

**症状**: 服务器响应缓慢,容器被 OOM Killer 杀死

**解决方法**:

```bash
# 检查内存使用
free -h

# 限制容器内存使用 (修改 docker-compose.yml)
services:
  web:
    deploy:
      resources:
        limits:
          memory: 1G

# 减少 Gunicorn 工作进程数 (修改 gunicorn_config.py)
workers = 2  # 减少工作进程数
```

### 问题 6: 迁移文件缺失

**症状**: 运行 `flask db upgrade` 时出现 `ImportError: Can't find Python file migrations/env.py`

**原因**: 项目中缺少 `migrations` 目录或迁移文件

**解决方法**:

```bash
# 在本地开发环境中初始化 Flask-Migrate
flask db init

# 创建初始迁移
flask db migrate -m "初始迁移"

# 将 migrations 目录提交到 Git
git add migrations/
git commit -m "添加数据库迁移文件"

# 重新部署到 Docker
docker compose up -d --build
```

**注意事项:**
- `migrations` 目录应该包含在 Git 仓库中
- 不要将 `migrations` 目录添加到 `.gitignore`
- 每次修改数据库模型后,都要创建新的迁移文件并提交到 Git

---

## 安全建议

### 1. 修改默认密码

- 修改 MySQL root 密码
- 修改管理员账户密码
- 使用强密码策略

### 2. 限制端口访问

```bash
# 只开放必要的端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 3. 使用环境变量管理敏感信息

- 不要将 `.env` 文件提交到 Git 仓库
- 定期更新 SECRET_KEY
- 使用 Docker secrets 管理敏感信息

### 4. 定期备份数据

```bash
# 创建备份脚本
cat > /root/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/root/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# 备份数据库
docker compose exec -T mysql mysqldump -u root -p${MYSQL_ROOT_PASSWORD} shop_db > $BACKUP_DIR/db_$DATE.sql

# 备份上传文件
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz app/static/images/uploads/

# 删除 30 天前的备份
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
EOF

chmod +x /root/backup.sh

# 添加到定时任务
crontab -e
# 添加: 0 2 * * * /root/backup.sh
```

### 5. 启用 HTTPS

使用 Let's Encrypt 免费证书:
```bash
sudo certbot --nginx -d your-domain.com
```

### 6. 配置日志轮转

```bash
# 创建 logrotate 配置
sudo tee /etc/logrotate.d/flask-shop << 'EOF'
/path/to/project/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 www-data www-data
}
EOF
```

### 7. 监控服务状态

```bash
# 使用健康检查脚本
cat > /root/check_health.sh << 'EOF'
#!/bin/bash
curl -f http://localhost/health || echo "Service down!" | mail -s "Alert" admin@example.com
EOF

chmod +x /root/check_health.sh

# 每 5 分钟检查一次
crontab -e
# 添加: */5 * * * * /root/check_health.sh
```

---

## 附录

### A. 配置文件说明

- `.env.production`: 生产环境配置模板
- `docker-compose.yml`: Docker Compose 编排文件
- `Dockerfile`: 应用容器镜像构建文件
- `gunicorn_config.py`: Gunicorn WSGI 服务器配置
- `nginx/nginx.conf`: Nginx 主配置文件
- `nginx/conf.d/flask_shop.conf`: 站点配置文件

### B. 目录结构

```
flask_shop_system/
├── app/                    # 应用主目录
│   ├── static/            # 静态文件
│   │   └── images/
│   │       └── uploads/   # 用户上传的图片
│   ├── templates/         # 模板文件
│   └── ...
├── nginx/                 # Nginx 配置
│   ├── conf.d/           # 站点配置
│   ├── ssl/              # SSL 证书
│   └── logs/             # Nginx 日志
├── logs/                  # 应用日志
├── docker-compose.yml     # Docker Compose 配置
├── Dockerfile            # 应用镜像构建文件
├── gunicorn_config.py    # Gunicorn 配置
└── .env                  # 环境变量(不提交到 Git)
```

### C. 测试账户信息

部署后可使用的测试账户:

- **管理员账户**:
  - 用户名: `admin`
  - 密码: `Admin@123` (首次部署后请立即修改)

- **测试用户**: 需自行注册

### D. 相关资源

- Docker 官方文档: https://docs.docker.com/
- Docker Compose 文档: https://docs.docker.com/compose/
- Nginx 文档: https://nginx.org/en/docs/
- Gunicorn 文档: https://docs.gunicorn.org/
- Flask 文档: https://flask.palletsprojects.com/

---

## 联系与支持

如有问题,请查看:
- 项目 GitHub Issues
- 项目 README.md
- 课程实验要求文档

**部署完成后,请在实验报告中记录:**
1. 部署的服务器IP地址或域名
2. 测试账户的用户名和密码
3. 部署过程中遇到的问题和解决方案
4. 网站功能测试截图
