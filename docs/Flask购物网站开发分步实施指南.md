# Flask购物网站开发分步实施指南

## 项目概述

这是一个基于Flask框架的在线购物网站项目，满足课程实验要求。通过本指南，你将一步步完成整个项目的开发，学到完整的Web应用开发流程。

## 技术栈

- **后端**: Python 3 + Flask
- **数据库**: MySQL + Flask-SQLAlchemy (ORM)
- **前端**: HTML5 + CSS3 + Bootstrap 5 + 少量JavaScript
- **认证**: Flask-Login
- **邮件**: Flask-Mail
- **部署**: Gunicorn + Nginx

## 开发环境准备

### 第1步：安装必要软件

#### 1.1 安装Python和包管理器
```bash
# 如果没有安装Python，从 https://python.org 下载Python 3.8+
# 安装uv包管理器（推荐）
pip install uv
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
- Live Server（用于前端调试）

### 第2步：项目初始化

#### 2.1 创建项目目录结构
```
flask_shop_system/
├── app/
│   ├── __init__.py         # Flask应用初始化
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
│   │   └── admin.py        # 管理员路由
│   ├── templates/          # HTML模板
│   │   ├── base.html       # 基础模板
│   │   ├── auth/           # 认证相关模板
│   │   ├── main/           # 主要页面模板
│   │   ├── product/        # 商品相关模板
│   │   ├── cart/           # 购物车模板
│   │   └── admin/          # 管理员页面模板
│   └── static/             # 静态文件
│       ├── css/
│       ├── js/
│       └── images/
├── migrations/             # 数据库迁移文件
├── config.py              # 配置文件
├── requirements.txt       # Python依赖
├── run.py                # 应用启动入口
└── README.md             # 项目说明
```

#### 2.2 创建虚拟环境和依赖文件
```bash
# 创建项目目录
mkdir flask_shop_system
cd flask_shop_system

# 初始化uv项目
uv init

# 创建依赖文件
cat > requirements.txt << EOF
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-Mail==0.9.1
Flask-Migrate==4.0.5
Werkzeug==2.3.7
PyMySQL==1.1.0
cryptography==41.0.4
python-dotenv==1.0.0
EOF

# 安装依赖
uv pip install -r requirements.txt
```

## 核心功能开发步骤

### 第3步：数据库设计与建模

#### 3.1 理解数据库设计原则
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

**商品表 (products)**
- id: 主键
- name: 商品名称
- description: 商品描述
- price: 价格
- stock: 库存数量
- image_url: 商品图片URL
- created_at: 创建时间

**购物车表 (cart_items)**
- id: 主键
- user_id: 用户ID（外键）
- product_id: 商品ID（外键）
- quantity: 数量
- created_at: 添加时间

**订单表 (orders)**
- id: 主键
- user_id: 用户ID（外键）
- total_amount: 总金额
- status: 订单状态（待支付/已支付/已发货/已完成）
- created_at: 创建时间

**订单明细表 (order_items)**
- id: 主键
- order_id: 订单ID（外键）
- product_id: 商品ID（外键）
- quantity: 数量
- price: 下单时的价格

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
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# 这里需要导入db实例，具体在app/__init__.py中初始化

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 建立与其他表的关系
    orders = db.relationship('Order', backref='user', lazy=True)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)

    def set_password(self, password):
        """设置密码（加密存储）"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
```

**你需要自己实现其他模型文件：**
- `app/models/product.py` - 商品模型
- `app/models/order.py` - 订单和订单明细模型
- `app/models/cart.py` - 购物车模型

### 第4步：Flask应用初始化

#### 4.1 创建配置文件 (config.py)
```python
import os
from datetime import timedelta

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://username:password@localhost/shop_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 邮件配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # 会话配置
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

#### 4.2 创建Flask应用工厂 (app/__init__.py)
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from config import config

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # 设置登录视图
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'

    # 注册蓝图
    from app.routes import auth_bp, main_bp, product_bp, cart_bp, admin_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
```

### 第5步：用户认证系统

#### 5.1 理解Flask-Login工作原理
- `LoginManager` 管理用户会话
- `@login_required` 装饰器保护需要登录的路由
- `UserMixin` 提供默认的用户会话方法

#### 5.2 实现认证路由 (app/routes/auth.py)

创建路由蓝图：
```python
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 验证逻辑（需要你实现）
        # 1. 检查用户名是否已存在
        # 2. 检查邮箱是否已存在
        # 3. 验证密码确认
        # 4. 创建新用户并保存到数据库

        flash('注册成功！请登录', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 获取表单数据并验证
        # 实现登录逻辑
        pass

    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录', 'info')
    return redirect(url_for('main.index'))
```

#### 5.3 创建认证模板
- `templates/auth/register.html` - 注册页面
- `templates/auth/login.html` - 登录页面

**基础模板结构示例 (templates/base.html):**
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask购物网站{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('main.index') }}">购物网站</a>

            <div class="navbar-nav ms-auto">
                {% if current_user.is_authenticated %}
                    <a class="nav-link" href="{{ url_for('cart.index') }}">购物车</a>
                    <a class="nav-link" href="{{ url_for('auth.logout') }}">退出</a>
                {% else %}
                    <a class="nav-link" href="{{ url_for('auth.login') }}">登录</a>
                    <a class="nav-link" href="{{ url_for('auth.register') }}">注册</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

### 第6步：商品展示与管理

#### 6.1 商品路由实现 (app/routes/product.py)
需要实现的功能：
- 商品列表展示
- 商品详情页
- 商品搜索（可选）
- 管理员添加/编辑/删除商品

#### 6.2 商品模板
- `templates/product/list.html` - 商品列表
- `templates/product/detail.html` - 商品详情
- `templates/admin/product_form.html` - 商品添加/编辑表单

### 第7步：购物车功能

#### 7.1 购物车逻辑理解
购物车数据可以存储在：
- 数据库（持久化，适合登录用户）
- Session（临时，适合游客）
本项目建议使用数据库存储

#### 7.2 购物车实现要点
- 添加商品到购物车
- 修改商品数量
- 删除购物车商品
- 清空购物车

### 第8步：订单系统

#### 8.1 订单流程
1. 用户从购物车点击"结算"
2. 确认订单信息
3. 创建订单（从购物车数据）
4. 清空购物车
5. 发送确认邮件

#### 8.2 订单状态管理
- 待支付
- 已支付
- 已发货
- 已完成
- 已取消

### 第9步：管理员功能

#### 9.1 权限验证
使用装饰器检查管理员权限：
```python
from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
```

#### 9.2 管理功能
- 商品管理
- 订单管理
- 销售统计（简单报表）

### 第10步：邮件发送配置

#### 10.1 设置邮件服务
以Gmail为例：
1. 开启两步验证
2. 生成应用专用密码
3. 配置环境变量

#### 10.2 发送订单确认邮件
```python
from flask_mail import Message
from app import mail

def send_order_confirmation_email(order):
    msg = Message(
        '订单确认',
        sender='your-email@gmail.com',
        recipients=[order.user.email]
    )
    msg.body = f'''
    亲爱的{order.user.username}，

    您的订单已确认！
    订单号：{order.id}
    总金额：¥{order.total_amount}

    谢谢您的购买！
    '''
    mail.send(msg)
```

## 开发顺序建议

1. **第1周**: 完成步骤1-3（环境搭建、数据库设计）
2. **第2周**: 完成步骤4-5（Flask初始化、用户认证）
3. **第3周**: 完成步骤6-7（商品和购物车）
4. **第4周**: 完成步骤8-10（订单、管理、邮件）

## 常见问题与解决方案

### 1. 数据库连接问题
- 确保MySQL服务已启动
- 检查用户名密码是否正确
- 确认数据库已创建

### 2. 模板渲染错误
- 检查模板文件路径
- 确认Jinja2语法正确
- 查看Flask错误日志

### 3. 静态文件404
- 确认static文件夹结构
- 检查url_for()使用是否正确

### 4. 登录问题
- 确保密码正确加密存储
- 检查session配置
- 验证login_manager设置

## 调试技巧

1. **使用Flask调试模式**
   ```python
   app.run(debug=True)
   ```

2. **打印调试信息**
   ```python
   app.logger.info('调试信息')
   ```

3. **数据库查询调试**
   ```python
   # 打印SQL语句
   from sqlalchemy import event
   from sqlalchemy.engine import Engine
   @event.listens_for(Engine, "before_cursor_execute")
   def receive_before_cursor_execute(conn, cursor, statement, ...):
       print("SQL:", statement)
   ```

## 部署准备

1. **生产环境配置**
   - 关闭调试模式
   - 使用环境变量存储敏感信息
   - 配置HTTPS

2. **部署步骤**
   - 购买云服务器
   - 安装必要的软件
   - 上传代码
   - 配置Nginx和Gunicorn
   - 设置域名和SSL证书

## 学习建议

1. **先理解，后实现**
   - 不要直接复制代码
   - 理解每个功能的作用
   - 尝试自己实现

2. **遇到问题时的求助方式**
   - 先尝试自己解决
   - 查看官方文档
   - 询问具体问题，而不是要完整代码

3. **记录学习过程**
   - 记录遇到的问题和解决方案
   - 为实验报告积累素材

## 实验报告准备

在开发过程中注意收集：
1. 设计思路的演进
2. 关键代码的实现
3. 功能测试截图
4. 部署过程记录

记住，这个指南的目的是帮助你学习，而不是替你完成。每个步骤都值得你深入理解和实践！