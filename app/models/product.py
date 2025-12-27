"""商品模型"""
from datetime import datetime, timezone, timedelta
from app.extensions import db
from flask import url_for

# 定义东八区时区
CHINA_TZ = timezone(timedelta(hours=8))

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
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), 
                           onupdate=lambda: datetime.now(timezone.utc))

    # 关系定义
    cart_items = db.relationship('CartItem', backref='product', 
                                 lazy='dynamic', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')

    def __repr__(self):
        return f'<Product {self.name}>'

    def is_in_stock(self, quantity=1):
        """检查库存是否充足"""
        return self.stock >= quantity

    def reduce_stock(self, quantity):
        """减少库存（不自动提交，由调用者控制事务）"""
        if self.is_in_stock(quantity):
            self.stock -= quantity
            return True
        raise ValueError(f"库存不足: 需要 {quantity}，当前库存 {self.stock}")

    def get_image_url(self):
        """获取图片URL，如果没有则返回默认图片"""
        if self.image_url:
            # 如果已经是完整URL,直接返回
            if self.image_url.startswith('http://') or self.image_url.startswith('https://'):
                return self.image_url
            # 否则作为静态文件路径处理
            return url_for('static', filename=self.image_url)
        return url_for('static', filename='images/default-product.png')

    @property
    def created_at_local(self):
        """获取本地时间(东八区)"""
        if self.created_at:
            if self.created_at.tzinfo is not None:
                return self.created_at.astimezone(CHINA_TZ)
            else:
                return self.created_at.replace(tzinfo=timezone.utc).astimezone(CHINA_TZ)
        return None

    @property
    def updated_at_local(self):
        """获取本地时间(东八区)"""
        if self.updated_at:
            if self.updated_at.tzinfo is not None:
                return self.updated_at.astimezone(CHINA_TZ)
            else:
                return self.updated_at.replace(tzinfo=timezone.utc).astimezone(CHINA_TZ)
        return None