class TransportPath(object):

    def __init__(self, path, vehicle_id, wating_tm, start_tm, back_tm,distance, trans_cost, charge_cost, wait_cost, total_cost,weight):
        self.path = path
        self.vehicle_id = vehicle_id
        self.weight = weight
        self.wating_tm = wating_tm
        self.distance = distance
        self.trans_cost = trans_cost
        self.start_tm = start_tm
        self.back_tm = back_tm
        self.charge_cost = charge_cost
        self.wait_cost = wait_cost
        self.total_cost = total_cost
    def calc_path_info(self, distance_matrix, time_matrix, vehicle_info):
        pass

    def to_list(self):
        """需要你自定义函数行为"""
        return [self.path, self.weight,self.start_tm,self.back_tm,self.distance, self.trans_cost,self.wating_tm,self.wait_cost, self.charge_cost, self.total_cost]