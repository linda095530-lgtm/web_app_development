"""
Professor Model — 教授模型
提供教授資料的 CRUD 操作
"""
import sqlite3
from datetime import datetime


class Professor:
    """教授模型，對應 professors 資料表"""

    def __init__(self, id=None, name=None, subject_id=None, created_at=None):
        self.id = id
        self.name = name
        self.subject_id = subject_id
        self.created_at = created_at

    @staticmethod
    def _get_db(db_path):
        """取得資料庫連線"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @staticmethod
    def create(db_path, name, subject_id=None):
        """
        新增一位教授
        :param db_path: 資料庫檔案路徑
        :param name: 教授姓名
        :param subject_id: 所屬科目 ID
        :return: 新增的教授 ID
        """
        conn = Professor._get_db(db_path)
        try:
            cursor = conn.execute(
                "INSERT INTO professors (name, subject_id) VALUES (?, ?)",
                (name, subject_id)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_all(db_path):
        """
        取得所有教授（含所屬科目名稱）
        :param db_path: 資料庫檔案路徑
        :return: 教授列表（dict 格式）
        """
        conn = Professor._get_db(db_path)
        try:
            rows = conn.execute(
                """SELECT p.*, s.name as subject_name,
                          COUNT(e.id) as exam_count
                   FROM professors p
                   LEFT JOIN subjects s ON p.subject_id = s.id
                   LEFT JOIN exams e ON p.id = e.professor_id
                   GROUP BY p.id
                   ORDER BY p.name"""
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_by_id(db_path, professor_id):
        """
        依 ID 取得單位教授（含所屬科目名稱）
        :param db_path: 資料庫檔案路徑
        :param professor_id: 教授 ID
        :return: 教授資料（dict 格式）或 None
        """
        conn = Professor._get_db(db_path)
        try:
            row = conn.execute(
                """SELECT p.*, s.name as subject_name
                   FROM professors p
                   LEFT JOIN subjects s ON p.subject_id = s.id
                   WHERE p.id = ?""",
                (professor_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def get_by_subject(db_path, subject_id):
        """
        依科目 ID 取得該科目的所有教授
        :param db_path: 資料庫檔案路徑
        :param subject_id: 科目 ID
        :return: 教授列表（dict 格式）
        """
        conn = Professor._get_db(db_path)
        try:
            rows = conn.execute(
                "SELECT * FROM professors WHERE subject_id = ? ORDER BY name",
                (subject_id,)
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def update(db_path, professor_id, name, subject_id=None):
        """
        更新一位教授
        :param db_path: 資料庫檔案路徑
        :param professor_id: 教授 ID
        :param name: 新的教授姓名
        :param subject_id: 新的所屬科目 ID
        """
        conn = Professor._get_db(db_path)
        try:
            conn.execute(
                "UPDATE professors SET name = ?, subject_id = ? WHERE id = ?",
                (name, subject_id, professor_id)
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete(db_path, professor_id):
        """
        刪除一位教授
        :param db_path: 資料庫檔案路徑
        :param professor_id: 教授 ID
        """
        conn = Professor._get_db(db_path)
        try:
            conn.execute(
                "DELETE FROM professors WHERE id = ?",
                (professor_id,)
            )
            conn.commit()
        finally:
            conn.close()
