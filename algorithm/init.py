import random
import utils
from copy import deepcopy
import datetime
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
# 计算一段路径的运输距离
def path_mileage(path, distance_matrix):
    path_mile = 0
    path_mile += distance_matrix[0][path[0]]
    for idx in range(len(path)-1):
        path_mile += distance_matrix[path[idx]][path[idx+1]]
    path_mile += distance_matrix[path[len(path)-1]][0]
    return path_mile

def if_path_legal(orders, path, distance_matrix, time_matrix, vehicles, id_type_map):
    start_time = datetime.datetime(2018, 6, 18, 8, 0, 0)
    back_tm = datetime.datetime(2018, 6, 18, 8, 0, 0)
    tp = TransportPath(path,vehicles,0,start_time,back_tm,0,0,0,0,0,0)
    wating_time =0
    mVehicle = {'weight': 0, 'volume': 0, 'charge_mile': 0, 'current_time': 0,'mileage': 0}  # current_time 预定义这个时间为开始工作时间
    for node_idx in range(len(path)):
        print(path[node_idx])
        if id_type_map[path[node_idx]] == 2:
        #对应序列号是否为0，也就是不是第一个 配送客户的情况下
            t_order = orders[path[node_idx]-1] #id对应的客户，可以该代码使更直观,.__dict__ 可以看到这个对象的结构
            #记录当前车辆载重，并于核定载重比较
            mVehicle["weight"] = mVehicle["weight"]+ float(t_order.weight)
            if mVehicle["weight"] < vehicles[1].weight:
                print("载重够")
                #记录当前车辆的容积，并与核定容积比较
                mVehicle["volume"] = mVehicle["volume"] + float(t_order.volume)
                if mVehicle["volume"] < vehicles[1].volume:
                    print("容量够")
                    #记录当前的充电后行驶里程，并与持续里程比较
                    # 把判断是否是被配送的第一个点放在这里。
                    if node_idx == 0:
                        mVehicle["charge_mile"] = distance_matrix[0][path[node_idx]]
                    else:
                        mVehicle["charge_mile"] = mVehicle["charge_mile"] + distance_matrix[path[node_idx-1]][path[node_idx]]
                    print(mVehicle["charge_mile"])
                    ####------临时测试用，之后要改成第二种车型
                    if mVehicle["charge_mile"] < vehicles[1].driving_range:
                        print("电量够到这个点")
                        #记录当前的时间，未明确离开时间
                        if node_idx == 0:  #如果是从配送站出发到达的第一个点
                            trans_time = time_matrix[0][path[node_idx]]
                            mVehicle["current_time"] = datetime.datetime(2018, 6, 18, 8, 0, 0) + datetime.timedelta(minutes=trans_time) #30分钟是客户服务时间
                        else:
                            trans_time = time_matrix[path[node_idx-1]][path[node_idx]] #两个节点之间的运输时间
                            mVehicle["current_time"] = mVehicle["current_time"] + datetime.timedelta(minutes=trans_time+30) #30分钟是前一个客户服务时间
                        # datetime.timedelta(hours=10,minutes=30)  #时间运算/时间加减
                        print(mVehicle["current_time"])
                        if mVehicle["current_time"] < datetime.datetime(2018,6,18,int(t_order.lst_time.split(":")[0]),int(t_order.lst_time.split(":")[1]),0):
                            print("满足时间窗上限",t_order.fst_time,t_order.lst_time)
                            if mVehicle["current_time"] < datetime.datetime(2018,6,18,int(t_order.fst_time.split(":")[0]),int(t_order.fst_time.split(":")[1]),0):
                                if node_idx != 0: #配送站出发没有等待时间
                                    wating_time = wating_time + (datetime.datetime(2018, 6, 18, int(t_order.fst_time.split(":")[0]),int(t_order.fst_time.split(":")[1]), 0) -mVehicle["current_time"]).seconds / 60
                                    print("配送站等待时间", wating_time)
                                if node_idx==0: #判断汽车从配送站出发的时间
                                    t_time = (datetime.datetime(2018, 6, 18, int(t_order.fst_time.split(":")[0]),int(t_order.fst_time.split(":")[1]), 0) -mVehicle["current_time"]).seconds/60
                                    tp.start_tm = datetime.datetime(2018, 6, 18, 8, 0, 0) + datetime.timedelta(minutes=t_time)
                                mVehicle["current_time"] = datetime.datetime(2018, 6, 18,int(t_order.fst_time.split(":")[0]),int(t_order.fst_time.split(":")[1]), 0)
                                # 如果比服务时间下限小，就将服务时间下限作为服务时间，否则就是到达时间
                            # 判断能否回到充电站
                            mVehicle["charge_mile"] = mVehicle["charge_mile"] + distance_matrix[path[node_idx - 1]][path[node_idx]]
                            if mVehicle["charge_mile"] < vehicles[1].driving_range:
                                print("不充电就直接回到配送站")
                                trans_time = time_matrix[path[node_idx]][0]  # 两个节点之间的运输时间
                                tp.back_tm = mVehicle["current_time"] + datetime.timedelta(minutes=trans_time + 30)  # 30分钟是前一个客户服务时间
                            else:
                                print("为了回家去充电")
                                #判断不充电回不了配送站的情况下，可不可以到附近的充电站充电
                                if mVehicle["charge_mile"] + t_order.charging_dist < vehicles[1].driving_range:
                                    print("为了回家可以去充电")
                                    trans_time =time_matrix[path[node_idx]][t_order.charging_binding]+ time_matrix[t_order.charging_binding][0]  # 两个节点之间的运输时间
                                    tp.back_tm = mVehicle["current_time"] + datetime.timedelta(minutes=trans_time + 30)  # 30分钟是前一个客户服务时间

                                else:
                                    print("不充电回不了配送站，而且去不了就近的充电站")
                                    return False
                        else:
                            print("超时无法服务客户")
                            return False

                    else:
                        # 车的电量不够，要去充电
                        print("车的电量不够")
                        return False
                else:
                    print("车辆容积不够")
                    return False
            else:
                print("车辆载重不够")
                return False
        else:
            # 判断到最近的充电站够不够
            if mVehicle["charge_mile"] + t_order.charging_dist < vehicles[1].driving_range:
                # 充电会影响充电行驶里程，还有行驶总路程，还有时间
                mVehicle["charge_mile"] = distance_matrix[t_order.charging_binding][path[node_idx]]
                trans_time_withCharge = time_matrix[path[node_idx - 1]][t_order.charging_binding] + time_matrix[t_order.charging_binding][path[node_idx]]  # t_order.char 经过充电站后到下一个客户的时间
                mVehicle["current_time"] = mVehicle["current_time"] + datetime.timedelta(minutes=trans_time_withCharge + 30)  # 30分钟是客户服务时间
                # charge_position_id.append(node_idx)
            else:
                # 如果电量不够去充电
                print("电量不够去充电")
                return False

    # tp = TransportPath(path,vehicles,0,0,0)
    tp.weight = mVehicle["weight"]
    tp.wating_tm = wating_time
    return True,tp
    pass

def random_individual(warehouse, id_sorted_orders, angle_sorted_orders, chargings, vehicle_info, id_type_map, distance_matrix, time_matrix):


    distance_thres = 10000
    num_vehicle_type = len(vehicle_info)

    individual = []

    #整个过程从这个点开始
    start_idx = random.randint(0, len(angle_sorted_orders) - 1)
    part1 = angle_sorted_orders[start_idx:len(angle_sorted_orders)]
    part2 = angle_sorted_orders[0:start_idx - 1]
    angle_sorted_orders = part1 + part2

    used = [0] * len(angle_sorted_orders)
    num_considered_order = 0

    while(num_considered_order < len(angle_sorted_orders)):
        used_try = deepcopy(used)
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
        num_considered_order += 1
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
                    try_path = deepcopy(path)
                    try_path.append(id_sorted_orders[path[-1] - 1].charging_binding)
                    can_go_charge = if_path_legal(id_sorted_orders, try_path, distance_matrix, time_matrix, vehicle_info, id_type_map)
                    if (can_go_charge):
                        # 电够就去
                        path.append(id_sorted_orders[path[-1] - 1].charging_binding)
                        cost_charge += 50 #充电后充电成本为
                    else:
                        # 电不够，挂掉
                        break

        if (if_path_legal(id_sorted_orders, path, distance_matrix, time_matrix, vehicle_info, id_type_map)):
            used = used_try
            #刘治修改
            tp = if_path_legal(id_sorted_orders, path, distance_matrix, time_matrix, vehicle_info, id_type_map)[1]
            tp.charge_cost = cost_charge
            tp.calc_path_info(distance_matrix, time_matrix, vehicle_info)
            tp.distance = path_mileage(path, distance_matrix)
            #总成本=运输成本+等待成本+充电成本+固定成本
            tp.trans_cost = tp.distance * 0.014
            tp.wait_cost = tp.wating_tm / 60 * 24
            tp.total_cost = tp.trans_cost  + tp.wait_cost + tp.charge_cost + 300
            individual.append(tp.to_list())

    return individual