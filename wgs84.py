#!/usr/bin/env python3
from sys import stdin, argv
import re

wgs_dec = re.compile(r'-?\d+\.?\d*[\/ ]-?\d+\.?\d*$')
wgs_min = re.compile(r'^[NS] ?\d+[° ] ?\d+\.\d\d\d [EW] ?\d+[° ] ?\d+\.\d\d\d$', re.IGNORECASE)
grad = re.compile(r'\d+\.\d+')
num = re.compile(r'\d+')


def dec_to_min(m):
    lat, lon = 'N', 'E'

    n = float(m.group().split()[0])
    e = float(m.group().split()[1])

    if float(m.group().split()[0]) < 0:
        lat = 'S'
    if float(m.group().split()[1]) < 0:
        lon = 'W'

    return "{} {:02}° {:06.3f} {} {:03}° {:06.3f}" \
        .format(lat, abs(int(n)), 60 * abs(n - int(n)), \
                lon, abs(int(e)), 60 * abs(e - int(e)))


def min_to_dec(m):
    lat, lon = 1, 1

    if m.group().upper().find('N') == -1:
        lat = -1
    if m.group().upper().find('E') == -1:
        lon = -1
    coord = re.split(r'E|W', m.group())

    return '{:.5f}/{:.5f}' \
        .format(lat * convert(coord[0]), lon * convert(coord[1]))


def convert(coordstr):
    a = num.search(coordstr)
    a = int(a.group())
    b = grad.search(coordstr)
    b = float(b.group()) / 60
    return a + b


# Read parameters and else from stdin
if len(argv) > 1:
    inputstr = " ".join(argv[1:]).split('/')
else:
    inputstr = stdin.readline().split('/')

inputstr = " ".join(inputstr).upper()

# Convert one way or the other
str = '\n{} [COORDINATE]\n\tConverts WGS84 coordinate in decimal or minutes ' \
      'into the opposite format.\n\tReads from stdin or parametes.\n\t' \
      '(Works even for complete Openstreetmap URLs.)\n' \
    .format(argv[0])

m = wgs_dec.search(inputstr)
if m:
    str = dec_to_min(m)

m = wgs_min.search(inputstr)
if m:
    str = min_to_dec(m)

print(str)
