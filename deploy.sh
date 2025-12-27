#!/bin/bash

# Flask 商城系统 Docker 部署脚本
# 使用方法: bash deploy.sh [环境]
# 环境选项: dev(开发环境), prod(生产环境)

set -e  # 遇到错误立即退出

ENV=${1:-dev}

echo "========================================"
echo "Flask 商城系统 Docker 部署脚本"
echo "环境: $ENV"
echo "========================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Docker 是否安装
check_docker() {
    echo -e "${YELLOW}检查 Docker...${NC}"
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}错误: Docker 未安装!${NC}"
        echo "请先安装 Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker 已安装${NC}"
}

# 检查 Docker Compose 是否安装
check_docker_compose() {
    echo -e "${YELLOW}检查 Docker Compose...${NC}"
    if ! docker compose version &> /dev/null; then
        echo -e "${RED}错误: Docker Compose 未安装!${NC}"
        echo "请先安装 Docker Compose"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker Compose 已安装${NC}"
}

# 准备配置文件
prepare_config() {
    echo -e "${YELLOW}准备配置文件...${NC}"

    if [ ! -f .env ]; then
        if [ "$ENV" = "prod" ]; then
            cp .env.production .env
            echo -e "${GREEN}✓ 已复制生产环境配置文件${NC}"
        else
            cp .env.production .env
            echo -e "${GREEN}✓ 已复制开发环境配置文件${NC}"
        fi

        echo -e "${YELLOW}⚠ 请编辑 .env 文件并设置必要的配置项:${NC}"
        echo "  - SECRET_KEY (运行: python3 -c \"import secrets; print(secrets.token_hex(32))\")"
        echo "  - MYSQL_ROOT_PASSWORD"
        echo "  - MYSQL_PASSWORD"
        echo "  - MAIL_USERNAME"
        echo "  - MAIL_PASSWORD"
        echo ""
        read -p "按 Enter 继续 (确保已编辑 .env 文件)..."
    else
        echo -e "${GREEN}✓ .env 文件已存在${NC}"
    fi
}

# 创建必要的目录
create_directories() {
    echo -e "${YELLOW}创建必要的目录...${NC}"
    mkdir -p app/static/images/uploads
    mkdir -p logs
    mkdir -p nginx/ssl
    mkdir -p nginx/logs
    echo -e "${GREEN}✓ 目录创建完成${NC}"
}

# 构建 Docker 镜像
build_images() {
    echo -e "${YELLOW}构建 Docker 镜像...${NC}"
    docker compose build
    echo -e "${GREEN}✓ 镜像构建完成${NC}"
}

# 启动服务
start_services() {
    echo -e "${YELLOW}启动服务...${NC}"
    docker compose up -d
    echo -e "${GREEN}✓ 服务启动完成${NC}"
}

# 等待服务就绪
wait_for_services() {
    echo -e "${YELLOW}等待服务就绪...${NC}"
    sleep 10

    # 等待 MySQL 就绪
    echo -e "${YELLOW}等待 MySQL 启动...${NC}"
    until docker compose exec -T mysql mysqladmin ping -h localhost --silent; do
        echo "MySQL 还未就绪,等待中..."
        sleep 3
    done
    echo -e "${GREEN}✓ MySQL 已就绪${NC}"

    # 等待 Web 服务就绪
    echo -e "${YELLOW}等待 Web 服务启动...${NC}"
    until docker compose exec -T web curl -f http://localhost:5000/health &> /dev/null; do
        echo "Web 服务还未就绪,等待中..."
        sleep 3
    done
    echo -e "${GREEN}✓ Web 服务已就绪${NC}"
}

# 初始化数据库
init_database() {
    echo -e "${YELLOW}初始化数据库...${NC}"

    # 运行数据库迁移
    docker compose exec -T web flask db upgrade

    echo -e "${GREEN}✓ 数据库初始化完成${NC}"
}

# 创建管理员账户
create_admin() {
    echo -e "${YELLOW}创建管理员账户...${NC}"

    docker compose exec -T web python3 << 'EOF'
from app import create_app
from app.extensions import db
from app.models import User

app = create_app('production')
with app.app_context():
    # 检查管理员是否已存在
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print("管理员账户已存在,跳过创建")
    else:
        from werkzeug.security import generate_password_hash
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('Admin@123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("管理员账户创建成功!")
        print("用户名: admin")
        print("密码: Admin@123")
        print("⚠ 请在生产环境中立即修改默认密码!")
EOF

    echo -e "${GREEN}✓ 管理员账户设置完成${NC}"
}

# 显示部署信息
show_info() {
    echo ""
    echo "========================================"
    echo -e "${GREEN}🎉 部署完成!${NC}"
    echo "========================================"
    echo ""
    echo "访问地址:"
    echo "  HTTP:  http://localhost"
    echo ""
    echo "管理员账户:"
    echo "  用户名: admin"
    echo "  密码: Admin@123"
    echo ""
    echo "常用命令:"
    echo "  查看日志: docker compose logs -f"
    echo "  停止服务: docker compose stop"
    echo "  重启服务: docker compose restart"
    echo "  删除服务: docker compose down"
    echo ""
    echo "========================================"
}

# 主函数
main() {
    check_docker
    check_docker_compose
    create_directories
    prepare_config
    build_images
    start_services
    wait_for_services
    init_database
    create_admin
    show_info
}

# 运行主函数
main
