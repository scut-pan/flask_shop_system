"""辅助函数"""
from flask import current_app, request, render_template
from werkzeug.utils import secure_filename
from app.extensions import mail
from flask_mail import Message
import os
import uuid
import sys
from threading import Thread

# 修复Flask-Mail中文编码问题
def patch_flask_mail():
    """修补Flask-Mail以支持中文邮件主题"""
    import flask_mail
    from email.policy import SMTPUTF8

    original_as_bytes = flask_mail.Message.as_bytes

    def patched_as_bytes(self):
        """使用UTF-8策略编码邮件"""
        # 创建使用SMTPUTF8策略的消息
        msg = self._message()
        return msg.as_bytes(policy=SMTPUTF8)

    flask_mail.Message.as_bytes = patched_as_bytes

# 应用修补
patch_flask_mail()

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
            current_app.logger.warning('邮件未配置,跳过发送订单确认邮件')
            return False

        # 创建邮件消息
        msg = Message(
            subject=f'订单确认 - {order.order_number}',
            sender=current_app.config.get('MAIL_DEFAULT_SENDER') or current_app.config['MAIL_USERNAME'],
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