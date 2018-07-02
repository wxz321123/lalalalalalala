import pandas as pd
from openpyxl import load_workbook
import os

def to_dataframe(individual):
    individual_list =[]
    for TransportPath in individual:
        individual_list.append(TransportPath.to_list())
    init_pop_pd = pd.DataFrame(individual_list)
    init_pop_pd.rename(
        columns={0: "trans_code ", 1: "vehicle_type", 2: "dist_seq", 3: 'distribute_lea_tm', 4: 'distribute_arr_tm',
                 5: 'distance', 6: 'trans_cost', 7: 'charge_cost', 8: 'wait_cost', 9: "fixed_use_cost",
                 10: 'total_cost', 11: "charge_cnt", 12: "weight", 13: "volume"}, inplace=True)

    return  init_pop_pd
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