from fingerprint import fingerprintBuilder
from identify import audioIdentification
from eval import evaluate

# file path variables
db_path = "_database_recordings"
fingerprints_path = "_fingerprints"
query_path = "_query_recordings"
output_path = "_output.txt"

# fingerprint dataset
fingerprintBuilder(db_path, fingerprints_path)

# run identification on query set   
audioIdentification(query_path, fingerprints_path, output_path)

# run evaluation on output file
rank = 1
precision, recall, f_measure = evaluate(output_path, rank)
print("Avg Precision: {}, Avg Recall: {}, Avg F Measure: {}".format(precision, recall, f_measure))