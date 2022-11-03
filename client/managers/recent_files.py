import sqlite3

DATABASE_INITIALIZING_SCRIPT = """
CREATE TABLE IF NOT EXISTS recent_files (
    id INTEGER PRIMARY KEY,
    path TEXT NOT NULL
)
"""


class RecentFilesManager:
    def __init__(self, database_path: str, max_recent_files=10):
        self.recent_files_limit = max_recent_files
        self.connection = sqlite3.connect(database_path)
        cursor = self._get_cursor()
        cursor.execute(DATABASE_INITIALIZING_SCRIPT)
        self.connection.commit()
        self.clean_database_to_limit()

    def get_files(self):
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM recent_files ORDER BY id DESC")
        return cursor.fetchall()

    def get_last(self):
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM recent_files ORDER BY id DESC LIMIT 1")
        return cursor.fetchone()

    def push(self, path: str):
        cursor = self._get_cursor()

        if path in list(map(lambda item: item[1], self.get_files())):
            cursor.execute(
                "UPDATE recent_files SET id=? WHERE path=?", (self.get_last()[0]+1, path))
        else:
            cursor.execute(
                "INSERT INTO recent_files (path) VALUES (?)", (path,))

        self.connection.commit()
        self.clean_database_to_limit()

    def clean_database_to_limit(self):
        cursor = self._get_cursor()
        cursor.execute(
            """DELETE FROM recent_files WHERE id NOT IN (SELECT id FROM recent_files ORDER BY id DESC LIMIT ?)""",
            (self.recent_files_limit,))

        self.connection.commit()

    def _get_cursor(self):
        return self.connection.cursor()

    def __del__(self):
        self.connection.close()
