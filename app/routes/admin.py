"""管理员路由"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required
from app.utils.decorators import admin_required
from app.utils.files import save_uploaded_file, delete_file
from app.extensions import db
from app.models import User, Product, Order, OrderItem
from app.forms import ProductForm, UserEditForm
from sqlalchemy import func, and_
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """管理员仪表盘"""
    # 基础统计数据
    total_orders = Order.query.count()
    total_products = Product.query.count()
    total_users = User.query.count()

    # 销售统计(只统计已完成的订单)
    total_sales = db.session.query(func.sum(Order.total_amount))\
        .filter(Order.status == 'delivered').scalar()
    total_sales = total_sales or 0

    # 待处理订单数
    pending_orders = Order.query.filter_by(status='pending').count()

    # 本月销售额
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_sales = db.session.query(func.sum(Order.total_amount))\
        .filter(and_(Order.status == 'delivered', Order.created_at >= month_start)).scalar()
    monthly_sales = monthly_sales or 0

    # 最新订单
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()

    return render_template('admin/dashboard.html',
                         total_orders=total_orders,
                         total_products=total_products,
                         total_users=total_users,
                         total_sales=total_sales,
                         pending_orders=pending_orders,
                         monthly_sales=monthly_sales,
                         recent_orders=recent_orders)

@admin_bp.route('/products')
@login_required
@admin_required
def products():
    """商品管理列表"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    pagination = Product.query.order_by(Product.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('admin/products.html', pagination=pagination)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def product_add():
    """添加商品"""
    form = ProductForm()

    if form.validate_on_submit():
        # 处理图片上传
        image_url = None
        if form.image.data:
            try:
                image_url = save_uploaded_file(form.image.data)
            except ValueError as e:
                flash(str(e), 'danger')
                return render_template('admin/product_form.html', form=form, action='add')

        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            image_url=image_url,
            is_active=form.is_active.data
        )
        db.session.add(product)
        db.session.commit()
        flash('商品添加成功', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, action='add')

@admin_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def product_edit(product_id):
    """编辑商品"""
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        # 处理图片上传
        if form.image.data:
            try:
                # 删除旧图片
                if product.image_url:
                    delete_file(product.image_url)
                # 保存新图片
                product.image_url = save_uploaded_file(form.image.data)
            except ValueError as e:
                flash(str(e), 'danger')
                return render_template('admin/product_form.html', form=form, product=product, action='edit')

        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.is_active = form.is_active.data
        db.session.commit()
        flash('商品更新成功', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, product=product, action='edit')

@admin_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
@admin_required
def product_delete(product_id):
    """删除商品"""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('商品删除成功', 'success')
    return redirect(url_for('admin.products'))

@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    """订单管理列表"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    status = request.args.get('status', '')

    query = Order.query
    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(Order.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('admin/orders.html', pagination=pagination, current_status=status)

@admin_bp.route('/orders/<int:order_id>')
@login_required
@admin_required
def order_detail(order_id):
    """订单详情"""
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)

@admin_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@login_required
@admin_required
def order_update_status(order_id):
    """更新订单状态"""
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')

    if new_status in ['pending', 'paid', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash('订单状态更新成功', 'success')
    else:
        flash('无效的订单状态', 'danger')

    return redirect(url_for('admin.order_detail', order_id=order_id))

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """用户管理列表"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    pagination = User.query.order_by(User.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('admin/users.html', pagination=pagination)

@admin_bp.route('/users/<int:user_id>')
@login_required
@admin_required
def user_detail(user_id):
    """用户详情"""
    user = User.query.get_or_404(user_id)
    # 获取用户订单统计
    total_orders = user.orders.count()
    total_spent = db.session.query(func.sum(Order.total_amount))\
        .filter_by(user_id=user_id, status='delivered').scalar()
    total_spent = total_spent or 0

    return render_template('admin/user_detail.html', user=user,
                         total_orders=total_orders, total_spent=total_spent)

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit(user_id):
    """编辑用户"""
    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        user.is_active = form.is_active.data
        db.session.commit()
        flash('用户信息更新成功', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user_edit.html', form=form, user=user)

@admin_bp.route('/statistics')
@login_required
@admin_required
def statistics():
    """销售统计"""
    # 按日期统计最近30天销售额
    thirty_days_ago = datetime.now() - timedelta(days=30)
    daily_sales = db.session.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total_amount).label('sales')
    ).filter(
        and_(Order.status == 'delivered', Order.created_at >= thirty_days_ago)
    ).group_by(func.date(Order.created_at)).all()

    dates = [str(row.date) for row in daily_sales]
    sales = [float(row.sales) for row in daily_sales]

    # 按商品统计销量
    product_sales = db.session.query(
        Product.name,
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.quantity * OrderItem.price).label('total_amount')
    ).join(OrderItem).group_by(Product.id, Product.name)\
        .order_by(func.sum(OrderItem.quantity).desc()).limit(10).all()

    # 订单状态分布
    status_distribution = db.session.query(
        Order.status,
        func.count(Order.id).label('count')
    ).group_by(Order.status).all()

    status_data = {row[0]: row[1] for row in status_distribution}

    return render_template('admin/statistics.html',
                         dates=dates,
                         sales=sales,
                         product_sales=product_sales,
                         status_data=status_data)
