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

n = int(input())

primes = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,  947, 953, 967, 971, 977, 983, 991, 997 ]

alpha = [ 0 ]

n_uniq_primes = 0

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
    p2 = factor(n)
    p2.sort()
    p2.append(0)
    k = 1
    for d in range(0, len(p2) - 1):
        if p2[d] == p2[d + 1]: k += 1
        else:
            if k == 1: n_uniq_primes += 1
            else: alpha.append(k)
            k = 1

l = len(alpha)
salpha = sum(alpha)
alpha[0] = salpha
alpha.sort(reverse = True)

def e_opt(n):
    d = math.sqrt(1 + 8 * n) - 1
    return math.floor(d * 0.5)

best = n_uniq_primes + sum(e_opt(alpha[i]) for i in range(1, l))
if l <= 2:
    print(best)
    exit(0)

f = []
for i in range(1, l):
    s = [0] * l
    s[0] = 1
    s[i] = 1
    f.append(tuple(s))

factors = { 1: set(f) }
smax = salpha - best + 1

for ssum in range(2, smax + 1):
    f = []
    for g in factors[ssum - 1]:
        for i in range(1, l):
            if g[i] + 1 > alpha[i]: continue
            h = list(g)
            h[i] += 1
            h[0] = ssum
            f.append(tuple(h))
    factors[ssum] = set(f)

list_factors = []
for ssum in range(1, smax + 1):
    list_factors += list(factors[ssum])

def a_minus(a, b):
    global l

    r = [0] * l
    for i in range(l):
        c = a[i] - b[i]
        if c < 0: return None
        r[i] = c
    return r

# 4 debug calls to comment
debug_stack = []
#print(alpha)

def optimize(alpha, sindex, nf):
    global best, l, list_factors, debug_stack
    print('optimize', alpha, sindex, nf, debug_stack)

    f = list_factors[sindex]

    salpha = alpha[0]
    if salpha < f[0] * max(1, best + 1 - nf):
        #print('cut')
        return 

    if salpha == f[0]:
        t = tuple(alpha)

        for i in range(sindex, len(list_factors)):
            f = list_factors[i]
            if salpha < f[0]: return

            if t == f:
                r = 1 + nf
                if best < r: best = r
                print('best', best, debug_stack)
                return
        return

    sindex1 = sindex + 1
    if sindex1 == len(list_factors): return
    alpha1 = a_minus(alpha, f)
   
    s = list(debug_stack)
    debug_stack.append(f)
    if not alpha1 is None: optimize(alpha1, sindex1, nf + 1)

    debug_stack = s
    optimize(alpha, sindex1, nf)
    return

sys.setrecursionlimit(len(list_factors) * 2 + 20)
optimize(alpha, 0, n_uniq_primes)
print(best)



