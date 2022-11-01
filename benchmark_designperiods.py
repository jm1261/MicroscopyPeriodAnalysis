import os
import json
import numpy as np
import src.GUI as gui
import src.fileIO as io
import src.filepaths as fp


def extractallfiles(dir_path,
                    file_extension):
    '''
    Extract all files with specific file string in directory path.
    Args:
        dir_path: <string> directory path
        file_extension: <string> file extension
    Returns:
        dir_list: <array> sorted file names with extension
    '''
    dir_list = sorted(os.listdir(dir_path))
    return [file for file in dir_list if file_extension in file]


def open_json(file_path):
    '''
    Extract dictionary from json file.
    Args:
        file_path: <string> path to file
    Returns:
        file: <dict> json dictionary
    '''
    with open(file_path, 'r') as f:
        return json.load(f)


if __name__ == '__main__':

    ''' Organisation '''
    root = os.getcwd()
    directory_path = gui.prompt_for_path(
        default=root,
        title='Select Target Directory',
        dir_path=True)
    results_path = fp.check_directory_exists(
        dir_path=os.path.join(
            directory_path,
            'Results'))

    design_periods = {
        'A1': 340,
        'A2': 405,
        'A3': 365,
        'A4': 440,
        'A5': 390,
        'A6': 475}

    ''' Find Files '''
    all_files = extractallfiles(
        dir_path=results_path,
        file_extension='.json')

    ''' Loop Files '''
    benchmark_dictionary = {}
    all_other_benchmarks = {}
    for file in all_files:
        file_path = os.path.join(
            results_path,
            file)
        file_parameters = open_json(file_path=file_path)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_key = file_name.split('_')[0]
        grating_key = f'{file_key}_{file_name.split("_")[1]}'
        threshold_key = file_name.split('_')[2]

        calculated_periods = file_parameters['Average_Periods_nm']
        calculated_differences = [
            np.abs(design_periods[f'{file_key}'] - period)
            for period in calculated_periods]
        min_difference = np.min(calculated_differences)
        benchmark_values = [f'{threshold_key}', min_difference]
        if f'{grating_key}' in benchmark_dictionary.keys():
            if benchmark_dictionary[f'{grating_key}'][1] > min_difference:
                benchmark_dictionary.update(
                    {f'{grating_key}': benchmark_values})
            else:
                all_other_benchmarks.update(
                    {f'{file_name}_{threshold_key}': min_difference})
        else:
            benchmark_dictionary.update(
                {f'{grating_key}': benchmark_values})
            all_other_benchmarks.update(
                {f'{file_name}_{threshold_key}': min_difference})
    io.save_json_dicts(
        out_path=os.path.join(
            directory_path,
            '..',
            'All_design_Benchmark_Data.json'),
        dictionary=all_other_benchmarks)
    io.save_json_dicts(
        out_path=os.path.join(
            directory_path,
            '..',
            'Best_design_Benchmarks.json'),
        dictionary=benchmark_dictionary)
    methods = []
    for key, values in benchmark_dictionary.items():
        methods.append(values[0])
    negstd = methods.count('Mean-StdDev')
    posstd = methods.count('Mean+StdDev')
    mean = methods.count('Mean')
    nones = methods.count('None')
    print(negstd, posstd, mean, nones)
