"""Flask 扩展初始化"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

def init_extensions(app):
    """初始化所有扩展"""
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # 配置登录管理器
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录访问此页面'
    login_manager.login_message_category = 'info'