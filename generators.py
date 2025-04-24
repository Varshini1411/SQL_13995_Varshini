import time  #for Measuring Execution Time
import tracemalloc #for Memory Usage

# Generator function
def generator_example(n):
    for i in range(n):
        yield i ** 2

# List comprehension
def list_example(n):
    return [i ** 2 for i in range(n)]

# Benchmarking
N = 10_000_000

# Measure generator execution time
start = time.time()
gen = generator_example(N)
for _ in gen:
    pass
gen_time = time.time() - start

# Measure generator memory usage
tracemalloc.start()
gen = generator_example(N)
for _ in gen:
    pass
gen_memory = tracemalloc.get_traced_memory()[1]
tracemalloc.stop()

# Measure list execution time
start = time.time()
lst = list_example(N)
for _ in lst:
    pass
list_time = time.time() - start

# Measure list memory usage
tracemalloc.start()
lst = list_example(N)
list_memory = tracemalloc.get_traced_memory()[1]
tracemalloc.stop()

print(f"Generator time: {gen_time:.4f} seconds")
print(f"List time: {list_time:.4f} seconds")

print(f"Generator peak memory: {gen_memory / (1024 * 1024):.2f} MB")
print(f"List peak memory: {list_memory / (1024 * 1024):.2f} MB")