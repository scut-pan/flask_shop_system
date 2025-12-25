"""数据库初始化脚本"""
from app import create_app
from app.extensions import db
from app.models import User

def init_database():
    """初始化数据库"""
    app = create_app()

    with app.app_context():
        # 删除所有表(谨慎使用!)
        db.drop_all()
        print('[OK] 已删除所有旧表')

        # 创建所有表
        db.create_all()
        print('[OK] 已创建所有新表')

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
            print('[OK] 管理员用户创建成功')
            print('  用户名: admin')
            print('  密码: admin123')
            print('  邮箱: admin@shop.com')
        else:
            print('[OK] 管理员用户已存在')

        # 创建测试用户（如果不存在）
        test_user = User.query.filter_by(username='test').first()
        if not test_user:
            test_user = User(
                username='test',
                email='test@example.com',
                is_admin=False
            )
            test_user.set_password('test123')
            db.session.add(test_user)
            db.session.commit()
            print('[OK] 测试用户创建成功')
            print('  用户名: test')
            print('  密码: test123')
            print('  邮箱: test@example.com')
        else:
            print('[OK] 测试用户已存在')

        print('\n数据库初始化完成！')

if __name__ == '__main__':
    init_database()