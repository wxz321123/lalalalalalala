# 可视化一个给定的路径

from visualize.v import plot_one_path
import load_data as ldd

warehouse, orders, charging, id_type_map = ldd.load_node_info("../data/input_node.csv")

plot_one_path(warehouse, orders, charging, [196,448,131,1070,598,811,322,928], id_type_map)