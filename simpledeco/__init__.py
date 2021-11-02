from collections.abc import Callable
from typing import Any, TypeVar, ParamSpec
from functools import wraps
from .utils import _FunctionArguments, Wrapped, empty_hook


Hook = Callable[[Wrapped, Callable], Any]
OriginalParams = ParamSpec('OriginalParams')
OriginalReturn = TypeVar('OriginalReturn')


class SimpleDeco:
    _original_func: Callable[OriginalParams, OriginalReturn]
    _after_wrapping_func: Hook
    _before_decorating_func: Hook

    def __init__(self, func: Callable[OriginalParams, OriginalReturn]):
        self._original_func = func
        self._after_wrapping_func = empty_hook
        self._before_decorating_func = empty_hook

    def __call__(self, *args: OriginalParams.args, **kwargs: OriginalParams.kwargs) -> OriginalReturn:
        self_wrapped = Wrapped(self._original_func, (None,) + args, kwargs)

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*func_args, **func_kwargs):
                wrapped = Wrapped(func, func_args, func_kwargs)
                return self._original_func(wrapped, *args, **kwargs)

            self._after_wrapping_func(self_wrapped, wrapper)
            return wrapper

        self._before_decorating_func(self_wrapped, decorator)
        return decorator

    def after_wrapping(self, func: Hook) -> Hook:
        self._after_wrapping_func = func
        return func

    def before_decorating(self, func: Hook) -> Hook:
        self._before_decorating_func = func
        return func
