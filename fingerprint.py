import numpy as np
import librosa
from skimage.feature import peak_local_max
import pickle
import os

# helper function to dump all database items to a file
def dump(data, dir, name):
    # Ensure the directory exists
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    #create the file path
    file_path = os.path.join(dir, f"{name}.pkl")
    
    # write the data to the file
    with open(file_path, 'wb') as file:
        pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)

def spectral_peaks(y, sr, window_hop=5, threshhold=0.05, show=False):    
    # take STFT
    stft = np.abs(librosa.stft(y))
    # stft = stft / np.max(stft) # normalise 0 - 1
            
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
            data       = {'id': id, "time_stamp": time_stamp} # object containing id and offset timestamp
            # key
            time_diff  = neighbours[i][1] - time_stamp
            hash       = (anchor[0], neighbours[i][0], time_diff)
            
            # create key value pair
            combinations[hash] = [data] # add new key
            
            if i == fan_max: 
                break
    
    return combinations

def fingerprint_file(file, id=None, show=False):
    y, sr    = librosa.load(file)
    peaks    = spectral_peaks(y, sr, show=show)
    features = peak_combinations(peaks, id)    
    return features

# helper function to get id frrom genre and song number
def get_id(file):
    split = file.name.split('.')
    id = split[0] + split[1][:5]
    return id

def fingerprintBuilder(db_path, fingerprints_path, dataset_size=200, show=True):
    doc_count = 0
    num_documents = len(os.listdir(db_path))
    
    fingerprints = {}
    
    for entry in os.scandir(db_path):
        id = get_id(entry)  
        combinations = fingerprint_file(entry, id) # fingerprint
        
        # add combinations to fingerprints data structure
        for hash in combinations.keys():
            value = combinations[hash][0] # this is insane ??? 
            if hash in fingerprints: fingerprints[hash].append(value) # if the a hash exists append to current array
            else: fingerprints[hash] = [value] # add new key
        
        print("length fingerprints: {}".format(len(fingerprints)))  
        
        doc_count+=1
        if show:
            print("{} - {} of {} documents processed".format(id, doc_count, num_documents))
        if doc_count == dataset_size: break
        
    # dump values to file
    dump(fingerprints, fingerprints_path, "documents")

db_path = "_database_recordings"
fingerprint_path = '_fingerprints'
fingerprintBuilder(db_path, fingerprint_path)