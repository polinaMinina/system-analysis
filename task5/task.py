import numpy as np

def expand_list(ranks):
    expanded_ranks = []
    for element in ranks:
        if isinstance(element, int):
            expanded_ranks.append(element)
        else:
            expanded_ranks.extend(element)
    return sorted(expanded_ranks)

def construct_matrix(rank_list):
    expanded_list = expand_list(rank_list)
    rank_matrix = np.zeros(shape=(len(expanded_list), len(expanded_list)), dtype=int)
    for i, val_i in enumerate(expanded_list):
        for j, val_j in enumerate(expanded_list):
            if val_i == val_j or not is_inferior(rank_list, val_i, val_j):
                rank_matrix[i, j] = 1
    return rank_matrix

def is_inferior(rank_list, first, second):
    for item in rank_list:
        if isinstance(item, int):
            if first == item:
                return True
            if second == item:
                return False
            continue
        if first in item:
            return second not in item
        if second in item:
            return first in item
    return False

def assemble_ranking(disputed_pairs, ranks_a, ranks_b):
    expanded_a = expand_list(ranks_a)
    expanded_b = expand_list(ranks_b)
    final_ranking = []

    added_items = set()

    for item in expanded_a + expanded_b:
        if item not in added_items:
            controversy_group = [item]
            for pair in disputed_pairs:
                if item in pair:
                    other_item = pair[0] if pair[1] == item else pair[1]
                    controversy_group.append(other_item)
            
            if len(controversy_group) > 1:
                final_ranking.append(controversy_group)
            else:
                final_ranking.append(item)
            
            added_items.update(controversy_group)

    return final_ranking

def task(input_a, input_b):
    rank_a = construct_matrix(input_a)
    rank_b = construct_matrix(input_b)

    combined_matrix = np.multiply(rank_a, rank_b)
    transposed_matrix = np.multiply(np.transpose(rank_a), np.transpose(rank_b))
    dispute_matrix = np.zeros(rank_a.shape, dtype=int)
    for i in range(len(combined_matrix)):
        for j in range(len(combined_matrix[i])):
            dispute_matrix[i, j] = combined_matrix[i, j] or transposed_matrix[i, j]

    disputed_pairs = []
    for i in range(len(dispute_matrix)):
        for j in range(len(dispute_matrix[i])):
            if i < j:
                continue
            if dispute_matrix[i, j] == 0:
                disputed_pairs.append((j + 1, i + 1))

    return assemble_ranking(disputed_pairs, input_a, input_b)

input_a = [1, [2, 3], 4, [5, 6, 7], 8, 9, 10]
input_b = [[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]
print(task(input_a, input_b))
