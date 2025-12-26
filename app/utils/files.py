"""文件处理工具函数"""
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename, allowed_extensions=None):
    """
    检查文件类型是否允许

    Args:
        filename: 文件名
        allowed_extensions: 允许的扩展名集合,默认使用配置中的ALLOWED_EXTENSIONS

    Returns:
        bool: 文件类型是否允许
    """
    if allowed_extensions is None:
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_uploaded_file(file, folder='uploads'):
    """
    保存上传的文件并返回相对路径

    Args:
        file: FileStorage对象
        folder: 上传文件夹名称(相对于static/images)

    Returns:
        str: 文件的相对路径(用于存储到数据库)

    Raises:
        ValueError: 文件类型不允许时抛出
    """
    if file is None or file.filename == '':
        raise ValueError('没有选择文件')

    # 检查文件类型
    if not allowed_file(file.filename):
        allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})
        raise ValueError(f'不支持的文件类型,仅支持: {", ".join(allowed)}')

    # 获取原始文件扩展名
    original_filename = secure_filename(file.filename)
    file_ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''

    # 生成唯一文件名
    unique_filename = f"{uuid.uuid4().hex}.{file_ext}"

    # 构建保存路径
    upload_folder = os.path.join(
        current_app.root_path,
        'static',
        'images',
        folder
    )

    # 确保目录存在
    os.makedirs(upload_folder, exist_ok=True)

    # 保存文件
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)

    # 返回相对路径(用于数据库存储和前端访问)
    return f"images/{folder}/{unique_filename}"


def delete_file(file_path):
    """
    删除指定的文件

    Args:
        file_path: 文件的相对路径
    """
    if not file_path:
        return

    try:
        # 构建完整的文件系统路径
        full_path = os.path.join(current_app.root_path, 'static', file_path)

        # 删除文件
        if os.path.exists(full_path):
            os.remove(full_path)
    except Exception as e:
        # 记录错误但不中断程序
        current_app.logger.error(f"删除文件失败: {file_path}, 错误: {e}")
