"""应用启动文件"""
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