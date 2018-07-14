import datetime


def if_weight_legal(orders, path, vehicle_info, id_type_map):
    weight = 0
    for node_idx in range(len(path)):
        if id_type_map[path[node_idx]] == 2:
            weight += orders[path[node_idx] - 1].weight
    if (weight > vehicle_info.weight):
        return False
    else:
        return True


def if_volume_legal(orders, path, vehicle_info, id_type_map):
    volume = 0
    for node_idx in range(len(path)):
        if id_type_map[path[node_idx]] == 2:
            volume += orders[path[node_idx] - 1].volume
    if (volume > vehicle_info.volume):
        return False
    else:
        return True


def if_power_legal(orders, path, distance_matrix, vehicle_info, id_type_map):
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
    back_power = power + distance_matrix[0][path[-1]]
    if (back_power > vehicle_info.driving_range):
        if (id_type_map[path[-1]] == 3):
            return False, -1
        else:
            charge_power = power + orders[path[-1] - 1].charging_dist
            if (charge_power > vehicle_info.driving_range):
                return False, -1
            else:
                return True, orders[path[-1] - 1].charging_binding
    else:
        return True, -1


def if_time_legal(orders, start_time, path, time_matrix, id_type_map):
    #datetime.datetime(2018, 6, 18, 8, 0, 0)
    current_time = start_time
    for node_idx in range(len(path)):
        if node_idx == 0:  # 如果是从配送站出发到达的第一个点
            trans_time = time_matrix[0][path[node_idx]]
        else:
            trans_time = time_matrix[path[node_idx - 1]][path[node_idx]]  # 两个节点之间的运输时间
        current_time = current_time + datetime.timedelta(
            minutes=trans_time)
        if (id_type_map[path[node_idx]] == 2):
            if (current_time > datetime.datetime(2018, 6, 18, int(orders[path[node_idx]-1].lst_time.split(":")[0]),
                                                 int(orders[path[node_idx]-1].lst_time.split(":")[1]), 0)):
                return False
            elif (current_time < datetime.datetime(2018, 6, 18, int(orders[path[node_idx]-1].fst_time.split(":")[0]),
                              int(orders[path[node_idx]-1].fst_time.split(":")[1]), 0)):
                current_time = datetime.datetime(2018, 6, 18, int(orders[path[node_idx]-1].fst_time.split(":")[0]),
                              int(orders[path[node_idx]-1].fst_time.split(":")[1]), 0)
            current_time += datetime.timedelta(minutes=30)
            # 这里current_time是当前顾客服务后的时间
        elif (id_type_map[path[node_idx]] == 3):
            current_time += datetime.timedelta(minutes=30)
    return True


# orders is sorted by id
def if_path_legal(orders, path, start_time, distance_matrix, time_matrix, vehicle_info, id_type_map):
    reason_dic = {
        'w': False,
        'v': False,
        'p': False,
        't': False
    }
    if (len(path) == 0):
        return False, -1, reason_dic
    for node in path:
        if id_type_map[node] == 1:
            return False, -1, reason_dic
    w = if_weight_legal(orders, path, vehicle_info, id_type_map)
    v = if_volume_legal(orders, path, vehicle_info, id_type_map)
    p, charge_idx = if_power_legal(orders, path, distance_matrix, vehicle_info, id_type_map)
    t = if_time_legal(orders, start_time, path, time_matrix, id_type_map)

    reason_dic['w'] = w
    reason_dic['v'] = v
    reason_dic['p'] = p
    reason_dic['t'] = t

    if (w and v and p and t):
        return  True, charge_idx, reason_dic
    else:
        return False, charge_idx, reason_dic
    

def if_go_to_charge(orders, path, distance_matrix, time_matrix, vehicle_info, id_type_map, thres_percent):
    distance = distance_matrix[0][path[0]]
    for i in range(1, len(path)):
        if (id_type_map[path[i]] == 2):
            distance += distance_matrix[path[i]][path[i - 1]]
        elif (id_type_map[path[i]] == 3):
            distance = 0
    if ((1 - float(distance) / float(vehicle_info.driving_range)) <= thres_percent
        or distance + distance_matrix[path[-1]][0] > vehicle_info.driving_range):
        return True
    else:
        return False

