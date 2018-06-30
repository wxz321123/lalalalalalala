class TransportPath(object):

    def __init__(self, path, vehicle_id, wating_tm, start_tm, back_tm,distance, trans_cost, charge_cost, wait_cost, fixed_use_cost,total_cost,charge_cnt,weight,volume):
        self.id = id
        self.path = path
        self.vehicle_id = vehicle_id
        self.weight = weight
        self.volume = volume
        self.wating_tm = wating_tm
        self.distance = distance
        self.trans_cost = trans_cost
        self.start_tm = start_tm
        self.back_tm = back_tm
        self.charge_cost = charge_cost
        self.wait_cost = wait_cost
        self.fixed_use_cost = fixed_use_cost
        self.total_cost = total_cost
        self.charge_cnt = charge_cnt
    def calc_path_info(self, distance_matrix, time_matrix, vehicle_info):
        pass

    def to_list(self):
        """需要你自定义函数行为"""
        return [self.id, self.vehicle_id, self.path, self.start_tm,self.back_tm,self.distance,
                self.trans_cost, self.charge_cost, self.wait_cost,self.fixed_use_cost,self.total_cost,
                self.charge_cnt, self.weight, self.volume]