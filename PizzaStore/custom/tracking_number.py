import random
import string


def generate_tracking_number():
    # Generate a random tracking number with a combination of letters and digits
    tracking_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return tracking_number