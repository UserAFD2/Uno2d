import sys
import os

def resource_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundles files into a temp folder stored in _MEIPASS
        base_path = sys._MEIPASS
    else:
        # Use the root of the project (the parent directory of 'scripts')
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    return os.path.join(base_path, relative_path)
