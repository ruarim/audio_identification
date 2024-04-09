from collections import defaultdict, Counter
import numpy as np
from matplotlib import pyplot as plt
import pickle
import os
from fingerprint import fingerprint_file
from utils import get_id

# helpering function for loading pickled data
def load(name):
    with open(name + '.pkl', 'rb') as file:
        loaded_data = pickle.load(file)
    return loaded_data

def identify(Q, D, show=False):    
    offset_counter = defaultdict(Counter) # counter for shift - allow abitrary indexes
    
    # find valid shifts   
    for h_q in Q: # for each hash index in query
        if h_q not in D: continue # only search hash indexes in query
        for n in Q[h_q]:
            for l in D[h_q]:
                m    = l["time_stamp"] - n["time_stamp"]
                D_id = l["id"]
                offset_counter[D_id][m] += 1
    
    
    # rank function
    # find documents with most frequnent shifts
    candidates = {}
    largest = {"id": None, "offset": 0, "count": 0}
        
    for D_id, counter in offset_counter.items():
        most_common_offset, count = counter.most_common(1)[0] # get most common time shift
        candidates[D_id] = [most_common_offset, count] # add to list of possible matches
         # keep track of largest
        if(largest["count"] < count):
            largest = {"id": D_id, "offset": most_common_offset, "count": count}

    # instead sort candidates by count to get top ids
    return largest

def rank():
    # move ranking code here
    return ""

def audioIdentification(query_path, fingerprints_path, output_file=None):
    D = load(fingerprints_path) # load fingerprints
    matches = 0
    count   = 0
    
    for entry in os.scandir(query_path):
        id = get_id(entry)
        Q = fingerprint_file(entry, id=id)

        largest = identify(Q, D)
        
        count+=1
        if(largest["id"] == id): matches+=1
        # output to file
    
    print("percentage correct {}".format(matches / count))

fingerprints_path = '_fingerprints/documents'
db_file = "_database_recordings/classical.00050.wav"
query_file = "_query_recordings/classical.00050-snippet-10-20.wav"

query_path = "_query_recordings"
audioIdentification(query_path, fingerprints_path)