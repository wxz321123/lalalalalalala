import random

def polar_cmp(x, y):
    if (x.polar_angle != y.polar_angle):
        return x.polar_angle - y.polar_angle
    else:
        return x.polar_dist - y.polar_dist

def init(warehouse, orders, chargings, vehicle_info, distance_matrix, time_matrix):
    sorted_orders = sorted(orders, key=lambda x: x.polar_angle)
    used = [0] * len(distance_matrix)

def first_unused_idx(used):
    for i in range(used):
        if (used[i] == 0):
            return i
    return -1

def random_individual(warehouse, sorted_orders, chargings, vehicle_info, distance_matrix, time_matrix):
    num_vehicle_type = len(vehicle_info)

    #整个过程从这里开始
    start_idx = random.randint(0, len(sorted_orders) - 1)
    part1 = sorted_orders[start_idx:len(sorted_orders)]
    part2 = sorted_orders[0:start_idx - 1]
    sorted_orders = part2 + part1

    used = [0] * len(sorted_orders)

    considered_point = 0
    random_v_type = random.randint(0, len(vehicle_info) - 1)
    while(considered_point < len(sorted_orders)):
        path = []

        max_weight = vehicle_info[random_v_type].weight
        max_volume = vehicle_info[random_v_type].volume
        cur_weight = 0
        cur_volume = 0

        # 这一条路径从这里开始
        path_starting = first_unused_idx(used)
        path.append()



        random_v_type = random.randint(0, len(vehicle_info) - 1)