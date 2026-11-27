#!/usr/bin/env python3
"""Writes a story file (WOS2.STn) like the game does: storyfile.py out 'flag,flag|item,item'"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import story
f, i = sys.argv[2].split('|')
bits = bytearray(32)
for n in filter(None, f.split(',')):
    k = story.FLAGS.index(n)
    bits[k >> 3] |= 1 << (k & 7)
for n in filter(None, i.split(',')):
    k = story.ITEMS.index(n)
    bits[16 + (k >> 3)] |= 1 << (k & 7)
open(sys.argv[1], 'wb').write(b'WSTY' + bytes(bits))
