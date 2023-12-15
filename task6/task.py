import numpy as np
import json

def task(*rankings):
    num_experts = len(rankings)
    rank_template = {}
    rank_counter = 0

    for element in rankings[0]:
        if isinstance(element, list):
            for sub_elem in element:
                rank_template[sub_elem] = rank_counter
                rank_counter += 1
        else:
            rank_template[element] = rank_counter
            rank_counter += 1

    rank_matrix = []
    for ranking in rankings:
        order_list = [0] * len(rank_template)
        for i, item in enumerate(ranking):
            if isinstance(item, list):
                for sub_item in item:
                    order_list[rank_template[sub_item]] = i + 1
            else:
                order_list[rank_template[item]] = i + 1
        rank_matrix.append(order_list)

    rank_array = np.array(rank_matrix)
    sum_ranks = np.sum(rank_array, axis=0)
    
    D = np.var(sum_ranks) * rank_counter / (rank_counter - 1)
    D_max = (num_experts ** 2) * ((rank_counter ** 3 - rank_counter) / 12) / (rank_counter - 1)
    
    return format(D / D_max, ".2f")


ranking_a = [1, [2, 3], 4, [5, 6, 7], 8, 9, 10]
ranking_b = [[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]
ranking_c = [3, [1, 4], 2, 6, [5, 7, 8], [9, 10]]

print(task(ranking_a, ranking_b, ranking_c))
