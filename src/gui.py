import tkinter as tk
from tkinter import filedialog

def prompt_for_path(default,
                title,
                dir_path=False,
                file_path=False,
                file_type=False):
    '''
    Interactive path finder. Uses tkinter to select directory of file path(s).
    Returns path to directory or file(s).
    Args:
        default: <string> path to default directory for interactive window
        title: <string> window title
        dir_path: <bool> if True, find path looks for directory path
        file_path: <bool> if True, find path looks for file path, returns
                    tuple of file paths
        file_type: <string> if file_path True, file_type must be of the form
                    "[(file type, *.file extension)]"
    Returns:
        path: <string/tuple> string to desired object(s), or tuple of filepaths
    '''
    root = tk.Tk()
    root.withdraw()
    path = 'Please Select dir_path or file_path'
    if dir_path:
        path = filedialog.askdirectory(
            initialdir=default,
            title=title)
    if file_path:
        path = filedialog.askopenfilenames(
            initialdir=default,
            filetypes=file_type,
            title=title)
    return path