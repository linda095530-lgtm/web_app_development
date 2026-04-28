-- =============================================
-- 考古題收藏系統 — 資料庫建表語法
-- 資料庫：SQLite
-- =============================================

-- 啟用外鍵約束（SQLite 預設關閉）
PRAGMA foreign_keys = ON;

-- -----------------------------------------
-- 1. 科目表 (subjects)
-- -----------------------------------------
CREATE TABLE IF NOT EXISTS subjects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    description TEXT    DEFAULT '',
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- -----------------------------------------
-- 2. 教授表 (professors)
-- -----------------------------------------
CREATE TABLE IF NOT EXISTS professors (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    subject_id  INTEGER,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
        ON DELETE SET NULL
);

-- -----------------------------------------
-- 3. 考古題表 (exams)
-- -----------------------------------------
CREATE TABLE IF NOT EXISTS exams (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    title         TEXT    NOT NULL,
    subject_id    INTEGER NOT NULL,
    professor_id  INTEGER NOT NULL,
    year          TEXT    NOT NULL,
    semester      TEXT    NOT NULL,
    exam_type     TEXT    NOT NULL,
    content       TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at    TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (subject_id)   REFERENCES subjects(id)   ON DELETE CASCADE,
    FOREIGN KEY (professor_id) REFERENCES professors(id) ON DELETE CASCADE
);

-- -----------------------------------------
-- 建立索引以提升查詢效能
-- -----------------------------------------
CREATE INDEX IF NOT EXISTS idx_exams_subject_id    ON exams(subject_id);
CREATE INDEX IF NOT EXISTS idx_exams_professor_id  ON exams(professor_id);
CREATE INDEX IF NOT EXISTS idx_exams_year          ON exams(year);
CREATE INDEX IF NOT EXISTS idx_exams_exam_type     ON exams(exam_type);
CREATE INDEX IF NOT EXISTS idx_professors_subject_id ON professors(subject_id);
