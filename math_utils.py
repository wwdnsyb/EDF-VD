def gcd(a, b):
    """
    计算两个数的最大公约数，使用欧几里得算法。
    """
    while b > 0:
        temp = b
        b = a % b
        a = temp
    return a


def gcd_list(input_list):
    """
    计算输入列表中所有数字的最大公约数。
    """
    result = input_list[0]
    for num in input_list[1:]:
        result = gcd(result, num)
    return result


def lcm(a, b):
    """
    计算两个数的最小公倍数。
    """
    return a * (b // gcd(a, b))


def lcm_list(periods):
    """
    计算输入周期列表中所有周期的最小公倍数。
    """
    result = periods[0]
    for num in periods[1:]:
        result = lcm(result, num)
    return result
