"""
Search Routes — 搜尋相關路由
"""
from flask import Blueprint, render_template, request, current_app
from app.models.exam import Exam
from app.models.subject import Subject
from app.models.professor import Professor

search_bp = Blueprint('search', __name__)


@search_bp.route('/search')
def search():
    """搜尋考古題"""
    db_path = current_app.config['DATABASE']

    keyword = request.args.get('q', '').strip()
    subject_id = request.args.get('subject_id', '').strip()
    professor_id = request.args.get('professor_id', '').strip()
    year = request.args.get('year', '').strip()

    subject_id = int(subject_id) if subject_id else None
    professor_id = int(professor_id) if professor_id else None
    year = year if year else None

    results = []
    if keyword:
        results = Exam.search(db_path, keyword,
                              subject_id=subject_id,
                              professor_id=professor_id,
                              year=year)

    # 取得篩選選項
    subjects = Subject.get_all(db_path)
    professors = Professor.get_all(db_path)
    years = Exam.get_years(db_path)

    return render_template('search/results.html',
                           results=results,
                           keyword=keyword,
                           subjects=subjects,
                           professors=professors,
                           years=years,
                           selected_subject=subject_id,
                           selected_professor=professor_id,
                           selected_year=year)
