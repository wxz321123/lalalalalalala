import load_data as ldd
import copy

warehouse, orders, charging, id_type_map = ldd.load_node_info("data/input_node.csv")
vehicles = ldd.load_vehicle_info('data/input_vehicle_type.csv')
distance_matrix, time_matrix = ldd.load_distance_time_info('data/input_distance-time.csv')
idx=0
for o in orders:
    print(idx)
    o.set_charging(charging, distance_matrix)
    #o.set_distance_sorted_order(copy.deepcopy(orders), distance_matrix)
    idx+=1


print("done")