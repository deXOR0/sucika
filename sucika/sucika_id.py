import random

def generate_id(name):
    name = name.lower()
    numeric = sum(list(map(ord, list(name)))) * random.randint(0, ord(name[0])) + ord(name[-1])
    return '{}{}'.format(name.split(' ')[0], hex(numeric).lstrip('0x'))