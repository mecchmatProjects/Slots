import time


def benchmark(func):
    """функція декоратор, яка використовується для обрахунку часу роботи функції func

    Args:
      func: функція, яка декорується

    Returns:
      функція _benchmark

    """
    def _benchmark(*args, **kwargs):
        t0 = time.time()
        res = func(*args, **kwargs)
        print(f"{func.__name__} elapsed {time.time() - t0} secs")
        return res
    return _benchmark
