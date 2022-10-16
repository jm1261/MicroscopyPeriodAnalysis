import os


def GetFilename(file_path):
    '''
    Split file path to obtain only filename without extension.
    Args:
        file_path: <string> path to file
    Returns:
        file_name: <string> file name string without path or extension
    '''
    return os.path.splitext(os.path.basename(file_path))[0]


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
