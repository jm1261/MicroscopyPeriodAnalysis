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
    JEOL_parameters = lines_to_parameters(sanitized_lines)
    sanitized_parameters = sanitize_JEOL_parameters(JEOL_parameters)
    return sanitized_parameters


def remove_unwanted_characters(raw_lines):
    '''
    Remove $ and \n characters from lines
    '''
    lines = [
        (line.translate({ord('$'): None}))[0: -1]
        for line in raw_lines]
    return lines


def lines_to_parameters(lines):
    '''
    Pull important parameters into dictionary. 
    To further add parameters, simply add names and keys to the sample dictionary in this function. 

    Args:
        lines: <array> array of lines from txt file, stripped of '$' and '\n'
    Returns:
        parameterdict: <dict> parameter dictionary
    '''
    parameters = dict()
    for line in lines:
        parameter_label, *parameter_values = line.strip().split(' ')
        parameters[parameter_label] = parameter_values
    return parameters


def sanitize_JEOL_parameters(raw_parameters):
    sanitized_parameters = {
        'acceleration_voltage': float(raw_parameters['CM_ACCEL_VOLT'][0]),
        'brightness': int(raw_parameters['CM_BRIGHTNESS'][0]),
        'calibration_number_of_pixels': int(raw_parameters['SM_MICRON_BAR'][0]),
        'contrast': int(raw_parameters['CM_CONTRAST'][0]),
        'emission_current': float(raw_parameters['SM_EMI_CURRENT'][0]),
        'magnification': int(raw_parameters['CM_MAG'][0]),
        'working_distance': float(raw_parameters['SM_WD'][0]),
    }

    # CM_FULL_SIZE is [width, height].
    width = 0
    height = 1
    sanitized_parameters['image_width'] = int(
        raw_parameters['CM_FULL_SIZE'][width])
    sanitized_parameters['image_height'] = int(
        raw_parameters['CM_FULL_SIZE'][height])

    unit_suffix_length = 2
    calibration_distance = raw_parameters['SM_MICRON_MARKER'][0]
    sanitized_parameters['calibration_distance_value'] = int(
        calibration_distance[: -unit_suffix_length])
    sanitized_parameters['calibration_distance_unit'] = calibration_distance[-unit_suffix_length:]

    return sanitized_parameters


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
