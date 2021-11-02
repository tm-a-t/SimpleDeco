# SimpleDeco - make decorators not thinking about higher-order functions

Example of usage:

```python
from time import time
from simpledeco import SimpleDeco, Wrapped


@SimpleDeco
def count_time(wrapped: Wrapped, iterations: int):
    t1 = time()
    for _ in range(iterations):
        wrapped.func(*wrapped.args, **wrapped.kwargs)
    t2 = time()
    print('time:', (t2 - t1) / iterations)


@count_time(1000)
def f(x, y):
    return sum(range(x, y))


f(1, 50000)
# Counts the sum of numbers from 1 to 50000 for 1000 times
# and prints the average time
```

The `count_time(iterations)` decorator counts the time of running the given function the given number of iterations.

**Without SimpleDeco**, the `count_time` function could be rewritten this way:

```python
def count_time(iterations: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            t1 = time()
            for _ in range(iterations):
                wrapped.func(*wrapped.args, **wrapped.kwargs)
            t2 = time()
            print('time:', (t2 - t1) / iterations)

        return wrapper
    return decorator
```

