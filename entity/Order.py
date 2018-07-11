import math

class Order(object):

    def __init__(self, id, type, lng, lat, weight, volume,
                 fst_time, lst_time):
        self.id = id
        self.type = type
        # x axis
        self.lng = lng
        # y axis
        self.lat = lat
        if (weight == '-'):
            self.weight = -1
        else:
            self.weight = float(weight)
        if (volume == '-'):
            self.volume = -1
        else:
            self.volume = float(volume)
        self.fst_time = fst_time
        self.lst_time = lst_time

    def set_polar(self, origin_x, origin_y):
        arctan = math.atan(float(self.lng - origin_x) / float(self.lat - origin_y))
        if (self.lng - origin_x > 0 and self.lat - origin_y > 0):
            self.polar_angle = arctan
        elif (self.lng - origin_x < 0 and self.lat - origin_y < 0):
            self.polar_angle = arctan + math.pi
        elif (self.lng - origin_x > 0 and self.lat - origin_y < 0):
            self.polar_angle = math.pi + arctan
        elif (self.lng - origin_x < 0 and self.lat - origin_y > 0):
            self.polar_angle = arctan + math.pi * 2
        self.polar_dist = math.sqrt(math.pow((self.lng - origin_x), 2) + math.pow((self.lat - origin_y), 2))

    def set_charging(self, charging, distance_matrix):
        if (self.type != 2):
            return
        else:
            min_idx = -1
            min_dist = 0
            for i in range(len(charging)):
                if (min_idx == -1 or distance_matrix[self.id][charging[i].id] < min_dist):
                    min_idx = charging[i].id
                    min_dist = distance_matrix[self.id][charging[i].id]
            self.charging_binding = min_idx
            self.charging_dist = min_dist

    def set_distance_sorted_order(self, orders, distance_matrix):
        sorted_orders = sorted(orders, key=lambda x: distance_matrix[self.id][x.id])
        self.distance_sorted_orders = sorted_orders