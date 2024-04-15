import random

# create a function that returns a string of 6 hexadecimal random characters
def generate_id():
    return ''.join(random.choice('0123456789ABCDEF') for i in range(6))

BufferData = str