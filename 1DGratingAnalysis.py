import os
import src.GUI as gui
import src.fileIO as io
import src.filepaths as fp
import src.analysis as anal
'''Developments required: Plot the raw row vs threshold graphs for inspection'''

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
    sem_files = fp.find_sem_file_paths(
        dir_path=directory_path,
        file_extension='.txt',
        image_extension='.bmp')

    ''' Loop Files '''
    for sem_file in sem_files:
        filename = sem_file['filename']
        log_path = sem_file['log_path']
        image_path = sem_file['image_path']
        print(filename)

        ''' Load Files '''
        image_parameters = io.read_SEM_log(file_path=log_path)
        image = io.read_image(file_path=image_path)

        ''' Trim ROI '''
        grating_region = anal.trim_img_to_roi(
            image=image,
            height=image_parameters['image_height'],
            width=image_parameters['image_width'])

        ''' Calculations '''
        distanceperpixel = anal.calc_distance_per_pixel(
            distance_value = image_parameters['calibration_distance'],
            distance_unit=image_parameters['distance_unit'],
            number_of_pixels=image_parameters['calibration_pixels'])

        ''' Treshold Filters '''
        thresholds = [
            'None', 'Mean', 'Mean-StdDev', 'Mean+StdDev']
        for threshold in thresholds:
            grating_parameters = anal.calculate_grating_frequency(
                grating=grating_region,
                distance_per_pixel=distanceperpixel,
                threshold=threshold,
                save_figure=True,
                figure_outpath=[
                    os.path.join(
                        results_path,
                        f'{filename}_{threshold}_Results.png'),
                    os.path.join(
                        results_path,
                        f'{filename}_{threshold}_Rows.png')],
                file_name=filename)

            ''' Results Out '''
            grating_properties = dict(image_parameters, **grating_parameters)
            io.save_json_dicts(
                out_path=os.path.join(
                    results_path,
                    f'{filename}_{threshold}_Results.json'),
                dictionary=grating_properties)
