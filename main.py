import load_data as ldd
import copy
import algorithm.init as ai
import random
import time
import pandas as pd

random.seed(time.time())

warehouse, orders, charging, id_type_map = ldd.load_node_info("data/input_node.csv")

id_sorted_orders = sorted(orders, key = lambda x: x.id)
angle_sorted_orders = sorted(orders, key = lambda x: x.polar_angle)

vehicles = ldd.load_vehicle_info('data/input_vehicle_type.csv')
distance_matrix, time_matrix = ldd.load_distance_time_info('data/input_distance-time.csv')

for o in orders:
    o.set_charging(charging, distance_matrix)
    #o.set_distance_sorted_order(copy.deepcopy(orders), distance_matrix)

print("generation initial population")
init_population = []
INIT_POPULATION_SIZE = 10

for i in range(INIT_POPULATION_SIZE):
    init_population.append(ai.random_individual(warehouse, id_sorted_orders, angle_sorted_orders, charging, vehicles, id_type_map, distance_matrix, time_matrix))

    print(init_population[i])
    init_pop_pd = pd.DataFrame(init_population[i])
    init_pop_pd.rename(columns={0:"path", 1:'weight',2:'start_tm',3:'back_tm',4:'distance',5:'trans_cost',6:'wating_tm',7:'wait_cost',8:'charge_cost', 9:'total_cost'}, inplace=True)
    # print(init_pop_pd)
    ldd.excelAddSheet(init_pop_pd,'excel_output.xlsx','sheet'+str(i+1))

print("done")