import copy

a = [1]
b = copy.deepcopy(a)
b.append(2)
print(a)
print(b)