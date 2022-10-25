import numpy as np

# Generating match combinations
def generate_matches():
    # matches = []
    # for i in range(4):
    #     for j in range(3):
    #         if [i, j] not in matches and [j, i] not in matches and i != j:
    #             matches.append([i, j])
    matches = [[0, 1], [2, 3], [3, 1], [0, 2], [1, 2], [3, 0]]
    return matches

# Algorithm for estimating match results
def estimate_results(team_a, team_b, penalties=False):
    mean_factor = 1.0
    dev_factor = 0.4
    std = 1.25
    prop_a = mean_factor + dev_factor*(team_a[1] - team_b[0])
    prop_b = mean_factor + dev_factor*(team_b[1] - team_a[0])
    if penalties:
        prop = 4
        a = int(np.random.normal(prop, std))
        b = int(np.random.normal(prop, std))
    else:
        a = int(np.random.normal(prop_a, std))
        b = int(np.random.normal(prop_b, std)) 
    if a < 0:
        a = 0
    if b < 0:
        b = 0
    if penalties:
        if a > 4 and a > b:
            b = a - 1
        elif b > 4 and b > a:
            a = b - 1
        elif a - b > 3:
            b += (a-b) - 3
        elif b - a > 3:
            a += (b-a) - 3
    return [a, b]