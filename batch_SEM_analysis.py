import src.fileIO as io
import src.filepaths as fp
import src.analysis as anal

from pathlib import Path


def batch_grating_frequency(parent_directory,
                            batch_name,
                            file_paths,
                            directory_paths,
                            plot_files):
    '''
    Calculate sample batch grating frequency and period for optimised data
    thresholding.
    Args:
        parent_directory: <string> parent directory identifier
        batch_name: <string> batch name string
        file_paths: <array> array of target file paths
        directory_paths: <dict> dictionary containing required paths
        plot_files: <string> "True" or "False" for plotting output
    Returns:
    '''
    batch_dictionary = fp.update_batch_dictionary(
        parent=parent_directory,
        batch_name=batch_name,
        file_paths=file_paths)
    period_dictionary = {}
    for file in file_paths:
        sample_image = io.read_image(file_path=file)
        sample_parameters = fp.sample_information(file_path=file)
        log_path, log_parameters = fp.find_semlog(
            log_path=directory_paths['SEM Path'],
            sample_details=sample_parameters,
            file_string='.txt')
        if len(log_path) == 0:
            pass
        else:
            image_parameters = io.read_SEM_log(file_path=log_path[0])
            grating_region = anal.trim_img_to_roi(
                image=sample_image,
                height=image_parameters['image_height'],
                width=image_parameters['image_width'])
            distanceperpixel = anal.calc_distance_per_pixel(
                distance_value=image_parameters['calibration_distance'],
                distance_unit=image_parameters['distance_unit'],
                number_of_pixels=image_parameters['calibration_pixels'])
            out_string = sample_parameters[f'{parent} Secondary String']
            results_dictionary = anal.calculate_grating_frequency(
                grating_region=grating_region,
                distance_per_pixel=distanceperpixel,
                sample_name=out_string,
                design_period=int(sample_parameters[f'{parent} Design Period']),
                plot_files=plot_files,
                out_path=Path(
                    f'{directory_paths["Results Path"]}'
                    f'/{batch}_{out_string}'))
            batch_dictionary.update({f'{out_string} Image': sample_parameters})
            batch_dictionary.update({f'{out_string} Log File': log_parameters})
            batch_dictionary.update({f'{out_string} Log': image_parameters})
            batch_dictionary.update(results_dictionary)
            period_dictionary.update({
                f'{out_string}':
                results_dictionary[f'{out_string} Grating Period']})
    print(period_dictionary)
    average_dictionary = anal.average_grating_period(
        period_dictionary=period_dictionary)
    batch_dictionary.update(average_dictionary)
    return batch_dictionary


if __name__ == '__main__':

    ''' Organisation '''
    root = Path().absolute()
    info, directory_paths = fp.get_directory_paths(root_path=root)
    file_paths = fp.get_files_paths(
        directory_path=directory_paths["SEM Path"],
        file_string='.bmp')
    parent, batches = fp.get_all_batches(file_paths=file_paths)

    ''' Batch Processing '''
    for batch, filepaths in batches.items():
        out_file = Path(
            f'{directory_paths["Results Path"]}'
            f'/{batch}_Period.json')
        if out_file.is_file():
            pass
        else:
            results_dictionary = batch_grating_frequency(
                parent_directory=parent,
                batch_name=batch,
                file_paths=file_paths,
                directory_paths=directory_paths,
                plot_files=info['Plot Files'])
            io.save_json_dicts(
                out_path=out_file,
                dictionary=results_dictionary)
