#!/usr/bin/python3

import random, fractions, math, sys

def brent(n):
    y, c, m = random.randint(1, n - 1), random.randint(1, n - 1), random.randint(1, n - 1)
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for i in range(r):
            y = ((y * y) % n + c) % n
        k = 0
        while (k < r and g == 1):
            ys = y
            for i in range(min(m, r - k)):
                y = ((y * y) % n + c) % n
                q = q * (abs(x - y)) % n
            g = fractions.gcd(q, n)
            k = k + m
        r = r * 2
    if g == n:
        while True:
            ys = ((ys * ys) % n + c) % n
            g = fractions.gcd(abs(x - ys), n)
            if g > 1: break

    return g

def factor(n):
    d = brent(n)
    if d == 1 or d == n: return [n]
    else: return factor(n // d) + factor(d)

def get_alpha(n):
    global n_uniq_primes

    primes = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,  947, 953, 967, 971, 977, 983, 991, 997 ]
    alpha = []

    for d in primes:
        if n % d == 0:
            n //= d

            if n %d != 0:
                n_uniq_primes += 1
                continue

            n //= d
            k = 2
            while n % d == 0:
                n //= d
                k += 1
            alpha.append(k)

    if n > 1:
        f = factor(n)
        f.sort()
        f.append(0)
        k = 1
        for d in range(0, len(p2) - 1):
            if p2[d] == p2[d + 1]: k += 1
            else:
                if k == 1: n_uniq_primes += 1
                else: alpha.append(k)
                k = 1

    alpha.sort(reverse = True)
    return tuple(alpha)

def get_opt(n):
    d = math.sqrt(1 + 8 * n) - 1
    return math.floor(d * 0.5)

def get_best():
    global alpha
    return sum(get_opt(a) for a in alpha)

def get_next_list_factors():
    global alpha, list_factors, L
    global debug

    ssum = len(list_factors) 

    ff = []
    for fg in list_factors[ssum - 1]:
        for fi in range(L):
            if fg[fi] + 1 > alpha[fi]: continue
            fh = list(fg)
            fh[fi] += 1
            ff.append(tuple(fh))

    fs = set(ff)
    list_factors.append(list(fs))

    if debug:
        print('new factors', ssum, list_factors[ssum], len(list_factors[ssum]))

def get_4_list_factors():
    global L, list_factors, sums

    sums = {}
    f = []
    ff = []

    for i in range(L):
        s = [0] * L
        s[i] = 1
        t = tuple(s)
        f.append(t)

        for j in range(i):
            ss = list(s)
            ss[j] = 1
            t = tuple(ss)
            ff.append(t)

        s[i] = 2
        t = tuple(s)
        ff.append(t)

    list_factors = [0, f, ff]
    get_next_list_factors()
    get_next_list_factors()

def is_divisor(t):
    global alpha, L
    for i in range(L):
        if alpha[i] < t[i]: return False
    return True

def set_sums(t, n):
    global sums
    if t in sums and sums[t] > n: return
    if debug: print('sums', t, n)
    sums[t] = n

def enumerate_sums(cur, sindex, ssum, nf):
    global list_factors, L, MAX_SUM
    global debug

    if debug:
        print('enumerate_sums', cur, sindex, ssum, nf)

    lf = list_factors[ssum]
    f = lf[sindex]

    sindex_next = sindex + 1
    ssum_next = ssum

    cur_next = tuple(cur[i] + f[i] for i in range(L))
    if sindex_next == len(lf):
        sindex_next = 0
        ssum_next = ssum + 1
        if ssum_next > MAX_SUM:
            if is_divisor(cur_next): set_sums(cur_next, nf + 1)
            return

    if is_divisor(cur_next):
        set_sums(cur_next, nf + 1)
        enumerate_sums(cur_next, sindex_next, ssum_next, nf + 1)

    enumerate_sums(cur, sindex_next, ssum_next, nf)

def optimize(cur, scur, sindex, ssum, nf):
    global alpha, best, list_factors
    global debug, debug_stack, best_stack

    if debug:
        print('optimize', cur, scur, sindex, ssum, nf)
        print('stack', len(debug_stack), debug_stack)

    if scur in sums:
        r = sums[scur] + nf
        if best < r:
            print('best', len(debug_stack), debug_stack.append(cur))
            best_stack = list(debug_stack)

    if scur < ssum:
        return

    lf = list_factors[ssum]
    if scur == ssum:
        for ti in range(sindex, len(lf)):
            tf = lf[ti]

            if cur == tf:
                r = nf + 1
                if best < r:
                    best = r
                    if debug:
                        print('best', len(debug_stack), debug_stack.append(cur))
                        best_stack = list(debug_stack)
                return
        return

    if scur < ssum * 2:
        r = nf + 1
        if best < r:
            best = r
            if debug:
                print('best', len(debug_stack), debug_stack.append(cur))
                best_stack = list(debug_stack)
        return

    f = lf[sindex]
    sindex_next = sindex + 1
    ssum_next = ssum

    if sindex_next == len(lf):
        sindex_next = 0
        ssum_next = ssum + 1
        if ssum_next == len(list_factors): get_next_list_factors()

    cur_next = tuple(cur[i] - f[i] for i in range(L))
    if min(cur_next) >= 0:
        if debug:
            s = list(debug_stack)
            debug_stack.append(f)
        optimize(cur_next, scur - ssum, sindex_next, ssum_next, nf + 1) 
        if debug: debug_stack = s

    optimize(cur, scur, sindex_next, ssum_next, nf)


n_uniq_primes = 0
alpha = get_alpha(int(input()))
L = len(alpha)

best = get_best()

debug = True
debug_stack = []
best_stack = []
MAX_SUM = 3

if L < 2:
    print(n_uniq_primes + best)
else:
    sys.setrecursionlimit(20000)
    get_4_list_factors()
    enumerate_sums(tuple([0] * L), 0, 1, 0)
    optimize(alpha, sum(alpha), 0, MAX_SUM + 1, 0)
    if debug: print('best', best, best_stack)
    print(n_uniq_primes + best)



