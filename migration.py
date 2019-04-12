import sys
import random
from collections import deque

if sys.version_info[0] > 2:
    xrange = range

INTERVAL_BLOCKS = 500
LATENCY_BLOCKS = 10
DUST_ZATOSHI = 1000000
(MIN_EXPONENT, MAX_EXPONENT) = (6, 9)
(MIN_MANTISSA, MAX_MANTISSA) = (1, 99)
TXNS_PER_BATCH = 5

ZEC = 100000000


def div_ceil(x, y):
    return (x+y-1)//y

def amount_to_send(unmigrated_amount):
    while True:
        exponent = random.randint(MIN_EXPONENT, MAX_EXPONENT)
        amount = 10**exponent * random.randint(MIN_MANTISSA, MAX_MANTISSA)
        if amount <= unmigrated_amount:
            return amount

def simulate(unmigrated_amount):
    amounts = deque()
    while unmigrated_amount > DUST_ZATOSHI:
        amount = amount_to_send(unmigrated_amount)
        amounts.append(amount)
        unmigrated_amount -= amount

    #print(list(amounts))
    #print(len(amounts))
    return amounts

def table(total_amount):
    times = deque()
    n = 100000
    for i in xrange(n):
        amounts = simulate(total_amount)
        latency = random.randint(LATENCY_BLOCKS, LATENCY_BLOCKS+INTERVAL_BLOCKS)
        times.append((div_ceil(len(amounts), TXNS_PER_BATCH)*INTERVAL_BLOCKS + latency)/576.0)

    times = list(times)
    times.sort()
    print("%5.2f %5.2f %5.2f" % (times[n//10], times[n//2], times[n*9//10]))

table(1*ZEC)
table(10*ZEC)
table(100*ZEC)
table(1000*ZEC)
table(10000*ZEC)
