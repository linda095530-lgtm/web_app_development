"""
Main Routes — 首頁與通用路由
"""
from flask import Blueprint, render_template, current_app
from app.models.subject import Subject
from app.models.professor import Professor
from app.models.exam import Exam

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    首頁
    - 顯示系統統計資訊（科目數、教授數、考古題數）
    - 顯示最新上傳的考古題
    """
    db_path = current_app.config['DATABASE']

    subjects = Subject.get_all(db_path)
    professors = Professor.get_all(db_path)
    exams = Exam.get_all(db_path)

    # 取得最新 5 筆考古題
    recent_exams = exams[:5] if exams else []

    return render_template('index.html',
                           subject_count=len(subjects),
                           professor_count=len(professors),
                           exam_count=len(exams),
                           recent_exams=recent_exams)
