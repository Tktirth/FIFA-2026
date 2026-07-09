import functools
from cachetools import TTLCache
from typing import Callable, Any

def async_cache(maxsize: int = 128, ttl: int = 300):
    """
    Simple decorator to cache async function results with TTL (in seconds).
    Uses cachetools TTLCache.
    """
    cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Create a cache key from args and kwargs
            key = str(args) + str(kwargs)
            
            if key in cache:
                return cache[key]
                
            result = await func(*args, **kwargs)
            cache[key] = result
            return result
        return wrapper
    return decorator
