class Note:
    """
    Base abstract class for note object
    """

    def __init__(self, id: str, text: str, is_private: bool, owner_token: str) -> None:
        self.id = id
        self.text = text
        self.is_private = is_private
        self.owner_token = owner_token

    def is_owner(self, owner_token: str) -> bool:
        return self.owner_token == owner_token

    def get_id(self) -> str:
        return self.id

    def get_text(self) -> str:
        return self.text

    def get_is_private(self) -> bool:
        return self.is_private

    def set_owner(self, owner_token: str):
        raise NotImplementedError()

    def set_text(self, new_text: str):
        raise NotImplementedError()

    def set_is_private(self, is_private: bool):
        raise NotImplementedError()

    def can_view(self, owner_token: str) -> bool:
        return self.owner_token == owner_token or not self.get_is_private()

    def __str__(self) -> str:
        return f"Note with id {self.get_id()}"

    def __repr__(self) -> str:
        return f"Note(id={self.get_id()})"
