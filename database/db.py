import sqlite3
import os

#DBファイルのパスを定義
#os.path.dirname(__file__)は、現在のファイルが存在するディレクトリのパスを返す
#../ =一つ上の階層を意味する(job_trackerディレクトリ)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'job_tracker.db')


def get_connection():
    """DB接続を返す関数"""
    return sqlite3.connect(DB_PATH)

def initialize_db():
    """テーブルを作成する関数。アプリ起動時に一回だけ呼ぶ"""
    conn = get_connection()
    cursor = conn.cursor()

    #フェーズマスターテーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phases(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            order_no INTEGER NOT NULL
        )             
    '''  )

    # チケットテーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            company     TEXT NOT NULL,
            phase_id    INTEGER NOT NULL,
            deadline    TEXT,
            apply_limit TEXT,
            priority    INTEGER,
            location    TEXT,
            employees   TEXT,
            job_desc    TEXT,
            required    TEXT,
            memo        TEXT,
            custom_1    TEXT,
            custom_2    TEXT,
            custom_3    TEXT,
            is_deleted  INTEGER DEFAULT 0,
            created_at  TEXT DEFAULT (datetime('now', 'localtime')),
            updated_at  TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (phase_id) REFERENCES phases(id)
        )
    ''')

    # 初期フェーズデータを投入（既に存在する場合はスキップ）
    cursor.execute('SELECT COUNT(*) FROM phases')
    if cursor.fetchone()[0] == 0:
        initial_phases = [
            ('応募前検討', 1),
            ('書類選考中', 2),
            ('一次面接',   3),
            ('二次面接',   4),
            ('最終面接',   5),
            ('内定',       6),
            ('辞退',       7),
            ('不合格',     8),
        ]
        cursor.executemany(
            'INSERT INTO phases (name, order_no) VALUES (?, ?)',
            initial_phases
        )

    conn.commit()
    conn.close()