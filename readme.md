## Motif Mark : create an image of motifs on a sequence
 Written for Bi625 at BGMP. 

## Description
 This program takes a FASTA file with exons denoted in caps, and a text file of motifs with one motif per line (case insensitive). The output is a single .png with one image per sequence, with motif and exon positions displayed positionally on the sequence, to scale. 
 
 This program uses object-oriented code where sequences, motifs, and the drawing canvas are objects that interact with one another. Pycairo (https://pycairo.readthedocs.io/en/latest/) was used for creating the image.

 - Aware of ambiguous nucleotides and inclusive of 'n's in sequence. e.g., 'ygcy' will match to 'tgnc'
 - Automatically generates a FASTA file with one line per sequence 

## Running the program

This program is Python 3 compatible and requires pycairo (https://pycairo.readthedocs.io/en/latest/). 

To run this program, create a conda environment with pycairo and Python installed.

```
conda create -n my_pycairo python=3.11 pycairo
conda activate my_pycairo
```


### Ambiguous nucleotides supported

| Description | Symbol | Base |
| ----------- | ------ | ---- | 
| Adenine | A |	A |
| Cytosine | C | C | 
| Guanine | G | G |
| Thymine | T | T |
| Uracil | U | U |
| Weak | W | AT |
| Strong | S | CG |
| Amino | M | AC |
| Ketone | K | GT |
| Purine | R | AG |
| Pyrimidine | Y | CT |
| Not A | B | CGT |
| Not C | D | AGT |
| Not G | H | ACT | 
| Not T	| V	| ACG |
| Any one base | N | ACGT |

From: https://en.wikipedia.org/wiki/Nucleic_acid_notation 

### Limitations and future developments



## Resources 


see info on re https://docs.python.org/3/howto/regex.html 
see info on using variables in re  https://stackoverflow.com/questions/6930982/how-to-use-a-variable-inside-a-regular-expression


how to write a readme: 
 https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/