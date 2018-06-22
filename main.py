import load_data as ldd
import copy

warehouse, orders, charging = ldd.load_node_info("data/input_node.csv")
vehicles = ldd.load_vehicle_info('data/input_vehicle_type.csv')
distance_matrix, time_matrix = ldd.load_distance_time_info('data/input_distance-time.csv')
for o in orders:
    o.set_charging(charging, distance_matrix)
    o.set_distance_sorted_order(copy.deepcopy(orders), distance_matrix)



print("done")