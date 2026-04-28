"""
Exam Routes — 考古題相關路由
Blueprint 前綴：/exams
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort
from app.models.exam import Exam
from app.models.subject import Subject
from app.models.professor import Professor

exam_bp = Blueprint('exams', __name__, url_prefix='/exams')


@exam_bp.route('/')
def list_exams():
    """考古題列表頁（支援篩選）"""
    db_path = current_app.config['DATABASE']

    # 取得篩選參數
    subject_id = request.args.get('subject_id', '').strip()
    professor_id = request.args.get('professor_id', '').strip()
    year = request.args.get('year', '').strip()
    exam_type = request.args.get('exam_type', '').strip()

    # 轉換為適當型別
    subject_id = int(subject_id) if subject_id else None
    professor_id = int(professor_id) if professor_id else None
    year = year if year else None
    exam_type = exam_type if exam_type else None

    exams = Exam.get_all(db_path, subject_id=subject_id,
                         professor_id=professor_id,
                         year=year, exam_type=exam_type)

    # 取得篩選選項
    subjects = Subject.get_all(db_path)
    professors = Professor.get_all(db_path)
    years = Exam.get_years(db_path)

    return render_template('exams/list.html',
                           exams=exams,
                           subjects=subjects,
                           professors=professors,
                           years=years,
                           selected_subject=subject_id,
                           selected_professor=professor_id,
                           selected_year=year,
                           selected_type=exam_type)


@exam_bp.route('/create', methods=['GET', 'POST'])
def create_exam():
    """新增考古題"""
    db_path = current_app.config['DATABASE']

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        subject_id = request.form.get('subject_id', '').strip()
        professor_id = request.form.get('professor_id', '').strip()
        year = request.form.get('year', '').strip()
        semester = request.form.get('semester', '').strip()
        exam_type = request.form.get('exam_type', '').strip()
        content = request.form.get('content', '').strip()

        # 驗證必填欄位
        errors = []
        if not title:
            errors.append('標題為必填')
        if not subject_id:
            errors.append('請選擇科目')
        if not professor_id:
            errors.append('請選擇教授')
        if not year:
            errors.append('請填寫學年度')
        if not semester:
            errors.append('請選擇學期')
        if not exam_type:
            errors.append('請選擇考試類型')

        if errors:
            for error in errors:
                flash(error, 'error')
            subjects = Subject.get_all(db_path)
            professors = Professor.get_all(db_path)
            return render_template('exams/form.html', exam=None,
                                   subjects=subjects, professors=professors)

        Exam.create(db_path, title, int(subject_id), int(professor_id),
                    year, semester, exam_type, content)
        flash('考古題新增成功！', 'success')
        return redirect(url_for('exams.list_exams'))

    subjects = Subject.get_all(db_path)
    professors = Professor.get_all(db_path)
    return render_template('exams/form.html', exam=None,
                           subjects=subjects, professors=professors)


@exam_bp.route('/<int:id>')
def detail_exam(id):
    """考古題詳情頁"""
    db_path = current_app.config['DATABASE']
    exam = Exam.get_by_id(db_path, id)

    if not exam:
        abort(404)

    return render_template('exams/detail.html', exam=exam)


@exam_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_exam(id):
    """編輯考古題"""
    db_path = current_app.config['DATABASE']
    exam = Exam.get_by_id(db_path, id)

    if not exam:
        abort(404)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        subject_id = request.form.get('subject_id', '').strip()
        professor_id = request.form.get('professor_id', '').strip()
        year = request.form.get('year', '').strip()
        semester = request.form.get('semester', '').strip()
        exam_type = request.form.get('exam_type', '').strip()
        content = request.form.get('content', '').strip()

        if not title:
            flash('標題為必填欄位！', 'error')
            subjects = Subject.get_all(db_path)
            professors = Professor.get_all(db_path)
            return render_template('exams/form.html', exam=exam,
                                   subjects=subjects, professors=professors)

        Exam.update(db_path, id, title, int(subject_id), int(professor_id),
                    year, semester, exam_type, content)
        flash('考古題更新成功！', 'success')
        return redirect(url_for('exams.detail_exam', id=id))

    subjects = Subject.get_all(db_path)
    professors = Professor.get_all(db_path)
    return render_template('exams/form.html', exam=exam,
                           subjects=subjects, professors=professors)


@exam_bp.route('/<int:id>/delete', methods=['POST'])
def delete_exam(id):
    """刪除考古題"""
    db_path = current_app.config['DATABASE']
    exam = Exam.get_by_id(db_path, id)

    if not exam:
        abort(404)

    Exam.delete(db_path, id)
    flash('考古題已刪除！', 'success')
    return redirect(url_for('exams.list_exams'))
