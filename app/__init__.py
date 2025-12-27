"""Flask应用"""
from dotenv import load_dotenv
import os
from pathlib import Path

# 优先加载 .env.local (本地开发),如果不存在则加载 .env (Docker部署)
env_path = Path(__file__).parent.parent / '.env.local'
load_dotenv(env_path, override=True)  # 优先加载 .env.local
load_dotenv()  # 如果 .env.local 不存在,加载 .env

from flask import Flask, render_template
from app.extensions import db
from config import config
from app.extensions import init_extensions
from app import models  # 导入所有模型

def create_app(config_name='default'):
    """创建Flask应用实例"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化扩展
    init_extensions(app)

    # 注册蓝图
    from app.routes import auth_bp, main_bp, product_bp, cart_bp, order_bp, admin_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # 注册错误处理器
    register_error_handlers(app)

    # 注册模板上下文处理器
    register_template_context(app)

    # 注册健康检查端点
    @app.route('/health')
    def health_check():
        """健康检查端点,用于容器编排和服务监控"""
        return {'status': 'healthy', 'message': 'Flask Shop is running'}, 200

    return app

def register_error_handlers(app):
    """注册错误处理器"""
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

def register_template_context(app):
    """注册模板上下文处理器"""
    @app.context_processor
    def inject_cart_count():
        """在所有模板中注入购物车数量（商品总件数）"""
        from flask_login import current_user
        from app.extensions import db
        # 检查 current_user 是否存在且已认证(避免在邮件模板等非请求上下文中出错)
        if current_user and getattr(current_user, 'is_authenticated', False):
            # 统计购物车商品总件数
            count = db.session.query(db.func.sum(models.CartItem.quantity))\
                             .filter_by(user_id=current_user.id)\
                             .scalar()
            count = count or 0
            return dict(cart_count=count)
        return dict(cart_count=0)