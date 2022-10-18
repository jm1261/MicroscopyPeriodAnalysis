# Benchmarking Threshold

* During initial testing, I found that minor dust, material, or imaging abnormalities in the SEM images could create a "bunny ear" effect on the pixel data.
* This effect would then create problems with the Fourier transform, namely allowing the code to find the period of the bunny ears, which would dominate the signal.
* To remove this effect, we can threshold the analog pixel data to create a binary signal.
* There are likely several methods this can be done, but here I will detail what I did and why I chose those methods.

## Thresholding Methods

* There were two primary methods I considered when thresholding the analog pixel data.
  * Mean
  * mean +/- standard deviation
* Anything greater than 1 * standard deviation didn't allow for a great enough shift in the data to allow the Fourier transform to find frequency peaks.
* Both the mean and the standard deviation are calculated using standard equations, and I analysed the mean threshold, mean + standard deviation, and mean - standard deviation.
* The thresholds, as floats, were then set so that any pixel value below this float is set to a minimum pixel value (0) and anything above this value is set to maximum pixel value (255).
* Thus creating a binary signal, far easier for Fourier analysis.

## Benchmarking Thresholds

* I produced a Fourier period analysis for each of the thresholding methods (and the None threshold method) to produce the results json files detailed in the software documentation.
* I then used the benchmark_periods.py file to look at the given design periods and calculate which method gave us a period closest to the design parameters.
* Based purely on the grating period analysis, the mean - standard deviation threshold gave values closest to the expected value, while no threshold gave values farthest from expected values.
* Comparing to measured values for period using built in software in the JEOL SEM software, the mean - standard deviation method also comes out on top.
* It follows, therefore, that thresholding should be done to all data to ensure random variations caused by dust, excess material, or SEM imaging properties are removed to the best of our abilities.

### Notes From Developer

* We acknowledge that the benchmarking methodology is limited.
* Comparing measured grating periods to designed periods is inherintly flawed as it ignores any fabrication variations.
* Comparing to the values measured by the SEM tool does increase accuracy.
* Measuring with the SEM tool, however, is highly user dependent and can vary depending on angle, acceleration voltage, brightness, contrast, and a variety of other imaging properties.
* All three methods can be applied and filtered by the user.