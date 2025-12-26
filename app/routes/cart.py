"""购物车路由"""
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models import CartItem, Product

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/')
@login_required
def index():
    """显示购物车"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    # 计算总价
    total_amount = sum(item.get_subtotal() for item in cart_items)

    # 统计购物车商品总数
    total_items = sum(item.quantity for item in cart_items)

    return render_template('cart/index.html',
                         cart_items=cart_items,
                         total_amount=total_amount,
                         total_items=total_items)


@cart_bp.route('/add', methods=['POST'])
@login_required
def add():
    """添加商品到购物车"""
    product_id = request.form.get('product_id', type=int)

    if not product_id:
        flash('商品ID不能为空', 'danger')
        return redirect(url_for('product.list'))

    # 查询商品
    product = Product.query.get_or_404(product_id)

    # 检查商品是否上架
    if not product.is_active:
        flash('该商品已下架', 'warning')
        return redirect(url_for('product.detail', product_id=product_id))

    # 检查库存
    if not product.is_in_stock():
        flash('该商品库存不足', 'warning')
        return redirect(url_for('product.detail', product_id=product_id))

    try:
        # 获取或创建购物车项
        cart_item = CartItem.get_or_create(current_user.id, product_id)

        # 检查是否超过库存
        if cart_item.quantity > product.stock:
            flash(f'购物车中该商品数量已达库存上限({product.stock})', 'warning')
            return redirect(url_for('product.detail', product_id=product_id))

        db.session.commit()
        flash(f'已将"{product.name}"加入购物车', 'success')

    except Exception as e:
        db.session.rollback()
        flash('添加购物车失败，请重试', 'danger')

    return redirect(url_for('product.detail', product_id=product_id))


@cart_bp.route('/update', methods=['POST'])
@login_required
def update():
    """更新购物车商品数量"""
    item_id = request.form.get('item_id', type=int)
    quantity = request.form.get('quantity', type=int)

    if not item_id or not quantity:
        flash('参数错误', 'danger')
        return redirect(url_for('cart.index'))

    # 查询购物车项
    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()

    try:
        # 更新数量（会验证库存）
        cart_item.update_quantity(quantity)
        db.session.commit()
        flash('数量已更新', 'success')

    except ValueError as e:
        flash(str(e), 'warning')
    except Exception as e:
        db.session.rollback()
        flash('更新失败，请重试', 'danger')

    return redirect(url_for('cart.index'))


@cart_bp.route('/delete', methods=['POST'])
@login_required
def delete():
    """删除购物车商品"""
    item_id = request.form.get('item_id', type=int)

    if not item_id:
        flash('参数错误', 'danger')
        return redirect(url_for('cart.index'))

    # 查询购物车项
    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()

    try:
        product_name = cart_item.product.name
        db.session.delete(cart_item)
        db.session.commit()
        flash(f'已从购物车删除"{product_name}"', 'success')

    except Exception as e:
        db.session.rollback()
        flash('删除失败，请重试', 'danger')

    return redirect(url_for('cart.index'))


@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear():
    """清空购物车"""
    try:
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('购物车已清空', 'success')

    except Exception as e:
        db.session.rollback()
        flash('清空购物车失败，请重试', 'danger')

    return redirect(url_for('cart.index'))


@cart_bp.route('/count')
@login_required
def count():
    """获取购物车商品数量（用于AJAX）"""
    count = db.session.query(db.func.sum(CartItem.quantity))\
                    .filter_by(user_id=current_user.id)\
                    .scalar()
    count = count or 0
    return jsonify({'count': count})
