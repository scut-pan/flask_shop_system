"""商品模型"""
from datetime import datetime
from app.extensions import db
from flask import url_for
from datetime import timezone

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