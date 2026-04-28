"""
Config — 應用程式設定檔
"""
import os

# 專案根目錄
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Flask 設定"""
    # Flask Secret Key（用於 flash message 與 session）
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # SQLite 資料庫路徑
    DATABASE = os.path.join(BASE_DIR, 'instance', 'database.db')
