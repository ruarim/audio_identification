import numpy as np
import librosa
from skimage.feature import peak_local_max
import os
import time
from utils import dump, get_id, sec_to_min_sec_str

def spectral_peaks(y, window_hop=5, threshhold=0.05):    
    # take STFT and get magnitude values
    stft = np.abs(librosa.stft(y))
    # get the peaks           
    peaks = peak_local_max(stft, min_distance=window_hop, threshold_abs=threshhold)
    return peaks # index of peaks

# use every point in constelation map as anchor then find pair in target zone        
def peak_combinations(peaks, id, target_size=32, fan_max=10):
    peaks = np.array(peaks) # use numpy for brevity
    
    combinations = {}
    # set each peak as an anchor
    for anchor in peaks: 
        # define the current target bounds
        upper_bound = anchor + target_size
        # find peaks in target range
        neighbours = peaks[(peaks > anchor)     .all(axis=1) & # this is slow - instead directly index the constelation map with window
                           (peaks < upper_bound).all(axis=1)] 
        
        # combine anchor with each neighbour and time diff
        for i in range(len(neighbours)): # create get neighbours function
            # value 
            time_stamp = anchor[1]
            data       = {"id": id, "time_stamp": time_stamp} # object containing id and offset timestamp
            # key
            time_diff  = neighbours[i][1] - time_stamp
            hash       = (anchor[0], neighbours[i][0], time_diff) # create hash tuple
            
            # create key value pair
            combinations[hash] = [data] # add new key
            
            if i == fan_max: 
                break
    
    return combinations

def fingerprint_file(file, id=None, resample=16384):
    y, sr    = librosa.load(file, sr=resample)
    peaks    = spectral_peaks(y)
    features = peak_combinations(peaks, id)    
    return features

def fingerprintBuilder(db_path, fingerprints_path, dataset_size=200, show=False):
    doc_count = 0
    num_docs = len(os.listdir(db_path))
    fingerprints = {}
    
    start_time = time.perf_counter()
    for entry in os.scandir(db_path):
        if os.path.splitext(entry.name)[1] != ".wav": continue
        
        id = get_id(entry.name)
        combinations = fingerprint_file(entry, id=id) # fingerprint
        
        # add combinations to fingerprints data structure
        for hash in combinations.keys():
            value = combinations[hash][0] # this is not ideal but it works
            if hash in fingerprints: fingerprints[hash].append(value) # if the a hash exists append to current array
            else: fingerprints[hash] = [value] # add new key
                
        doc_count+=1
        if show:
            print("{} - {} of {} documents processed".format(id, doc_count, num_docs))
        if doc_count == dataset_size: break
        
    # show run time and hash count
    end_time = time.perf_counter()
    run_time = end_time - start_time
    
    print("---fingerprinting runtime {} mins---".format(sec_to_min_sec_str(run_time)))
    print("---number of hashes {}---".format(len(fingerprints)))
    
    # dump values to file
    dump(fingerprints, fingerprints_path, "documents")