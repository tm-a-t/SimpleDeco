import inspect
from collections.abc import Callable


class _FunctionArguments:
    def __init__(self, func: Callable, args: tuple, kwargs: dict):
        bind = inspect.signature(func).bind(*args, **kwargs)
        bind.apply_defaults()
        for key, val in bind.arguments.items():
            setattr(self, key, val)


class Wrapped:
    func: Callable
    args: tuple
    kwargs: dict

    def __init__(self, func: Callable, args: tuple, kwargs: dict):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.arguments = _FunctionArguments(func, args, kwargs)


def empty_hook(_: Wrapped, __: Callable) -> None:
    pass
