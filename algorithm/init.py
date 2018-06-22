import random
import utils
from copy import deepcopy

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

def if_go_to_charge(path, vehicle, id_type_map, distance_matrix, thres_percent):
    if (len(path) == 0):
        return False
    distance = distance_matrix[0][path[0]]
    for i in range(1, len(path)):
        if (id_type_map[path[i]] == 2):
            distance += distance_matrix[path[i]][path[i - 1]]
        elif (id_type_map[path[i]] == 3):
            distance = 0
    if ((1 - float(distance) / float(vehicle.driving_range)) > thres_percent):
        return False
    else:
        return True

def if_path_legal(orders, path, distance_matrix, time_matrix):
    pass

def random_individual(warehouse, id_sorted_orders, angle_sorted_orders, chargings, vehicle_info, id_type_map, distance_matrix, time_matrix):
    distance_thres = 0
    num_vehicle_type = len(vehicle_info)

    individual = []

    #整个过程从这个点开始
    start_idx = random.randint(0, len(angle_sorted_orders) - 1)
    part1 = angle_sorted_orders[start_idx:len(angle_sorted_orders)]
    part2 = angle_sorted_orders[0:start_idx - 1]
    angle_sorted_orders = part2 + part1

    used = [0] * len(angle_sorted_orders)
    num_considered_order = 0

    while(num_considered_order < len(angle_sorted_orders)):
        random_v_type = random.randint(0, len(vehicle_info) - 1)
        path = []

        max_weight = vehicle_info[random_v_type].weight
        max_volume = vehicle_info[random_v_type].volume
        cur_weight = 0
        cur_volume = 0

        # 这一条路径从这里开始
        path_starting_idx = first_unused_idx(used)
        path.append(angle_sorted_orders[path_starting_idx].id)
        used[path_starting_idx] = 1
        num_considered_order += 1
        cur_weight += angle_sorted_orders[path_starting_idx].weight
        cur_volume += angle_sorted_orders[path_starting_idx].volume

        # 这里是备选项在angle_sorted_orders里的index
        candidate_idxs = filter_in_range(angle_sorted_orders[path_starting_idx].id, angle_sorted_orders, distance_matrix, distance_thres)
        candidate = []
        for idx in candidate_idxs:
            candidate.append(angle_sorted_orders[idx])

        used2 = []
        num_considered_order2 = 0
        for idx in candidate_idxs:
            used2.append(used[idx])
            if (used[idx] == 1):
                num_considered_order2 += 1

        while (num_considered_order2 < len(candidate)):
            num_considered_order3 = num_considered_order2
            used3 = deepcopy(used2)
            fail_flag = False
            while (True):
                random_idx = random.randint(0, len(candidate) - 1)
                while (used3[random_idx] == 1):
                    random_idx = random.randint(0, len(candidate) - 1)
                try_path = deepcopy(path).append(candidate[random_idx].id)
                if (if_path_legal(id_sorted_orders, try_path, distance_thres, time_matrix)):
                    path.append(candidate[random_idx].id)
                    cur_weight += candidate[random_idx].weight
                    cur_volume += candidate[random_idx].volume
                    used[candidate_idxs[random_idx]] = 1
                    used2[random_idx] = 1
                    num_considered_order += 1
                    num_considered_order2 += 1
                    break
                else:
                    used3[random_idx] = 1
                    num_considered_order3 += 1
                    if (num_considered_order3 >= len(candidate)):
                        fail_flag = True
                        break
            if (fail_flag == True):
                #找不到任何下一个合法点，挂掉
                break
            else:
                #没挂就看看去不去充电站
                thres_percent = random.random() / 3.0 + 0.2
                go_charge = if_go_to_charge(path, vehicle_info[random_v_type], id_type_map, distance_matrix, thres_percent)
                if (go_charge):
                    try_path = deepcopy(path).append(id_sorted_orders[path[-1] - 1].charging_binding)
                    can_go_charge = if_path_legal(try_path)
                    if (can_go_charge):
                        # 电够就去
                        path.append(id_sorted_orders[path[-1] - 1].charging_binding)
                    else:
                        # 电不够，挂掉
                        break

        individual.append(path)