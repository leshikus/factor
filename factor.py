#!/usr/bin/python3

import random, fractions, math, sys
import threading

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

def factor(n, pd):
    global timeout

    for i in range(5):
        d = brent(n)
        if d > 1 and d < n:
            factor(n // d, pd)
            factor(d, pd)
            return

        if timeout: break

    if n in pd: pd[n] += 1
    else: pd[n] = 1

def factor_input():
    global alpha, n_uniq_primes
    n = int(input())

    primes = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
	67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139,
	149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227,
	229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311,
	313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401,
	409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
	499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599,
	601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683,
	691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
	809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887,
	907, 911, 919, 929, 937, 941,  947, 953, 967, 971, 977, 983, 991, 997 ]

    alpha = []
    n_uniq_primes = 0

    for d in primes:
        if n % d == 0:
            n //= d

            if n % d != 0:
                n_uniq_primes += 1
                if n == 1: break
                continue

            n //= d
            k = 2
            while n % d == 0:
                n //= d
                k += 1
            alpha.append(k)
            if n == 1: break

    if n > 1:
        pd = {}
        factor(n, pd)
        for k in pd.values():
            if k == 1: n_uniq_primes += 1
            else: alpha.append(k)

    alpha.sort(reverse = True)
    return tuple(alpha)

def e_opt(n):
    d = math.sqrt(1 + 8 * n) - 1
    return math.floor(d * 0.5)

def get_list_factors_set(ssum):
    global alpha, list_factors, list_factors_set
    global debug_stack
    if ssum < len(list_factors): return list_factors_set[ssum]

    ssum1 = len(list_factors) - 1
    while ssum1 < ssum:
        ff = []
        for fg in list_factors[ssum1]:
            for fi in range(l):
                if fg[fi] + 1 > alpha[fi]: continue
                fh = list(fg)
                fh[fi] += 1
                ff.append(tuple(fh))

        fs = set(ff)
        list_factors_set.append(fs)
        list_factors.append(list(fs))
        ssum1 += 1

    if not debug_stack is None:
        print('new factors', ssum1, list_factors, len(list_factors[ssum1]))

    return fs

def a_minus(a, b):
    global l

    r = [0] * l
    for i in range(l):
        c = a[i] - b[i]
        if c < 0: return None
        r[i] = c
    return tuple(r)

def optimize(cur, scur, sindex, ssum, nf):
    global alpha, best, l, list_factors
    global debug_stack, best_stack, dict_opts, timeout

    if timeout: return -1

    if (cur, sindex, ssum) in bestd:
        dict_opts += 1
        return bestd[cur, sindex, ssum]

    if not debug_stack is None:
        print('optimize', cur, scur, sindex, ssum, nf)
        print('stack', len(debug_stack), debug_stack)

    if scur < ssum: return 0

    lf = list_factors[ssum]
    if scur == ssum:
        for ti in range(sindex, len(lf)):
            tf = lf[ti]

            if cur == tf:
                r = nf + 1
                if best < r:
                    best = r
                    if not debug_stack is None:
                        print('best', len(debug_stack), debug_stack.append(cur))
                        best_stack = list(debug_stack)
                return 1
        return 0

    if scur < ssum * 2:
        lf = get_list_factors_set(scur)
        if cur in lf:
            r = nf + 1
            if best < r:
                best = r
                if not debug_stack is None:
                    print('best', len(debug_stack), debug_stack.append(cur))
                    best_stack = list(debug_stack)
            return 1
        return 0

    if scur < ssum * (best + 1 - nf):
        #print('cut')
        return -1

    f = lf[sindex]
    sindex1 = sindex + 1
    ssum1 = ssum

    if sindex1 == len(lf):
        sindex1 = 0
        ssum1 = ssum + 1
        get_list_factors_set(ssum1)

    cur1 = a_minus(cur, f)

    bestl = 0
    if not cur1 is None:
        if not debug_stack is None:
            s = list(debug_stack)
            debug_stack.append(f)
        bestl = optimize(cur1, scur - ssum, sindex1, ssum1, nf + 1) + 1
        if not debug_stack is None: debug_stack = s

    bestr = optimize(cur, scur, sindex1, ssum1, nf)
    if bestl == -1 or bestr == -1: return -1

    bestc = max(bestl, bestr)
    bestd[cur, sindex, ssum] = bestc
    return bestc

def cancel_run():
    global timeout
    timeout = True

timeout = False
wd = threading.Timer(1.7, cancel_run, ())
wd.start()

alpha = factor_input()
l = len(alpha)
salpha = sum(alpha)

best = sum(e_opt(alpha[i]) for i in range(l))

if l <= 1:
    print(n_uniq_primes + best)
    wd.cancel()
    exit(0)

f = []
for i in range(l):
    s = [0] * l
    s[i] = 1
    f.append(tuple(s))

list_factors = [0, f]
list_factors_set = [0, set(f)]
sys.setrecursionlimit(20000)

debug_stack = []
debug_stack = None # comment this to debug
best_stack = []

#print(alpha, salpha)

bestd = {}
dict_opts = 0

r = optimize(alpha, salpha, 0, 1, 0)
if not debug_stack is None:
    print('best', best, best_stack)
    print('dict', len(bestd), dict_opts)

wd.cancel()
print(n_uniq_primes + (r if r != -1 else best))



