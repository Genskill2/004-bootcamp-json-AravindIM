# Add the functions in this file
import math
import json

def load_journal(file):
    f = open(file, 'r')
    contents = f.read()
    f.close()
    return json.loads(contents)


def compute_phi(file, event):
    data = load_journal(file)
    n11 = 0
    n00 = 0
    n10 = 0
    n01 = 0
    n1_ = 0
    n0_ = 0
    n_1 = 0
    n_0 = 0
    for day in data:
        if event in day['events']:
            n1_ += 1
            if day['squirrel']:
                n_1 += 1
                n11 += 1
            else:
                n_0 += 1
                n10 += 1
        else:
            n0_ += 1
            if day['squirrel']:
                n_1 += 1
                n01 += 1
            else:
                n_0 += 1
                n00 += 1

    phi = (n11 * n00 - n10 * n01) / math.sqrt(n1_ * n0_ * n_1 * n_0)
    return phi


def compute_correlations(file):
    data = load_journal(file)
    correlations = {}
    for day in data:
        for event in day['events']:
            if event in correlations:
                continue
            else:
                correlations[event] = compute_phi(file, event)
    return correlations


def diagnose(file):
    correlations = compute_correlations(file)
    highlypositive = list(correlations)[0]
    highlynegative = highlypositive
    for key in correlations.keys():
        if(correlations[key] > correlations[highlypositive]):
            highlypositive = key
        if(correlations[key] < correlations[highlynegative]):
            highlynegative = key
    return [highlypositive, highlynegative]
