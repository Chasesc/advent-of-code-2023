import inspect
from pathlib import Path


def load_input(filename: str) -> str:
    calling_module = Path(inspect.stack()[1].filename).stem
    file_path = Path("inputs") / calling_module / filename
    return file_path.read_text()
