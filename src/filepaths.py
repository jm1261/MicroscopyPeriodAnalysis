import os
from pathlib import Path


def get_working_directory(subdirectory='TestImages'):
    current_directory = os.getcwd()
    working_directory = os.path.join(
        current_directory, subdirectory)
    return working_directory


def FindDirFile(working_directory,
                log_extension,
                image_extension):
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
    working_path = Path(working_directory)

    logfile_paths = sorted(working_path.glob(f'*{log_extension}'))
    image_paths = sorted(working_path.glob(f'*{image_extension}'))

    return [{
                'filename': logfile_path.stem,
                'logfile_path': logfile_path,
                'image_path': image_path,
            } for logfile_path, image_path in zip(logfile_paths, image_paths)
        if logfile_path.stem == image_path.stem]
