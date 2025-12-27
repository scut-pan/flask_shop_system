"""订单模型"""
from datetime import datetime, timezone, timedelta
from app.extensions import db
import uuid

# 定义东八区时区
CHINA_TZ = timezone(timedelta(hours=8))

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

    @property
    def created_at_local(self):
        """获取本地时间(东八区)"""
        if self.created_at:
            # 如果created_at有时区信息,转换到东八区
            if self.created_at.tzinfo is not None:
                return self.created_at.astimezone(CHINA_TZ)
            # 如果没有时区信息,假设是UTC时间,添加时区后转换
            else:
                return self.created_at.replace(tzinfo=timezone.utc).astimezone(CHINA_TZ)
        return None

    @property
    def updated_at_local(self):
        """获取本地时间(东八区)"""
        if self.updated_at:
            # 如果updated_at有时区信息,转换到东八区
            if self.updated_at.tzinfo is not None:
                return self.updated_at.astimezone(CHINA_TZ)
            # 如果没有时区信息,假设是UTC时间,添加时区后转换
            else:
                return self.updated_at.replace(tzinfo=timezone.utc).astimezone(CHINA_TZ)
        return None

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