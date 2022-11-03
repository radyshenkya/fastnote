from importlib import util
import os
from types import ModuleType
from typing import List


def load_module_from_file(module_name: str, file_path: str) -> ModuleType:
    spec = util.spec_from_file_location(module_name, file_path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def list_files_in_dir(path: str) -> List[str]:
    return list(
        filter(lambda item: os.path.isfile(
            os.path.join(path, item)), os.listdir(path))
    )


def list_dirs_in_dir(path: str) -> List[str]:
    return list(
        filter(lambda item: os.path.isdir(
            os.path.join(path, item)), os.listdir(path))
    )
