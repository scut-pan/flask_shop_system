"""Flask 扩展初始化"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
csrf = CSRFProtect()

def init_extensions(app):
    """初始化所有扩展"""
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # 配置登录管理器
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录访问此页面'
    login_manager.login_message_category = 'info'

    # 用户加载器
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))