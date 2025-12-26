"""修复现有图片文件的扩展名并更新数据库"""
import os
import sys
import struct

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models import Product


def get_image_extension(file_path):
    """通过文件内容检测图片类型并返回扩展名"""
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


def fix_images():
    """修复图片文件扩展名和数据库路径"""
    app = create_app()
    app.app_context().push()

    upload_folder = os.path.join(app.root_path, 'static', 'images', 'uploads')

    if not os.path.exists(upload_folder):
        print(f"上传文件夹不存在: {upload_folder}")
        return

    print("开始修复图片文件...")

    # 获取所有商品
    products = Product.query.filter(Product.image_url.like('images/uploads/%')).all()

    for product in products:
        if not product.image_url:
            continue

        # 提取文件名
        old_filename = product.image_url.split('/')[-1]
        old_path = os.path.join(upload_folder, old_filename)

        # 如果文件不存在,跳过
        if not os.path.exists(old_path):
            print(f"文件不存在,跳过: {old_filename}")
            continue

        # 检测文件类型
        ext = get_image_extension(old_path)

        if not ext:
            print(f"无法识别文件类型: {old_filename}")
            continue

        # 如果文件已经有正确的扩展名,跳过
        if old_filename.endswith(f'.{ext}'):
            print(f"文件扩展名正确,跳过: {old_filename}")
            continue

        # 生成新文件名
        name_without_ext = old_filename.rsplit('.', 1)[0] if '.' in old_filename else old_filename
        new_filename = f"{name_without_ext}.{ext}"
        new_path = os.path.join(upload_folder, new_filename)

        # 重命名文件
        try:
            os.rename(old_path, new_path)
            print(f"重命名: {old_filename} -> {new_filename}")

            # 更新数据库
            new_image_url = f"images/uploads/{new_filename}"
            product.image_url = new_image_url
            db.session.commit()

            print(f"已更新数据库: 商品 ID {product.id} ({product.name})")
        except Exception as e:
            print(f"重命名失败: {old_filename}, 错误: {e}")
            db.session.rollback()

    print("\n修复完成!")


if __name__ == '__main__':
    fix_images()
