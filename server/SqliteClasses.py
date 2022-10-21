import sqlite3
from typing import List
from xxlimited import new

from notes.Note import Note
from notes.Notes import Notes
from utils import hash_str, generate_new_note_id

SQLITE_DB_PATH = "./main.db"


conn = sqlite3.connect(SQLITE_DB_PATH, check_same_thread=False)
cur = conn.cursor()


class SqlNotes(Notes):
    def __init__(self) -> None:
        pass

    def new_note(self, owner_token: str, text: str, is_private: bool) -> Note:
        owner_token = hash_str(owner_token)
        new_note_id = generate_new_note_id()

        # Inserting new note into database
        cur.execute(
            "INSERT INTO notes (id, content, is_private, owner_token) VALUES (?, ?, ?, ?)",
            (
                new_note_id,
                text,
                int(is_private),
                owner_token,
            ),
        )

        conn.commit()

        return SqlNote(new_note_id, text, is_private, owner_token)

    def get_by_id(self, id: str) -> Note:
        res = cur.execute("SELECT * FROM notes WHERE id=?", (id,))

        fetched = res.fetchone()
        if fetched is None:
            raise IndexError(f"Can not find note with id {id}")

        return SqlNote(fetched[0], fetched[1], fetched[2], fetched[3])

    def get_user_notes(self, user_token: str) -> List[Note]:
        res = cur.execute(
            "SELECT * FROM notes WHERE owner_token=?", (hash_str(user_token),)
        )
        return [Note(x[0], x[1], x[2], x[3]) for x in res.fetchall()]

    def delete_note(self, note: Note):
        note_id = note.get_id()

        cur.execute("DELETE FROM notes WHERE id=?", (note_id,))
        conn.commit()


class SqlNote(Note):
    def is_owner(self, owner_token: str) -> bool:
        return self.owner_token == hash_str(owner_token)

    def set_owner(self, owner_token: str):
        owner_token = hash_str(owner_token)

        cur.execute(
            "UPDATE notes SET owner_token=? WHERE id=?",
            (owner_token, self.get_id()),
        )
        conn.commit()

        self.owner_token = owner_token

    def set_text(self, new_text: str):
        cur.execute(
            "UPDATE notes SET content=? WHERE id=?",
            (new_text, self.get_id()),
        )

        conn.commit()

        self.text = new_text

    def set_is_private(self, is_private: bool):
        cur.execute(
            "UPDATE notes SET is_private=? WHERE id=?",
            (int(is_private), self.get_id()),
        )

        conn.commit()

        self.is_private = is_private

    def can_view(self, owner_token: str) -> bool:
        owner_token = hash_str(owner_token)
        return super().can_view(owner_token)


# This file can run sql scripts for database
if __name__ == "__main__":
    from sys import argv

    if len(argv) <= 1:
        exit("Specify script path.")

    with open(argv[1]) as sql_file:
        script = sql_file.read()

        cur.executescript(script)

        conn.commit()
        conn.close()

        print("Successfully executed")
