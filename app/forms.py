"""表单类"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, IntegerField, DecimalField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_wtf.file import FileAllowed, FileRequired
from app.models import User

class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    """注册表单"""
    username = StringField('用户名', validators=[
        DataRequired(),
        Length(min=4, max=20, message='用户名长度必须在4-20个字符之间')
    ])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[
        DataRequired(),
        Length(min=6, message='密码至少6个字符')
    ])
    password2 = PasswordField('确认密码', validators=[
        DataRequired(),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    submit = SubmitField('注册')

    def validate_username(self, field):
        """验证用户名是否已存在"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

    def validate_email(self, field):
        """验证邮箱是否已存在"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

class ProfileForm(FlaskForm):
    """个人信息表单"""
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    submit = SubmitField('更新')

class PasswordChangeForm(FlaskForm):
    """修改密码表单"""
    old_password = PasswordField('当前密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(),
        Length(min=6, message='密码至少6个字符')
    ])
    password2 = PasswordField('确认新密码', validators=[
        DataRequired(),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    submit = SubmitField('修改密码')

class ProductForm(FlaskForm):
    """商品表单"""
    name = StringField('商品名称', validators=[
        DataRequired(),
        Length(min=2, max=200, message='商品名称长度必须在2-200个字符之间')
    ])
    description = TextAreaField('商品描述', validators=[
        Length(max=1000, message='描述不能超过1000个字符')
    ])
    price = DecimalField('价格', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='价格必须大于0')
    ], places=2)
    stock = IntegerField('库存', validators=[
        DataRequired(),
        NumberRange(min=0, message='库存不能为负数')
    ])
    image_url = StringField('图片URL', validators=[
        Length(max=300, message='URL长度不能超过300个字符')
    ])
    is_active = BooleanField('是否上架')
    submit = SubmitField('保存')


class CheckoutForm(FlaskForm):
    """结算表单"""
    shipping_address = TextAreaField('收货地址', validators=[
        DataRequired(message='请输入收货地址'),
        Length(min=10, max=500, message='收货地址长度必须在10-500个字符之间')
    ])
    contact_phone = StringField('联系电话', validators=[
        DataRequired(message='请输入联系电话'),
        Length(min=11, max=11, message='请输入正确的手机号码')
    ])
    recipient_name = StringField('收货人姓名', validators=[
        DataRequired(message='请输入收货人姓名'),
        Length(min=2, max=50, message='姓名长度必须在2-50个字符之间')
    ])
    submit = SubmitField('提交订单')

class UserEditForm(FlaskForm):
    """用户编辑表单(管理员)"""
    username = StringField('用户名', validators=[
        DataRequired(),
        Length(min=4, max=20, message='用户名长度必须在4-20个字符之间')
    ])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    is_admin = BooleanField('管理员')
    is_active = BooleanField('启用状态')
    submit = SubmitField('保存')

class AccountDeleteForm(FlaskForm):
    """注销账号表单"""
    password = PasswordField('请输入当前密码确认身份', validators=[DataRequired()])
    confirm = BooleanField('我确认要永久注销账号,此操作不可撤销', validators=[DataRequired(message='请勾选确认框以继续')])
    submit = SubmitField('确认注销账号')