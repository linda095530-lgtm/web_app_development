"""
Subject Model — 科目模型
提供科目資料的 CRUD 操作
"""
import sqlite3
from datetime import datetime


class Subject:
    """科目模型，對應 subjects 資料表"""

    def __init__(self, id=None, name=None, description='', created_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at

    @staticmethod
    def _get_db(db_path):
        """取得資料庫連線"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # 讓查詢結果可以用欄位名稱存取
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @staticmethod
    def create(db_path, name, description=''):
        """
        新增一筆科目
        :param db_path: 資料庫檔案路徑
        :param name: 科目名稱
        :param description: 科目描述
        :return: 新增的科目 ID
        """
        conn = Subject._get_db(db_path)
        try:
            cursor = conn.execute(
                "INSERT INTO subjects (name, description) VALUES (?, ?)",
                (name, description)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_all(db_path):
        """
        取得所有科目
        :param db_path: 資料庫檔案路徑
        :return: 科目列表（dict 格式）
        """
        conn = Subject._get_db(db_path)
        try:
            rows = conn.execute(
                """SELECT s.*, COUNT(e.id) as exam_count
                   FROM subjects s
                   LEFT JOIN exams e ON s.id = e.subject_id
                   GROUP BY s.id
                   ORDER BY s.name"""
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_by_id(db_path, subject_id):
        """
        依 ID 取得單筆科目
        :param db_path: 資料庫檔案路徑
        :param subject_id: 科目 ID
        :return: 科目資料（dict 格式）或 None
        """
        conn = Subject._get_db(db_path)
        try:
            row = conn.execute(
                "SELECT * FROM subjects WHERE id = ?",
                (subject_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def update(db_path, subject_id, name, description=''):
        """
        更新一筆科目
        :param db_path: 資料庫檔案路徑
        :param subject_id: 科目 ID
        :param name: 新的科目名稱
        :param description: 新的科目描述
        """
        conn = Subject._get_db(db_path)
        try:
            conn.execute(
                "UPDATE subjects SET name = ?, description = ? WHERE id = ?",
                (name, description, subject_id)
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete(db_path, subject_id):
        """
        刪除一筆科目
        :param db_path: 資料庫檔案路徑
        :param subject_id: 科目 ID
        """
        conn = Subject._get_db(db_path)
        try:
            conn.execute(
                "DELETE FROM subjects WHERE id = ?",
                (subject_id,)
            )
            conn.commit()
        finally:
            conn.close()
