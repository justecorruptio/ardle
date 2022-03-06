from pprint import pprint

fh = open('input_data/full.txt', 'r')
FULL = [w.upper() for w in fh.read().split()]

#FULL = ['CARTS', 'ARTSY', 'SYSOP']


prefixes = [{} for i in range(5)]

for word in FULL:
    for i, level in enumerate(prefixes):
        level.setdefault(word[:i], set()).add(word)

pprint(prefixes)

def remove_from_prefixes(word):
    for i, level in enumerate(prefixes):
        prefix = word[:i]
        s = level.get(prefix)
        if s is None:
            continue
        if word in s:
            s.remove(word)
        if not s:
            del level[prefix]

stream = FULL[0]
remove_from_prefixes(FULL[0])

while prefixes[0].get(''):
    print(stream[-75:], len(prefixes[0]['']))
    #if len(prefixes[0]) == 1:
    #    print(prefixes[0])
    for i in range(4, -1, -1):
        level = prefixes[i]
        if i:
            prefix = stream[-i:]
        else:
            prefix = ''
        if prefix in level:
            word = level[prefix].pop()
            stream += word[-(5 - i):]
            remove_from_prefixes(word)
            break

print(stream)
print(len(stream))
