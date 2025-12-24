"""辅助函数"""
from flask import current_app, request
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