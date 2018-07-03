import datetime

def path_distance_time(path, distance_matrix, time_matrix):
    path_distance = 0
    path_time = 0
    path_distance += distance_matrix[0][path[0]]
    path_time += time_matrix[0][path[0]]
    for idx in range(len(path)-1):
        path_distance += distance_matrix[path[idx]][path[idx+1]]
        path_time += time_matrix[path[idx]][path[idx + 1]]
    path_distance += distance_matrix[path[len(path)-1]][0]
    path_time += time_matrix[path[len(path) - 1]][0]
    return path_distance,path_time

def path_nodes(path, orders):
    weight = 0
    volume = 0
    for idx in path:
        if idx <= 1000: #大于1000的id是充电站
            weight += orders[idx-1].weight
            volume += orders[idx-1].volume
    return weight,volume

def count_charge_cnt(path):
    cnt = 0
    for node_id in path:
        if node_id > 1000:
            cnt += 1
    return cnt

# 输出汽车出发时间、返回时间、等待时间
def path_time_info(orders, path, distance_matrix, time_matrix, vehicle_info, id_type_map):
    start_tm = datetime.datetime(2018, 6, 18, 8, 0, 0)
    back_tm = datetime.datetime(2018, 6, 18, 8, 0, 0)
    waiting_time =0
    mVehicle = {'weight': 0, 'volume': 0, 'charge_mile': 0, 'current_time': 0,'mileage': 0}  # current_time 预定义这个时间为开始工作时间
    for node_idx in range(len(path)):
        # print("判断当前点",path[node_idx],"当前路径",path)
        if id_type_map[path[node_idx]] == 2:
        #对应序列号是否为0，也就是不是第一个 配送客户的情况下
            t_order = orders[path[node_idx]-1] #id对应的客户，可以该代码使更直观,.__dict__ 可以看到这个对象的结构
            #记录当前车辆载重，并于核定载重比较
            mVehicle["weight"] = mVehicle["weight"]+ float(t_order.weight)
            if mVehicle["weight"] < vehicle_info.weight:
                # print("载重够")
                #记录当前车辆的容积，并与核定容积比较
                mVehicle["volume"] = mVehicle["volume"] + float(t_order.volume)
                if mVehicle["volume"] < vehicle_info.volume:
                    # print("容量够")
                    # 记录当前的充电后行驶里程，并与持续里程比较
                    if node_idx == 0:
                        mVehicle["charge_mile"] = distance_matrix[0][path[node_idx]]
                    else:
                        mVehicle["charge_mile"] = mVehicle["charge_mile"] + distance_matrix[path[node_idx-1]][path[node_idx]]
                    # print(mVehicle["charge_mile"])
                    if mVehicle["charge_mile"] < vehicle_info.driving_range:
                        # print("电量够到这个点")
                        #记录当前的时间，未明确离开时间
                        if node_idx == 0:  #如果是从配送站出发到达的第一个点
                            trans_time = time_matrix[0][path[node_idx]]
                            mVehicle["current_time"] = datetime.datetime(2018, 6, 18, 8, 0, 0) + datetime.timedelta(minutes=trans_time) #30分钟是客户服务时间
                        else:
                            trans_time = time_matrix[path[node_idx-1]][path[node_idx]] #两个节点之间的运输时间
                            mVehicle["current_time"] = mVehicle["current_time"] + datetime.timedelta(minutes=trans_time+30) #30分钟是前一个客户服务时间
                        # datetime.timedelta(hours=10,minutes=30)  #时间运算/时间加减
                        # print(mVehicle["current_time"])
                        if mVehicle["current_time"] < datetime.datetime(2018, 6, 18,int(t_order.lst_time.split(":")[0]),int(t_order.lst_time.split(":")[1]),0):
                            # print("满足时间窗上限",t_order.fst_time,t_order.lst_time)
                            if mVehicle["current_time"] < datetime.datetime(2018, 6, 18,int(t_order.fst_time.split(":")[0]),int(t_order.fst_time.split(":")[1]),0):
                                if node_idx != 0:
                                    waiting_time = waiting_time + (datetime.datetime(2018, 6, 18, int(t_order.fst_time.split(":")[0]),int(t_order.fst_time.split(":")[1]), 0) -mVehicle["current_time"]).seconds / 60
                                    # print("等待客户时间", waiting_time)
                                if node_idx==0: # 配送站出发没有等待时间
                                    t_time = (datetime.datetime(2018, 6, 18, int(t_order.fst_time.split(":")[0]),int(t_order.fst_time.split(":")[1]), 0) -mVehicle["current_time"]).seconds/60
                                    start_tm = datetime.datetime(2018, 6, 18, 8, 0, 0) + datetime.timedelta(minutes=t_time)
                                mVehicle["current_time"] = datetime.datetime(2018, 6, 18,int(t_order.fst_time.split(":")[0]),int(t_order.fst_time.split(":")[1]), 0)
                                # print(mVehicle["current_time"])
                                # 如果比服务时间下限小，就将服务时间下限作为服务时间，否则就是到达时间
                            # 判断能否回到配送站
                            if mVehicle["charge_mile"] +distance_matrix[path[node_idx]][0] < vehicle_info.driving_range:
                                # print("不充电就直接回到配送站")
                                trans_time = time_matrix[path[node_idx]][0]  # 两个节点之间的运输时间
                                back_tm = mVehicle["current_time"] + datetime.timedelta(minutes=trans_time + 30)  # 30分钟是前一个客户服务时间
                            else:
                                if mVehicle["charge_mile"] + t_order.charging_dist > vehicle_info.driving_range:
                                    print("需要充电才能回配送站,但去不了充电")
                                    return False
                        else:
                            # print("超时无法服务客户")
                            return False

                    else:
                        # 车的电量不够，要去充电
                        # print("车的电量不够")
                        return False
                else:
                    # print("车辆容积不够")
                    return False
            else:
                # print("车辆载重不够")
                return False
        else:
            # 判断到最近的充电站够不够
            mVehicle["charge_mile"] = mVehicle["charge_mile"] +t_order.charging_dist
            if mVehicle["charge_mile"] < vehicle_info.driving_range:
                # 充电会影响充电行驶里程，还有行驶总路程，还有时间
                mVehicle["charge_mile"] = 0
                mVehicle["current_time"] = mVehicle["current_time"] + datetime.timedelta(minutes=time_matrix[t_order.id][t_order.charging_binding] + 30)
                # print("到充电站的时间", mVehicle["current_time"])
                # 增加判断能否回家
                if mVehicle["charge_mile"] < vehicle_info.driving_range:
                    # print("不充电就直接回到配送站")
                    trans_time = time_matrix[path[node_idx]][0]  # 两个节点之间的运输时间
                    back_tm = mVehicle["current_time"] + datetime.timedelta(minutes=trans_time + 30)  # 30分钟是前一个客户服务时间
                else:
                    return False
            else:
                return False# print("电量不够去充电")
    t_tm = [start_tm,back_tm,waiting_time]
    return t_tm
