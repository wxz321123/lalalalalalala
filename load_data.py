import pandas as pd
from entity.Order import Order
from entity.Vehicle import Vehicle
from openpyxl import load_workbook
import os

def load_node_info(path):
    print('loading node information')

    df = pd.read_csv(path)
    warehouse = None
    orders = []
    charging = []

    for idx in df.index:
        row = df.loc[idx]
        order = Order(id=row['ID'], type=row['type'], lng=row['lng'], lat=row['lat'],
                      weight=row['pack_total_weight'], volume=row['pack_total_volume'], fst_time=row['first_receive_tm'],
                      lst_time=row['last_receive_tm'])
        if (order.type == 1):
            warehouse = order
        elif (order.type == 2):
            orders.append(order)
        elif (order.type == 3):
            charging.append(order)

    for o in orders:
        o.set_polar(warehouse.lng, warehouse.lat)

    for c in charging:
        c.set_polar(warehouse.lng, warehouse.lat)

    id_type_map = {}

    id_type_map[warehouse.id] = warehouse.type

    for o in orders:
        id_type_map[o.id] = o.type

    for c in charging:
        id_type_map[c.id] = c.type

    return warehouse, orders, charging, id_type_map

def load_vehicle_info(path):
    print("loading vehicle information")
    vehicles = []
    vdf = pd.read_csv(path)
    for idx in vdf.index:
        row = vdf.loc[idx]
        v = Vehicle(id=row['vehicle_type_ID'], name=row['vehicle_type_name'], weight=row['max_weight'], volume=row['max_volume'],
                    driving_range=row['driving_range'], charge_time=row['charge_tm'], unit_cost=row['unit_trans_cost'], day_cost=row['vehicle_cost'])
        vehicles.append(v)
    return vehicles

def load_distance_time_info(path):
    print("loading distance and time matrix")

    df = pd.read_csv(path)

    num_node = len(set(df['from_node'].tolist()))

    dist_matrix = [[-1 for col in range(num_node)] for row in range(num_node)]
    time_matrix = [[-1 for col in range(num_node)] for row in range(num_node)]

    dist_series = df['distance'].tolist()
    time_series = df['spend_tm'].tolist()

    for i in range(num_node):
        if (i % 100 == 0):
            print(str(float(i) / float(num_node) * 100) + '%')
        base = 1100 * i
        for j in range(num_node):
            if (i == j):
                dist_matrix[i][j] = 0
                time_matrix[i][j] = 0
            elif (i > j):
                dist_matrix[i][j] = dist_series[base + j]
                time_matrix[i][j] = time_series[base + j]
            elif (i < j):
                dist_matrix[i][j] = dist_series[base + j - 1]
                time_matrix[i][j] = time_series[base + j - 1]

    return dist_matrix, time_matrix
# 将解以EXCEL的形式输出
def excelAddSheet(dataframe, outfile, name):
    writer = pd.ExcelWriter(outfile, engine='openpyxl')
    if os.path.exists(outfile) != True:
        dataframe.to_excel(writer, name, index=None)
    else:
        book = load_workbook(writer.path)
        writer.book = book
        dataframe.to_excel(excel_writer=writer, sheet_name = name, index=None)
    writer.save()
    writer.close()