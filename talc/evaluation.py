import numpy as np
from dtw import dtw

def stats(ground_truth, predicted, audio_length):
    # initialize boolean masks representing seconds
    truth_mask = np.zeros((audio_length,), dtype=bool)
    predicted_mask = np.zeros((audio_length,), dtype=bool)

    # set masks
    for segment in ground_truth:
        truth_mask[segment[0]:segment[1]] = True

    for segment in predicted:
        predicted_mask[segment[0]:segment[1]] = True

    # f-score, precision, recall (sensitivity), specificity
    TP = np.count_nonzero(truth_mask & predicted_mask)
    FP = np.count_nonzero(~truth_mask & predicted_mask)
    FN = np.count_nonzero(truth_mask & ~predicted_mask)
    TN = np.count_nonzero(~truth_mask & ~predicted_mask)

    if TP == 0 or TN == 0 or FP == 0 or FN == 0:
        # cannot compute the statistics
        precision = 0
        recall = 0
        specificity = 0
        f_measure = 0
    else:
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        specificity = TN / (TN + FP)
        f_measure = 2 * precision * recall / (precision + recall)

    return f_measure, precision, recall, specificity

# measures boundary deviation of start and end boundaries
def dist_both(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])

# measures boundary deviation of only start boundaries
def dist_start(x, y):
    return abs(x[0] - y[0])

def error(ground_truth, predicted, audio_length, distance=dist_both):
    if len(predicted) == 0:
        # cannot compute the error
        return 0
    else:
        # actual error divided by normalization (a worst case in some way)
        return dtw(ground_truth, predicted, distance)[0] / dtw(ground_truth, [(0, audio_length)], distance)[0]
