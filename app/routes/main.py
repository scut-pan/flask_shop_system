"""主页路由"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """网站首页"""
    return render_template('main/index.html')

@main_bp.route('/about')
def about():
    """关于我们页面"""
    return render_template('main/about.html')