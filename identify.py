import os
import time
from fingerprint import fingerprint_file
from utils import get_id, load, sec_to_min_sec_str, write_output_line
from collections import defaultdict, Counter
from visualise import plot_shift_frequnecy

# function to call each part of the identification process for a single document
def identify(Q, D):    
    # calulcate the frequnecy of matching offsets
    matches = get_matches(Q, D)
    # find documents with most frequnent shifts
    candidates = get_largest_matches(matches)
    # sort most frequnent ids by count
    sorted_candidates = sort_dic(candidates)
    # return a list of valid matches sorted from most to least frequent 
    return sorted_candidates

# count the number of valid shift for each hash - returns counter dict {"id": [ m : count ]}
def get_matches(Q, D):
     # counter for shift frequency - defaultdict allows arbitrary keys
    matches = defaultdict(Counter)
    
    # find valid shifts for each hash in query
    for h_q in Q: 
        # only search hashes in query
        if h_q not in D: continue
        # get the query hash data
        n = Q[h_q]
        # for each timstamp at the document hash
        for l in D[h_q]:
             # calculate the valid shift
            m = l["time_stamp"] - n["time_stamp"]
            # store the id
            D_id = l["id"] 
            # increment the number of valid shifts at current id and shift
            matches[D_id][m] += 1
    
    # return a the frequnecy of valid shifts at ids        
    return matches

# create dict of most most common matches for each id - returns dict {"document id" : count}
def get_largest_matches(matches):
    candidates = {}
    
    # for every id and number of valid shifts in the counter
    for D_id, counter in matches.items():
        # get most common time shift
        _, count = counter.most_common(1)[0] 
        
        # visualise shift
        # if count > 100: plot_shift_frequnecy(counter)
        
        # add to list of possible matches
        candidates[D_id] = count
    
    return candidates

# sort a dict by value - returns array of keys
def sort_dic(dict):
    values = [key for key in dict]
    keys_by_value = sorted(values, key=lambda x: -dict[x])
    return keys_by_value
    
def print_correct_incorrect(D_ids, Q_id):
    most_likley = D_ids[0]
    if(len(D_ids) > 0 and most_likley == Q_id):
        print("correct match document: {} - query: {}".format(most_likley, Q_id))
    else: 
        print("incorrect match document: {} - query: {}".format(most_likley, Q_id)) 

def audioIdentification(query_path, fingerprints_path, output_path):
    print("running audio identification on query set")
    
    # load fingerprints data structure
    D = load(fingerprints_path, "documents")
    output_file = open(output_path, "w")
    
    # start performance counter
    start_time = time.perf_counter()
        
    # start profile timer
    for entry in os.scandir(query_path):
        # skip non wave files
        if os.path.splitext(entry.name)[1] != ".wav": continue
        
        # process the query
        query_name = entry.name
        Q_id  = get_id(query_name)
         # finger print the query
        Q = fingerprint_file(entry, id=Q_id)
         # find matching documents
        D_ids = identify(Q, D)
        
        # show correct and incorrect document matches
        print_correct_incorrect(D_ids, Q_id)
                    
        # write top 3 documents to file
        write_output_line(output_file, D_ids, query_name)
    
    # stop profile timer
    end_time = time.perf_counter()
    
    # show runtime
    run_time = end_time - start_time

    # print results
    print("---time to run identification {} mins---".format(sec_to_min_sec_str(run_time)))
    
    output_file.close()