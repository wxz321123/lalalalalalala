class TransportPath(object):

    def __init__(self, path, vehicle_id, wating_tm, start_tm, back_tm,distance, charge_cost, weight):
        self.path = path
        self.vehicle_id = vehicle_id
        self.weight = weight
        self.wating_tm = wating_tm
        self.distance = distance
        self.start_tm = start_tm
        self.back_tm = back_tm
        self.charge_cost = charge_cost
    def calc_path_info(self, distance_matrix, time_matrix, vehicle_info):
        pass