"""
Professor Routes — 教授相關路由
Blueprint 前綴：/professors
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort
from app.models.professor import Professor
from app.models.subject import Subject
from app.models.exam import Exam

professor_bp = Blueprint('professors', __name__, url_prefix='/professors')


@professor_bp.route('/')
def list_professors():
    """教授列表頁"""
    db_path = current_app.config['DATABASE']
    professors = Professor.get_all(db_path)
    return render_template('professors/list.html', professors=professors)


@professor_bp.route('/create', methods=['GET', 'POST'])
def create_professor():
    """新增教授"""
    db_path = current_app.config['DATABASE']

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        subject_id = request.form.get('subject_id', '').strip()

        if not name:
            flash('教授姓名為必填欄位！', 'error')
            subjects = Subject.get_all(db_path)
            return render_template('professors/form.html', professor=None, subjects=subjects)

        subject_id = int(subject_id) if subject_id else None
        Professor.create(db_path, name, subject_id)
        flash('教授新增成功！', 'success')
        return redirect(url_for('professors.list_professors'))

    subjects = Subject.get_all(db_path)
    return render_template('professors/form.html', professor=None, subjects=subjects)


@professor_bp.route('/<int:id>')
def detail_professor(id):
    """教授詳情頁"""
    db_path = current_app.config['DATABASE']
    professor = Professor.get_by_id(db_path, id)

    if not professor:
        abort(404)

    exams = Exam.get_by_professor(db_path, id)

    return render_template('professors/detail.html',
                           professor=professor,
                           exams=exams)


@professor_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_professor(id):
    """編輯教授"""
    db_path = current_app.config['DATABASE']
    professor = Professor.get_by_id(db_path, id)

    if not professor:
        abort(404)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        subject_id = request.form.get('subject_id', '').strip()

        if not name:
            flash('教授姓名為必填欄位！', 'error')
            subjects = Subject.get_all(db_path)
            return render_template('professors/form.html', professor=professor, subjects=subjects)

        subject_id = int(subject_id) if subject_id else None
        Professor.update(db_path, id, name, subject_id)
        flash('教授資訊更新成功！', 'success')
        return redirect(url_for('professors.detail_professor', id=id))

    subjects = Subject.get_all(db_path)
    return render_template('professors/form.html', professor=professor, subjects=subjects)


@professor_bp.route('/<int:id>/delete', methods=['POST'])
def delete_professor(id):
    """刪除教授"""
    db_path = current_app.config['DATABASE']
    professor = Professor.get_by_id(db_path, id)

    if not professor:
        abort(404)

    Professor.delete(db_path, id)
    flash('教授已刪除！', 'success')
    return redirect(url_for('professors.list_professors'))
