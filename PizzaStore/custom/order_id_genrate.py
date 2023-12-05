import random
import string


def genrate_orderId():
    return ''.join(random.choice(
        string.digits + string.digits) for _ in range(6))
