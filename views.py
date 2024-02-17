from functools import reduce

# функции для просчёт процентов take profit & stop loss


def plus_percent(price, percent):
    current_percent = (percent / 100) * price
    result = price + current_percent
    return round(result, 4)


def minus_percent(price, percent):
    current_percent = (percent / 100) * price
    result = price - current_percent
    return round(result, 4)


def get_in_dict(c, key_path, default=None):
    def _getter(c, key):
        if c is default:
            return c
        return c.get(key, default)
    return reduce(_getter, key_path.split('.'), c)
