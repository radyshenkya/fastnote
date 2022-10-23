class INote:
    """
    Base class for note edits
    """

    def __init__(self, text: str, readonly: str) -> None:
        self.text = text
        self.readonly = readonly

    def set_text(self, text: str):
        self.text = text

    def _save(self):
        raise NotImplementedError()

    def save(self):
        if self.readonly:
            raise IOError()

        self._save()

    def __str__(self) -> str:
        return "BaseNoteClass"
