# 生成一个个体并且可视化所有路径
# 当可视化所有路径时，去往第一个点和从最后一个点返回的线没有被画

import load_data as ldd
import algorithm.init as ai
import random
from visualize.v import plot_pathes

#random.seed(time.time())
random.seed(0)

warehouse, orders, charging, id_type_map = ldd.load_node_info("../data/input_node.csv")

id_sorted_orders = sorted(orders, key = lambda x: x.id)
angle_sorted_orders = sorted(orders, key = lambda x: x.polar_angle)

vehicles = ldd.load_vehicle_info('../data/input_vehicle_type.csv')
distance_matrix, time_matrix = ldd.load_distance_time_info('../data/input_distance-time.csv')

for o in orders:
    o.set_charging(charging, distance_matrix)

print("generating initial population")

individual = ai.better_init_individual(warehouse, id_sorted_orders, charging, vehicles, id_type_map, distance_matrix, time_matrix)

print("ploting")

pathes = []
for i in individual:
    pathes.append(i.path)

plot_pathes(warehouse, orders, charging, pathes, id_type_map)