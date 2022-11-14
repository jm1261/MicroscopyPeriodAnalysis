import os

from pathlib import Path
from sys import platform
from src.fileIO import load_json
from src.GUI import prompt_for_path


def check_platform():
    '''
    Check operating system.
    Args:
        None
    Returns:
        operating_system: <string> "Windows", "Linux", or "Mac"
    '''
    if platform == 'linux' or platform == 'linux2':
        operating_system = 'Linux'
    elif platform == 'darwin':
        operating_system = 'Mac'
    elif platform == 'win32':
        operating_system = 'Windows'
    return operating_system


def get_directory_paths(root_path):
    '''
    Get target data path and results path from info dictionary file.
    Args:
        root_path: <string> path to root directory
    Returns:
        data_path: <string> path to data directory
        bg_path: <string> path to background directory
        results_path: <string> path to results directory
        info: <dict> information dictionary (info.json)
    '''
    info = load_json(file_path=Path(f'{root_path}/info.json'))
    directory_paths = {}
    for key, value in info.items():
        if 'Path' in key:
            directory_paths.update({key: Path(f'{root_path}/{value}')})
    return info, directory_paths


def extractfile(directory_path,
                file_string):
    '''
    Pull file from directory path.
    Args:
        directory_path: <string> path to file
        file_string: <string> string contained within file name
    Returns:
        array: <array> array of selected files
    '''
    directory_list = sorted(os.listdir(directory_path))
    return [file for file in directory_list if file_string in file]


def get_files_paths(directory_path,
                    file_string):
    '''
    Get target files and directory paths depending on the operating system.
    Args:
        directory_path: <string> path to data directory
        file_string: <string> file extension (e.g. .csv)
    Returns:
        file_paths: <string> path to files
    '''
    operating_system = check_platform()
    if operating_system == 'Linux' or operating_system == 'Mac':
        file_list = extractfile(
            directory_path=directory_path,
            file_string=file_string)
        file_paths = [Path(f'{directory_path}/{file}') for file in file_list]
    elif operating_system == 'Windows':
        file_paths = prompt_for_path(
            default=directory_path,
            title='Select Target File(s)',
            file_path=True,
            file_type=[(f'{file_string}', f'*{file_string}')])
    return file_paths


def find_semlog(log_path,
                sample_details,
                file_string):
    '''
    Find image log file from SEM.
    Args:
        log_path: <string> path to log directory
        sample_details: <dict> dictionary containing image sample information
        file_string: <string> log file path extension
    Returns:
        log_file: <array> path to log file or empty if no file
        log_details: <dict> log parameters (same as sample_information)
    '''
    parent = sample_details['Parent Directory']
    primary = f'{parent} Primary String'
    secondary = f'{parent} Secondary String'
    try:
        log_files = extractfile(
            directory_path=log_path,
            file_string=file_string)
        log_file = []
        for file in log_files:
            file_path = Path(f'{log_path}/{file}')
            log_details = sample_information(file_path=file_path)
            if log_details[primary] == sample_details[primary]:
                if log_details[secondary] == sample_details[secondary]:
                    log_file.append(file_path)
    except:
        log_file = []
        log_details = {"Log String": "No Log File"}
    return log_file, log_details


def get_parent_directory(file_path):
    '''
    Find parent directory name of target file.
    Args:
        file_path: <string> path to file
    Returns:
        parent_directory: <string> parent directory name (not path)
    '''
    dirpath = os.path.dirname(file_path)
    dirpathsplit = dirpath.split('\\')
    parent_directory = dirpathsplit[-1]
    return parent_directory


def get_filename(file_path):
    '''
    Splits file path to remove directory path and file extensions.
    Args:
        file_path: <string> path to file
    Returns:
        file_name: <string> file name without path or extensions
    '''
    return os.path.splitext(os.path.basename(file_path))[0]


def get_design_period(file_name):
    '''
    Pull design period from secondary string in file name. Only if secondary
    string is p250 or P250 for grating period 250. Otherwise returns None.
    Args:
        file_name: <string> file name string
    Returns:
        design_period: <int> design period in nm
    '''
    file_split = file_name.split('_')
    period_string = file_split[1]
    if f'{period_string[0]}' == 'P' or f'{period_string[0]}' == 'p':
        design_period = period_string[1:]
    else:
        design_period = 'None'
    return design_period


def sem_sample_information(file_path):
    '''
    Pull sample parameters from file name string for various processes.
    Args:
        file_path: <string> path to file
    Returns:
        sample_parameters: <dict>
    '''
    parent_directory = get_parent_directory(file_path=file_path)
    file_name = get_filename(file_path=file_path)
    file_split = file_name.split('_')
    design_period = get_design_period(file_name=file_name)
    return {
        'Parent Directory': parent_directory,
        f'{parent_directory} File Name': file_name,
        f'{parent_directory} File Path': f'{file_path}',
        f'{parent_directory} Primary String': file_split[0],
        f'{parent_directory} Secondary String': '_'.join(file_split[1:]),
        f'{parent_directory} Design Period': design_period}


def sample_information(file_path):
    '''
    Pull sample parameters based on which type of file is being analysed.
    Args:
        file_path: <string> path to file
    Returns:
        sample_parameters: <dict>
    '''
    parent_directory = get_parent_directory(file_path=file_path)
    if parent_directory == 'SEM':
        sample_parameters = sem_sample_information(
            file_path=file_path)
    else:
        sample_parameters = {}
    return sample_parameters


def get_all_batches(file_paths):
    '''
    Find all sample batches in series of file paths and append file paths to
    batch names for loop processing.
    Args:
        file_paths: <array> array of target file paths
    Returns:
        parent: <string> parent directory string
        batches: <dict>
            Batch inidicators: respective file paths for all samples in batch
    '''
    batches = {}
    for file in file_paths:
        sample_parameters = sample_information(file_path=file)
        parent = sample_parameters['Parent Directory']
        key = f'{parent} Primary String'
        if sample_parameters[key] in batches.keys():
            batches[f'{sample_parameters[key]}'].append(file)
        else:
            batches.update({f'{sample_parameters[key]}': [file]})
    return parent, batches


def update_batch_dictionary(parent,
                            batch_name,
                            file_paths):
    '''
    Update batch results dictionary.
    Args:
        parent: <string> parent directory identifier
        batch_name: <string> batch name identifier
        file_paths: <array> list of target file paths
    Returns:
        batch_dictionary: <dict>
            Batch Name
            File Names
            File Paths
            Secondary Strings
    '''
    batch_dictionary = {
        f'{parent} Batch Name': batch_name,
        f'{parent} File Name': [],
        f'{parent} File Path': [],
        f'{parent} Secondary String': []}
    for file in file_paths:
        sample_parameters = sample_information(file_path=file)
        for key, value in sample_parameters.items():
            if key in batch_dictionary.keys():
                batch_dictionary[key].append(value)
    return batch_dictionary
