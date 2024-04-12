def parse_output_file(output_file):
    with open(output_file) as f:
        lines = [line.split() for line in f]

    relevances = []
    for line in lines:
        split_line = line[0].split("-")
        ground_truth = split_line[0]
        relevances.append(
            [1 if ground_truth in doc else 0 for doc in line[1:]])
    
    return relevances

def calculate_precision_recall(relevances, rank):
    precision = []
    recall = []

    # calculate precision and recall for each query
    for rel in relevances:
        rel = rel[:rank]
        # calculate precision for the current list of relevances
        tp = sum(rel)  # Count of relevant documents
        precision.append(tp / len(rel))  # Precision: TP / (TP + FP) 

        # recall is calculated as TP / |Q|, where |Q| is the total number of relevant documents
        # assuming |Q| = 1 for each query since there is only one correct match for each
        recall.append(tp / 1)  # Recall: TP / |Q|

    return precision, recall

def evaluate(output_file, rank):
   relevances = parse_output_file(output_file)
   
   precision, recall = calculate_precision_recall(relevances, rank)
   f_measures = [2 * p * r / (p + r) if p + r > 0 else 0 for p, r in zip(precision, recall)]
   
   avg_precision = sum(precision) / len(precision)
   avg_recall = sum(recall) / len(recall)
   avg_f_measure = sum(f_measures) / len(f_measures)
   
   return avg_precision, avg_recall, avg_f_measure