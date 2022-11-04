"""
Decorators file
"""

from config import LANG_MANAGER
from util.pyqt import alert_message_box


def try_function(fail_message="Error"):
    def wrapper_with_args(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except IOError as e:
                alert_message_box(LANG_MANAGER.get(
                    LANG_MANAGER.ERROR), fail_message)

        return wrapper

    return wrapper_with_args
