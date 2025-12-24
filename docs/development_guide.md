# Flask购物网站开发详细指南

## 📋 项目概述

**项目名称**：Flask在线购物网站
**技术栈**：Flask + MySQL + SQLAlchemy + Bootstrap + HTML/CSS
**核心功能**：用户注册登录、商品展示、购物车、订单管理、管理员后台
**开发时间**：建议4周完成

---

## 🎯 学习目标

通过这个项目，你将学习到：
- Flask Web框架的深入使用（蓝图、工厂模式、扩展集成）
- MySQL数据库设计与ORM映射
- 用户认证与会话管理
- 购物车与订单系统的实现
- 邮件发送功能
- 文件上传处理
- Bootstrap前端框架的使用
- Web应用的部署

---

## 📂 项目结构规划

```
flask_shop_system/
├── app/
│   ├── __init__.py             # Flask应用工厂
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py            # 用户模型
│   │   ├── product.py         # 商品模型
│   │   ├── order.py           # 订单模型
│   │   └── cart.py            # 购物车模型
│   ├── routes/                # 路由蓝图
│   │   ├── __init__.py
│   │   ├── auth.py            # 认证路由
│   │   ├── main.py            # 主页路由
│   │   ├── product.py         # 商品路由
│   │   ├── cart.py            # 购物车路由
│   │   ├── order.py           # 订单路由
│   │   └── admin.py           # 管理员路由
│   ├── templates/             # HTML模板
│   │   ├── base.html          # 基础模板
│   │   ├── auth/              # 认证模板
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   └── profile.html
│   │   ├── main/              # 主页模板
│   │   │   └── index.html
│   │   ├── product/           # 商品模板
│   │   │   ├── list.html
│   │   │   └── detail.html
│   │   ├── cart/              # 购物车模板
│   │   │   └── cart.html
│   │   ├── order/             # 订单模板
│   │   │   ├── checkout.html
│   │   │   └── orders.html
│   │   └── admin/             # 管理员模板
│   │       ├── dashboard.html
│   │       ├── products.html
│   │       └── orders.html
│   ├── static/                # 静态文件
│   │   ├── css/
│   │   │   └── style.css      # 自定义样式
│   │   ├── js/
│   │   │   └── main.js        # JavaScript文件
│   │   └── images/            # 图片资源
│   │       └── uploads/       # 用户上传图片
│   ├── utils/                 # 工具函数
│   │   ├── __init__.py
│   │   ├── decorators.py      # 装饰器
│   │   └── helpers.py         # 辅助函数
│   └── extensions.py          # Flask扩展初始化
├── migrations/                # 数据库迁移文件
├── config.py                  # 配置文件
├── pyproject.toml             # 项目配置和依赖管理
├── run.py                     # 应用启动文件
├── .env                       # 环境变量文件
├── .gitignore                 # Git忽略文件
└── README.md                  # 项目说明
```

---

## 🚀 开发阶段详细步骤

### **阶段一：环境准备与项目初始化（第1周）**

#### 步骤 1.1：安装必要软件

##### 1.1.1 安装Python和包管理器
```bash
# 从 https://python.org 下载Python 3.8+ （推荐3.10）
# 验证安装
python --version

# 安装uv包管理器（比pip更快速）
pip install uv

# 验证uv安装
uv --version
```

##### 1.1.2 安装MySQL数据库

**Windows:**
1. 下载MySQL Community Server：https://dev.mysql.com/downloads/mysql/
2. 安装时记住root密码
3. 配置环境变量

**macOS:**
```bash
# 使用Homebrew安装
brew install mysql
brew services start mysql

# 设置root密码
mysql_secure_installation
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo mysql_secure_installation
```

##### 1.1.3 安装代码编辑器和插件

推荐使用 VS Code，安装以下插件：
- Python
- Pylance（Python语言服务器）
- MySQL
- Live Server
- GitLens

#### 步骤 1.2：创建项目基础结构

##### 1.2.1 创建项目目录
```bash
# 创建项目根目录
mkdir flask_shop_system
cd flask_shop_system

# 使用uv初始化项目（自动生成pyproject.toml）
uv init

# 创建必要的目录结构
mkdir -p app/{models,routes,templates/{auth,main,product,cart,order,admin},static/{css,js,images/uploads},utils}
mkdir migrations
```

##### 1.2.2 创建基础空文件
```bash
# 创建所有必要的Python文件
touch app/__init__.py
touch app/extensions.py
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
touch run.py
touch .env
touch .gitignore
```

#### 步骤 1.3：配置项目依赖

使用 `uv add` 命令添加依赖，它会自动更新 `pyproject.toml` 和 `uv.lock` 文件：

```bash
# 添加核心Flask依赖
uv add Flask Flask-SQLAlchemy Flask-Login Flask-Mail Flask-Migrate Flask-WTF
uv add Werkzeug PyMySQL cryptography python-dotenv Pillow email-validator WTForms

# 添加开发依赖
uv add --dev pytest pytest-flask black flake8

# 查看已安装的依赖
uv tree

# 同步安装所有依赖
uv sync
```

**说明**：
- `uv add` 会自动将依赖添加到 `pyproject.toml` 的 `dependencies` 部分
- `uv add --dev` 会将依赖添加到 `dev-dependencies` 部分
- `uv.lock` 文件会自动更新，锁定具体的依赖版本
- 无需手动编辑 `pyproject.toml` 文件

##### 1.3.1 uv 常用命令说明

```bash
# 项目初始化
uv init                          # 初始化新项目
uv init flask-shop-system        # 指定项目名称

# 依赖管理
uv add flask                     # 添加依赖到 pyproject.toml
uv add --dev pytest              # 添加开发依赖
uv remove flask                  # 移除依赖
uv sync                          # 同步安装所有依赖

# 运行代码
uv run python run.py             # 运行 Python 文件
uv run flask run                 # 运行 Flask 命令

# 脚本管理（可在 pyproject.toml 中定义）
uv run init-db                   # 运行自定义脚本

# 查看信息
uv tree                          # 查看依赖树
uv pip list                      # 列出已安装的包
```

#### 步骤 1.4：配置Git版本控制

创建 `.gitignore` 文件：
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.env

# uv
.venv/
uv.lock

# Flask
instance/
.webassets-cache

# Database
*.db
*.sqlite
*.sqlite3

# Migrations
migrations/versions/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Uploads
app/static/images/uploads/*
!app/static/images/uploads/.gitkeep
```

创建上传目录的占位文件：
```bash
touch app/static/images/uploads/.gitkeep
```

#### 步骤 1.5：创建数据库

使用MySQL命令行创建数据库：

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

**注意**：
- 将 `ShopPass456@secure` 替换为你自己的密码
- 创建专用用户比直接使用 root 更安全
- 记住这个密码，后面配置 `.env` 时会用到

---

### **阶段二：数据库设计与建模（第1-2周）**

#### 步骤 2.1：设计数据库表结构

##### 2.1.1 理解数据库设计原则

**ORM（对象关系映射）概念：**
- 让你用Python类操作数据库表
- 自动生成SQL语句
- 提供数据库迁移支持

**表关系类型：**
- 一对多（One-to-Many）：一个用户可以有多个订单
- 多对多（Many-to-Many）：订单和商品的关系（通过订单明细表）

##### 2.1.2 设计数据库表

**用户表 (users)**
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**商品表 (products)**
```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    image_url VARCHAR(300),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**购物车表 (cart_items)**
```sql
CREATE TABLE cart_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_product (user_id, product_id)
);
```

**订单表 (orders)**
```sql
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'paid', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    shipping_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**订单明细表 (order_items)**
```sql
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

#### 步骤 2.2：实现数据模型

##### 2.2.1 创建Flask扩展配置文件

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
```

##### 2.2.2 创建用户模型

编辑 `app/models/user.py`：
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
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # 关系定义
    orders = db.relationship('Order', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    cart_items = db.relationship('CartItem', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """设置密码（加密存储）"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def get_cart_items(self):
        """获取用户的购物车商品"""
        return self.cart_items.all()

    def get_cart_total(self):
        """计算购物车总价"""
        total = 0
        for item in self.cart_items:
            total += item.product.price * item.quantity
        return total
```

##### 2.2.3 创建商品模型

编辑 `app/models/product.py`：
```python
from datetime import datetime, timezone
from app.extensions import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(300))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # 关系定义
    cart_items = db.relationship('CartItem', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')

    def __repr__(self):
        return f'<Product {self.name}>'

    def is_in_stock(self, quantity=1):
        """检查库存是否充足"""
        return self.stock >= quantity

    def reduce_stock(self, quantity):
        """减少库存"""
        if self.is_in_stock(quantity):
            self.stock -= quantity
            db.session.commit()
            return True
        return False

    def get_image_url(self):
        """获取图片URL，如果没有则返回默认图片"""
        if self.image_url:
            return self.image_url
        return url_for('static', filename='images/default-product.png')
```

##### 2.2.4 创建购物车模型

编辑 `app/models/cart.py`：
```python
from datetime import datetime, timezone
from app.extensions import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # 创建唯一约束，防止重复添加
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_user_product'),)

    def __repr__(self):
        return f'<CartItem {self.product.name} x {self.quantity}>'

    def get_subtotal(self):
        """计算小计金额"""
        return self.product.price * self.quantity

    @staticmethod
    def get_or_create(user_id, product_id):
        """获取或创建购物车项"""
        item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
        if not item:
            item = CartItem(user_id=user_id, product_id=product_id)
            db.session.add(item)
        return item
```

##### 2.2.5 创建订单模型

编辑 `app/models/order.py`：
```python
from datetime import datetime, timezone
from app.extensions import db
import uuid

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('pending', 'paid', 'shipped', 'delivered', 'cancelled',
                            name='order_status'), default='pending')
    shipping_address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # 关系定义
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.order_number:
            self.order_number = self.generate_order_number()

    def __repr__(self):
        return f'<Order {self.order_number}>'

    @staticmethod
    def generate_order_number():
        """生成唯一订单号"""
        return f"ORD{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"

    def get_status_display(self):
        """获取订单状态显示文本"""
        status_map = {
            'pending': '待支付',
            'paid': '已支付',
            'shipped': '已发货',
            'delivered': '已完成',
            'cancelled': '已取消'
        }
        return status_map.get(self.status, '未知')

    def can_cancel(self):
        """检查是否可以取消订单"""
        return self.status in ['pending', 'paid']

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # 下单时的价格

    def __repr__(self):
        return f'<OrderItem {self.product.name} x {self.quantity}>'

    def get_subtotal(self):
        """计算小计金额"""
        return self.price * self.quantity
```

##### 2.2.6 更新模型初始化文件

编辑 `app/models/__init__.py`：
```python
from .user import User
from .product import Product
from .order import Order, OrderItem
from .cart import CartItem

__all__ = ['User', 'Product', 'Order', 'OrderItem', 'CartItem']
```

#### 步骤 2.3：配置应用

##### 2.3.1 创建配置文件

编辑 `config.py`：
```python
import os
from datetime import timedelta

class Config:
    """基础配置类"""
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change-in-production'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:password@localhost/shop_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # 设为True可以看到SQL语句

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

    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        # 确保上传目录存在
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

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

##### 2.3.2 创建环境变量文件

**重要提示**：`.env` 文件包含敏感信息，已配置在 `.gitignore` 中，不会提交到 Git。

创建 `.env` 文件（复制示例文件）：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入真实配置：
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

**说明**：
- 将 `ShopPass456@secure` 替换为你在步骤 1.5 中设置的密码
- 将 `your-super-secret-key-here` 替换为一个随机字符串
- `.env` 文件不会被提交到 Git，所以可以安全地存储密码

#### 步骤 2.4：创建Flask应用工厂

##### 2.4.1 编辑应用初始化文件

编辑 `app/__init__.py`：
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

    # 注册模板上下文处理器
    register_template_context(app)

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
        """在所有模板中注入购物车数量"""
        from flask_login import current_user
        if current_user.is_authenticated:
            count = models.CartItem.query.filter_by(user_id=current_user.id).count()
            return dict(cart_count=count)
        return dict(cart_count=0)
```

##### 2.4.2 编辑应用启动文件

编辑 `run.py`：
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

---

### **阶段三：用户认证系统（第2周）**

#### 步骤 3.1：创建工具函数

##### 3.1.1 创建装饰器

编辑 `app/utils/decorators.py`：
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

##### 3.1.2 创建辅助函数

编辑 `app/utils/helpers.py`：
```python
from flask import current_app
from werkzeug.utils import secure_filename
import os
import uuid

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file, folder='uploads'):
    """保存上传的文件"""
    if file and allowed_file(file.filename):
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        # 添加UUID前缀防止重复
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        # 保存文件
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(upload_path)
        # 返回相对路径
        return f"images/uploads/{unique_filename}"
    return None

def format_currency(amount):
    """格式化货币显示"""
    return f"¥{amount:,.2f}"

def pagination_url(page):
    """生成分页URL"""
    return request.args.copy().update(page=page)
```

#### 步骤 3.2：实现认证路由

##### 3.2.1 创建表单类

创建 `app/forms.py`：
```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, IntegerField, DecimalField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_wtf.file import FileAllowed, FileRequired
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

class ProfileForm(FlaskForm):
    """个人信息表单"""
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    submit = SubmitField('更新')

class PasswordChangeForm(FlaskForm):
    """修改密码表单"""
    old_password = PasswordField('当前密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(),
        Length(min=6, message='密码至少6个字符')
    ])
    password2 = PasswordField('确认新密码', validators=[
        DataRequired(),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    submit = SubmitField('修改密码')
```

##### 3.2.2 编辑认证路由

编辑 `app/routes/auth.py`：
```python
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User
from app.forms import LoginForm, RegistrationForm, ProfileForm, PasswordChangeForm
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

@auth_bp.route('/profile')
@login_required
def profile():
    """个人信息页面"""
    return render_template('auth/profile.html')

@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """编辑个人信息"""
    form = ProfileForm()
    if form.validate_on_submit():
        # 检查邮箱是否已被其他用户使用
        if form.email.data != current_user.email:
            if User.query.filter_by(email=form.email.data).first():
                flash('该邮箱已被其他用户使用', 'danger')
                return render_template('auth/edit_profile.html', form=form)

        current_user.email = form.email.data
        db.session.commit()
        flash('个人信息已更新', 'success')
        return redirect(url_for('auth.profile'))

    # 预填充表单
    form.email.data = current_user.email
    return render_template('auth/edit_profile.html', form=form)

@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """修改密码"""
    form = PasswordChangeForm()
    if form.validate_on_submit():
        # 验证当前密码
        if not current_user.check_password(form.old_password.data):
            flash('当前密码错误', 'danger')
            return render_template('auth/change_password.html', form=form)

        # 设置新密码
        current_user.set_password(form.password.data)
        db.session.commit()

        flash('密码修改成功，请重新登录', 'success')
        logout_user()
        return redirect(url_for('auth.login'))

    return render_template('auth/change_password.html', form=form)
```

#### 步骤 3.3：创建认证模板

##### 3.3.1 创建基础模板

创建 `app/templates/base.html`：
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

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('main.index') }}">首页</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('product.list') }}">商品</a>
                    </li>
                </ul>

                <ul class="navbar-nav">
                    <!-- 搜索框 -->
                    <li class="nav-item">
                        <form class="d-flex me-3" action="{{ url_for('product.search') }}" method="GET">
                            <input class="form-control me-2" type="search" name="q" placeholder="搜索商品..."
                                   value="{{ request.args.get('q', '') }}">
                            <button class="btn btn-outline-light" type="submit">
                                <i class="fas fa-search"></i>
                            </button>
                        </form>
                    </li>

                    <!-- 购物车 -->
                    {% if current_user.is_authenticated %}
                    <li class="nav-item">
                        <a class="nav-link position-relative" href="{{ url_for('cart.index') }}">
                            <i class="fas fa-shopping-cart"></i> 购物车
                            {% if cart_count > 0 %}
                            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                {{ cart_count }}
                            </span>
                            {% endif %}
                        </a>
                    </li>
                    {% endif %}

                    <!-- 用户菜单 -->
                    {% if current_user.is_authenticated %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button"
                           data-bs-toggle="dropdown">
                            <i class="fas fa-user"></i> {{ current_user.username }}
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="{{ url_for('auth.profile') }}">个人中心</a></li>
                            <li><a class="dropdown-item" href="{{ url_for('order.orders') }}">我的订单</a></li>
                            {% if current_user.is_admin %}
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="{{ url_for('admin.dashboard') }}">管理后台</a></li>
                            {% endif %}
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="{{ url_for('auth.logout') }}">退出登录</a></li>
                        </ul>
                    </li>
                    {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('auth.login') }}">登录</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('auth.register') }}">注册</a>
                    </li>
                    {% endif %}
                </ul>
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
            <div class="row">
                <div class="col-md-4">
                    <h5>关于我们</h5>
                    <p>这是一个基于Flask开发的购物网站演示项目。</p>
                </div>
                <div class="col-md-4">
                    <h5>快速链接</h5>
                    <ul class="list-unstyled">
                        <li><a href="{{ url_for('main.index') }}" class="text-light">首页</a></li>
                        <li><a href="{{ url_for('product.list') }}" class="text-light">商品</a></li>
                        <li><a href="{{ url_for('main.about') }}" class="text-light">关于我们</a></li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h5>联系方式</h5>
                    <p><i class="fas fa-envelope"></i> contact@shop.com</p>
                    <p><i class="fas fa-phone"></i> 123-456-7890</p>
                </div>
            </div>
            <hr class="mt-4">
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

##### 3.3.2 创建登录页面

创建 `app/templates/auth/login.html`：
```html
{% extends "base.html" %}

{% block title %}登录 - Flask购物网站{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow">
            <div class="card-header bg-primary text-white text-center">
                <h4 class="mb-0">
                    <i class="fas fa-sign-in-alt"></i> 用户登录
                </h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {{ form.hidden_tag() }}

                    <!-- 用户名 -->
                    <div class="mb-3">
                        {{ form.username.label(class="form-label") }}
                        {{ form.username(class="form-control") }}
                        {% if form.username.errors %}
                            {% for error in form.username.errors %}
                                <div class="text-danger small">{{ error }}</div>
                            {% endfor %}
                        {% endif %}
                    </div>

                    <!-- 密码 -->
                    <div class="mb-3">
                        {{ form.password.label(class="form-label") }}
                        <div class="input-group">
                            {{ form.password(class="form-control", id="password") }}
                            <button class="btn btn-outline-secondary" type="button" onclick="togglePassword()">
                                <i class="fas fa-eye" id="password-icon"></i>
                            </button>
                        </div>
                        {% if form.password.errors %}
                            {% for error in form.password.errors %}
                                <div class="text-danger small">{{ error }}</div>
                            {% endfor %}
                        {% endif %}
                    </div>

                    <!-- 记住我 -->
                    <div class="mb-3 form-check">
                        {{ form.remember_me(class="form-check-input") }}
                        {{ form.remember_me.label(class="form-check-label") }}
                    </div>

                    <!-- 提交按钮 -->
                    <div class="d-grid gap-2">
                        {{ form.submit(class="btn btn-primary") }}
                    </div>
                </form>
            </div>
            <div class="card-footer text-center">
                <p class="mb-0">
                    还没有账号？
                    <a href="{{ url_for('auth.register') }}">立即注册</a>
                </p>
            </div>
        </div>
    </div>
</div>

<script>
function togglePassword() {
    const passwordField = document.getElementById('password');
    const icon = document.getElementById('password-icon');

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordField.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}
</script>
{% endblock %}
```

##### 3.3.3 创建注册页面

创建 `app/templates/auth/register.html`：
```html
{% extends "base.html" %}

{% block title %}注册 - Flask购物网站{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-5">
        <div class="card shadow">
            <div class="card-header bg-success text-white text-center">
                <h4 class="mb-0">
                    <i class="fas fa-user-plus"></i> 用户注册
                </h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {{ form.hidden_tag() }}

                    <!-- 用户名 -->
                    <div class="mb-3">
                        {{ form.username.label(class="form-label") }}
                        {{ form.username(class="form-control") }}
                        <div class="form-text">4-20个字符，支持字母、数字和下划线</div>
                        {% if form.username.errors %}
                            {% for error in form.username.errors %}
                                <div class="text-danger small">{{ error }}</div>
                            {% endfor %}
                        {% endif %}
                    </div>

                    <!-- 邮箱 -->
                    <div class="mb-3">
                        {{ form.email.label(class="form-label") }}
                        {{ form.email(class="form-control") }}
                        {% if form.email.errors %}
                            {% for error in form.email.errors %}
                                <div class="text-danger small">{{ error }}</div>
                            {% endfor %}
                        {% endif %}
                    </div>

                    <!-- 密码 -->
                    <div class="mb-3">
                        {{ form.password.label(class="form-label") }}
                        {{ form.password(class="form-control", id="password") }}
                        <div class="form-text">至少6个字符</div>
                        {% if form.password.errors %}
                            {% for error in form.password.errors %}
                                <div class="text-danger small">{{ error }}</div>
                            {% endfor %}
                        {% endif %}
                    </div>

                    <!-- 确认密码 -->
                    <div class="mb-3">
                        {{ form.password2.label(class="form-label") }}
                        {{ form.password2(class="form-control", id="password2") }}
                        {% if form.password2.errors %}
                            {% for error in form.password2.errors %}
                                <div class="text-danger small">{{ error }}</div>
                            {% endfor %}
                        {% endif %}
                    </div>

                    <!-- 提交按钮 -->
                    <div class="d-grid gap-2">
                        {{ form.submit(class="btn btn-success") }}
                    </div>
                </form>
            </div>
            <div class="card-footer text-center">
                <p class="mb-0">
                    已有账号？
                    <a href="{{ url_for('auth.login') }}">立即登录</a>
                </p>
            </div>
        </div>
    </div>
</div>

<script>
// 实时检查密码确认
document.getElementById('password2').addEventListener('input', function() {
    const password = document.getElementById('password').value;
    const password2 = this.value;

    if (password2 && password !== password2) {
        this.setCustomValidity('两次输入的密码不一致');
    } else {
        this.setCustomValidity('');
    }
});
</script>
{% endblock %}
```

---

## 🔧 常用Python语法和技巧

### 1. Flask路由和视图函数

```python
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

# 创建蓝图
bp = Blueprint('main', __name__)

# 基础路由
@bp.route('/')
def index():
    return render_template('index.html')

# 带参数的路由
@bp.route('/user/<username>')
def user_profile(username):
    return f'用户: {username}'

# 支持GET和POST的路由
@bp.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # 获取表单数据
        data = request.form.get('data')
        flash('提交成功！', 'success')
        return redirect(url_for('main.index'))

    return render_template('submit.html')

# 需要登录的路由
@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
```

### 2. SQLAlchemy数据库操作

```python
from app.extensions import db
from app.models import User, Product

# 查询操作
# 获取所有用户
users = User.query.all()

# 获取单个用户
user = User.query.get(1)  # 通过ID
user = User.query.filter_by(username='admin').first()

# 条件查询
products = Product.query.filter(
    Product.price > 100,
    Product.stock > 0
).order_by(Product.created_at.desc()).limit(10).all()

# 模糊查询
products = Product.query.filter(
    Product.name.like('%手机%')
).all()

# 创建记录
user = User(username='test', email='test@example.com')
user.set_password('password123')
db.session.add(user)
db.session.commit()

# 更新记录
user = User.query.get(1)
user.email = 'new@example.com'
db.session.commit()

# 删除记录
user = User.query.get(1)
db.session.delete(user)
db.session.commit()

# 使用上下文管理器确保事务安全
try:
    user = User(username='test', email='test@example.com')
    db.session.add(user)
    db.session.commit()
except:
    db.session.rollback()
    raise
```

### 3. Flask-Login用户认证

```python
from flask_login import login_user, logout_user, login_required, current_user

# 登录用户
user = User.query.filter_by(username=form.username.data).first()
if user and user.check_password(form.password.data):
    login_user(user, remember=form.remember_me.data)
    flash('登录成功', 'success')

# 登出用户
logout_user()
flash('已退出登录', 'info')

# 检查用户状态
from flask_login import current_user

if current_user.is_authenticated:
    # 用户已登录
    print(f'当前用户: {current_user.username}')
    if current_user.is_admin:
        print('管理员用户')
else:
    # 用户未登录
    print('游客访问')
```

### 4. 表单验证（WTForms）

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=20, message='用户名长度为3-20个字符')
    ])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

# 在视图函数中使用
form = LoginForm()
if form.validate_on_submit():
    # 处理表单数据
    username = form.username.data
    password = form.password.data

# 在模板中渲染
<form method="POST">
    {{ form.hidden_tag() }}
    {{ form.username.label }} {{ form.username(class="form-control") }}
    {% if form.username.errors %}
        {% for error in form.username.errors %}
            <div class="text-danger">{{ error }}</div>
        {% endfor %}
    {% endif %}
    {{ form.submit(class="btn btn-primary") }}
</form>
```

### 5. 文件上传处理

```python
from werkzeug.utils import secure_filename
import os
from flask import current_app

def save_file(file):
    if file:
        # 安全文件名
        filename = secure_filename(file.filename)
        # 保存路径
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        # 保存文件
        file.save(upload_path)
        return filename
    return None

# 在路由中处理上传
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = save_file(file)
            flash('文件上传成功', 'success')
            return redirect(url_for('uploaded_file', filename=filename))
```

### 6. 分页实现

```python
from flask import request

# 在视图函数中
@app.route('/products')
def product_list():
    page = request.args.get('page', 1, type=int)
    per_page = 12

    products = Product.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template('products.html', products=products)

# 在模板中使用分页
{% for product in products.items %}
    <!-- 显示商品 -->
{% endfor %}

<!-- 分页导航 -->
<nav>
  <ul class="pagination">
    {% if products.has_prev %}
      <li class="page-item">
        <a class="page-link" href="{{ url_for('product_list', page=products.prev_num) }}">上一页</a>
      </li>
    {% endif %}

    {% for page_num in products.iter_pages() %}
      {% if page_num %}
        {% if page_num != products.page %}
          <li class="page-item">
            <a class="page-link" href="{{ url_for('product_list', page=page_num) }}">{{ page_num }}</a>
          </li>
        {% else %}
          <li class="page-item active">
            <span class="page-link">{{ page_num }}</span>
          </li>
        {% endif %}
      {% else %}
        <li class="page-item disabled">
          <span class="page-link">...</span>
        </li>
      {% endif %}
    {% endfor %}

    {% if products.has_next %}
      <li class="page-item">
        <a class="page-link" href="{{ url_for('product_list', page=products.next_num) }}">下一页</a>
      </li>
    {% endif %}
  </ul>
</nav>
```

### 7. 邮件发送

```python
from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, msg):
    """异步发送邮件"""
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, html_body):
    """发送邮件"""
    msg = Message(
        subject=subject,
        sender=current_app.config['MAIL_USERNAME'],
        recipients=recipients
    )
    msg.html = html_body

    # 异步发送
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

# 发送订单确认邮件
def send_order_confirmation(order):
    html = render_template('email/order_confirmation.html', order=order)
    send_email(
        subject='订单确认',
        recipients=[order.user.email],
        html_body=html
    )
```

---

## ⚠️ 常见问题与解决方案

### 问题1：数据库连接失败

**错误信息**：`pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")`

**解决方案**：
1. 检查MySQL服务是否启动
   ```bash
   # Windows
   net start mysql

   # macOS/Linux
   sudo systemctl start mysql
   ```

2. 检查数据库配置
   - 确认用户名和密码正确
   - 确认数据库名存在
   - 检查防火墙设置

3. 测试数据库连接
   ```python
   import pymysql
   try:
       conn = pymysql.connect(
           host='localhost',
           user='root',
           password='your_password',
           database='shop_db'
       )
       print("数据库连接成功！")
   except Exception as e:
       print(f"连接失败: {e}")
   ```

### 问题2：表单验证失败

**错误信息**：表单提交后数据丢失

**解决方案**：
1. 确保表单中有CSRF令牌
   ```html
   {{ form.hidden_tag() }}
   ```

2. 检查表单字段名称是否正确
3. 使用`form.validate_on_submit()`检查验证结果

### 问题3：静态文件404错误

**错误信息**：CSS/JS文件加载失败

**解决方案**：
1. 确保static文件夹结构正确
   ```
   app/
   └── static/
       ├── css/
       ├── js/
       └── images/
   ```

2. 使用`url_for()`生成URL
   ```html
   <link href="{{ url_for('static', filename='css/style.css') }}">
   ```

3. 检查文件名拼写

### 问题4：登录状态不持久

**可能原因**：
1. SECRET_KEY未设置或每次运行都变化
2. 浏览器Cookie被禁用
3. 会话配置问题

**解决方案**：
```python
# 设置固定的SECRET_KEY
app.config['SECRET_KEY'] = 'your-very-secret-key-here'

# 配置会话
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
```

### 问题5：文件上传失败

**错误信息**：`No file part` 或 `File type not allowed`

**解决方案**：
1. 确保HTML表单设置正确
   ```html
   <form method="POST" enctype="multipart/form-data">
   ```

2. 检查文件大小限制
   ```python
   app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
   ```

3. 验证文件扩展名
   ```python
   ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
   ```

---

## 📝 开发测试清单

### 第1周测试项目
- [ ] Python和MySQL安装成功
- [ ] uv包管理器安装成功
- [ ] 项目初始化完成（uv init）
- [ ] pyproject.toml配置正确
- [ ] 依赖安装成功（uv sync）
- [ ] 数据库创建成功
- [ ] 基础Flask应用可以运行（uv run python run.py）

### 第2周测试项目
- [ ] 用户注册功能正常
- [ ] 用户登录功能正常
- [ ] 密码加密存储
- [ ] 登录状态保持
- [ ] 用户权限验证

### 第3周测试项目
- [ ] 商品展示功能
- [ ] 购物车添加商品
- [ ] 购物车修改数量
- [ ] 购物车删除商品
- [ ] 商品搜索功能

### 第4周测试项目
- [ ] 订单创建功能
- [ ] 订单状态更新
- [ ] 邮件发送功能
- [ ] 管理员后台
- [ ] 文件上传功能

### 最终测试项目
- [ ] 所有功能正常工作
- [ ] 错误处理完善
- [ ] 页面样式美观
- [ ] 用户体验良好
- [ ] 数据安全性

---

## 💡 开发建议

### 1. 遵循Python之禅
- 代码要简洁明了
- 使用有意义的变量名
- 添加必要的注释
- 保持代码风格一致

### 2. 使用Git版本控制
```bash
# 提交代码
git add .
git commit -m "feat: 实现用户注册功能"
git push

# 查看历史
git log --oneline
```

### 3. 现代Python项目管理
```bash
# 使用uv进行高效的依赖管理
uv add package-name              # 添加新依赖
uv sync                          # 同步依赖环境
uv run python script.py          # 在虚拟环境中运行脚本

# 保持pyproject.toml整洁
# 定期更新依赖版本
# 使用开发依赖进行代码质量检查
```

### 4. 编写测试代码
```python
import pytest
from app.models import User

def test_user_password():
    user = User(username='test')
    user.set_password('password')
    assert user.check_password('password')
    assert not user.check_password('wrong')
```

### 5. 调试技巧
```python
# 打印调试信息
import logging
logging.basicConfig(level=logging.DEBUG)

# Flask调试模式
app.run(debug=True)

# 使用pdb调试
import pdb; pdb.set_trace()
```

---

## 🎓 项目总结要点

### 实验报告应包含：

1. **项目设计思路**
   - 数据库表设计（ER图）
   - 功能模块划分
   - 技术选型理由

2. **核心代码说明**
   - 用户认证实现
   - 购物车逻辑
   - 订单处理流程
   - 难点解决方案

3. **功能演示截图**
   - 注册/登录页面
   - 商品列表/详情页
   - 购物车页面
   - 订单页面
   - 管理员后台

4. **遇到的问题和解决方案**
   - 技术难点
   - 调试过程
   - 最终解决方法

5. **项目改进方向**
   - 功能扩展
   - 性能优化
   - 安全增强

---

## 🚀 最后的话

这个项目是一个完整的Web应用开发实践，涵盖了从数据库设计到前端展示的全过程。记住：

- **动手实践是最好的学习方式**
- **遇到问题不要怕，调试是成长的必经之路**
- **保持代码整洁，良好的习惯让你受益终生**
- **及时保存代码，使用Git版本控制**

祝你开发顺利，收获满满！💪

记住，完成这个项目后，你将掌握：
✅ Flask Web开发技能
✅ 数据库设计与使用
✅ 用户认证系统实现
✅ 电商网站核心功能
✅ 完整的项目开发经验