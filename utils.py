import random

def random_member(list):
    idx = random.randint(0, len(list) - 1)
    return list[idx]

def verify_path_distance(path, distance_matrix, id_type_map, distance_limit):
    if (id_type_map[0] != 2):
        raise Exception
    cur_distance = distance_matrix[0][path[0]]
    if (cur_distance > distance_limit):
        return False
    for idx in range(len(path) - 1):
        if (id_type_map[idx + 1] == 1):
            raise Exception
        cur_distance += distance_matrix[idx][idx + 1]
        if (cur_distance > distance_limit):
            return False
        if (id_type_map[idx + 1] == 3):
            cur_distance = 0
    cur_distance += distance_matrix[path[-1]][0]
    if (cur_distance > distance_limit):
        return False
    else:
        return True