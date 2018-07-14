from algorithm.utils import group_by_last_time
from entity.TransportPath import TransportPath
from algorithm.verify import if_path_legal
import random
import math
import datetime
import load_data as ldd

# try form better path according to two existing path
def exchange_path(id_sorted_orders, px, py, id_type_map, distance_matrix, time_matrix, vehicle_info):
    lenx = len(px)
    leny = len(py)
    tpx = TransportPath(px, 2)
    tpx.calc_path_info(0, distance_matrix, time_matrix, vehicle_info, id_sorted_orders, id_type_map)
    costx = tpx.total_cost
    tpy = TransportPath(py, 2)
    tpy.calc_path_info(0, distance_matrix, time_matrix, vehicle_info, id_sorted_orders, id_type_map)
    costy = tpy.total_cost

    orders_in_x = []
    for nx in px:
        if id_type_map[nx] == 2:
            orders_in_x.append(id_sorted_orders[nx - 1])
    orders_in_y = []
    for ny in py:
        if id_type_map[ny] == 2:
            orders_in_y.append(id_sorted_orders[ny - 1])

    orders_in_p = orders_in_x + orders_in_y

    grouped_order = group_by_last_time(orders_in_p)

    times = sorted(list(grouped_order.keys()))

    time_dicx = {}
    time_dicy = {}
    for time in times:
        time_dicx.setdefault(time, [])
        time_dicy.setdefault(time, [])
    for o in orders_in_x:
        time_dicx[o.lst_time].append(o)
    for o in orders_in_y:
        time_dicy[o.lst_time].append(o)

    num_node_in_window = []
    for time in times:
        num_node_in_window.append(min(len(time_dicx[time]), len(time_dicy[time])))

    ans = []

    dfs(0, 1, px, py,
        id_sorted_orders, distance_matrix, time_matrix, vehicle_info, id_type_map,
        times, num_node_in_window, time_dicx, time_dicy, costx, costy, ans)
    return ans

def path_swap(pathx, pathy, window_idx, node_idx, time_dicx, time_dicy, windows):
    x_swap_id = time_dicx[windows[window_idx]][node_idx].id
    y_swap_id = time_dicy[windows[window_idx]][node_idx].id

    x_ = -1
    for idx, n in enumerate(pathx):
        if n == x_swap_id:
            x_ = idx

    y_ = -1
    for idx, n in enumerate(pathy):
        if n == y_swap_id:
            y_ = idx

    new_path_x = pathx[0:x_] + pathy[y_:]
    new_path_y = pathy[0:y_] + pathx[x_:]

    return new_path_x, new_path_y


def path_cost(p, id_sorted_orders, distance_matrix, time_matrix, vehicle_info, id_type_map):
    tp = TransportPath(p, 2)
    tp.calc_path_info(0, distance_matrix, time_matrix, vehicle_info, id_sorted_orders, id_type_map)
    return tp.total_cost

def dfs(start_window_idx, start_node_idx, cur_pathx, cur_pathy,
        id_sorted_orders, distance_matrix, time_matrix, vehicle_info, id_type_map,
        windows, num_node_in_window, time_dicx, time_dicy, costx, costy, ans):
    if (start_window_idx > len(windows)):
        legal_x = if_path_legal(cur_pathx)
        legal_y = if_path_legal(cur_pathy)
        if (legal_x and legal_y):
            better = path_cost(cur_pathx, id_sorted_orders, distance_matrix, time_matrix, vehicle_info, id_type_map) + \
                     path_cost(cur_pathy, id_sorted_orders, distance_matrix, time_matrix, vehicle_info, id_type_map) < costx + costy
            if (better):
                ans.append((cur_pathx, cur_pathy))
        return
    # 这里在遍历时间窗
    for wi in range(start_window_idx, len(windows)):
        if wi != start_window_idx:
            start_node_idx_ = 0
        else:
            start_node_idx_ = start_node_idx
        leng = num_node_in_window[wi]
        # 这里在遍历时间窗里的节点
        for ni in range(start_node_idx_, leng):
            # 这里交换了路径，之后判断是不是合法，大多数都不合法。
            new_path_x, new_path_y = path_swap(cur_pathx, cur_pathy, wi, ni, time_dicx, time_dicy, windows)
            legal_x = if_path_legal(id_sorted_orders, new_path_x, datetime.datetime(2018, 6, 18, 8, 0, 0), distance_matrix, time_matrix,
                  vehicle_info[1], id_type_map)
            legal_y = if_path_legal(id_sorted_orders, new_path_y, datetime.datetime(2018, 6, 18, 8, 0, 0), distance_matrix, time_matrix,
                  vehicle_info[1], id_type_map)
            if (legal_x[0] and legal_y[0]):
                better = path_cost(new_path_x, id_sorted_orders, distance_matrix, time_matrix, vehicle_info, id_type_map) + \
                         path_cost(new_path_y, id_sorted_orders, distance_matrix, time_matrix, vehicle_info, id_type_map) < costx + costy
                if (better):
                    if (ni == num_node_in_window[start_window_idx] - 1):
                        next_window = start_window_idx + 1
                        while (next_window < len(windows) and num_node_in_window[next_window] == 0):
                            next_window += 1
                        next_node_idx = 0
                    else:
                        next_window = start_window_idx
                        next_node_idx = start_node_idx +1
                    dfs(next_window, next_node_idx, new_path_x, new_path_y,
                        id_sorted_orders, distance_matrix, time_matrix, vehicle_info, id_type_map,
                        windows, num_node_in_window, time_dicx, time_dicy, costx, costy, ans)

random.seed(0)
warehouse, orders, charging, id_type_map = ldd.load_node_info("../../data/input_node.csv")

id_sorted_orders = sorted(orders, key = lambda x: x.id)
angle_sorted_orders = sorted(orders, key = lambda x: x.polar_angle)

vehicles = ldd.load_vehicle_info('../../data/input_vehicle_type.csv')
distance_matrix, time_matrix = ldd.load_distance_time_info('../../data/input_distance-time.csv')

print(exchange_path(id_sorted_orders,[220, 856, 501, 250, 911, 700, 106, 783, 304, 205, 114],[605, 763, 947, 408, 801, 459, 693, 283, 590, 269],id_type_map,distance_matrix, time_matrix, vehicles))