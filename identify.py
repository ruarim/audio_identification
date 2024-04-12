import os
import time
from fingerprint import fingerprint_file
from utils import get_id, load, sec_to_min_sec_str
from collections import defaultdict, Counter

def identify(Q, D):    
    # calulcate the frequnecy of matching offsets
    matches = get_matches(Q, D)
    # find documents with most frequnent shifts
    candidates = get_largest_matches(matches)
    # sort most frequnent ids by count
    sorted_candidates = sort_dic(candidates)

    return sorted_candidates # [0] = most common

def get_matches(Q, D):
    matches = defaultdict(Counter) # counter for shift frequency - defaultdict allows arbitrary keys
     # find valid shifts   
    for h_q in Q: # for each hash index in query
        if h_q not in D: continue # only search hash indexes in query
        for n in Q[h_q]:
            for l in D[h_q]:
                m    = l["time_stamp"] - n["time_stamp"]
                D_id = l["id"]
                matches[D_id][m] += 1
                
    return matches

# create dict of most most common matches for each id - returns dict {"doc_id" : count}
def get_largest_matches(matches):
    candidates = {}
    
    for D_id, counter in matches.items():
        most_common_offset, count = counter.most_common(1)[0] # get most common time shift
        candidates[D_id] = count # add to list of possible matches
    
    return candidates

# sort a dict by value - return keys
def sort_dic(dict):
    values = [key for key in dict]
    keys_by_value = sorted(values, key=lambda x: -dict[x])
    return keys_by_value

def write_output_line(output_file, docs, query_name):
    if len(docs) > 0:
        output_line = "%s\t%s\n" % (
            query_name,
            "\t".join([doc + '.wav' for doc in docs[:min(3, len(docs))]]))
    else:
        output_line = query_name
    output_file.write(output_line)

def audioIdentification(query_path, fingerprints_path, output_path):
    print("running audio identification on query set")
    
    D = load(fingerprints_path) # load fingerprints
    output_file = open(output_path, "w")
    
    num_correct = 0 # keep track of correct matches
    queries   = 0
    start_time = time.perf_counter()
    
    # start profile timer
    for entry in os.scandir(query_path):
        # skip non wave files
        if os.path.splitext(entry.name)[1] != ".wav": continue
        
        # process the query
        queries+=1
        query_name = entry.name
        id  = get_id(query_name)
        Q = fingerprint_file(entry, id=id)  # finger print the query
        doc_ids = identify(Q, D) # find matching documents
        
        # store correct and incorrect document matches
        if(len(doc_ids) > 0 and doc_ids[0] == id):
            num_correct+=1 
            print("correct match D_id: {} - Q_id: {}".format(doc_ids[0], id))
                    
        # write top documents 3 to file
        write_output_line(output_file, doc_ids, query_name)
    
    # stop profile timer 
    end_time = time.perf_counter()
    
    # show runtime
    run_time = end_time - start_time
    
    # print results
    print("---time to run identification {} mins---".format(sec_to_min_sec_str(run_time)))
    print("---percentage correct {}---".format(num_correct / queries))
    print("---correct matches: {}---".format(num_correct))
    
    output_file.close()
    
    return num_correct