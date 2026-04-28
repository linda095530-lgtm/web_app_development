"""
App Factory — Flask 應用程式工廠
使用 create_app() 建立並設定 Flask 應用程式實體
"""
import os
import sqlite3
from flask import Flask
from config import Config


def create_app():
    """建立並設定 Flask 應用程式"""
    app = Flask(__name__,
                instance_relative_config=True,
                template_folder='app/templates',
                static_folder='app/static')

    # 載入設定
    app.config.from_object(Config)

    # 確保 instance 資料夾存在
    os.makedirs(app.instance_path, exist_ok=True)

    # 初始化資料庫
    init_db(app)

    # 註冊 Blueprint
    from app.routes.main import main_bp
    from app.routes.subject import subject_bp
    from app.routes.professor import professor_bp
    from app.routes.exam import exam_bp
    from app.routes.search import search_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(subject_bp)
    app.register_blueprint(professor_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(search_bp)

    return app


def init_db(app):
    """初始化資料庫：讀取 schema.sql 並建立資料表"""
    db_path = app.config['DATABASE']

    # 確保資料庫目錄存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # 讀取 schema.sql 並執行建表語法
    schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
    if os.path.exists(schema_path):
        conn = sqlite3.connect(db_path)
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.close()


# 應用程式入口
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
