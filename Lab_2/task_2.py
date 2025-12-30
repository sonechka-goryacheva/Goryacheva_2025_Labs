import random

def gen_random(num_count, begin, end):
    return [random.randint(begin, end) for i in range(num_count)]

if __name__ == "__main__":
    print(gen_random(5, 2, 10))