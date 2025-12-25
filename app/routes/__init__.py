"""路由"""
from app.routes import auth, main, product, cart, order, admin

# 创建蓝图实例
auth_bp = auth.auth_bp
main_bp = main.main_bp
product_bp = product.product_bp
cart_bp = cart.cart_bp
order_bp = order.order_bp
admin_bp = admin.admin_bp

__all__ = ['auth_bp', 'main_bp', 'product_bp', 
           'cart_bp', 'order_bp', 'admin_bp']