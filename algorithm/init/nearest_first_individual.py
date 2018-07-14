import random
import datetime
from copy import deepcopy
from algorithm.verify import if_path_legal
from algorithm.verify import if_go_to_charge
from algorithm.utils import group_by_last_time
from entity.TransportPath import TransportPath

def first_order(grouped_orders, used, distance_matrix):
    last_times = sorted(grouped_orders.keys())
    for lt in last_times:
        orders = sorted(grouped_orders[lt], key=lambda x:distance_matrix[0][x.id])
        for o in orders:
            if used[o.id] == 0:
                return o
    return None

def next_order(id_sorted_orders, path, grouped_orders, used, distance_matrix, id_type_map):
    last_times = sorted(grouped_orders.keys())
    begin = False
    cur_order = None
    if (id_type_map[path[-1]] == 2):
        cur_order = id_sorted_orders[path[-1] - 1]
    else:
        cur_order = id_sorted_orders[path[-2] - 1]
    for lt in last_times:
        if (lt == cur_order.lst_time):
            begin = True
        if (begin):
            orders = sorted(grouped_orders[lt], key=lambda x:distance_matrix[path[-1]][x.id])
            for o in orders:
                if used[o.id] == 0 and distance_matrix[o.id][path[-1]] < 12000:
                    return o
    return None

def can_go_to_charge(path, charging_distance, distance_matrix, vehicle_info, id_type_map):
    if (len(path) == 0):
        return False
    power = 0
    for node_idx in range(len(path)):
        if (node_idx == 0):
            power += distance_matrix[0][path[node_idx]]
        else:
            power += distance_matrix[path[node_idx - 1]][path[node_idx]]
        if power > vehicle_info.driving_range:
            return False, -1
        if (id_type_map[path[node_idx]] == 3):
            power = 0
    if (power + charging_distance > vehicle_info.driving_range):
        return False
    else:
        return True


def decide_v_type(id_sorted_orders, path, vehicle_info, distance_matrix, time_matrix, id_type_map):
    b = if_path_legal(id_sorted_orders, path, datetime.datetime(2018, 6, 18, 8, 0, 0), distance_matrix, time_matrix,
                  vehicle_info[0], id_type_map)
    if (b[0] == True and b[1] == -1):
        return 0
    else:
        return 1


def better_init_individual(warehouse, id_sorted_orders, chargings, vehicle_info, id_type_map, distance_matrix, time_matrix):
    used = {}
    for o in id_sorted_orders:
        used[o.id] = 0
    num_considered_order = 0

    grouped_orders = group_by_last_time(id_sorted_orders)

    pathes = []
    while (num_considered_order < len(id_sorted_orders)):
        v_type = 1

        print('reached order: ' + str(num_considered_order))
        used_cp = deepcopy(used)
        num_considered_order_cp = num_considered_order

        path = []
        fo = first_order(grouped_orders, used, distance_matrix)
        if (fo == None):
            break
        path.append(fo.id)
        used_cp[fo.id] = 1
        num_considered_order_cp += 1


        while(True):
            used_try = deepcopy(used_cp)
            num_considered_order_try = num_considered_order_cp
            fail_flag = False
            while (True):
                no = next_order(id_sorted_orders, path, grouped_orders, used_try, distance_matrix, id_type_map)
                if (no == None):
                    # # 这里应该可以保证已有路径是可行的
                    fail_flag = True
                    break
                try_path = deepcopy(path)
                try_path.append(no.id)
                legal = if_path_legal(id_sorted_orders, try_path,
                                      datetime.datetime(2018, 6, 18, 8, 0, 0),
                                      distance_matrix, time_matrix,
                                      vehicle_info[v_type], id_type_map)
                if (legal[0] == True):
                    path.append(no.id)
                    used_cp[no.id] = 1
                    num_considered_order_cp += 1
                    break
                elif (legal[2]['p'] == False and legal[2]['w'] == True
                      and legal[2]['v'] == True and legal[2]['t'] == True):
                    if (id_type_map[path[-1]] == 2):
                        if (can_go_to_charge(path, id_sorted_orders[path[-1] - 1].charging_dist,
                                             distance_matrix, vehicle_info[v_type], id_type_map)):
                            path.append(id_sorted_orders[path[-1] - 1].charging_binding)
                            break
                        else:
                            used_try[no.id] = 1
                            num_considered_order_try += 1
                    else:
                        #这里退出的话 可能路径是不可行的
                        fail_flag = True
                        break
                else:
                    used_try[no.id] = 1
                    num_considered_order_try += 1
                    if (num_considered_order_try >= len(id_sorted_orders)):
                        # 这里应该可以保证已有路径是可行的
                        fail_flag = True
                        break
            if (fail_flag == True):
                break

        b = if_path_legal(id_sorted_orders, path,
                          datetime.datetime(2018, 6, 18, 8, 0, 0),
                          distance_matrix, time_matrix,
                          vehicle_info[v_type], id_type_map)
        if b[0] == True:
            if b[1] != -1:
                path.append(b[1])
            for n in path:
                if (id_type_map[n] == 2):
                    used[n] = 1
                    num_considered_order += 1
            pathes.append(path)


    ans = []
    custom_map = {}
    for idx, path in enumerate(pathes):
        v_type = decide_v_type(id_sorted_orders, path, vehicle_info, distance_matrix, time_matrix, id_type_map)

        b = if_path_legal(id_sorted_orders, path,
                          datetime.datetime(2018, 6, 18, 8, 0, 0),
                          distance_matrix, time_matrix,
                          vehicle_info[v_type], id_type_map)
        if b[0] == False or b[1] != -1:
            raise Exception

        for n in path:
            if (id_type_map[n] == 2):
                custom_map[n] = 1

        tp = TransportPath(path, v_type + 1)  # 实例化一个运输路径，接下来计算一些属性
        tp = tp.calc_path_info(idx + 1, distance_matrix, time_matrix, vehicle_info, id_sorted_orders, id_type_map)
        ans.append(tp)

    custom_count = 0
    for k in custom_map.keys():
        custom_count += 1

    print("custom count: " + str(custom_count))
    return ans