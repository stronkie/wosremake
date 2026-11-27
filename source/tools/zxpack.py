"""V1.7 cruncher: a bit-oriented LZ packer with an optimal parse (in the spirit of ZX0).
About 20% smaller than the old byte-oriented lzpack.

Stream: bits (MSB first, fetched a byte at a time when needed) mixed with whole bytes.
  0 <byte>                         literal
  1 gamma(hi+1) <lo> gamma(len-1)  match: offset = hi*256 + lo + 1, length 2..255
  1 gamma(128)                     end of stream
gamma(v), v >= 1: 'interlaced' Elias gamma. For every bit of v after the leading 1:
a 0 then that bit; then a 1. So 1 -> '1', 2 -> '0 0 1', 3 -> '0 1 1', 4 -> '0 0 0 0 1' ...
"""
END_HI = 128
MAX_OFF = 126 * 256 + 256      # hi <= 126
MAX_LEN = 255


def gbits(v):
    return 2 * v.bit_length() - 1


def match_cost(off, ln):
    return 1 + gbits((off - 1) // 256 + 1) + 8 + gbits(ln - 1)


def parse(data, chain=64):
    """Optimal parse (shortest bit cost) -> list of ('L', byte) / ('M', off, len)."""
    n = len(data)
    INF = 1 << 60
    cost = [INF] * (n + 1)
    nxt = [None] * (n + 1)
    cost[n] = 0
    heads = {}
    cands = [()] * n
    for i in range(n - 1):
        lst = heads.setdefault(data[i:i + 2], [])
        cands[i] = lst[-chain:][::-1]
        lst.append(i)
    for i in range(n - 1, -1, -1):
        best = cost[i + 1] + 9
        bn = ('L',)
        maxl = 1
        for c in cands[i]:
            off = i - c
            if off > MAX_OFF:
                break
            ln = 0
            lim = min(MAX_LEN, n - i)
            while ln < lim and data[c + ln] == data[i + ln]:
                ln += 1
            if ln > maxl:
                base = 1 + gbits((off - 1) // 256 + 1) + 8
                for L in range(maxl + 1, ln + 1):
                    v = cost[i + L] + base + gbits(L - 1)
                    if v < best:
                        best, bn = v, ('M', off, L)
                maxl = ln
                if ln == lim:
                    break
        cost[i] = best
        nxt[i] = bn
    out = []
    i = 0
    while i < n:
        t = nxt[i]
        if t[0] == 'L':
            out.append(('L', data[i]))
            i += 1
        else:
            out.append(t)
            i += t[2]
    return out


class BitWriter:
    def __init__(self):
        self.out = bytearray()
        self.bitpos = None
        self.nbits = 8

    def bit(self, b):
        if self.nbits == 8:
            self.bitpos = len(self.out)
            self.out.append(0)
            self.nbits = 0
        if b:
            self.out[self.bitpos] |= 0x80 >> self.nbits
        self.nbits += 1

    def gamma(self, v):
        bits = bin(v)[3:]
        for b in bits:
            self.bit(0)
            self.bit(int(b))
        self.bit(1)

    def byte(self, b):
        self.out.append(b)


def pack(data):
    w = BitWriter()
    for t in parse(bytes(data)):
        if t[0] == 'L':
            w.bit(0)
            w.byte(t[1])
        else:
            _, off, ln = t
            w.bit(1)
            w.gamma((off - 1) // 256 + 1)
            w.byte((off - 1) & 0xFF)
            w.gamma(ln - 1)
    w.bit(1)
    w.gamma(END_HI)
    return bytes(w.out)


def unpack(stream, trace=None):
    """Mirror of the 6502 decoder; trace gets (bytes written, bytes read) after every token."""
    st = {'i': 0, 'buf': 0x80}
    out = bytearray()

    def rbyte():
        b = stream[st['i']]
        st['i'] += 1
        return b

    def bit():
        st['buf'] = (st['buf'] << 1) & 0x1FF
        c = st['buf'] >> 8
        st['buf'] &= 0xFF
        if st['buf'] == 0:
            b = rbyte()
            c = b >> 7
            st['buf'] = ((b << 1) | 1) & 0xFF
        return c

    def gamma():
        v = 1
        while not bit():
            v = ((v << 1) | bit()) & 0xFF
        return v

    while True:
        if not bit():
            out.append(rbyte())
        else:
            hi = gamma()
            if hi == END_HI:
                return bytes(out)
            off = (hi - 1) * 256 + rbyte() + 1
            ln = gamma() + 1
            for _ in range(ln):
                out.append(out[-off])
        if trace is not None:
            trace.append((len(out), st['i']))


def packed_file(data, dest=0x4000, top=0xC400):
    """C64 file with the stream placed so it can be unpacked in place to `dest`.
    The last two bytes hold the stream's start address."""
    stream = pack(data)
    trace = []
    assert unpack(stream, trace) == bytes(data)
    worst = max(o - inp for o, inp in trace) if trace else 0
    size = len(stream) + 2
    start = dest + max(worst, 0) + 4                      # 4 bytes of safety
    start = max(start, dest + len(data) + 4 - size)
    end = start + size
    assert end <= top, f'packed data reaches ${end:04X}'
    body = stream + bytes([start & 0xFF, start >> 8])
    return bytes([start & 0xFF, start >> 8]) + body, start
