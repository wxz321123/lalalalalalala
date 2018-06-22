import random

def random_member(list):
    idx = random.randint(0, len(list) - 1)
    return list[idx]