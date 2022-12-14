"""
Realization of BaseNote class.
Gives api for saving and loading files from local computer.
"""

from pathlib import Path
from notes.BaseNote import BaseNote


def is_file_exists(file_path: str):
    return Path(file_path).is_file()


class LocalNote(BaseNote):
    def __init__(self, file_path, text: str, readonly=False) -> None:
        self.file_path = file_path

        if not is_file_exists(self.file_path):
            raise FileNotFoundError()

        super().__init__(text, readonly)

    def _save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(self.text)

    def __str__(self) -> str:
        return self.file_path

    @staticmethod
    def load_file(file_path: str):
        if not is_file_exists(file_path):
            raise FileNotFoundError()

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            f.close()
            return LocalNote(file_path, content)

    @staticmethod
    def new_file(file_path: str):
        if is_file_exists(file_path):
            raise FileExistsError()

        open(file_path, "a", encoding="utf-8").close()
        return LocalNote(file_path, "")

    @staticmethod
    def get_or_create_file(file_path: str):
        try:
            return LocalNote.new_file(file_path)
        except:
            return LocalNote.load_file(file_path)
