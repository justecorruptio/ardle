import struct

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALLOWABLE = 'AEIOUNRLBDCGHPTK'
assert len(ALLOWABLE) <= 16

fh = open('input_data/full.txt', 'r')


PRE = 1
POST = 5 - PRE

BASE = 32
EXTRA = BASE - 26

FULL = [w.upper() for w in fh.read().split()]
FULL_SPLIT = {}
for w in FULL:
    FULL_SPLIT.setdefault(w[:PRE], []).append(w[PRE:])


def letter_diff(a, b):
    x = 0
    while x < POST:
        if a[x] != b[x]:
            pair = a[x] + b[x] if a[x] < b[x] else b[x] + a[x]
            break
        x += 1
    else:
        return None

    x += 1

    while x < POST:
        if a[x] != b[x]:
            return None
        x += 1

    return pair

def do_diff(a, b, replacement):
    ret = ''
    for x in xrange(POST):
        if a[x] == b[x]:
            ret += a[x]
        else:
            ret += replacement

    return ret


def top_diffs(suffix_list):

    diff_count = {}
    for i in xrange(len(suffix_list)):
        a = suffix_list[i]
        for j in xrange(i - 1):
            b = suffix_list[j]
            diff = letter_diff(a, b)
            if not diff:
                continue

            #if diff[0] not in ALLOWABLE or diff[1] not in ALLOWABLE:
            #    continue

            #print a, b, diff
            if diff not in diff_count:
                diff_count[diff] = 1
            else:
                diff_count[diff] += 1

    ret = []
    for i, (diff, count) in enumerate(sorted(diff_count.items(), key=lambda x: -x[1])):
        if i >= EXTRA:
            break
        print diff, count
        ret.append(diff)

    while len(ret) < EXTRA:
        ret.append('AA')

    return ret

def reduce_suffix_list(suffix_list, replacements):
    rep_idx = {r: i for i, r in enumerate(replacements)}
    replaced = {}

    for i in xrange(len(suffix_list)):
        a = suffix_list[i]
        if a in replaced:
            continue
        for j in xrange(i - 1):
            b = suffix_list[j]
            if b in replaced:
                continue

            diff = letter_diff(a, b)
            idx = rep_idx.get(diff)
            if idx is not None:
                suffix = do_diff(a, b, chr(ord('Z') + idx + 1))
                replaced[a] = suffix
                replaced[b] = suffix
                #print a, b, suffix

    ret_set = set()
    for w in suffix_list:
        rep = replaced.get(w)
        if rep is not None:
            ret_set.add(rep)
        else:
            ret_set.add(w)

    return list(sorted(list(ret_set)))

def encode_suffix(suffix):
    s = 0
    for i, c in enumerate(suffix):
        s = (s * BASE) + (ord(c) - ord('A'))

    return s

def encode_delta(d):
    d-=1
    assert d<0x80*0x80*0x80
    if d < 0x80:
        return chr(0x80 | d)
    elif d < 0x80*0x80:
        return chr(d & 0x7F) + chr(0x80 | (d>>7))
    else:
        return chr(d & 0x7F) + chr((d>>7) & 0x7F) + chr(d>>14)


FULL_REDUCED = {}
tot = 0
for prefix in sorted(FULL_SPLIT.keys()):
    print "====" + prefix + "===="
    replacements = top_diffs(FULL_SPLIT[prefix])
    suffix_list = reduce_suffix_list(FULL_SPLIT[prefix], replacements)
    #suffix_list = FULL_SPLIT[prefix]

    stream = bytes()
    prev = 0
    for suffix in suffix_list:
        v = encode_suffix(suffix)

        delta = v - prev
        prev = v

        stream += encode_delta(delta)
        #print suffix, "%05x" % (v,), "%05x" % (delta,)

    print len(stream)
    tot += len(stream)

print "TOT", tot
