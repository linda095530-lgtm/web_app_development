"""
Exam Model — 考古題模型
提供考古題資料的 CRUD 操作與搜尋功能
"""
import sqlite3
from datetime import datetime


class Exam:
    """考古題模型，對應 exams 資料表"""

    def __init__(self, id=None, title=None, subject_id=None,
                 professor_id=None, year=None, semester=None,
                 exam_type=None, content='', created_at=None,
                 updated_at=None):
        self.id = id
        self.title = title
        self.subject_id = subject_id
        self.professor_id = professor_id
        self.year = year
        self.semester = semester
        self.exam_type = exam_type
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def _get_db(db_path):
        """取得資料庫連線"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @staticmethod
    def create(db_path, title, subject_id, professor_id, year,
               semester, exam_type, content=''):
        """
        新增一份考古題
        :return: 新增的考古題 ID
        """
        conn = Exam._get_db(db_path)
        try:
            cursor = conn.execute(
                """INSERT INTO exams
                   (title, subject_id, professor_id, year, semester, exam_type, content)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (title, subject_id, professor_id, year, semester, exam_type, content)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_all(db_path, subject_id=None, professor_id=None,
                year=None, exam_type=None):
        """
        取得所有考古題（可篩選）
        :param subject_id: 篩選科目（可選）
        :param professor_id: 篩選教授（可選）
        :param year: 篩選學年度（可選）
        :param exam_type: 篩選考試類型（可選）
        :return: 考古題列表（dict 格式）
        """
        conn = Exam._get_db(db_path)
        try:
            query = """
                SELECT e.*, s.name as subject_name, p.name as professor_name
                FROM exams e
                LEFT JOIN subjects s ON e.subject_id = s.id
                LEFT JOIN professors p ON e.professor_id = p.id
                WHERE 1=1
            """
            params = []

            if subject_id:
                query += " AND e.subject_id = ?"
                params.append(subject_id)
            if professor_id:
                query += " AND e.professor_id = ?"
                params.append(professor_id)
            if year:
                query += " AND e.year = ?"
                params.append(year)
            if exam_type:
                query += " AND e.exam_type = ?"
                params.append(exam_type)

            query += " ORDER BY e.year DESC, e.semester DESC, e.created_at DESC"

            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_by_id(db_path, exam_id):
        """
        依 ID 取得單份考古題（含科目與教授名稱）
        :return: 考古題資料（dict 格式）或 None
        """
        conn = Exam._get_db(db_path)
        try:
            row = conn.execute(
                """SELECT e.*, s.name as subject_name, p.name as professor_name
                   FROM exams e
                   LEFT JOIN subjects s ON e.subject_id = s.id
                   LEFT JOIN professors p ON e.professor_id = p.id
                   WHERE e.id = ?""",
                (exam_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def get_by_subject(db_path, subject_id):
        """依科目 ID 取得該科目的所有考古題"""
        return Exam.get_all(db_path, subject_id=subject_id)

    @staticmethod
    def get_by_professor(db_path, professor_id):
        """依教授 ID 取得該教授的所有考古題"""
        return Exam.get_all(db_path, professor_id=professor_id)

    @staticmethod
    def update(db_path, exam_id, title, subject_id, professor_id,
               year, semester, exam_type, content=''):
        """
        更新一份考古題
        """
        conn = Exam._get_db(db_path)
        try:
            conn.execute(
                """UPDATE exams
                   SET title = ?, subject_id = ?, professor_id = ?,
                       year = ?, semester = ?, exam_type = ?, content = ?,
                       updated_at = datetime('now', 'localtime')
                   WHERE id = ?""",
                (title, subject_id, professor_id, year, semester,
                 exam_type, content, exam_id)
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete(db_path, exam_id):
        """
        刪除一份考古題
        """
        conn = Exam._get_db(db_path)
        try:
            conn.execute(
                "DELETE FROM exams WHERE id = ?",
                (exam_id,)
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def search(db_path, keyword, subject_id=None, professor_id=None,
               year=None):
        """
        搜尋考古題（依標題與內容全文搜尋）
        :param keyword: 搜尋關鍵字
        :param subject_id: 篩選科目（可選）
        :param professor_id: 篩選教授（可選）
        :param year: 篩選學年度（可選）
        :return: 搜尋結果列表（dict 格式）
        """
        conn = Exam._get_db(db_path)
        try:
            query = """
                SELECT e.*, s.name as subject_name, p.name as professor_name
                FROM exams e
                LEFT JOIN subjects s ON e.subject_id = s.id
                LEFT JOIN professors p ON e.professor_id = p.id
                WHERE (e.title LIKE ? OR e.content LIKE ?)
            """
            like_keyword = f"%{keyword}%"
            params = [like_keyword, like_keyword]

            if subject_id:
                query += " AND e.subject_id = ?"
                params.append(subject_id)
            if professor_id:
                query += " AND e.professor_id = ?"
                params.append(professor_id)
            if year:
                query += " AND e.year = ?"
                params.append(year)

            query += " ORDER BY e.year DESC, e.semester DESC"

            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_years(db_path):
        """取得所有不重複的學年度（用於篩選下拉選單）"""
        conn = Exam._get_db(db_path)
        try:
            rows = conn.execute(
                "SELECT DISTINCT year FROM exams ORDER BY year DESC"
            ).fetchall()
            return [row['year'] for row in rows]
        finally:
            conn.close()
