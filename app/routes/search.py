"""
Search Routes — 搜尋相關路由
"""
from flask import Blueprint, render_template, request

search_bp = Blueprint('search', __name__)


@search_bp.route('/search')
def search():
    """
    搜尋考古題
    GET /search?q=關鍵字&subject_id=&professor_id=&year=
    - 取得 query 參數 q（搜尋關鍵字）
    - 呼叫 Exam.search(keyword, subject_id, professor_id, year)
    - 呼叫 Subject.get_all() 取得科目篩選選項
    - 呼叫 Professor.get_all() 取得教授篩選選項
    - 關鍵字為空時顯示空結果
    - 模板：search/results.html
    """
    pass
