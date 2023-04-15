import random
from string import ascii_lowercase


def generate_mail():
    return "".join(random.choice(ascii_lowercase) for i in range(random.randint(7, 15)))
