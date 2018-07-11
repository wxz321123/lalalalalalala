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
    if (len(path) == 0):
        return False, -1
    for node in path:
        if id_type_map[node] == 1:
            return False, -1
    w = if_weight_legal(orders, path, vehicle_info, id_type_map)
    v = if_volume_legal(orders, path, vehicle_info, id_type_map)
    p, charge_idx = if_power_legal(orders, path, distance_matrix, vehicle_info, id_type_map)
    t = if_time_legal(orders, start_time, path, time_matrix, id_type_map)

    reason_dic = {
        'w': w,
        'v': v,
        'p': p,
        't': t
    }

    if (w and v and p and t):
        return  True, charge_idx, reason_dic
    else:
        return False, charge_idx, reason_dic


# 判断路径是否合规
# def if_path_legal1(orders, path, distance_matrix, time_matrix, vehicle_info, id_type_map):
#     mVehicle = {'weight': 0, 'volume': 0, 'charge_mile': 0, 'current_time': 0,'mileage': 0}  # current_time 预定义这个时间为开始工作时间
#     append_charge = -1
#     for node_idx in range(len(path)):
#         # print("判断当前点",path[node_idx],"当前路径",path)
#         if id_type_map[path[node_idx]] == 2:
#         #对应序列号是否为0，也就是不是第一个 配送客户的情况下
#             t_order = orders[path[node_idx]-1] #id对应的客户，可以该代码使更直观,.__dict__ 可以看到这个对象的结构
#             #记录当前车辆载重，并于核定载重比较
#             mVehicle["weight"] = mVehicle["weight"]+ float(t_order.weight)
#             if mVehicle["weight"] < vehicle_info.weight:
#                 # print("载重够")
#                 #记录当前车辆的容积，并与核定容积比较
#                 mVehicle["volume"] = mVehicle["volume"] + float(t_order.volume)
#                 if mVehicle["volume"] < vehicle_info.volume:
#                     # print("容量够")
#                     # 记录当前的充电后行驶里程，并与持续里程比较
#                     if node_idx == 0:
#                         mVehicle["charge_mile"] = distance_matrix[0][path[node_idx]]
#                     else:
#                         mVehicle["charge_mile"] = mVehicle["charge_mile"] + distance_matrix[path[node_idx-1]][path[node_idx]]
#                     # print(mVehicle["charge_mile"])
#                     if mVehicle["charge_mile"] < vehicle_info.driving_range:
#                         # print("电量够到这个点")
#                         #记录当前的时间，未明确离开时间
#                         if node_idx == 0:  #如果是从配送站出发到达的第一个点
#                             trans_time = time_matrix[0][path[node_idx]]
#                             mVehicle["current_time"] = datetime.datetime(2018, 6, 18, 8, 0, 0) + datetime.timedelta(minutes=trans_time) #30分钟是客户服务时间
#                         else:
#                             trans_time = time_matrix[path[node_idx-1]][path[node_idx]] #两个节点之间的运输时间
#                             mVehicle["current_time"] = mVehicle["current_time"] + datetime.timedelta(minutes=trans_time+30) #30分钟是前一个客户服务时间
#                         # print(mVehicle["current_time"])
#                         if mVehicle["current_time"] < datetime.datetime(2018, 6, 18,int(t_order.lst_time.split(":")[0]),int(t_order.lst_time.split(":")[1]),0):
#                             # print("满足时间窗上限",t_order.fst_time,t_order.lst_time)
#                             if mVehicle["current_time"] < datetime.datetime(2018, 6, 18,int(t_order.fst_time.split(":")[0]),int(t_order.fst_time.split(":")[1]),0):
#                                 mVehicle["current_time"] = datetime.datetime(2018, 6, 18,int(t_order.fst_time.split(":")[0]),int(t_order.fst_time.split(":")[1]), 0)
#                                 # print(mVehicle["current_time"])
#                                 # 如果比服务时间下限小，就将服务时间下限作为服务时间，否则就是到达时间
#                             # 判断能否回到配送站
#                             if mVehicle["charge_mile"] + distance_matrix[path[node_idx]][0] > vehicle_info.driving_range:
#                                 if mVehicle["charge_mile"] + t_order.charging_dist > vehicle_info.driving_range:
#                                     print("需要充电才能回配送站,但去不了充电")
#                                     return False
#                         else:
#                             # print("超时无法服务客户")
#                             return False
#                     else:
#                         # print("车的电量不够")
#                         return False
#                 else:
#                     # print("车辆容积不够")
#                     return False
#             else:
#                 # print("车辆载重不够")
#                 return False
#         else:
#             # 判断到最近的充电站够不够
#             mVehicle["charge_mile"] = mVehicle["charge_mile"] +t_order.charging_dist
#             if mVehicle["charge_mile"] < vehicle_info.driving_range:
#                 # 充电会影响充电行驶里程，还有行驶总路程，还有时间
#                 mVehicle["charge_mile"] = 0
#                 mVehicle["current_time"] = mVehicle["current_time"] + datetime.timedelta(minutes=time_matrix[t_order.id][t_order.charging_binding] + 30)
#                 # print("到充电站的时间", mVehicle["current_time"])
#                 if mVehicle["charge_mile"] > vehicle_info.driving_range:
#                    return False #print("充电后回不了配送站")
#             else:
#                 return False# print("电量不够去充电")
#     return True


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

