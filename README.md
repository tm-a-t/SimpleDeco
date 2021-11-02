# SimpleDeco
### Decorators without nested functions

SimpleDeco is a way to create decorators with arguments and not to think about higher-order functions.

Instead, of nested functions, with SimpleDeco you split the decorator definitions into one or more plain functions.

## Basic example

Let's create a `count_time(iterations)` decorator, which runs the given function the given number of iterations and counts the average time.

```python
from time import time
from simpledeco import SimpleDeco, Wrapped


@SimpleDeco
def count_time(wrapped: Wrapped, iterations: int):
    t1 = time()
    
    for _ in range(iterations):
        # run the wrapped func with given arguments
        wrapped.func(*wrapped.args, **wrapped.kwargs)
    
    t2 = time()
    print('time:', (t2 - t1) / iterations)


@count_time(1000)
def f(x, y):
    return sum(range(x, y))


# Counts the sum of numbers from 1 to 50000 for 1000 times
# and prints the average time
f(1, 50000)
```

**Without SimpleDeco**, the `count_time` function would be similar to this:

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

Pretty more complex.

## Wrapped object

SimpleDeco objects (like `count_time` above) are callable objects, which return decorators.

When using a SimpleDeco object with arguments as a decorator, the `Wrapped` instance and given arguments
are passed.

`Wrapped` object has simple attributes:

- `wrapped.func` - the given function
- `wrapped.args` - a tuple of all positional arguments passed to a function
- `wrapped.kwargs` - a dict of all keyword arguments passed to a function
- `wrapped.arguments` - an object with all passed arguments

Thus, you can use `wrapped.func(*wrapped.args, **wrapped.kwargs)` to call the original function with original arguments.

If you need to use specific arguments, use `wrapped.arguments` attributes. For example, if you need to decorate only functions with `x` and `y` arguments:

```python
@SimpleDeco
def count_time(wrapped: Wrapped, iterations: int):
    t1 = time()
    
    for _ in range(iterations):
        wrapped.func(wrapped.arguments.x, wrapped.arguments.y)
    
    t2 = time()
    print('x:', wrapped.arguments.x, 'y:', wrapped.arguments.y)
    print('time:', (t2 - t1) / iterations)
```

## Hooks

Sometimes you need to do something after wrapping a function or before decorating it.
There are special SimpleDeco methods for that.

- `simpledeco.after_wrapping` decorates a function that takes wrapped SimpleDeco and wrapper as arguments
- `simpledeco.after_wrapping` decorates a function that takes wrapped SimpleDeco and decorator as arguments

For example:

```python
from time import time
from simpledeco import SimpleDeco


@SimpleDeco
def count_time(wrapped, iterations):
    t1 = time()
    
    for _ in range(iterations):
        # run the wrapped func with given arguments
        wrapped.func(*wrapped.args, **wrapped.kwargs)
    
    t2 = time()
    print('time:', (t2 - t1) / iterations)


@count_time.after_wrapping
def after_wrapping(count_time_wrapped, wrapper):
    print('Running function for', count_time_wrapped.arguments.iterations, 'times')
    print('With arguments (1, 50000)')
    wrapper(1, 50000)

    
@count_time.before_decorating
def before_decorating(count_time_wrapped, decorator):
    print('Generated decorator with argument:', count_time_wrapped.arguments.iterations)
    # 'decorator' is the generated decorator

    
@count_time(1000)
def f(x, y):
    return sum(range(x, y))
```
The output:
```
Generated decorator with argument: 1000
Running function for 1000 times
With arguments (1, 50000)
time: 0.0022199389934539795
```

**Without SimpleDeco**, the code above could be rewritten as follows:

```python
from time import time


def count_time(iterations: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            t1 = time()
            for _ in range(iterations):
                func(*args, **kwargs)
            t2 = time()
            print('time:', (t2 - t1) / iterations)
        print('Running function for', iterations, 'times')
        print('With arguments (1, 50000)')
        wrapper(1, 50000)
        return wrapper
    print('Generated decorator with argument:', iterations)
    return decorator


@count_time(1000)
def f(x, y):
    return sum(range(x, y))
```

## License

This project is licensed under the terms of the MIT license.
