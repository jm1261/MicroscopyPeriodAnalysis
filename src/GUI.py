import tkinter as tk

from pathlib import Path
from tkinter import filedialog


def prompt_for_path(default,
                    title,
                    dir_path=False,
                    file_path=False,
                    file_type=False):
    '''
    Interactive path finder for windows only. Uses tkinter to select directory
    or file path(s). Returns path to directory or file(s).
    Args:
        default: <string> path to default directory for interactive window
        title: <string> window title
        dir_path: <bool>
        file_path: <bool>
        file_type: <string>
    Returns:
    '''
    root = tk.Tk()
    root.withdraw()
    path = 'Please Select dir_path or file_path'
    if dir_path:
        directory_path = filedialog.askdirectory(
            initialdir=default,
            title=title)
        path = Path(directory_path)
    if file_path:
        file_path = filedialog.askopenfilenames(
            initialdir=default,
            filetypes=file_type,
            title=title)
        path = [Path(paths) for paths in file_path]
    return path
