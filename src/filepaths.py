import os


def check_directory_exists(dir_path):
    '''
    Check to see if a directory path exists, if not create one.
    Args:
        dir_path: <string> path to directory
    Return:
        dir_path: <string> path to directory
    '''
    if os.path.isdir(dir_path) is False:
        os.mkdir(dir_path)
    else:
        pass
    return dir_path


def find_sem_file_paths(dir_path,
                        file_extension,
                        image_extension):
    '''
    Find text and image files in target directory. Create two arrays based on
    file extensions.
    Args:
        dir_path: <string> path to directory
        file_extension: <string> text file extension
        iamge_extension: <string> image file extension
    Returns:
        files: <array> array of dictionaries containing file names, file paths,
                and corresponding image paths
    '''
    text_paths = sorted(dir_path.glob(f'*{file_extension}'))
    image_paths = sorted(dir_path.glob(f'*{image_extension}'))
    return [
        {
            'filename': text_path.stem,
            'log_path': text_path,
            'image_path': image_path
        } for text_path, image_path in zip(text_paths, image_paths)
        if text_path.stem == image_path.stem]
