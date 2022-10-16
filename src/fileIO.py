from PIL import Image
import json
import numpy as np


def read_sem_log(file_path):
    '''
    Load JEOL-SEM txt file as a dictionary of key parameters

    Args:
        file_path: <string> path to file
    Returns:
        parameterdict: <dict> parameter dictionary
    '''
    with open(file_path) as infile:
        raw_lines = infile.readlines()
    sanitized_lines = remove_unwanted_characters(raw_lines)
    return extract_parameters(lines=sanitized_lines)

def remove_unwanted_characters(raw_lines):
    '''
    Remove $ and \n characters from lines
    '''
    lines = [
        (line.translate({ord('$'): None}))[0: -1]
        for line in raw_lines]
    return lines

def extract_parameters(lines):
    '''
    Pull important parameters into dictionary. To further add parameters, simply add names and keys to the
    sample dictionary in this function. Remember FULL_SIZE parameter is [width,
    height].
    
    Args:
        lines: <array> array of lines from txt file, stripped of '$' and '\n'
    Returns:
        parameterdict: <dict> parameter dictionary
    '''
    parameters = {
        'CM_ACCEL_VOLT': None,
        'CM_BRIGHTNESS': None,
        'CM_CONTRAST': None,
        'CM_FULL_SIZE': None,
        'CM_MAG': None,
        'SM_EMI_CURRENT': None,
        'SM_MICRON_BAR': None,
        'SM_MICRON_MARKER': None,
        'SM_WD': None,
    }
    for line in lines:
        parameter_label, *parameter_values = line.split(' ')
        if parameter_label in parameters.keys():
            parameters[parameter_label] = parameter_values
    return parameters

def read_image(file_path):
    '''
    Loads image file.
    Args:
        file_path: <string> path to file
    Returns:
        image: <np.array> array of pixels
    '''
    image = Image.open(file_path)
    return np.array(image)

def save_json(out_path,
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

def convert(o):
    '''
    Check type of data string
    '''
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError