"""购物车模型"""
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
            item = CartItem(user_id=user_id, product_id=product_id, quantity=1)
            db.session.add(item)
        else:
            item.quantity += 1
        return item

    def update_quantity(self, quantity):
        """更新数量，验证库存"""
        from app.models import Product

        product = Product.query.get(self.product_id)
        if not product:
            raise ValueError("商品不存在")

        if quantity > product.stock:
            raise ValueError(f"库存不足，当前库存: {product.stock}")

        if quantity < 1:
            raise ValueError("数量不能小于1")

        self.quantity = quantity

    def can_purchase(self):
        """检查是否可以购买（库存是否充足）"""
        return self.product.stock >= self.quantity