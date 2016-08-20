#!/usr/bin/env python

import sys

f = open('matrix_adf1a8f010f541cb171910f7afe1f86d41ce1669c51e318bb84c3c2e4397e2f4.txt', 'r')
numbers = f.read().split()
f.close()

#print numbers
numbers = map(lambda s: int(s, 16), numbers)
#print len(numbers)

matrix = [[]] * len(numbers)
#print matrix

print
print
print
print
print
i = 0
j = 0
for num in numbers :
    matrix[i] = [' '] * 32
    mask = 0x80000000
    j = 0
    while mask != 0x00000001 :
        if (num & mask) == mask :
            matrix[i][j] = u'\u2588\u2588'
#            sys.stdout.write(u'\u2584\u2584')
        else :
            matrix[i][j] = u'\u2591\u2591'
#            sys.stdout.write('  ')
        mask >>= 1
        j += 1

    i += 1
#    print

for line in matrix :
    print "                ", ''.join(line)

print
print
print
print
print
print

'''
matrix = [[]] * len(numbers)
i = 0
j = 0
for num in numbers :
    matrix[i] = [' '] * 32
    mask = 0x00000001
    j = 0
    while mask != 0x80000000 :
        if (num & mask) == mask :
            matrix[i][j] = u'\u2588\u2588'
#            sys.stdout.write(u'\u2584\u2584')
        else :
            matrix[i][j] = u'\u2591\u2591'
#            sys.stdout.write('  ')
        mask <<= 1
        j += 1

    i += 1
#    print

for line in matrix :
    print "                ", ''.join(line)

print
print
print
print
'''
