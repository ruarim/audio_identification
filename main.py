from fingerprint import fingerprintBuilder
from identify import audioIdentification

# run identification on query set
db_path = "_database_recordings"
fingerprint_path = "_fingerprints"
fingerprintBuilder(db_path, fingerprint_path, show=True)

# fingerprint dataset
fingerprints_path = '_fingerprints/documents'
query_path = "_query_recordings"
output_path = "_output.txt"
correct = audioIdentification(query_path, fingerprints_path, output_path)

# run analysis
# precicion
# recall 
# f-measure