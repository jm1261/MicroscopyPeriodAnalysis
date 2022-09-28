import os
import json
import numpy as np
import tkinter as tk
from tkinter import filedialog


def GetFilename(file_path):
    '''
    Split file path to obtain only filename without extension.
    Args:
        file_path: <string> path to file
    Returns:
        file_name: <string> file name string without path or extension
    '''
    return os.path.splitext(os.path.basename(file_path))[0]


def FindThePath(default,
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


def FileSort(dir_path):
    '''
    Numerically sort a directory containing a combination of string file names
    and numerical file names.
    Args:
        dir_path: <string> path to directory
    Returns:
        sorted_array: <array> contents of dir_path sorted numerically
    '''
    return sorted(os.listdir(dir_path))


def ExtractFile(dir_path,
                file_string):
    '''
    Stack file names in a directory into an array. Returns data files array
    if file_string in file names.
    Args:
        dir_path: <string> path to directory
        file_string: <string> string within desired file names
    Returns:
        array: <array> array of sorted and selected file names
    '''
    dirlist = FileSort(dir_path=dir_path)
    return [file for file in dirlist if file_string in file]


def FindDirFile(dir_path,
                file_string,
                image_string):
    '''
    Find files in target directory. Creates two arrays, data files and plotted
    files. Find files searches for target strings in directory, namely file
    extensions.
    Args:
        dir_path: <string> path to directory
        file_String: <string> string within data files
        image_string: <string> string within image files
    Returns:
        datafiles: <array> array of all files within directory with file_string
                    in file name
        imagefiles: <arrau> array of all files within directory with image_
                    string in file name
    '''
    datafiles = ExtractFile(
        dir_path=dir_path,
        file_string=file_string)
    plotfiles = ExtractFile(
        dir_path=dir_path,
        file_string=image_string)
    return datafiles, plotfiles


def convert(o):
    '''
    Check type of data string
    '''
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError


def JsonOut(out_path,
            dictionary):
    '''
    Save dictionary to json file.
    Args:
        out_path: <string> path to file, including file name and extension
        dictionary: <dict> python dictionary to save out
    Returns:
        None
    '''
    with open(out_path, 'w') as outfile:
        json.dump(
            dictionary,
            outfile,
            indent=2,
            default=convert)
        outfile.write('\n')
