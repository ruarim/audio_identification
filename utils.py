import pickle
import os

# helper function to get id based on GTZAN dataset file names
def get_id(file_name):
    split = file_name.split('.')
    id = split[0] + "." + split[1][:5]
    return id

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
        
# helpering function for loading pickled data
def load(path, name):
    with open(path + "/" + name + '.pkl', 'rb') as file:
        loaded_data = pickle.load(file)
    return loaded_data
        
def sec_to_min_sec_str(seconds):
    minutes = seconds // 60  # Get the number of full minutes
    remaining_seconds = seconds % 60  # Get the remaining seconds
    return "{}:{}".format(round(minutes), round(remaining_seconds))

# write the query id and top three document ids to a file
def write_output_line(output_file, docs, query_name):
    if len(docs) > 0:
        output_line = "%s\t%s\n" % (
            query_name,
            "\t".join([doc + '.wav' for doc in docs[:min(3, len(docs))]]))
    else:
        output_line = query_name
    output_file.write(output_line)