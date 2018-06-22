import random
import utils

def polar_cmp(x, y):
    if (x.polar_angle != y.polar_angle):
        return x.polar_angle - y.polar_angle
    else:
        return x.polar_dist - y.polar_dist

def init(warehouse, orders, chargings, vehicle_info, distance_matrix, time_matrix):
    sorted_orders = sorted(orders, key=lambda x: x.polar_angle)
    used = [0] * len(distance_matrix)

def filter_in_range(from_id, angle_sorted_orders, distance_matrix, distance_thres):
    ans = []
    for i in range(len(angle_sorted_orders)):
        if (distance_matrix[from_id][angle_sorted_orders[i].id] <= distance_thres):
            ans.append(id)
    return ans

def first_unused_idx(used):
    for i in range(used):
        if (used[i] == 0):
            return i
    return -1

def if_path_legal(orders, path, distance_matrix, time_matrix):
    pass

def random_individual(warehouse, angle_sorted_orders, chargings, vehicle_info, distance_matrix, time_matrix):
    distance_thres = 0
    num_vehicle_type = len(vehicle_info)

    #整个过程从这里开始
    start_idx = random.randint(0, len(angle_sorted_orders) - 1)
    part1 = angle_sorted_orders[start_idx:len(angle_sorted_orders)]
    part2 = angle_sorted_orders[0:start_idx - 1]
    angle_sorted_orders = part2 + part1

    used = [0] * len(angle_sorted_orders)

    considered_point = 0
    random_v_type = random.randint(0, len(vehicle_info) - 1)
    while(considered_point < len(angle_sorted_orders)):
        path = []

        max_weight = vehicle_info[random_v_type].weight
        max_volume = vehicle_info[random_v_type].volume
        cur_weight = 0
        cur_volume = 0

        # 这一条路径从这里开始
        path_starting_idx = first_unused_idx(used)
        path.append(angle_sorted_orders[path_starting_idx].id)
        used[path_starting_idx] = 1
        cur_weight += angle_sorted_orders[path_starting_idx].weight
        cur_volume += angle_sorted_orders[path_starting_idx].volume

        # 这里是备选项在angle_sorted_orders里的index
        candidate_idxs = filter_in_range(angle_sorted_orders[path_starting_idx].id, angle_sorted_orders, distance_matrix, distance_thres)





        random_v_type = random.randint(0, len(vehicle_info) - 1)