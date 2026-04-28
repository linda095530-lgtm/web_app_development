"""
Main Routes — 首頁與通用路由
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    首頁
    - 顯示系統統計資訊（科目數、教授數、考古題數）
    - 提供快速導覽連結
    - 模板：index.html
    """
    pass
