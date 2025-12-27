.PHONY: help build up down restart logs status db-upgrade db-backup clean test

help: ## 显示帮助信息
	@echo "Flask 商城系统 - Docker 管理命令"
	@echo ""
	@echo "使用方法: make [目标]"
	@echo ""
	@echo "可用目标:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## 构建 Docker 镜像
	docker compose build

up: ## 启动所有服务
	docker compose up -d

down: ## 停止并删除所有服务
	docker compose down

restart: ## 重启所有服务
	docker compose restart

logs: ## 查看所有服务日志
	docker compose logs -f

logs-web: ## 查看 Web 服务日志
	docker compose logs -f web

logs-nginx: ## 查看 Nginx 日志
	docker compose logs -f nginx

logs-mysql: ## 查看 MySQL 日志
	docker compose logs -f mysql

status: ## 查看服务状态
	docker compose ps

db-upgrade: ## 升级数据库
	docker compose exec web flask db upgrade

db-backup: ## 备份数据库
	@mkdir -p backups
	docker compose exec -T mysql mysqldump -u root -p$$(grep MYSQL_ROOT_PASSWORD .env | cut -d '=' -f2) shop_db > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "数据库备份完成: backups/backup_$$(date +%Y%m%d_%H%M%S).sql"

db-restore: ## 恢复数据库 (用法: make db-restore FILE=backup_20250127.sql)
	@if [ -z "$(FILE)" ]; then echo "错误: 请指定备份文件,例如: make db-restore FILE=backup_20250127.sql"; exit 1; fi
	docker compose exec -T mysql mysql -u root -p$$(grep MYSQL_ROOT_PASSWORD .env | cut -d '=' -f2) shop_db < $(FILE)
	@echo "数据库恢复完成"

clean: ## 清理未使用的 Docker 资源
	docker image prune -f
	docker system prune -f

test: ## 运行测试
	docker compose exec web pytest

shell: ## 进入 Web 容器 Shell
	docker compose exec web bash

shell-mysql: ## 进入 MySQL 容器
	docker compose exec mysql bash

init: ## 初始化项目(首次部署)
	@echo "初始化 Flask 商城系统..."
	@mkdir -p app/static/images/uploads logs nginx/ssl nginx/logs
	@if [ ! -f .env ]; then \
		cp .env.production .env; \
		echo "已创建 .env 文件,请编辑配置后再次运行 'make up'"; \
		exit 1; \
	fi
	docker compose up -d --build
	@echo "等待服务启动..."
	@sleep 10
	docker compose exec web flask db upgrade
	@echo "初始化完成!"
	@echo "请运行以下命令创建管理员账户:"
	@echo "make create-admin"

create-admin: ## 创建管理员账户
	docker compose exec web python -c "
from app import create_app
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app('production')
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print('管理员账户已存在')
    else:
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
        print('请尽快修改默认密码!')
"

health: ## 检查服务健康状态
	@echo "检查服务状态..."
	@docker compose ps
	@echo ""
	@echo "检查 Web 服务..."
	@curl -f http://localhost/health && echo " ✓ Web 服务正常" || echo " ✗ Web 服务异常"
	@echo ""
	@echo "检查 MySQL..."
	@docker compose exec -T mysql mysqladmin ping -h localhost --silent && echo " ✓ MySQL 正常" || echo " ✗ MySQL 异常"

ps: ## 查看运行的容器
	docker compose ps

stats: ## 查看容器资源使用情况
	docker stats

install: ## 安装项目依赖(本地开发)
	uv sync

dev: ## 本地开发模式运行
	uv run python main.py

format: ## 格式化代码
	uv run black app/
	uv run flake8 app/

lint: ## 代码检查
	uv run flake8 app/
