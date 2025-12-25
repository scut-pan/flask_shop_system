"""商品路由"""
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Product, OrderItem
from app.forms import ProductForm
from app.utils.decorators import admin_required

product_bp = Blueprint('product', __name__)

@product_bp.route('/')
def list():
    """商品列表(支持分页和搜索)"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    search_query = request.args.get('q', '')

    # 构建查询
    query = Product.query

    # 搜索过滤
    if search_query:
        query = query.filter(
            db.or_(
                Product.name.like(f'%{search_query}%'),
                Product.description.like(f'%{search_query}%')
            )
        )

    # 只显示已上架的商品
    query = query.filter_by(is_active=True)

    # 分页
    pagination = query.order_by(Product.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template('product/list.html',
                         products=pagination.items,
                         pagination=pagination,
                         search_query=search_query)

@product_bp.route('/<int:product_id>')
def detail(product_id):
    """商品详情页"""
    product = Product.query.get_or_404(product_id)
    return render_template('product/detail.html', product=product)

@product_bp.route('/search')
def search():
    """商品搜索"""
    search_query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 12

    query = Product.query.filter_by(is_active=True)

    if search_query:
        query = query.filter(
            db.or_(
                Product.name.like(f'%{search_query}%'),
                Product.description.like(f'%{search_query}%')
            )
        )

    pagination = query.order_by(Product.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template('product/list.html',
                         products=pagination.items,
                         pagination=pagination,
                         search_query=search_query)

# ============ 管理员功能 ============

@product_bp.route('/admin/manage')
@login_required
@admin_required
def manage():
    """商品管理列表"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    pagination = Product.query.order_by(Product.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template('product/admin/list.html',
                         pagination=pagination)

@product_bp.route('/admin/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    """添加商品"""
    form = ProductForm()

    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            image_url=form.image_url.data if form.image_url.data else None,
            is_active=form.is_active.data
        )

        db.session.add(product)
        db.session.commit()

        flash(f'商品"{product.name}"添加成功！', 'success')
        return redirect(url_for('product.manage'))

    return render_template('product/admin/form.html',
                         form=form,
                         action='create')

@product_bp.route('/admin/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(product_id):
    """编辑商品"""
    product = Product.query.get_or_404(product_id)
    form = ProductForm()

    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.image_url = form.image_url.data if form.image_url.data else None
        product.is_active = form.is_active.data

        db.session.commit()

        flash(f'商品"{product.name}"更新成功！', 'success')
        return redirect(url_for('product.manage'))

    # 预填充表单
    form.name.data = product.name
    form.description.data = product.description
    form.price.data = product.price
    form.stock.data = product.stock
    form.image_url.data = product.image_url
    form.is_active.data = product.is_active

    return render_template('product/admin/form.html',
                         form=form,
                         product=product,
                         action='edit')

@product_bp.route('/admin/<int:product_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(product_id):
    """删除商品"""
    product = Product.query.get_or_404(product_id)

    # 检查是否有关联的订单项
    order_items_count = OrderItem.query.filter_by(product_id=product_id).count()
    if order_items_count > 0:
        flash(f'无法删除商品"{product.name}"，该商品存在{order_items_count}条订单记录！', 'danger')
        return redirect(url_for('product.manage'))

    product_name = product.name
    db.session.delete(product)
    db.session.commit()

    flash(f'商品"{product_name}"已删除！', 'success')
    return redirect(url_for('product.manage'))
