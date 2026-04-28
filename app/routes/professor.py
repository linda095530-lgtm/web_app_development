"""
Professor Routes — 教授相關路由
Blueprint 前綴：/professors
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

professor_bp = Blueprint('professors', __name__, url_prefix='/professors')


@professor_bp.route('/')
def list_professors():
    """
    教授列表頁
    GET /professors
    - 呼叫 Professor.get_all() 取得所有教授（含所屬科目名稱與考古題數量）
    - 模板：professors/list.html
    """
    pass


@professor_bp.route('/create', methods=['GET', 'POST'])
def create_professor():
    """
    新增教授
    GET  /professors/create — 顯示空白表單（含科目下拉選單）
    POST /professors/create — 接收表單並存入資料庫
    - 表單欄位：name（必填）、subject_id（選填）
    - 需呼叫 Subject.get_all() 取得科目選項
    - 成功後重導向至 /professors
    - 模板：professors/form.html
    """
    pass


@professor_bp.route('/<int:id>')
def detail_professor(id):
    """
    教授詳情頁
    GET /professors/<id>
    - 呼叫 Professor.get_by_id(id) 取得教授資料
    - 呼叫 Exam.get_by_professor(id) 取得該教授考古題
    - 教授不存在時回傳 404
    - 模板：professors/detail.html
    """
    pass


@professor_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_professor(id):
    """
    編輯教授
    GET  /professors/<id>/edit — 顯示預填資料的編輯表單
    POST /professors/<id>/edit — 接收表單並更新資料庫
    - 表單欄位：name（必填）、subject_id（選填）
    - 需呼叫 Subject.get_all() 取得科目選項
    - 成功後重導向至 /professors/<id>
    - 模板：professors/form.html（與新增共用）
    """
    pass


@professor_bp.route('/<int:id>/delete', methods=['POST'])
def delete_professor(id):
    """
    刪除教授
    POST /professors/<id>/delete
    - 呼叫 Professor.delete(id)
    - 成功後重導向至 /professors
    - 教授不存在時回傳 404
    """
    pass
