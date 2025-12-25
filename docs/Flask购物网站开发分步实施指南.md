# Flask购物网站开发分步实施指南

## 项目概述

这是一个基于Flask框架的在线购物网站项目，满足课程实验要求。通过本指南，你将一步步完成整个项目的开发，学到完整的Web应用开发流程。

## 技术栈

- **后端**: Python 3 + Flask
- **数据库**: MySQL + Flask-SQLAlchemy (ORM)
- **前端**: HTML5 + CSS3 + Bootstrap 5 + 少量JavaScript
- **认证**: Flask-Login
- **表单**: Flask-WTF
- **邮件**: Flask-Mail
- **文件上传**: Pillow
- **包管理**: uv (现代Python包管理器)
- **部署**: Gunicorn + Nginx

## 开发环境准备

### 第1步：安装必要软件

#### 1.1 安装Python和包管理器
```bash
# 如果没有安装Python，从 https://python.org 下载Python 3.10+ （推荐3.10）
# 安装uv包管理器（比pip更快速、更现代）
pip install uv

# 验证安装
uv --version
```

#### 1.2 安装MySQL数据库
- Windows: 下载MySQL Community Server
- macOS: `brew install mysql`
- Linux: `sudo apt-get install mysql-server`

#### 1.3 代码编辑器
推荐使用 VS Code，并安装以下插件：
- Python
- Pylance
- MySQL
- GitLens

### 第2步：项目初始化

#### 2.1 创建项目目录结构
```
flask_shop_system/
├── app/
│   ├── __init__.py         # Flask应用工厂
│   ├── extensions.py       # Flask扩展初始化
│   ├── forms.py            # WTForms表单类
│   ├── models/             # 数据库模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── cart.py
│   ├── routes/             # 路由（视图函数）
│   │   ├── __init__.py
│   │   ├── auth.py         # 认证相关路由
│   │   ├── main.py         # 主要页面路由
│   │   ├── product.py      # 商品相关路由
│   │   ├── cart.py         # 购物车路由
│   │   ├── order.py        # 订单相关路由
│   │   └── admin.py        # 管理员路由
│   ├── templates/          # HTML模板
│   │   ├── base.html       # 基础模板
│   │   ├── auth/           # 认证相关模板
│   │   ├── main/           # 主要页面模板
│   │   ├── product/        # 商品相关模板
│   │   ├── cart/           # 购物车模板
│   │   ├── order/          # 订单模板
│   │   └── admin/          # 管理员页面模板
│   ├── static/             # 静态文件
│   │   ├── css/
│   │   │   └── style.css   # 自定义样式
│   │   ├── js/
│   │   │   └── main.js     # JavaScript文件
│   │   └── images/
│   │       └── uploads/    # 用户上传图片
│   └── utils/              # 工具函数
│       ├── __init__.py
│       ├── decorators.py   # 装饰器
│       └── helpers.py      # 辅助函数
├── migrations/             # 数据库迁移文件
├── config.py               # 配置文件
├── pyproject.toml          # 项目配置和依赖管理（uv）
├── main.py                 # 应用启动文件
├── init_db.py              # 数据库初始化脚本
├── .env                    # 环境变量文件（不提交到Git）
├── .gitignore              # Git忽略文件
└── README.md               # 项目说明
```

#### 2.2 创建项目基础结构
```bash
# 创建项目目录
mkdir flask_shop_system
cd flask_shop_system

# 初始化uv项目（自动生成pyproject.toml）
uv init

# 创建必要的目录结构
mkdir -p app/{models,routes,templates/{auth,main,product,cart,order,admin},static/{css,js,images/uploads},utils}
mkdir migrations

# 创建基础空文件
touch app/__init__.py
touch app/extensions.py
touch app/forms.py
touch app/models/__init__.py
touch app/models/user.py
touch app/models/product.py
touch app/models/order.py
touch app/models/cart.py
touch app/routes/__init__.py
touch app/routes/auth.py
touch app/routes/main.py
touch app/routes/product.py
touch app/routes/cart.py
touch app/routes/order.py
touch app/routes/admin.py
touch app/utils/__init__.py
touch app/utils/decorators.py
touch app/utils/helpers.py
touch config.py
touch main.py
touch init_db.py
touch .env
touch .gitignore
```

#### 2.3 配置项目依赖

使用 `uv add` 命令添加依赖，它会自动更新 `pyproject.toml` 文件：

```bash
# 添加核心Flask依赖
uv add Flask Flask-SQLAlchemy Flask-Login Flask-Mail Flask-Migrate Flask-WTF
uv add Werkzeug PyMySQL cryptography python-dotenv Pillow email-validator WTForms

# 添加开发依赖（可选）
uv add --dev pytest pytest-flask black flake8

# 查看已安装的依赖
uv tree

# 同步安装所有依赖
uv sync
```

**说明**：
- `uv add` 会自动将依赖添加到 `pyproject.toml`
- `uv.lock` 文件会自动更新，锁定具体的依赖版本
- 无需手动编辑 `pyproject.toml` 文件

#### 2.4 配置环境变量

创建 `.env` 文件（此文件已配置在 `.gitignore` 中，不会提交到Git）：

```env
# Flask配置
SECRET_KEY=your-super-secret-key-here

# 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=shop_user
MYSQL_PASSWORD=ShopPass456@secure
MYSQL_DB=shop_db
MYSQL_CHARSET=utf8mb4

# 环境标识
FLASK_ENV=development
FLASK_DEBUG=1
```

**注意**：在使用前需要先创建MySQL数据库和用户：

```sql
-- 登录MySQL
mysql -u root -p

-- 创建数据库
CREATE DATABASE shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建专用用户（推荐）
CREATE USER 'shop_user'@'localhost' IDENTIFIED BY 'ShopPass456@secure';
GRANT ALL PRIVILEGES ON shop_db.* TO 'shop_user'@'localhost';
FLUSH PRIVILEGES;

-- 退出
EXIT;
```

## 核心功能开发步骤

### 第3步：数据库设计与建模

#### 3.1 创建Flask扩展配置文件

创建 `app/extensions.py`：
```python
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

    # 用户加载器
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
```

#### 3.2 理解数据库设计原则
在设计数据库之前，先理解以下概念：

**什么是ORM？**
- ORM（Object-Relational Mapping）是对象关系映射
- 让你能用Python类来操作数据库表
- 不需要写原生SQL语句

**数据库表关系：**
- 一对多：一个用户可以有多个订单
- 多对多：订单和商品之间的关系（一个订单包含多个商品，一个商品可以在多个订单中）

#### 3.2 设计数据库表结构

**用户表 (users)**
- id: 主键
- username: 用户名（唯一）
- email: 邮箱（唯一）
- password_hash: 加密后的密码
- is_admin: 是否是管理员
- created_at: 创建时间
- updated_at: 更新时间

**商品表 (products)**
- id: 主键
- name: 商品名称
- description: 商品描述
- price: 价格
- stock: 库存数量
- image_url: 商品图片URL
- is_active: 是否上架
- created_at: 创建时间
- updated_at: 更新时间

**购物车表 (cart_items)**
- id: 主键
- user_id: 用户ID（外键）
- product_id: 商品ID（外键）
- quantity: 数量
- created_at: 添加时间

**订单表 (orders)**
- id: 主键
- order_number: 订单号（唯一）
- user_id: 用户ID（外键）
- total_amount: 总金额
- status: 订单状态（待支付/已支付/已发货/已完成/已取消）
- shipping_address: 收货地址
- created_at: 创建时间
- updated_at: 更新时间

**订单明细表 (order_items)**
- id: 主键
- order_id: 订单ID（外键）
- product_id: 商品ID（外键）
- quantity: 数量
- price: 下单时的价格（快照）

#### 3.3 实现数据模型

创建 `app/models/__init__.py`:
```python
from .user import User
from .product import Product
from .order import Order, OrderItem
from .cart import CartItem

__all__ = ['User', 'Product', 'Order', 'OrderItem', 'CartItem']
```

**示例：用户模型 (app/models/user.py)**
你需要创建以下文件，这里给出基本结构，你需要根据理解自己实现：

```python
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                          onupdate=lambda: datetime.now(timezone.utc))

    # 建立与其他表的关系
    orders = db.relationship('Order', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    cart_items = db.relationship('CartItem', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """设置密码（加密存储）"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
```

**你需要自己实现其他模型文件：**
- `app/models/product.py` - 商品模型
  - 包含字段：id, name, description, price, stock, image_url, is_active, created_at, updated_at
  - 方法：is_in_stock(), reduce_stock()
- `app/models/order.py` - 订单和订单明细模型
  - Order：id, order_number（自动生成）, user_id, total_amount, status, shipping_address
  - OrderItem：id, order_id, product_id, quantity, price（快照价格）
- `app/models/cart.py` - 购物车模型
  - CartItem：id, user_id, product_id, quantity（唯一约束：user_id + product_id）

### 第4步：Flask应用初始化

#### 4.1 创建配置文件 (config.py)
```python
import os
from datetime import timedelta

class Config:
    """基础配置类"""
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change-in-production'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://shop_user:ShopPass456@localhost/shop_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # 开发环境可以设为True查看SQL语句

    # 邮件配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'app/static/images/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # 会话配置
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    # 分页配置
    PRODUCTS_PER_PAGE = 12
    ORDERS_PER_PAGE = 10

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # 开发环境显示SQL语句

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_ECHO = False

# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

#### 4.2 创建Flask应用工厂 (app/__init__.py)
```python
from flask import Flask
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
```

#### 4.3 创建应用启动文件 (main.py)
```python
import os
from app import create_app
from app.extensions import db
from app.models import User, Product, Order, CartItem

# 从环境变量获取配置
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    """为shell提供上下文"""
    return dict(db=db, User=User, Product=Product, Order=Order, CartItem=CartItem)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

#### 4.4 创建数据库初始化脚本 (init_db.py)
```python
"""数据库初始化脚本"""
from app import create_app
from app.extensions import db
from app.models import User

def init_database():
    """初始化数据库"""
    app = create_app()

    with app.app_context():
        # 创建所有表
        db.create_all()

        # 创建管理员用户（如果不存在）
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@shop.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('✓ 管理员用户创建成功')
            print('  用户名: admin')
            print('  密码: admin123')
            print('  邮箱: admin@shop.com')
        else:
            print('✓ 管理员用户已存在')

        print('\n数据库初始化完成！')

if __name__ == '__main__':
    init_database()
```

### 第5步：用户认证系统

#### 5.1 创建表单类 (app/forms.py)

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    """注册表单"""
    username = StringField('用户名', validators=[
        DataRequired(),
        Length(min=4, max=20, message='用户名长度必须在4-20个字符之间')
    ])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[
        DataRequired(),
        Length(min=6, message='密码至少6个字符')
    ])
    password2 = PasswordField('确认密码', validators=[
        DataRequired(),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    submit = SubmitField('注册')

    def validate_username(self, field):
        """验证用户名是否已存在"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

    def validate_email(self, field):
        """验证邮箱是否已存在"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')
```

#### 5.2 创建装饰器 (app/utils/decorators.py)

```python
from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    """管理员权限装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('需要管理员权限访问此页面', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def anonymous_required(f):
    """游客（未登录）权限装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash('您已经登录', 'info')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function
```

#### 5.3 理解Flask-Login工作原理
- `LoginManager` 管理用户会话
- `@login_required` 装饰器保护需要登录的路由
- `UserMixin` 提供默认的用户会话方法

#### 5.4 实现认证路由 (app/routes/auth.py)

创建路由蓝图：
```python
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User
from app.forms import LoginForm, RegistrationForm
from app.utils.decorators import anonymous_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
@anonymous_required
def register():
    """用户注册"""
    form = RegistrationForm()
    if form.validate_on_submit():
        # 创建新用户
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        # 保存到数据库
        db.session.add(user)
        db.session.commit()

        flash('注册成功！请登录', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
@anonymous_required
def login():
    """用户登录"""
    form = LoginForm()
    if form.validate_on_submit():
        # 查找用户
        user = User.query.filter_by(username=form.username.data).first()

        # 验证用户和密码
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            # 获取下一页URL
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')

            flash(f'欢迎回来，{user.username}！', 'success')
            return redirect(next_page)
        else:
            flash('用户名或密码错误', 'danger')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    flash('您已成功退出登录', 'info')
    return redirect(url_for('main.index'))
```

#### 5.5 创建路由初始化文件 (app/routes/__init__.py)

```python
from app.routes import auth, main, product, cart, order, admin

# 创建蓝图实例
auth_bp = auth.auth_bp
main_bp = main.main_bp
product_bp = product.product_bp
cart_bp = cart.cart_bp
order_bp = order.order_bp
admin_bp = admin.admin_bp

__all__ = ['auth_bp', 'main_bp', 'product_bp', 'cart_bp', 'order_bp', 'admin_bp']
```

#### 5.6 创建认证模板

- `app/templates/auth/register.html` - 注册页面
- `app/templates/auth/login.html` - 登录页面
- `app/templates/base.html` - 基础模板
- `app/templates/main/index.html` - 首页

**基础模板结构示例 (app/templates/base.html):**
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask购物网站{% endblock %}</title>

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <!-- 自定义CSS -->
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">

    {% block styles %}{% endblock %}
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('main.index') }}">
                <i class="fas fa-store"></i> 购物网站
            </a>

            <div class="navbar-nav ms-auto">
                {% if current_user.is_authenticated %}
                    <a class="nav-link" href="{{ url_for('cart.index') }}">
                        <i class="fas fa-shopping-cart"></i> 购物车
                    </a>
                    <a class="nav-link" href="{{ url_for('auth.logout') }}">退出</a>
                {% else %}
                    <a class="nav-link" href="{{ url_for('auth.login') }}">登录</a>
                    <a class="nav-link" href="{{ url_for('auth.register') }}">注册</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <!-- 消息闪现 -->
    <div class="container mt-3">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>

    <!-- 主要内容 -->
    <main class="container-fluid py-4">
        {% block content %}{% endblock %}
    </main>

    <!-- 页脚 -->
    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container">
            <div class="text-center">
                <p>&copy; 2025 Flask购物网站. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <!-- 自定义JS -->
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>

    {% block scripts %}{% endblock %}
</body>
</html>
```

**登录页面示例 (app/templates/auth/login.html):**
```html
{% extends "base.html" %}

{% block title %}登录 - Flask购物网站{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow">
            <div class="card-header bg-primary text-white text-center">
                <h4>用户登录</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {{ form.hidden_tag() }}

                    <div class="mb-3">
                        {{ form.username.label(class="form-label") }}
                        {{ form.username(class="form-control") }}
                        {% if form.username.errors %}
                            {% for error in form.username.errors %}
                                <div class="text-danger small">{{ error }}</div>
                            {% endfor %}
                        {% endif %}
                    </div>

                    <div class="mb-3">
                        {{ form.password.label(class="form-label") }}
                        {{ form.password(class="form-control") }}
                        {% if form.password.errors %}
                            {% for error in form.password.errors %}
                                <div class="text-danger small">{{ error }}</div>
                            {% endfor %}
                        {% endif %}
                    </div>

                    <div class="mb-3 form-check">
                        {{ form.remember_me(class="form-check-input") }}
                        {{ form.remember_me.label(class="form-check-label") }}
                    </div>

                    <div class="d-grid gap-2">
                        {{ form.submit(class="btn btn-primary") }}
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 第6步：商品展示与管理

#### 6.1 商品路由实现 (app/routes/product.py)
需要实现的功能：
- 商品列表展示（分页）
- 商品详情页
- 商品搜索（可选）
- 管理员添加/编辑/删除商品（使用 `@admin_required` 装饰器）

#### 6.2 商品模板
- `app/templates/product/list.html` - 商品列表
- `app/templates/product/detail.html` - 商品详情
- `app/templates/admin/product_form.html` - 商品添加/编辑表单

### 第7步：购物车功能

#### 7.1 购物车逻辑理解
购物车数据可以存储在：
- **数据库**（推荐）：持久化，适合登录用户
- Session：临时，适合游客

本项目建议使用数据库存储，CartItem 模型中设置 `user_id` 和 `product_id` 的唯一约束。

#### 7.2 购物车实现要点
- 添加商品到购物车（如果已存在则增加数量）
- 修改商品数量
- 删除购物车商品
- 清空购物车
- 计算总价

**关键方法**：
```python
# CartItem模型中的方法
@staticmethod
def get_or_create(user_id, product_id):
    """获取或创建购物车项"""
    item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not item:
        item = CartItem(user_id=user_id, product_id=product_id, quantity=1)
        db.session.add(item)
    else:
        item.quantity += 1
    return item
```

### 第8步：订单系统

#### 8.1 订单流程
1. 用户从购物车点击"结算"
2. 确认订单信息（填写收货地址）
3. 创建订单（从购物车数据复制到订单明细）
4. 减少商品库存
5. 清空购物车
6. 发送确认邮件（可选）

#### 8.2 订单状态管理
订单状态包括：
- `pending` - 待支付
- `paid` - 已支付
- `shipped` - 已发货
- `delivered` - 已完成
- `cancelled` - 已取消

**订单号生成**：
```python
@staticmethod
def generate_order_number():
    """生成唯一订单号"""
    return f"ORD{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
```

### 第9步：管理员功能

#### 9.1 权限验证
使用 `@admin_required` 装饰器（已在 `app/utils/decorators.py` 中定义）保护管理员路由：
```python
from app.utils.decorators import admin_required

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """管理员仪表盘"""
    # 统计数据
    total_orders = Order.query.count()
    total_products = Product.query.count()
    total_users = User.query.count()
    return render_template('admin/dashboard.html',
                         total_orders=total_orders,
                         total_products=total_products,
                         total_users=total_users)
```

#### 9.2 管理功能
- 商品管理（CRUD操作）
- 订单管理（查看、更新状态）
- 用户管理（查看、禁用）
- 销售统计（简单报表）

### 第10步：邮件发送配置

#### 10.1 设置邮件服务
以Gmail为例：
1. 开启两步验证
2. 生成应用专用密码
3. 在 `.env` 文件中配置：
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

#### 10.2 发送订单确认邮件
在 `app/utils/helpers.py` 中创建邮件发送函数：
```python
from flask_mail import Message
from app.extensions import mail
from threading import Thread

def send_async_email(app, msg):
    """异步发送邮件"""
    with app.app_context():
        mail.send(msg)

def send_order_confirmation_email(order):
    """发送订单确认邮件"""
    msg = Message(
        '订单确认',
        sender='your-email@gmail.com',
        recipients=[order.user.email]
    )
    msg.html = render_template('email/order_confirmation.html', order=order)

    # 异步发送
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()
```

## 开发顺序建议

1. **第1周**: 完成步骤1-3（环境搭建、数据库设计）
2. **第2周**: 完成步骤4-5（Flask初始化、用户认证）
3. **第3周**: 完成步骤6-7（商品和购物车）
4. **第4周**: 完成步骤8-10（订单、管理、邮件）

## 运行项目

### 初始化数据库
```bash
# 使用uv运行初始化脚本
uv run python init_db.py
```

### 启动开发服务器
```bash
# 使用uv运行Flask应用
uv run python main.py
```

应用将在 http://127.0.0.1:5000 上运行。

### 测试账号
- **管理员**：
  - 用户名：admin
  - 密码：admin123

## uv 常用命令

```bash
# 项目初始化
uv init                          # 初始化新项目

# 依赖管理
uv add flask                     # 添加依赖到 pyproject.toml
uv add --dev pytest              # 添加开发依赖
uv remove flask                  # 移除依赖
uv sync                          # 同步安装所有依赖

# 运行代码
uv run python main.py            # 运行 Python 文件
uv run flask run                 # 运行 Flask 命令

# 查看信息
uv tree                          # 查看依赖树
uv pip list                      # 列出已安装的包
```

## 常见问题与解决方案

### 1. 数据库连接问题
**错误信息**：`pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")`

**解决方案**：
- 确保MySQL服务已启动
  - Windows: `net start mysql`
  - macOS/Linux: `sudo systemctl start mysql`
- 检查 `.env` 文件中的数据库配置是否正确
- 确认数据库 `shop_db` 已创建

### 2. 找不到模块错误
**错误信息**：`ModuleNotFoundError: No module named 'app'`

**解决方案**：
- 确保在项目根目录运行命令
- 使用 `uv run python main.py` 而不是直接 `python main.py`
- 检查 `__init__.py` 文件是否已创建

### 3. 模板渲染错误
**错误信息**：`jinja2.exceptions.TemplateNotFound`

**解决方案**：
- 检查模板文件路径是否在 `app/templates/` 目录下
- 确认Jinja2语法正确
- 查看Flask错误日志

### 4. 静态文件404错误
**解决方案**：
- 确保static文件夹在 `app/static/` 路径下
- 使用 `url_for('static', filename='css/style.css')` 生成URL
- 检查文件名拼写

### 5. 登录问题
**解决方案**：
- 确保密码正确加密存储（使用 `set_password()` 方法）
- 检查 `app/extensions.py` 中的用户加载器是否正确配置
- 验证 SECRET_KEY 是否已设置

### 6. 表单CSRF错误
**错误信息**：`CSRF token missing`

**解决方案**：
- 确保表单中有 `{{ form.hidden_tag() }}`
- 检查 SECRET_KEY 配置

## 调试技巧

### 1. 使用Flask调试模式
在 `config.py` 中已配置：
```python
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # 显示SQL语句
```

### 2. 打印调试信息
```python
from flask import current_app

# 在路由中使用
current_app.logger.info('调试信息')
current_app.logger.error('错误信息')
```

### 3. 数据库查询调试
当 `SQLALCHEMY_ECHO = True` 时，所有SQL语句会在控制台输出。

### 4. 使用Python调试器
```python
# 在代码中插入断点
import pdb; pdb.set_trace()
```

或在VSCode中设置断点进行调试。

## 部署准备

### 1. 生产环境配置
修改 `.env` 文件：
```env
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-very-secure-random-key-here
```

### 2. 部署步骤
1. 购买云服务器（推荐使用Ubuntu）
2. 安装必要的软件：
   ```bash
   # 安装Python和uv
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   pip install uv

   # 安装MySQL
   sudo apt install mysql-server

   # 安装Nginx
   sudo apt install nginx
   ```
3. 上传代码到服务器
4. 配置Gunicorn（作为WSGI服务器）
5. 配置Nginx作为反向代理
6. 设置域名和SSL证书（Let's Encrypt）

## 学习建议

### 1. 先理解，后实现
- 不要直接复制代码，先理解原理
- 按照指南自己实现，遇到问题再查看详细版文档
- 尝试修改和改进代码

### 2. 遇到问题时的求助方式
- 先尝试自己解决
- 查看Flask官方文档：https://flask.palletsprojects.com/
- 搜索错误信息
- 询问具体问题，而不是要完整代码

### 3. 记录学习过程
- 记录遇到的问题和解决方案
- 为实验报告积累素材
- 截图保存重要步骤

## 实验报告准备

在开发过程中注意收集：
1. **设计思路的演进**
   - 数据库ER图
   - 功能模块划分
   - 技术选型理由

2. **关键代码的实现**
   - 用户认证流程
   - 购物车逻辑
   - 订单处理流程
   - 难点解决方案

3. **功能测试截图**
   - 注册/登录页面
   - 商品列表/详情页
   - 购物车页面
   - 订单页面
   - 管理员后台

4. **部署过程记录**
   - 环境配置
   - 遇到的问题
   - 解决方案