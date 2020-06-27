import random
from time import time


def user_profile(instance, filename):
    return "profile/%s_%s" % (str(time()).replace('.', '_'), filename)


def code():
    return "".join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
