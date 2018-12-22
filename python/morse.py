#!/usr/bin/python3

# kopierend von https://de.wikipedia.org/wiki/Morsezeichen
raw_wiki_copy = """
A· −
B− · · ·
C− · − ·
D− · ·
E·
F· · − ·
G− − ·
H· · · ·
I· ·
J· − − −
K− · −
L· − · ·
M− −
N− ·
O− − −
P· − − ·
Q− − · −
R· − ·
S· · ·
T−
U· · −
V· · · −
W· − −
X− · · −
Y− · − −
Z− − · ·
1· − − − −
2· · − − −
3· · · − −
4· · · · −
5· · · · ·
6− · · · ·
7− − · · ·
8− − − · ·
9− − − − ·
0− − − − −
"""

def wiki_copy_to_morse_dict(wikicopy):
    wikicopy = wikicopy.replace(' ', '')
    morse_dict = { l[0]: l[1:] for l in wikicopy.splitlines() if l }
    return morse_dict

ascii_morse = wiki_copy_to_morse_dict(raw_wiki_copy)
morse_ascii = { v:k for k,v in ascii_morse.items() }

# return dict of number of occurences of chars in string
def char_stats(string):
    stats = {}

    for c in string:
        try:
            stats[c] += 1
        except KeyError:
            stats[c] = 1

    return stats

# return morse-encoded string
def morse_encode(string, dot='·', dash='−', sep=' ', ignore_unknown=True):
    morse_codes = []

    for char in string.upper():
        try:
            morse_codes.append( ascii_morse[char].replace('·', dot).replace('−', dash) )
        except KeyError:
            if not ignore_unknown:
                morse_codes.append(char)

    return sep.join(morse_codes)

# return (encoded string, num errors)
def morse_decode(string, dot=None, dash=None):
    # dot and dash given, just decode
    if dot and dash:
        decoded = []
        errors = 0 

        for code in string.split():
            try:
                decoded.append( morse_ascii[code.replace(dot, '·').replace(dash, '−')] )
            except KeyError:
                decoded.append( code )
                errors += 1

        return (''.join(decoded), errors)

    # dot/dash given, search for dash/dot
    elif dot or dash:
        stats = char_stats(string)

        # we dont want ' ' in our stats, since it's just a separator
        # we also don't want dot/dash there, because we got this character already
        stats.pop(' ', None)
        stats.pop(dot, None)
        stats.pop(dash, None)

        try:
            char = max(stats, key=stats.get)
        except ValueError:
            # there is no other character. but we need two for decoding.
            # the second character must differ from the first character
            # and must differ from space.
            if dot:
                char = chr(ord(dot) + ord(' '))
            else:
                char = chr(ord(dash) + ord(' '))

        if not dot:
            dot = char
        else:
            dash = char

        return morse_decode(string, dot=dot, dash=dash)

    # neither dot nor dash given, search for both
    else:
        stats = char_stats(string.replace(' ', ''))
        stats.pop(' ', None) # space not wanted in stat.

        chars = sorted(stats, key=stats.get)[:2]

        if len(chars) == 0:
            return ('', 1)
        elif len(chars) == 1:
            # it's okay that in our string is only one char.
            # the next call to morse_decode will handle that ;)
            chars.append( None )
            
        try1 = morse_decode(string, dot=chars[0], dash=chars[1])
        try2 = morse_decode(string, dot=chars[1], dash=chars[0])

        if try1[1] < try2[1]:
            return try1
        else:
            return try2


print(morse_encode("Hallo du da"))
print(morse_decode("···· ·− ·−·· ·−·· −−− −·· ··− −·· ·−"))
