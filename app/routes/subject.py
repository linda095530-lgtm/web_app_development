"""
Subject Routes — 科目相關路由
Blueprint 前綴：/subjects
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort
from app.models.subject import Subject
from app.models.professor import Professor
from app.models.exam import Exam

subject_bp = Blueprint('subjects', __name__, url_prefix='/subjects')


@subject_bp.route('/')
def list_subjects():
    """科目列表頁"""
    db_path = current_app.config['DATABASE']
    subjects = Subject.get_all(db_path)
    return render_template('subjects/list.html', subjects=subjects)


@subject_bp.route('/create', methods=['GET', 'POST'])
def create_subject():
    """新增科目"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()

        # 驗證必填欄位
        if not name:
            flash('科目名稱為必填欄位！', 'error')
            return render_template('subjects/form.html', subject=None)

        db_path = current_app.config['DATABASE']
        Subject.create(db_path, name, description)
        flash('科目新增成功！', 'success')
        return redirect(url_for('subjects.list_subjects'))

    return render_template('subjects/form.html', subject=None)


@subject_bp.route('/<int:id>')
def detail_subject(id):
    """科目詳情頁"""
    db_path = current_app.config['DATABASE']
    subject = Subject.get_by_id(db_path, id)

    if not subject:
        abort(404)

    exams = Exam.get_by_subject(db_path, id)
    professors = Professor.get_by_subject(db_path, id)

    return render_template('subjects/detail.html',
                           subject=subject,
                           exams=exams,
                           professors=professors)


@subject_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_subject(id):
    """編輯科目"""
    db_path = current_app.config['DATABASE']
    subject = Subject.get_by_id(db_path, id)

    if not subject:
        abort(404)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()

        if not name:
            flash('科目名稱為必填欄位！', 'error')
            return render_template('subjects/form.html', subject=subject)

        Subject.update(db_path, id, name, description)
        flash('科目更新成功！', 'success')
        return redirect(url_for('subjects.detail_subject', id=id))

    return render_template('subjects/form.html', subject=subject)


@subject_bp.route('/<int:id>/delete', methods=['POST'])
def delete_subject(id):
    """刪除科目"""
    db_path = current_app.config['DATABASE']
    subject = Subject.get_by_id(db_path, id)

    if not subject:
        abort(404)

    Subject.delete(db_path, id)
    flash('科目已刪除！', 'success')
    return redirect(url_for('subjects.list_subjects'))
