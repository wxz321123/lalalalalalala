def group_by_last_time(id_sorted_orders):
    dic = {}
    for o in id_sorted_orders:
        dic.setdefault(o.lst_time, [])
        dic[o.lst_time].append(o)
    return dic