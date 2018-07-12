import matplotlib.pyplot as plt
from utils import search_node

def plot_one_path(warehouse, orders, charging, path, id_type_map):
    order_x_coor = []
    order_y_coor = []
    charging_x_coor = []
    charging_y_coor = []

    for o in orders:
        order_x_coor.append(o.lng)
        order_y_coor.append(o.lat)
    for c in charging:
        charging_x_coor.append(c.lng)
        charging_y_coor.append(c.lat)

    plt.scatter([warehouse.lng], [warehouse.lat], s=5, c='r')
    plt.scatter(order_x_coor, order_y_coor, s=5, c='b')
    plt.scatter(charging_x_coor, charging_y_coor, s=5, c='lime')

    path_x = [warehouse.lng]
    path_y = [warehouse.lat]

    for nid in path:
        node = None
        if (id_type_map[nid] == 2):
            node = search_node(orders, nid)
        elif (id_type_map[nid] == 3):
            node = search_node(charging, nid)
        else:
            raise Exception
        path_x.append(node.lng)
        path_y.append(node.lat)

    path_x.append(warehouse.lng)
    path_y.append(warehouse.lat)

    plt.plot(path_x, path_y, linewidth=1)


    plt.show()


def plot_pathes(warehouse, orders, charging, pathes, id_type_map):
    order_x_coor = []
    order_y_coor = []
    charging_x_coor = []
    charging_y_coor = []

    for o in orders:
        order_x_coor.append(o.lng)
        order_y_coor.append(o.lat)
    for c in charging:
        charging_x_coor.append(c.lng)
        charging_y_coor.append(c.lat)

    plt.scatter([warehouse.lng], [warehouse.lat], s=5, c='r')
    plt.scatter(order_x_coor, order_y_coor, s=5, c='b')
    plt.scatter(charging_x_coor, charging_y_coor, s=5, c='lime')

    for path in pathes:
        path_x = []
        path_y = []
        for nid in path:
            node = None
            if (id_type_map[nid] == 2):
                node = search_node(orders, nid)
            elif (id_type_map[nid] == 3):
                node = search_node(charging, nid)
            else:
                raise Exception
            path_x.append(node.lng)
            path_y.append(node.lat)

        plt.plot(path_x, path_y, linewidth=1)

    plt.show()

    #<class 'list'>: [770, 137, 196, 872, 377, 326, 152, 556, 1050]