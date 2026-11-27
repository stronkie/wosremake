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

def story_code(b):
    """the check code of the story (script.s story_code)"""
    d = 0x5354524B
    for x in b[:36]:
        d = ((d << 5) | (d >> 27)) & 0xffffffff
        d ^= x
        d = (d + 0x9E3779B9) & 0xffffffff
    return d


data = b'WSTY' + bytes(bits)
open(sys.argv[1], 'wb').write(data + story_code(data).to_bytes(4, 'big'))
