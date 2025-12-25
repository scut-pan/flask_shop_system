"""订单路由"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Order, OrderItem, CartItem, Product
from app.forms import CheckoutForm
from sqlalchemy.exc import IntegrityError

order_bp = Blueprint('order', __name__)


@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """结算页面"""
    # 获取购物车商品
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    # 检查购物车是否为空
    if not cart_items:
        flash('购物车为空，请先添加商品', 'warning')
        return redirect(url_for('product.list'))

    # 检查所有商品库存是否充足
    insufficient_stock = False
    for item in cart_items:
        if not item.can_purchase():
            flash(f'商品"{item.product.name}"库存不足，当前库存: {item.product.stock}', 'danger')
            insufficient_stock = True

    if insufficient_stock:
        return redirect(url_for('cart.index'))

    # 计算总金额
    total_amount = sum(item.get_subtotal() for item in cart_items)

    form = CheckoutForm()

    if form.validate_on_submit():
        try:
            # 组装收货地址信息
            shipping_address = f"收货人: {form.recipient_name.data}\n联系电话: {form.contact_phone.data}\n地址: {form.shipping_address.data}"

            # 创建订单
            order = Order(
                user_id=current_user.id,
                total_amount=total_amount,
                shipping_address=shipping_address,
                status='pending'
            )

            db.session.add(order)
            db.session.flush()  # 刷新以获取订单ID

            # 从购物车创建订单明细
            for cart_item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                db.session.add(order_item)

                # 减少商品库存
                cart_item.product.reduce_stock(cart_item.quantity)

            # 清空购物车
            CartItem.query.filter_by(user_id=current_user.id).delete()

            # 提交所有更改
            db.session.commit()

            flash(f'订单创建成功！订单号: {order.order_number}', 'success')

            # 发送订单确认邮件（如果配置了邮件）
            from app.utils.helpers import send_order_confirmation_email
            send_order_confirmation_email(order)

            return redirect(url_for('order.detail', id=order.id))

        except ValueError as e:
            db.session.rollback()
            flash(str(e), 'danger')
        except IntegrityError:
            db.session.rollback()
            flash('订单创建失败，请重试', 'danger')
        except Exception as e:
            db.session.rollback()
            flash('订单创建失败，请重试', 'danger')

    return render_template('order/checkout.html',
                         form=form,
                         cart_items=cart_items,
                         total_amount=total_amount)


@order_bp.route('/list')
@login_required
def list():
    """订单列表"""
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # 分页查询订单
    pagination = Order.query.filter_by(user_id=current_user.id)\
                           .order_by(Order.created_at.desc())\
                           .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('order/list.html',
                         orders=pagination.items,
                         pagination=pagination)


@order_bp.route('/detail/<int:id>')
@login_required
def detail(id):
    """订单详情"""
    # 查询订单（只能查看自己的订单）
    order = Order.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    return render_template('order/detail.html', order=order)


@order_bp.route('/cancel/<int:id>', methods=['POST'])
@login_required
def cancel(id):
    """取消订单"""
    # 查询订单
    order = Order.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    # 检查是否可以取消
    if not order.can_cancel():
        flash(f'订单状态为"{order.get_status_display()}"，无法取消', 'warning')
        return redirect(url_for('order.detail', id=id))

    try:
        # 恢复商品库存
        for item in order.items:
            item.product.stock += item.quantity

        # 更新订单状态
        order.status = 'cancelled'
        db.session.commit()

        flash(f'订单{order.order_number}已取消', 'success')

    except Exception as e:
        db.session.rollback()
        flash('取消订单失败，请重试', 'danger')

    return redirect(url_for('order.detail', id=id))
