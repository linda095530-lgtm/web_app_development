"""
Subject Routes — 科目相關路由
Blueprint 前綴：/subjects
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

subject_bp = Blueprint('subjects', __name__, url_prefix='/subjects')


@subject_bp.route('/')
def list_subjects():
    """
    科目列表頁
    GET /subjects
    - 呼叫 Subject.get_all() 取得所有科目（含考古題數量）
    - 模板：subjects/list.html
    """
    pass


@subject_bp.route('/create', methods=['GET', 'POST'])
def create_subject():
    """
    新增科目
    GET  /subjects/create — 顯示空白表單
    POST /subjects/create — 接收表單並存入資料庫
    - 表單欄位：name（必填）、description（選填）
    - 驗證：name 不可為空
    - 成功後重導向至 /subjects
    - 模板：subjects/form.html
    """
    pass


@subject_bp.route('/<int:id>')
def detail_subject(id):
    """
    科目詳情頁
    GET /subjects/<id>
    - 呼叫 Subject.get_by_id(id) 取得科目資料
    - 呼叫 Exam.get_by_subject(id) 取得該科目考古題
    - 呼叫 Professor.get_by_subject(id) 取得該科目教授
    - 科目不存在時回傳 404
    - 模板：subjects/detail.html
    """
    pass


@subject_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_subject(id):
    """
    編輯科目
    GET  /subjects/<id>/edit — 顯示預填資料的編輯表單
    POST /subjects/<id>/edit — 接收表單並更新資料庫
    - 表單欄位：name（必填）、description（選填）
    - 成功後重導向至 /subjects/<id>
    - 模板：subjects/form.html（與新增共用）
    """
    pass


@subject_bp.route('/<int:id>/delete', methods=['POST'])
def delete_subject(id):
    """
    刪除科目
    POST /subjects/<id>/delete
    - 呼叫 Subject.delete(id)
    - 成功後重導向至 /subjects
    - 科目不存在時回傳 404
    """
    pass
