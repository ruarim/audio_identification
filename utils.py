import pickle
import os

# helper function to get id based on GTZAN dataset file names
def get_id(file):
    split = file.name.split('.')
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
def load(name):
    with open(name + '.pkl', 'rb') as file:
        loaded_data = pickle.load(file)
    return loaded_data
        
