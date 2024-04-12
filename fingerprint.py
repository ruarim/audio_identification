import numpy as np
import librosa
from skimage.feature import peak_local_max
import os
import time
from utils import dump, get_id, sec_to_min_sec_str

# function to find the spectral peaks in a given 2D array - returns list of [x,y] values
def spectral_peaks(y, window_hop=5, threshhold=0.05):    
    # take STFT and get magnitude values
    stft = np.abs(librosa.stft(y))
    # get the peaks           
    peaks = peak_local_max(stft, min_distance=window_hop, threshold_abs=threshhold)
    return peaks # index of peaks

# use every point in constelation map as anchor then find pair in target zone        
def peak_combinations(peaks, id, target_size=32, fan_max=10):
    # use numpy for brevity
    peaks = np.array(peaks)
    
    combinations = {}
    # set each peak as an anchor
    for anchor in peaks: 
        # define the current target bounds
        upper_bound = anchor + target_size
        # find peaks in target range
        neighbours = peaks[(peaks > anchor)     .all(axis=1) &
                           (peaks < upper_bound).all(axis=1)] 
        
        # combine anchor with each neighbour and time diff
        for i in range(len(neighbours)): # create get neighbours function
            # get anchor timestamp 
            time_stamp = anchor[1]
            # create id and offset timestamp dict
            data = {"id": id, "time_stamp": time_stamp} 
            # key
            time_diff = neighbours[i][1] - time_stamp
             # create hash tuple
            hash = (anchor[0], neighbours[i][0], time_diff)
            # create key value pair
            combinations[hash] = data
            # stop if maximum fan out reached
            if i == fan_max: 
                break
    
    return combinations

# run the fingerprinting process on a single file - returns dict of { "combination hash" : [time_stamp] }
def fingerprint_file(file, id):
    y,_ = librosa.load(file)
    peaks = spectral_peaks(y)
    features = peak_combinations(peaks, id)    
    return features

def fingerprintBuilder(db_path, fingerprints_path):
    doc_count = 0
    num_docs = len(os.listdir(db_path))
    fingerprints = {}
    
    start_time = time.perf_counter()
    for entry in os.scandir(db_path):
        if os.path.splitext(entry.name)[1] != ".wav": continue
        
        id = get_id(entry.name)
        # fingerprint file
        combinations = fingerprint_file(entry, id=id) 
        
        # add combinations to fingerprints data structure
        for hash in combinations.keys():
            value = combinations[hash]
            # if the a hash exists append to current array
            if hash in fingerprints: fingerprints[hash].append(value)
             # add new key
            else: fingerprints[hash] = [value]
                
        doc_count+=1
        print("{} - {} of {} documents processed".format(id, doc_count, num_docs))
        
    # show run time and hash count
    end_time = time.perf_counter()
    run_time = end_time - start_time
    
    print("---fingerprinting runtime {} mins---".format(sec_to_min_sec_str(run_time)))
    print("---number of hashes {}---".format(len(fingerprints)))
    
    # dump values to file
    print("writing data to file...")
    dump(fingerprints, fingerprints_path, "documents")