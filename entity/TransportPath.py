from algorithm.calculate import path_nodes
from algorithm.calculate import path_distance_time
from algorithm.calculate import count_charge_cnt
from algorithm.calculate import path_time_info

class TransportPath(object):

    def __init__(self, path, vehicle_id):
        self.id = id
        self.path = path
        self.vehicle_id = vehicle_id
        self.weight = 0
        self.volume = 0
        self.waiting_tm = 0
        self.distance = 0
        self.trans_cost = 0
        self.start_tm = 0
        self.back_tm = 0
        self.charge_cost = 0
        self.wait_cost = 0
        self.fixed_use_cost = 0
        self.total_cost = 0
        self.charge_cnt = 0
    def calc_path_info(self,individual_id, distance_matrix, time_matrix, vehicle_info,  id_sorted_orders, id_type_map):
        # (tp, individual_id, distance_matrix, time_matrix, vehicle_info, id_sorted_orders, id_type_map):
        self.weight = path_nodes(self.path, id_sorted_orders)[0]
        self.volume = path_nodes(self.path, id_sorted_orders)[1]
        self.distance = path_distance_time(self.path, distance_matrix, time_matrix)[0]

        t_str = str(1000 + individual_id)
        t_tm = path_time_info(id_sorted_orders, self.path, distance_matrix, time_matrix, vehicle_info[self.vehicle_id - 1],
                              id_type_map)
        self.id = "DP0" + t_str[1:]
        self.back_tm = t_tm[0]
        self.start_tm = t_tm[1]

        self.waiting_tm = t_tm[2]
        self.charge_cnt = count_charge_cnt(self.path)

        if self.vehicle_id == 2:
            self.trans_cost = self.distance * 0.014
        else:
            self.trans_cost = self.distance * 0.012
        self.wait_cost = self.waiting_tm / 60 * 24
        self.charge_cost = self.charge_cnt * 50
        if self.vehicle_id == 2:
            self.fixed_use_cost = 300
        else:
            self.fixed_use_cost = 200
        # 总成本=运输成本+等待成本+充电成本+固定成本
        self.total_cost = self.trans_cost + self.wait_cost + self.charge_cost + self.fixed_use_cost
        return self

    def to_list(self):
        """需要你自定义函数行为"""
        return [self.id, self.vehicle_id, self.path, self.start_tm,self.back_tm,self.distance,
                self.trans_cost, self.charge_cost, self.wait_cost,self.fixed_use_cost,self.total_cost,
                self.charge_cnt, self.weight, self.volume]

#
# def tp_info_calculate(tp, individual_id, distance_matrix, time_matrix, vehicle_info, id_sorted_orders, id_type_map):
#     # cale_path_info 暂时没有写在里面
#     tp.calc_path_info(distance_matrix, time_matrix, tp.vehicle_id)
#     tp.weight = path_nodes(tp.path, id_sorted_orders)[0]
#     tp.volume = path_nodes(tp.path, id_sorted_orders)[1]
#     tp.distance = path_distance_time(tp.path, distance_matrix, time_matrix)[0]
#
#     t_str = str(1000 + individual_id)
#     t_tm = path_time_info(id_sorted_orders, tp.path, distance_matrix, time_matrix, vehicle_info[tp.vehicle_id-1], id_type_map)
#     tp.id = "DP0" + t_str[1:]
#     tp.back_tm = t_tm[0]
#     tp.start_tm = t_tm[1]
#
#     tp.waiting_tm = t_tm[2]
#     tp.charge_cnt = count_charge_cnt(tp.path)
#
#     if tp.vehicle_id == 2:
#         tp.trans_cost = tp.distance * 0.014
#     else:
#         tp.trans_cost = tp.distance * 0.012
#     tp.wait_cost = tp.waiting_tm / 60 * 24
#     tp.charge_cost = tp.charge_cnt * 50
#     if tp.vehicle_id == 2:
#         tp.fixed_use_cost = 300
#     else:
#         tp.fixed_use_cost = 200
#     # 总成本=运输成本+等待成本+充电成本+固定成本
#     tp.total_cost = tp.trans_cost + tp.wait_cost + tp.charge_cost + tp.fixed_use_cost
#     return  tp