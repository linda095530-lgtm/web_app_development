"""
Exam Routes — 考古題相關路由
Blueprint 前綴：/exams
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

exam_bp = Blueprint('exams', __name__, url_prefix='/exams')


@exam_bp.route('/')
def list_exams():
    """
    考古題列表頁（支援篩選）
    GET /exams?subject_id=&professor_id=&year=&exam_type=
    - 呼叫 Exam.get_all() 取得所有考古題（可帶篩選參數）
    - 呼叫 Subject.get_all() 取得科目篩選選項
    - 呼叫 Professor.get_all() 取得教授篩選選項
    - 呼叫 Exam.get_years() 取得年度篩選選項
    - 模板：exams/list.html
    """
    pass


@exam_bp.route('/create', methods=['GET', 'POST'])
def create_exam():
    """
    新增考古題
    GET  /exams/create — 顯示空白表單（含科目、教授下拉選單）
    POST /exams/create — 接收表單並存入資料庫
    - 表單欄位：title, subject_id, professor_id, year, semester, exam_type, content
    - 需呼叫 Subject.get_all() 和 Professor.get_all() 取得選項
    - 驗證：title, subject_id, professor_id, year, semester, exam_type 為必填
    - 成功後重導向至 /exams
    - 模板：exams/form.html
    """
    pass


@exam_bp.route('/<int:id>')
def detail_exam(id):
    """
    考古題詳情頁
    GET /exams/<id>
    - 呼叫 Exam.get_by_id(id) 取得考古題完整資料（含科目與教授名稱）
    - 考古題不存在時回傳 404
    - 模板：exams/detail.html
    """
    pass


@exam_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_exam(id):
    """
    編輯考古題
    GET  /exams/<id>/edit — 顯示預填資料的編輯表單
    POST /exams/<id>/edit — 接收表單並更新資料庫
    - 表單欄位：title, subject_id, professor_id, year, semester, exam_type, content
    - 需呼叫 Subject.get_all() 和 Professor.get_all() 取得選項
    - 成功後重導向至 /exams/<id>
    - 模板：exams/form.html（與新增共用）
    """
    pass


@exam_bp.route('/<int:id>/delete', methods=['POST'])
def delete_exam(id):
    """
    刪除考古題
    POST /exams/<id>/delete
    - 呼叫 Exam.delete(id)
    - 成功後重導向至 /exams
    - 考古題不存在時回傳 404
    """
    pass
