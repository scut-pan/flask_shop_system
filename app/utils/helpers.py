"""辅助函数"""
from flask import current_app, request, render_template
from werkzeug.utils import secure_filename
from app.extensions import mail
from flask_mail import Message
import os
import uuid
from threading import Thread

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


def send_async_email(app, msg):
    """异步发送邮件"""
    with app.app_context():
        try:
            mail.send(msg)
            current_app.logger.info(f'邮件发送成功: {msg.subject}')
        except Exception as e:
            current_app.logger.error(f'邮件发送失败: {str(e)}')


def send_order_confirmation_email(order):
    """发送订单确认邮件"""
    try:
        # 检查是否配置了邮件服务器
        if not current_app.config.get('MAIL_USERNAME'):
            current_app.logger.warning('邮件未配置，跳过发送订单确认邮件')
            return False

        # 创建邮件消息
        msg = Message(
            subject=f'订单确认 - {order.order_number}',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[order.user.email]
        )

        # 渲染HTML邮件内容
        msg.html = render_template('email/order_confirmation.html', order=order)

        # 异步发送邮件
        Thread(target=send_async_email,
               args=(current_app._get_current_object(), msg)).start()

        current_app.logger.info(f'订单确认邮件已发送: {order.order_number}')
        return True

    except Exception as e:
        current_app.logger.error(f'发送订单确认邮件失败: {str(e)}')
        return False