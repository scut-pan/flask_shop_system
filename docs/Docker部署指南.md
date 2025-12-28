# Flask 商城系统 Docker 部署指南

## 目录

- [部署架构](#部署架构)
- [前置要求](#前置要求)
- [本地部署测试](#本地部署测试)
- [云服务器部署](#云服务器部署)
  - [阿里云服务器部署](#阿里云服务器部署)
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

#### Ubuntu/Debian (阿里云ECS专用)

**⚠️ 重要提示:** 阿里云ECS服务器无法访问Docker官方源,必须使用阿里云镜像源。

```bash
# 更新包索引
sudo apt-get update

# 安装依赖
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# 创建密钥目录
sudo mkdir -p /etc/apt/keyrings

# 添加阿里云 Docker GPG 密钥
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 添加阿里云 Docker 仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 验证安装
docker --version
docker compose version
sudo systemctl status docker
```

#### Ubuntu/Debian (非阿里云服务器)

如果服务器不是阿里云ECS,可以使用Docker官方源:

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
docker compose exec web uv run python -c "from app import create_app; from app.extensions import db; from app.models import User; from werkzeug.security import generate_password_hash; app = create_app(); app.app_context().push(); admin = User(username='admin', email='admin@example.com', password_hash=generate_password_hash('admin123'), is_admin=True); db.session.add(admin); db.session.commit(); print('管理员账户创建成功!')"
```

**预期输出:**
```
管理员账户创建成功!
用户名: admin
密码: admin123
```

#### 步骤 6: 访问应用

打开浏览器访问: **http://localhost**

使用以下账户登录:
- 用户名: `admin`
- 密码: `admin123`

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
from app import create_app
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

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

## 阿里云服务器部署

### 步骤 0: 购买和配置阿里云 ECS 实例

在开始部署之前,你需要先在阿里云购买并配置 ECS 实例。

#### 0.1 购买 ECS 实例

1. **登录阿里云控制台**
   - 访问 [阿里云官网](https://www.aliyun.com/)
   - 登录你的阿里云账号

2. **创建 ECS 实例**
   - 进入「云服务器 ECS」控制台
   - 点击「创建实例」
   - 选择以下配置:
     - **付费模式**: 按量付费或包年包月(测试阶段推荐按量付费)
     - **地域**: 选择离你最近的地域(如华东、华北等)
     - **实例规格**: 推荐 2 核 4GB(如 `ecs.t6-c1m2.large` 或更高配置)
     - **镜像**: 选择 Ubuntu 20.04/22.04 或 CentOS 7/8
     - **存储**: 40GB 或以上 SSD 云盘
     - **网络带宽**: 选择「按使用流量付费」或「按固定带宽」

3. **设置安全组规则**
   - 在创建实例时,配置安全组规则,开放以下端口:
     - **端口 22**: 用于 SSH 连接(限制你的 IP 地址访问)
     - **端口 80**: 用于 HTTP 访问
     - **端口 443**: 用于 HTTPS 访问(可选)

4. **设置登录凭证**
   - 推荐使用「密钥对」认证,更安全
   - 或设置强密码(包含大小写字母、数字和特殊字符)

5. **购买并启动实例**
   - 确认订单并支付
   - 等待实例创建完成(通常 1-3 分钟)
   - 在 ECS 实例列表中查看实例的**公网 IP 地址**

#### 0.2 验证 ECS 实例

```bash
# 在本地终端测试连接(将 your-server-ip 替换为你的 ECS 公网 IP)
ping your-server-ip

# 尝试 SSH 连接(使用密码或密钥)
ssh root@your-server-ip
# 或使用密钥:
# ssh -i /path/to/key.pem root@your-server-ip
```

### 步骤 1: 连接到阿里云 ECS 服务器

#### 1.1 Windows 用户使用密钥文件连接

**如果遇到权限错误 (Permission denied):**

在 PowerShell 中执行以下命令修复权限:

```powershell
# 假设密钥文件路径是 D:\my-server-key.pem
$path = "D:\my-server-key.pem"

# 移除继承权限
icacls $path /inheritance:r

# 移除其他用户的权限
icacls $path /remove "NT AUTHORITY\Authenticated Users"
icacls $path /remove "BUILTIN\Users"

# 只给当前用户完全控制权限
icacls $path /grant "$($env:USERNAME):F"

# 验证权限
icacls $path
```

**或者使用更简单的方法(复制到用户目录):**

```powershell
# 创建.ssh目录
$sshPath = "$env:USERPROFILE\.ssh"
New-Item -Path $sshPath -ItemType Directory -Force

# 复制密钥到.ssh目录
Copy-Item "D:\path\to\your-key.pem" "$sshPath\server-key.pem"

# 移除继承权限并设置为只有当前用户可访问
icacls "$sshPath\server-key.pem" /inheritance:r
icacls "$sshPath\server-key.pem" /grant "$($env:USERNAME):F"

# 使用新路径连接
ssh -i "$sshPath\server-key.pem" root@your-server-ip
```

#### 1.2 使用 SSH 连接到服务器

```bash
# 使用 SSH 连接到阿里云 ECS 服务器
# 将 your-server-ip 替换为你的 ECS 实例公网 IP
ssh -i /path/to/key.pem root@your-server-ip

# Windows 示例:
# ssh -i "D:\my-server-key.pem" root@8.138.112.249
```

**登录成功后,你将看到类似以下的提示符:**
```
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-161-generic x86_64)
root@iZ7xvarr7yv637z9hpal1iZ:~#
```

### 步骤 2: 安装 Docker

**⚠️ 重要:** 阿里云ECS必须使用阿里云镜像源安装Docker,请参考前面的 "Ubuntu/Debian (阿里云ECS专用)" 章节。

快速安装命令:

```bash
# 更新包索引
sudo apt-get update

# 安装依赖
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# 创建密钥目录
sudo mkdir -p /etc/apt/keyrings

# 添加阿里云 Docker GPG 密钥
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 添加阿里云 Docker 仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

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

### 步骤 4: 配置阿里云安全组

在阿里云上部署应用,**必须配置安全组规则**才能让外部访问你的服务。

#### 4.1 通过阿里云控制台配置安全组(推荐)

1. **登录阿里云 ECS 控制台**
   - 进入「云服务器 ECS」→「实例」

2. **找到你的 ECS 实例**
   - 在实例列表中,点击实例 ID 进入详情页

3. **配置安全组规则**
   - 点击「安全组」标签页
   - 点击「配置规则」
   - 点击「手动添加」或「快速添加」

4. **添加以下入方向规则**:

   | 授权策略 | 协议类型 | 端口范围 | 授权对象 | 描述 |
   |---------|---------|---------|---------|------|
   | 允许 | TCP | 22/22 | 0.0.0.0/0 或你的 IP | SSH 远程连接 |
   | 允许 | TCP | 80/80 | 0.0.0.0/0 | HTTP 访问 |
   | 允许 | TCP | 443/443 | 0.0.0.0/0 | HTTPS 访问 |

   **安全建议**:
   - 对于 SSH 端口(22),建议限制为你的 IP 地址(可以在本地搜索「我的 IP」获取)
   - 如果不需要 SSH 访问,可以临时开放,部署完成后关闭

5. **保存规则**
   - 点击「确定」保存配置

#### 4.2 服务器内部防火墙配置(可选)

阿里云安全组已经提供了足够的防护,服务器内部防火墙可以不配置。如果你想额外配置,可以使用以下命令:

```bash
# Ubuntu/Debian (UFW)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp    # 允许 SSH
sudo ufw enable

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

**注意**: 如果配置了服务器内部防火墙,同时也要确保阿里云安全组规则已开放相应端口。

### 步骤 5: (可选) 配置域名和 HTTPS

#### 5.1 购买域名并配置 DNS

**在阿里云购买域名**:

1. **购买域名**
   - 登录阿里云控制台
   - 进入「域名注册」页面
   - 搜索并购买你想要的域名(如 `example.com`)

2. **配置域名解析**
   - 进入「云解析 DNS」控制台
   - 找到你购买的域名,点击「解析设置」
   - 添加以下记录:

   | 记录类型 | 主机记录 | 记录值 | TTL |
   |---------|---------|--------|-----|
   | A | @ | 你的 ECS 公网 IP | 600 |
   | A | www | 你的 ECS 公网 IP | 600 |

   **说明**:
   - `@` 表示主域名(如 `example.com`)
   - `www` 表示 www 子域名(如 `www.example.com`)
   - TTL 表示缓存时间,600 秒即可

3. **验证解析**
   - 等待 5-10 分钟后,在本地终端测试:
   ```bash
   # 检查域名是否解析成功
   nslookup your-domain.com
   # 或
   ping your-domain.com
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

#### 5.3 申请 SSL 证书

**方案一: 使用阿里云免费 SSL 证书(推荐)**

阿里云为每个实名认证账号提供 20 个免费 DV SSL 证书。

1. **申请免费证书**
   - 登录阿里云控制台
   - 搜索「SSL 证书」或进入「数字证书管理服务」
   - 点击「免费证书」→「申请证书」
   - 填写域名信息:
     - 证书类型: DV(域名验证)
     - 域名: `your-domain.com` 或 `*.your-domain.com`(通配符证书)
   - 提交申请

2. **域名验证**
   - 选择「DNS 验证」方式
   - 阿里云会自动添加 DNS 验证记录
   - 等待几分钟,证书自动签发

3. **下载证书**
   - 证书签发后,点击「下载」
   - 下载 Nginx 格式的证书
   - 解压后得到两个文件:
     - `your-domain.com.pem`(证书文件)
     - `your-domain.com.key`(私钥文件)

4. **上传证书到服务器**
   ```bash
   # 在本地终端执行,将证书上传到服务器
   scp /path/to/your-domain.com.pem root@your-server-ip:/root/flask_shop_system/nginx/ssl/cert.pem
   scp /path/to/your-domain.com.key root@your-server-ip:/root/flask_shop_system/nginx/ssl/key.pem
   ```

5. **修改 Nginx 配置启用 HTTPS**
   - 编辑 `nginx/conf.d/flask_shop.conf`
   - 取消 HTTPS 配置的注释,或添加以下内容:

   ```nginx
   server {
       listen 443 ssl;
       server_name your-domain.com;

       ssl_certificate /etc/nginx/ssl/cert.pem;
       ssl_certificate_key /etc/nginx/ssl/key.pem;

       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers HIGH:!aNULL:!MD5;
       ssl_prefer_server_ciphers on;

       # ... 其他配置
   }

   # HTTP 自动跳转 HTTPS
   server {
       listen 80;
       server_name your-domain.com;
       return 301 https://$server_name$request_uri;
   }
   ```

6. **重启 Nginx 容器**
   ```bash
   docker compose restart nginx
   ```

7. **验证 HTTPS**
   - 在浏览器访问 `https://your-domain.com`
   - 查看浏览器地址栏的锁形图标

**方案二: 使用 Let's Encrypt 免费证书**

```bash
# 安装 Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# 申请证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 证书文件位置:
# /etc/letsencrypt/live/your-domain.com/fullchain.pem
# /etc/letsencrypt/live/your-domain.com/privkey.pem

# 将证书复制到项目目录
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem /root/flask_shop_system/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem /root/flask_shop_system/nginx/ssl/key.pem

# 修改 Nginx 配置后重启容器
docker compose restart nginx
```

**方案三: 使用自签名证书(仅用于测试)**

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

**注意**: 自签名证书会导致浏览器显示「不安全」警告,仅用于开发测试。

### 步骤 6: 初始化数据库

```bash
# 运行数据库迁移
docker compose exec web uv run flask db upgrade

# 创建管理员账户
docker compose exec web uv run python -c "
from app import create_app
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

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

### 问题 6: Windows SSH 密钥权限错误

**症状**: SSH 连接时提示 `Permission denied` 或 `bad permissions`

**原因**: Windows 的 SSH 客户端要求密钥文件只能被当前用户访问,权限过于开放会拒绝连接。

**解决方法**:

**方法1: 使用 PowerShell 修复权限**

```powershell
# 假设密钥文件路径是 D:\my-server-key.pem
$path = "D:\my-server-key.pem"

# 移除继承权限
icacls $path /inheritance:r

# 移除其他用户的权限
icacls $path /remove "NT AUTHORITY\Authenticated Users"
icacls $path /remove "BUILTIN\Users"

# 只给当前用户完全控制权限
icacls $path /grant "$($env:USERNAME):F"
```

**方法2: 复制到用户 .ssh 目录**

```powershell
# 创建.ssh目录
$sshPath = "$env:USERPROFILE\.ssh"
New-Item -Path $sshPath -ItemType Directory -Force

# 复制密钥到.ssh目录
Copy-Item "D:\path\to\your-key.pem" "$sshPath\server-key.pem"

# 设置权限
icacls "$sshPath\server-key.pem" /inheritance:r
icacls "$sshPath\server-key.pem" /grant "$($env:USERNAME):F"

# 使用新路径连接
ssh -i "$sshPath\server-key.pem" root@your-server-ip
```

**方法3: 使用 Git Bash**

```bash
# 复制密钥到项目目录
cp "D:\path\to\your-key.pem" ./server-key.pem

# 修复权限
chmod 600 ./server-key.pem

# 连接
ssh -i ./server-key.pem root@your-server-ip
```

### 问题 7: 阿里云ECS无法访问Docker官方源

**症状**: `curl: (35) OpenSSL SSL_connect: Connection reset by peer`

**原因**: 阿里云ECS服务器无法访问Docker官方源 `https://download.docker.com`

**解决方法**: 使用阿里云镜像源

```bash
# 使用阿里云镜像源
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### 问题 8: 迁移文件缺失

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
