"""文件处理工具函数"""
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


def get_image_extension(file_path):
    """
    通过文件内容检测图片类型并返回扩展名

    Args:
        file_path: 文件的完整路径

    Returns:
        str: 图片扩展名(如 'jpg', 'png', 'gif', 'webp')或 None
    """
    with open(file_path, 'rb') as f:
        header = f.read(12)

    # 检测不同的图片格式
    if header.startswith(b'\xFF\xD8\xFF'):
        return 'jpg'
    elif header.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'
    elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
        return 'gif'
    elif header.startswith(b'RIFF') and header[8:12] == b'WEBP':
        return 'webp'
    elif header.startswith(b'BM'):
        return 'bmp'
    elif header.startswith(b'II*\x00') or header.startswith(b'MM\x00*'):
        return 'tiff'

    return None


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

    # 生成临时文件名(先不带扩展名)
    temp_filename = f"{uuid.uuid4().hex}.tmp"

    # 构建保存路径
    upload_folder = os.path.join(
        current_app.root_path,
        'static',
        'images',
        folder
    )

    # 确保目录存在
    os.makedirs(upload_folder, exist_ok=True)

    # 先保存为临时文件
    temp_path = os.path.join(upload_folder, temp_filename)
    file.save(temp_path)

    # 通过文件内容检测真实扩展名
    detected_ext = get_image_extension(temp_path)

    if detected_ext:
        # 使用检测到的扩展名
        final_filename = f"{uuid.uuid4().hex}.{detected_ext}"
    elif file_ext:
        # 如果检测失败但有原始扩展名,使用原始扩展名
        final_filename = f"{uuid.uuid4().hex}.{file_ext}"
    else:
        # 都没有则删除临时文件并报错
        os.remove(temp_path)
        raise ValueError('无法识别文件类型,请上传有效的图片文件')

    # 重命名为最终文件名
    final_path = os.path.join(upload_folder, final_filename)
    os.rename(temp_path, final_path)

    # 返回相对路径(用于数据库存储和前端访问)
    return f"images/{folder}/{final_filename}"


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
