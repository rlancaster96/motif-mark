## Motif Mark 

This program takes a FASTA file with exons denoted in caps, and a motif text file with one motif per line (case insensitive). The output is a single .png with one image per sequence, with motif and exon positions displayed positionally on the sequence, to scale.

## Description
 
 Written for Bi625 at BGMP. 
 
 Aware of ambiguous nucleotides and inclusive of 'n's in sequence. e.g., 'ygcy' will match to 'tgnc'.


to do:
fix motif colors
fix regex to accurately get all overlapping motifs 

see info on re https://docs.python.org/3/howto/regex.html 

how to write a readme: 
 https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/