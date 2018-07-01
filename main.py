import load_data as ldd
import copy
import algorithm.init as ai
import random
import pandas as pd

#random.seed(time.time())
random.seed(0)

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

    init_pop_pd = pd.DataFrame(init_population[i])
    init_pop_pd.rename(columns={0:"trans_code ", 1:"vehicle_type",2:"dist_seq",3:'distribute_lea_tm',4:'distribute_arr_tm',5:'distance',6:'trans_cost',7:'charge_cost', 8:'wait_cost',9:"fixed_use_cost",10:'total_cost',11:"charge_cnt",12:"weight", 13:"volume"}, inplace=True)
    ldd.excelAddSheet(init_pop_pd,'excel_output20180701.xlsx','sheet'+str(i+1))

print("done")