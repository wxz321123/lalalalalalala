import random
from copy import deepcopy
from algorithm.verify import if_path_legal


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


def if_go_to_charge(id_sorted_orders, path, distance_matrix, time_matrix, vehicle_info, id_type_map):
    if (len(path) == 0):
        return False
    if if_path_legal(id_sorted_orders, path, distance_matrix, time_matrix, vehicle_info, id_type_map) != False:
        if_charge = if_path_legal(id_sorted_orders, path, distance_matrix, time_matrix, vehicle_info, id_type_map)[2]
        mVehicle = if_charge[0]
        node_idx = if_charge[1]
        vehicle_type = if_charge[2]
        t_order = if_charge[3]
        # 判断能否回到配送站
        print("充电",mVehicle["charge_mile"],distance_matrix[path[node_idx]][0])
        if mVehicle["charge_mile"] + distance_matrix[path[node_idx]][0] < vehicle_info[vehicle_type - 1].driving_range:
            # print("不充电就直接回到配送站")
            return False
        else:
            if mVehicle["charge_mile"]+t_order.charging_dist < vehicle_info[vehicle_type - 1].driving_range:
                print("需要，且能去充电")
                return True
            else:
                print("需要充电，但去不了",t_order.charging_dist)
                return False
    else:
        print("返回值为 False")


# 计算一段路径的运输距离
def path_mileage(path, distance_matrix):
    path_mile = 0
    path_mile += distance_matrix[0][path[0]]
    for idx in range(len(path)-1):
        path_mile += distance_matrix[path[idx]][path[idx+1]]
    path_mile += distance_matrix[path[len(path)-1]][0]
    return path_mile


def random_individual(warehouse, id_sorted_orders, angle_sorted_orders, chargings, vehicle_info, id_type_map, distance_matrix, time_matrix):

    distance_thres = 10000
    num_vehicle_type = len(vehicle_info)
    individual_id = 1
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
        cost_charge = 0  # 充电成本默认为0
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
            fail_flag = False
            while (True):
                random_idx = random.randint(0, len(candidate) - 1)
                while (used3[random_idx] == 1):
                    random_idx = random.randint(0, len(candidate) - 1)
                try_path = deepcopy(path)
                try_path.append(candidate[random_idx].id)
                if (if_path_legal(id_sorted_orders, try_path, distance_matrix, time_matrix, vehicle_info, id_type_map)):
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
                        fail_flag = True
                        break
            go_charge = if_go_to_charge(id_sorted_orders, path, distance_matrix, time_matrix, vehicle_info, id_type_map)
            # 看一眼去不去充电，两条原则：电量低于一定比例去充电，电量不够回去去充电
            if (go_charge):
                try_path = deepcopy(path)
                try_path.append(id_sorted_orders[path[-1] - 1].charging_binding)
                can_go_charge = if_path_legal(id_sorted_orders, try_path, distance_matrix, time_matrix, vehicle_info, id_type_map)
                if (can_go_charge):
                    # 电够就去
                    path.append(id_sorted_orders[path[-1] - 1].charging_binding)
                    cost_charge += 50 #充电后充电成本为
                else:
                    # 电不够，挂掉，挂掉了只能回去，有可能回不去，交给if_path_legal判断
                    break
            if (fail_flag == True):
                #找不到任何下一个合法点，挂掉，挂掉了只能回去，有可能回不去，交给if_path_legal判断
                break
        if (if_path_legal(id_sorted_orders, path, distance_matrix, time_matrix, vehicle_info, id_type_map)):
            used = used_try
            num_considered_order = num_considered_order_try

            #刘治修改
            tp = if_path_legal(id_sorted_orders, path, distance_matrix, time_matrix, vehicle_info, id_type_map)[1]
            t_str = str(1000 + individual_id)
            tp.id = "DP0" + t_str[1:]
            tp.charge_cost = cost_charge
            tp.charge_cnt = cost_charge / 50
            tp.calc_path_info(distance_matrix, time_matrix, vehicle_info)
            tp.distance = path_mileage(path, distance_matrix)
            #总成本=运输成本+等待成本+充电成本+固定成本
            tp.trans_cost = tp.distance * 0.014
            tp.wait_cost = tp.wating_tm / 60 * 24
            tp.total_cost = tp.trans_cost  + tp.wait_cost + tp.charge_cost + 300
            print(tp.path)
            individual.append(tp.to_list())
            individual_id += 1
    return individual

