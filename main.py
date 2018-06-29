import load_data as ldd
import copy
import algorithm.init as ai
import random
import time
import xlwt

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
INIT_POPULATION_SIZE = 2

for i in range(INIT_POPULATION_SIZE):
    init_population.append(ai.random_individual(warehouse, id_sorted_orders, angle_sorted_orders, charging, vehicles, id_type_map, distance_matrix, time_matrix))

f = xlwt.Workbook()  # 创建工作簿
for idx in range(INIT_POPULATION_SIZE):
    sheet1 = f.add_sheet(str(idx), cell_overwrite_ok=True)  # 创建sheet
    obj = init_population[idx]
    # tp_feature = ["path", "vehicle_id", "wating_tm", "start_tm", "back_tm", "distance", "charge_cost", "weight"]
    for i in range(len(obj)):
        sheet1.write(i,0, str(obj[i].total_cost))  # 表格的第一行开始写。第一列，第二列。。。。
        # sheet1.write(0,0,start_date,set_style('Times New Roman',220,True))
f.save('text3.xls')  # 保存文件
print("done")