#!/usr/bin/env python

import re

fasta = "cgccgccgccaaaaa"
motif = "ygcy"

motiflen = len(motif)
matches = re.finditer(r'(?=([ct][g][c][ct]))', fasta)
print(matches)
results = [int(match.span()[0]) for match in matches] # extract starting position
motifpositions = []
for result in results:
    start = result
    end = result + motiflen
    position = (start, end)
    motifpositions.append(position)

print(results)
print(motifpositions)


