import os
import numpy as np
import src.fileIO as io
import scipy.signal as sig
import Functions.Maths as math
import Functions.Organisation as org
import Functions.StandardPlots as plot


def AddDictKeys(primary_dict,
                secondary_dict):
    '''
    Add one dictionary key and values to another dictionary.
    Args:
        primary_dict: <dict> intial dictionary to add keys to
        secondary_dict: <dict> dictionary of keys to add to primary
    Returns:
        primary_dict: <dict> initial dictionary with added keys and values
    '''
    for key, values in secondary_dict.items():
        primary_dict.update({f'{key}': values})
    return primary_dict


if __name__ == '__main__':

    ''' Organisation '''
    root = os.getcwd()
    rootpath = os.path.join(
        root,
        'TestImages')
    dirpath = org.FindThePath(
        default=rootpath,
        title='Select Target Directory',
        dir_path=True)
    resultspath = os.path.join(
        dirpath,
        'Results')
    org.CheckDirExists(dir_path=resultspath)
    txtfiles, imagefiles = org.FindDirFile(
        dir_path=dirpath,
        file_string='.txt',
        image_string='.bmp')

    ''' Loop Files '''
    for file in txtfiles:

        ''' Check To See If Image Data Exists '''
        if f'{file[0: -4]}.bmp' in imagefiles:
            print(file)

            ''' Pull TXT File Info '''
            txtpath = os.path.join(
                dirpath,
                file)
            semparameters = ReadSemLog(file_path=txtpath)

            ''' Load and Trim Image File '''
            imagepath = os.path.join(
                dirpath,
                f'{file[0: -4]}.bmp')
            image = ReadImage(file_path=imagepath)
            gratingregion = ImageRegionInterest(
                image=image,
                height=int(semparameters['CM_FULL_SIZE'][1]),
                width=int(semparameters['CM_FULL_SIZE'][0]))
            distanceperpixel = DistPix(
                marker=semparameters['SM_MICRON_MARKER'][0],
                bar=semparameters['SM_MICRON_BAR'][0])

            ''' Fourier Transform Analysis '''
            periods = []
            frequencies = []
            fspaces = []
            magnitudes = []
            for i in range(len(gratingregion)):
                row = gratingregion[i]
                frequencyspace, fftmagnitude = FourierTransformRow(
                    row=row)
                fourierfrequencies, fourierperiods = FourierSignalProcessing(
                    magnitude_fft=fftmagnitude,
                    num_peaks=4,
                    distance_pixel=distanceperpixel,
                    sample_size=len(row),
                    frequency_space=frequencyspace)
                periods.append(fourierperiods)
                frequencies.append(fourierfrequencies)
                if i % (len(gratingregion) / 10) == 0:
                    fspaces.append(frequencyspace[1:, ])
                    magnitudes.append(fftmagnitude[1:, ])
            plot.MultiXYPlot(
                xs=fspaces,
                ys=magnitudes,
                x_label='Frequency [au]',
                y_label='FFT Magnitude',
                title=f'{file[0: -4]}',
                out_path=os.path.join(
                    resultspath,
                    f'{file[0: -4]}_Results.png'))
            calculatedgratingproperties = AddDictKeys(
                primary_dict=semparameters,
                secondary_dict={
                    'Average_Periods_nm': [
                        np.sum(p) / len(p)
                        for p in np.array(periods).T],
                    'Periods_Errors_nm': [
                        math.StandardErrorMean(x=p)
                        for p in np.array(periods).T],
                    'Average_Frequencies': [
                        np.sum(f) / len(f)
                        for f in np.array(frequencies).T],
                    'Frequencies_Errors': [
                        math.StandardErrorMean(x=f)
                        for f in np.array(frequencies).T]})
            org.SaveJsonOut(
                out_path=os.path.join(
                    resultspath,
                    f'{file[0: -4]}_Results.json'),
                dictionary=calculatedgratingproperties)

            ''' Threshold Fourier Transform Analysis '''
            periods = []
            frequencies = []
            fspaces = []
            magnitudes = []
            for i in range(len(gratingregion)):
                row = PixelsThreshold(
                    row=gratingregion[i],
                    threshold=(np.sum(gratingregion[i]) / len(gratingregion[i])) - (np.std(gratingregion[i])))
                frequencyspace, fftmagnitude = FourierTransformRow(
                    row=row)
                fourierfrequencies, fourierperiods = FourierSignalProcessing(
                    magnitude_fft=fftmagnitude,
                    num_peaks=4,
                    distance_pixel=distanceperpixel,
                    sample_size=len(row),
                    frequency_space=frequencyspace)
                periods.append(fourierperiods)
                frequencies.append(fourierfrequencies)
                if i % (len(gratingregion) / 10) == 0:
                    fspaces.append(frequencyspace[1:, ])
                    magnitudes.append(fftmagnitude[1:, ])
            plot.MultiXYPlot(
                xs=fspaces,
                ys=magnitudes,
                x_label='Frequency [au]',
                y_label='FFT Magnitude',
                title=f'{file[0: -4]}',
                out_path=os.path.join(
                    resultspath,
                    f'{file[0: -4]}_ThresholdResults.png'))
            calculatedgratingproperties = AddDictKeys(
                primary_dict=semparameters,
                secondary_dict={
                    'Average_Periods_nm': [
                        np.sum(p) / len(p)
                        for p in np.array(periods).T],
                    'Periods_Errors_nm': [
                        math.StandardErrorMean(x=p)
                        for p in np.array(periods).T],
                    'Average_Frequencies': [
                        np.sum(f) / len(f)
                        for f in np.array(frequencies).T],
                    'Frequencies_Errors': [
                        math.StandardErrorMean(x=f)
                        for f in np.array(frequencies).T]})
            org.SaveJsonOut(
                out_path=os.path.join(
                    resultspath,
                    f'{file[0: -4]}_ThresholdResults.json'),
                dictionary=calculatedgratingproperties)

            ''' Mean Threshold Fourier Transform Analysis '''
            periods = []
            frequencies = []
            fspaces = []
            magnitudes = []
            for i in range(len(gratingregion)):
                row = PixelsThreshold(
                    row=gratingregion[i],
                    threshold=np.sum(gratingregion[i]) / len(gratingregion[i]))
                frequencyspace, fftmagnitude = FourierTransformRow(
                    row=row)
                fourierfrequencies, fourierperiods = FourierSignalProcessing(
                    magnitude_fft=fftmagnitude,
                    num_peaks=4,
                    distance_pixel=distanceperpixel,
                    sample_size=len(row),
                    frequency_space=frequencyspace)
                periods.append(fourierperiods)
                frequencies.append(fourierfrequencies)
                if i % (len(gratingregion) / 10) == 0:
                    fspaces.append(frequencyspace[1:, ])
                    magnitudes.append(fftmagnitude[1:, ])
            plot.MultiXYPlot(
                xs=fspaces,
                ys=magnitudes,
                x_label='Frequency [au]',
                y_label='FFT Magnitude',
                title=f'{file[0: -4]}',
                out_path=os.path.join(
                    resultspath,
                    f'{file[0: -4]}_MeanResults.png'))
            calculatedgratingproperties = AddDictKeys(
                primary_dict=semparameters,
                secondary_dict={
                    'Average_Periods_nm': [
                        np.sum(p) / len(p)
                        for p in np.array(periods).T],
                    'Periods_Errors_nm': [
                        math.StandardErrorMean(x=p)
                        for p in np.array(periods).T],
                    'Average_Frequencies': [
                        np.sum(f) / len(f)
                        for f in np.array(frequencies).T],
                    'Frequencies_Errors': [
                        math.StandardErrorMean(x=f)
                        for f in np.array(frequencies).T]})
            org.SaveJsonOut(
                out_path=os.path.join(
                    resultspath,
                    f'{file[0: -4]}_MeanResults.json'),
                dictionary=calculatedgratingproperties)
