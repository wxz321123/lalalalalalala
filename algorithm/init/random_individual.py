import random
import datetime
from copy import deepcopy
from algorithm.verify import if_path_legal
from algorithm.verify import if_go_to_charge
from entity.TransportPath import TransportPath

def polar_cmp(x, y):
    if (x.polar_angle != y.polar_angle):
        return x.polar_angle - y.polar_angle
    else:
        return x.polar_dist - y.polar_dist

def filter_in_range(from_id, angle_sorted_orders, distance_matrix, distance_thres):
    order_id_ans = []
    angle_sorted_orders_idx_ans = []
    for i in range(len(angle_sorted_orders)):
        if (distance_matrix[from_id][angle_sorted_orders[i].id] <= distance_thres):
            order_id_ans.append(angle_sorted_orders[i].id)
            angle_sorted_orders_idx_ans.append(i)
    return order_id_ans, angle_sorted_orders_idx_ans


def first_unused_idx(used):
    for i in range(len(used)):
        if (used[i] == 0):
            return i
    return -1

def random_individual(warehouse, id_sorted_orders, angle_sorted_orders, chargings, vehicle_info, id_type_map, distance_matrix, time_matrix):

    distance_thres = 10000
    num_vehicle_type = len(vehicle_info)
    path_t_id = 1
    individual = []

    #整个过程从这个点开始
    start_idx = random.randint(0, len(angle_sorted_orders) - 1)
    part1 = angle_sorted_orders[start_idx:len(angle_sorted_orders)]
    part2 = angle_sorted_orders[0:start_idx]
    angle_sorted_orders = part1 + part2

    used = [0] * len(angle_sorted_orders)
    num_considered_order = 0

    while(num_considered_order < len(angle_sorted_orders)):
        used_try = deepcopy(used)
        num_considered_order_try = num_considered_order
        random_v_type = random.randint(0, len(vehicle_info) - 1)
        path = []
        max_weight = vehicle_info[random_v_type].weight
        max_volume = vehicle_info[random_v_type].volume
        cur_weight = 0
        cur_volume = 0

        # 这一条路径从这里开始
        path_starting_idx = first_unused_idx(used_try)
        path.append(angle_sorted_orders[path_starting_idx].id)
        used_try[path_starting_idx] = 1
        num_considered_order_try += 1
        cur_weight += angle_sorted_orders[path_starting_idx].weight
        cur_volume += angle_sorted_orders[path_starting_idx].volume

        # 这里是备选项在angle_sorted_orders里的index
        candidate_id, candidate_idxs_in_anlge_sorted_orders = filter_in_range(angle_sorted_orders[path_starting_idx].id, angle_sorted_orders, distance_matrix, distance_thres)
        candidate = []
        for idx in candidate_idxs_in_anlge_sorted_orders:
            candidate.append(angle_sorted_orders[idx])

        # used2 和 used 信息是相同的，只是保存的数目不同，目的是方便检索
        used2 = []
        num_considered_order2 = 0
        for idx in candidate_idxs_in_anlge_sorted_orders:
            used2.append(used_try[idx])
            if (used_try[idx] == 1):
                num_considered_order2 += 1

        while (num_considered_order2 < len(candidate)):
            num_considered_order3 = num_considered_order2
            used3 = deepcopy(used2)
            next_node_fail_flag = False
            while (True):
                random_idx = random.randint(0, len(candidate) - 1)
                while (used3[random_idx] == 1):
                    random_idx = random.randint(0, len(candidate) - 1)
                try_path = deepcopy(path)
                try_path.append(candidate[random_idx].id)
                if (if_path_legal(id_sorted_orders, try_path,
                                  datetime.datetime(2018, 6, 18, 8, 0, 0),
                    distance_matrix, time_matrix, vehicle_info[random_v_type], id_type_map)[0] == 0):
                    path.append(candidate[random_idx].id)
                    cur_weight += candidate[random_idx].weight
                    cur_volume += candidate[random_idx].volume
                    used_try[candidate_idxs_in_anlge_sorted_orders[random_idx]] = 1
                    used2[random_idx] = 1
                    num_considered_order_try += 1
                    num_considered_order2 += 1
                    break
                else:
                    used3[random_idx] = 1
                    num_considered_order3 += 1
                    if (num_considered_order3 >= len(candidate)):
                        next_node_fail_flag = True
                        break
            if (next_node_fail_flag == True):
                # 不能续两秒
                if (id_type_map[path[-1]] == 3):
                    break
                try_path = deepcopy(path)
                try_path.append(id_sorted_orders[path[-1] - 1].charging_binding)
                can_go_charge = if_path_legal(id_sorted_orders, try_path, datetime.datetime(2018, 6, 18, 8, 0, 0), distance_matrix, time_matrix,
                                              vehicle_info[random_v_type], id_type_map)
                # 补一个充电站，能行续一秒，不行挂掉
                if (can_go_charge[0] != 0):
                    break
            thres_percent = random.random() / 3.0 + 0.2
            go_charge = if_go_to_charge(id_sorted_orders, path, distance_matrix, time_matrix, vehicle_info[random_v_type], id_type_map, thres_percent)
            # 看一眼去不去充电，两条原则：电量低于一定比例去充电，电量不够回去去充电
            if (go_charge):
                try_path = deepcopy(path)
                try_path.append(id_sorted_orders[path[-1] - 1].charging_binding)
                can_go_charge = if_path_legal(id_sorted_orders, try_path, datetime.datetime(2018, 6, 18, 8, 0, 0), distance_matrix, time_matrix, vehicle_info[random_v_type], id_type_map)[0]
                if (can_go_charge == 0):
                    # 电够就去
                    path.append(id_sorted_orders[path[-1] - 1].charging_binding)
                else:
                    # 电不够，挂掉，挂掉了只能回去，有可能回不去，交给if_path_legal判断
                    break
            # 给你续一秒你又不去，挂掉
            elif (next_node_fail_flag == True):
                break

        back_legal = if_path_legal(id_sorted_orders, path, datetime.datetime(2018, 6, 18, 8, 0, 0), distance_matrix, time_matrix, vehicle_info[random_v_type], id_type_map)
        if (back_legal[0] == 0):
            used = used_try
            num_considered_order = num_considered_order_try

            if (back_legal[1] != -1):
                path.append(back_legal[1])

            tp = TransportPath(path, random_v_type+1) # 实例化一个运输路径，接下来计算一些属性
            tp = tp.calc_path_info(path_t_id, distance_matrix, time_matrix, vehicle_info, id_sorted_orders, id_type_map)
            individual.append(tp)
            path_t_id += 1
    return individual
