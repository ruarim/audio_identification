from matplotlib import pyplot as plt
import librosa

# constelation map
def plot_spec_peaks(spec, peaks):
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(spec, y_axis="log", x_axis='frames')
    plt.title('Spectrogram (dB)')
    
    # get the indexes
    index_y, index_x = zip(*peaks)
    # plot the points on top of the spectrogram
    plt.scatter(index_x, index_y, color='cyan', s=5, edgecolor='none')
    plt.show()

# histogram of frequnecy of shifts for a document
def plot_shift_frequnecy(shift_counter):
    # specify bin edges based on the range and distribution shifts
    min_shift = min(shift_counter.keys())
    max_shift = max(shift_counter.keys())
    bin_width = 1
    bins = range(min_shift, max_shift + bin_width, bin_width)
    

    # Plotting the histogram of shifts with manually specified bins
    plt.hist(list(shift_counter.keys()), weights=list(shift_counter.values()), bins=bins)
    plt.xlabel('Shifts')
    plt.ylabel('Frequency')
    plt.title('Histogram of Shifts')
    plt.show()
