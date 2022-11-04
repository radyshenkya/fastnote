"""
Realization of BaseNote class.
Gives api for loading and saving remote notes on server.
"""

from notes.BaseNote import BaseNote
from util.server import *


class RemoteNote(BaseNote):
    def __init__(
        self,
        user_token: str,
        server_point: str,
        note_id: str,
        text: str,
        readonly=False,
    ) -> None:

        self.note_id = note_id
        self.user_token = user_token
        self.server_point = server_point

        super().__init__(text, readonly)

    def _save(self):
        patch_note(self.server_point, self.user_token,
                   self.note_id, self.text, False)

    def __str__(self) -> str:
        return f"{clear_address(self.server_point)}/{self.note_id}"

    @staticmethod
    def load_note_from_server(server_point: str, user_token: str, id: str):
        json_note = get_note_details(server_point, user_token, id)

        return RemoteNote(
            user_token,
            server_point,
            id,
            json_note["text"],
            not is_owned_note(server_point, user_token, id),
        )

    @staticmethod
    def new_note(server_point: str, user_token: str):
        note_id = new_note(server_point, user_token, "", False)

        return RemoteNote(
            user_token,
            server_point,
            note_id,
            "",
            False,
        )

    @staticmethod
    def fetch_notes_from_server(server_point: str, user_token: str):
        notes = get_user_note_ids(server_point, user_token)

        return notes
