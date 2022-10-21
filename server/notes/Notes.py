from typing import List
from notes.Note import Note


class Notes:
    """
    Base abstract class for notes object
    """

    def __init__(self) -> None:
        raise NotImplementedError()

    def new_note(self, owner_token: str, text: str, is_private: bool) -> Note:
        raise NotImplementedError()

    def get_by_id(self, id: str) -> Note:
        raise NotImplementedError()

    def get_user_notes(self, user_token: str) -> List[Note]:
        raise NotImplementedError()

    def delete_note(self, note: Note):
        raise NotImplementedError()
