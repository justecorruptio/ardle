import math
import random
import struct
random.seed(0)

BASE = 32

fh = open('input_data/en.txt', 'r')
EN_FULL = set([w.upper() for w in fh.read().split()][:])

fh = open('input_data/fr.txt', 'r')
FR_FULL = set([w.upper() for w in fh.read().split()][:])

FULL = list(sorted(list(EN_FULL | FR_FULL)))
print "NUM WORDS:", len(FULL)

#FULL = ['BAR', 'BET', 'BAT', 'CAR', 'VAR', 'VAT', 'VET', 'HAT', 'KAT', 'CAP']
#FULL = ['BAR']


def gen_masks(word):
    ret = []
    for i in xrange(len(word)):
        ret.append(word[:i] + '_' + word[i + 1:])
    return ret

class Graph(object):
    next_id = 1
    __slots__ = ('id', 'n', 'e')
    def __init__(self):
        self.n = set()
        self.e = set()
        self.id = Graph.next_id
        Graph.next_id += 1

    @classmethod
    def merge(cls, graphs):
        new = cls()
        for graph in graphs:
            new.n |= graph.n
            new.e |= graph.e
        return new

    def __hash__(self):
        return self.id

    def __repr__(self):
        nodes = ','.join(self.n)
        edges = ','.join(x + '-' + y for x, y in self.e)
        return 'N: ' + nodes + '\nE: ' + edges

def gen_graphs(word_list):
    graphs = set()
    word_to_graph = {}
    mask_to_words = {}

    for i, word in enumerate(word_list):
        masks = gen_masks(word)

        to_join = set()
        edges = set()
        for mask in masks:
            links = mask_to_words.get(mask, set())
            for link in links:
                edge = (link, word) if link < word else (word, link)
                edges.add(edge)
                to_join.add(word_to_graph[link])

        graphs -= to_join
        new_graph = Graph.merge(to_join)
        new_graph.n.add(word)
        new_graph.e |= edges

        graphs.add(new_graph)

        for node in new_graph.n:
            word_to_graph[node] = new_graph

        for mask in masks:
            mask_to_words.setdefault(mask, set()).add(word)

    return graphs



def find_paths(graph):
    if len(graph.n) == 1:
        return [[list(graph.n)[0]]]

    m = {}
    for s, d in graph.e:
        m.setdefault(s, set()).add(d)
        m.setdefault(d, set()).add(s)

    def pick_not_deadend(poss):
        while True:
            if not poss:
                return None
            next = poss.pop()
            if next in m:
                return next

    def walk(ptr):
        path = []
        while True:
            path.append(ptr)
            if ptr in m:
                poss = m.pop(ptr)
                next = pick_not_deadend(poss)
                if next is None:
                    break
                ptr = next
            else:
                break
        return path

    paths = []
    while m:
        start = min(m.keys())
        #print "START", start
        poss = m.pop(start)

        forward = pick_not_deadend(poss)

        path = [start]
        if forward is not None:
            for_path = walk(forward)
            path = path + for_path

        backward = pick_not_deadend(poss)
        if backward is not None:
            back_path = walk(backward)
            path = list(reversed(back_path)) + path

        if path[0] > path[-1]:
            path = list(reversed(path))

        paths.append(path)

    return paths

print '===== GENERATING GRAPHS ===='
graphs = gen_graphs(FULL)
print 'NUM GRAPHS:', len(graphs)

print '===== GENERATING PATHS ====='

check_count = 0
all_paths = []
for graph in graphs:
    #print '+++++++++++'
    #print len(graph.e)
    #print graph
    #print "PATHS"
    paths = find_paths(graph)
    for path in paths:
        check_count += len(path)
        #print path
        #for w in path:
        #    print w
    all_paths.extend(paths)

all_paths.sort()
#for path in all_paths:
#    print path

assert len(FULL) == check_count
print "NUM PATHS:", len(all_paths)


def encode_word(word):
    s = 0
    for i, c in enumerate(word):
        s = (s * BASE) + (ord(c) - ord('A'))

    return s

def encode_delta(d):
    stats[int(math.log(d + 1) / math.log(2))] += 1
    assert d<0x80*0x80*0x80
    if d < 0x80:
        return chr(0x80 | d)
    elif d < 0x80*0x80:
        return chr(d >> 7) + chr(0x80 | (d & 0x7f))
    else:
        return chr(d >> 14) + chr((d>>7) & 0x7F) + chr(0x80 | (d & 0x7f))

def get_diff_byte(a, b):
    for i in xrange(len(a)):
        if a[i] != b[i]:
            return i * 25 + ((ord(b[i]) - ord(a[i]) + 26) % 26) - 1

    assert False

def encode_path(path):
    buff = bytes()
    for i in xrange(len(path) - 1):
        b = get_diff_byte(path[i], path[i + 1])
        if i == len(path) - 2:
            b |= 0x80
        buff += chr(b)
    return buff


singletons = [path for path in all_paths if len(path) == 1]
full_paths = [path for path in all_paths if len(path) > 1]

print '===== OPTIMIZING PATH ORDERING ====='
print "      NUM FULL PATHS:", len(full_paths)

ordering = [0 for i in xrange(len(full_paths))]
terminals = []

for path in full_paths:
    assert path[0] != path[-1]
    terminals.append((encode_word(path[0]), encode_word(path[-1])))

def score_terminals(ordering, terminals):
    prev = 0
    score = 0
    values = []
    for i in xrange(len(ordering)):
        values.append(terminals[i][ordering[i]])

    values.sort()
    for v in values:
        d = v - prev
        prev = v
        score += (d >= 0x80) + (d >= 0x80*0x80) + 1 + 9999 * (d >= 0x80 * 0x80 * 0x80)
    return score

begin_score = score = score_terminals(ordering, terminals)

for n in xrange(50000):
    trial = ordering[:]
    flip = random.randint(0, len(ordering) - 1)
    trial[flip] ^= -1

    trial_score = score_terminals(trial, terminals)
    if trial_score < score:
        #print " TEMP SCORE:", trial_score
        ordering = trial
        score = trial_score

#print "FINAL SCORE:", score_terminals(ordering, terminals)

for i, order in enumerate(ordering):
    if order == -1:
        full_paths[i] = list(reversed(full_paths[i]))

full_paths.sort()

print "     BYTES OPTIMIZED:", begin_score - score


print '===== GENERATING BYTES ====='
single_stream = bytes()
path_stream = bytes()
path_steps = bytes()

stats = [0 for i in xrange(30)]

prev = 0
for path in singletons:
    v = encode_word(path[0])
    delta = v - prev
    prev = v

    single_stream += encode_delta(delta)

#print stats
stats = [0 for i in xrange(30)]

prev = 0
for path in full_paths:
    v = encode_word(path[0])
    delta = v - prev
    prev = v

    path_stream += encode_delta(delta)
    path_steps += encode_path(path)
#print stats

print "SINGLE STREAM LENGTH:", len(single_stream)
print "  PATH STREAM LENGTH:", len(path_stream)
print "   PATH STEPS LENGTH:", len(path_steps)
print "        TOTAL LENGTH:", len(single_stream) + len(path_stream) + len(path_steps)

print '===== VERIFYING BYTES ====='

def decode_word(val):
    w = ''
    for i in xrange(5):
        w = chr((val % BASE) + ord('A')) + w
        val /= BASE

    return w

decoded_words = []

val = 0
i = 0
while i < len(single_stream):
    delta = 0
    while True:
        b = ord(single_stream[i])
        i += 1
        delta = (delta << 7) | (b & 0x7f)

        if b & 0x80:
            break

    val += delta
    word = decode_word(val)
    decoded_words.append(word)

val = 0
i = 0
j = 0
while i < len(path_stream):
    delta = 0
    while True:
        b = ord(path_stream[i])
        i += 1
        delta = (delta << 7) | (b & 0x7f)

        if b & 0x80:
            break

    val += delta
    word = decode_word(val)
    decoded_words.append(word)
    while True:
        b = ord(path_steps[j])
        j += 1
        pos = (b & 0x7f) / 25
        rot = ((b & 0x7f) % 25) + 1
        c = chr((ord(word[pos]) - ord('A') + rot) % 26 + ord('A'))
        word = word[:pos] + c + word[pos + 1:]
        decoded_words.append(word)
        if b & 0x80:
            break

#for w in decoded_words:
#    print w
assert sorted(decoded_words) == sorted(FULL)

print '===== LOADING ANSWERS ======'

fh = open('input_data/en-answers.txt', 'r')
EN_ANSWERS = set([w.upper() for w in fh.read().split()]) & EN_FULL

fh = open('input_data/fr-answers.txt', 'r')
FR_ANSWERS = set([w.upper() for w in fh.read().split()]) & FR_FULL

ANSWER_SET = set()
for ans in list(EN_ANSWERS | FR_ANSWERS):
    ans_val = ((ans in EN_ANSWERS) << 1) | (ans in FR_ANSWERS)
    full_val = ((ans in EN_FULL) << 1) | (ans in FR_FULL)
    if ans_val == full_val:
        ANSWER_SET.add(ans)

ANSWERS = list(sorted(list(ANSWER_SET)))

unpacked = []

for word in decoded_words:
    unpacked.append( ((word in EN_FULL) << 2) | ((word in FR_FULL) << 1) | (word in ANSWER_SET) )

while len(unpacked) % 8:
    unpacked += [0]

flags_stream = bytes()
x = 0
for i, v in enumerate(unpacked):
    assert v <= 0x7
    x |= v << ((i % 8) * 3)
    assert x <= 0xffffff
    if i % 8 == 7:
        flags_stream += struct.pack("<i", x)[:3]
        x = 0

print "         NUM ANSWERS:", len(ANSWERS)
print " PACKED FLAGS LENGTH:", len(flags_stream)

print '===== VALIDATING FLAGS ==='

decoded_en = []
decoded_fr = []
decoded_ans = []

for i, word in enumerate(decoded_words):
    (val,) = struct.unpack("<i", flags_stream[i / 8 * 3: i / 8 * 3 + 3] + '\0')
    flags = (val >> ((i % 8) * 3)) & 0x7
    if flags & 0x4:
        decoded_en.append(word)
    if flags & 0x2:
        decoded_fr.append(word)
    if flags & 0x1:
        decoded_ans.append(word)

assert sorted(decoded_en) == sorted(EN_FULL)
assert sorted(decoded_fr) == sorted(FR_FULL)
assert sorted(decoded_ans) == sorted(ANSWERS)

print '===== GENERATING OUTPUT ===='

fh = open('generated_data/compresssed_data.h', 'w')

def format_bytes(stream):
    output = ''
    for i, c in enumerate(stream):
        output += '0x%02x,' % (ord(c),)
        if i % 16 == 15:
            output += '\n'
        else:
            output += ' '

    return output

output = ''

output += '#ifndef COMPRESSED_DATA_H\n'
output += '#define COMPRESSED_DATA_H\n'

output += 'PROGMEM const uint8_t SINGLE_STREAM [] = {\n'
output += format_bytes(single_stream)
output += '};\n\n'

output += 'PROGMEM const uint8_t PATH_STREAM [] = {\n'
output += format_bytes(path_stream)
output += '};\n\n'

output += 'PROGMEM const uint8_t PATH_STEPS [] = {\n'
output += format_bytes(path_steps)
output += '};\n\n'

output += 'PROGMEM const uint8_t FLAGS_STREAM [] = {\n'
output += format_bytes(flags_stream)
output += '};\n\n'

output += '#define SINGLE_STREAM_LENGTH %d\n' % (len(single_stream),)
output += '#define PATH_STREAM_LENGTH %d\n' % (len(path_stream),)
output += '#define FLAGS_STREAM_LENGTH %d\n' % (len(flags_stream),)

output += '#endif\n'
fh.write(output)
fh.close()
