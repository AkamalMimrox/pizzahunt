import random
import string

def generate_random_slug(title):
    # Generate a random slug based on the product title
    title_slug = ''.join(random.choice(
        string.ascii_lowercase + string.digits) for _ in range(6))
    return f"{title_slug}{title.replace(' ', '-')}"
