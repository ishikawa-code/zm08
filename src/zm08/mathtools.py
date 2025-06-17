def gcd(m, n):
    """最大公約数 http://bit.ly/3ZIFTuM"""
    
    if m < n:
        # m >= n となるように入れ替え
        m, n = n, m

    while n != 0:
        m, n = n, m % n

    return m


def lcm(m, n):
    """最小公倍数"""
    return m * n // gcd(m, n)


def divisors(x):
    divs = []

    i = 1
    while i <= x:
        if x % i == 0:
            divs.append(i)
        i += 1
        
    return divs


def is_prime(x):
    """素数判定"""
    if x == 1:
        return False
    
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i += 1
        
    return True

