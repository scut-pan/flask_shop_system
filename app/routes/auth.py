"""认证路由"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User
from app.forms import LoginForm, RegistrationForm, ProfileForm, PasswordChangeForm
from app.utils.decorators import anonymous_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
@anonymous_required
def register():
    """用户注册"""
    form = RegistrationForm()
    if form.validate_on_submit():
        # 创建新用户
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        # 保存到数据库
        db.session.add(user)
        db.session.commit()

        flash('注册成功！请登录', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
@anonymous_required
def login():
    """用户登录"""
    form = LoginForm()
    if form.validate_on_submit():
        # 查找用户
        user = User.query.filter_by(username=form.username.data).first()

        # 验证用户和密码
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            # 获取下一页URL
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')

            flash(f'欢迎回来，{user.username}！', 'success')
            return redirect(next_page)
        else:
            flash('用户名或密码错误', 'danger')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    flash('您已成功退出登录', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    """个人信息页面"""
    return render_template('auth/profile.html')

@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """编辑个人信息"""
    form = ProfileForm()
    if form.validate_on_submit():
        # 检查邮箱是否已被其他用户使用
        if form.email.data != current_user.email:
            if User.query.filter_by(email=form.email.data).first():
                flash('该邮箱已被其他用户使用', 'danger')
                return render_template('auth/edit_profile.html', form=form)

        current_user.email = form.email.data
        db.session.commit()
        flash('个人信息已更新', 'success')
        return redirect(url_for('auth.profile'))

    # 预填充表单
    form.email.data = current_user.email
    return render_template('auth/edit_profile.html', form=form)

@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """修改密码"""
    form = PasswordChangeForm()
    if form.validate_on_submit():
        # 验证当前密码
        if not current_user.check_password(form.old_password.data):
            flash('当前密码错误', 'danger')
            return render_template('auth/change_password.html', form=form)

        # 设置新密码
        current_user.set_password(form.password.data)
        db.session.commit()

        flash('密码修改成功，请重新登录', 'success')
        logout_user()
        return redirect(url_for('auth.login'))

    return render_template('auth/change_password.html', form=form)