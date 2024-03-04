## Motif Mark : create an image of motifs on a sequence
 Written for Bi625 at BGMP. 

## Description
 This program takes a FASTA file with exons denoted in caps, and a text file of motifs with one motif per line (case insensitive, maximum 5 motifs). The output is a single .png with one image per sequence, with motif and exon positions displayed positionally on the sequence, to scale. 
 
 This program uses object-oriented code where sequences, motifs, and the drawing canvas are objects that interact with one another. Pycairo (https://pycairo.readthedocs.io/en/latest/) was used for creating the image.

 - Aware of ambiguous nucleotides and inclusive of 'n's in sequence. e.g., 'ygcy' will match to 'tgnc'
 - Automatically generates a FASTA file with one line per sequence 
 - Sequences with no exons present are supported (will only display motifs)

## Running the program

This program is Python 3 compatible and requires pycairo (https://pycairo.readthedocs.io/en/latest/). 

To run this program, create a conda environment with pycairo and Python installed.

```
conda create -n my_pycairo python=3.11 pycairo
conda activate my_pycairo
```

##### Options 
motif-mark-oop.py takes two options: -f, and -m. 

| -h | --help | show this help message and exit |
| -f | --fastafile | FASTA file to read |
| -m | --motiffile | Motif text file to read |

Example:

```
./motif-mark-oop.py -f Figure_1.fasta -m Fig_1_motifs.txt
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

##### One line fasta file creation
This program automatically creates a FASTA file with one line per sequence while it runs. The creation of this additional file can be a nuisance and future developments should allow the user to choose whether to save this file by passing an option. 

##### Motif colors and options
Limited to a maximum of 5 motifs due to color and formatting constraints. Capable of handling any length of motif, but motifs will only display the first 10 characters in the legend. Motifs should be shorter than the sequence of interest.

##### Inclusive of "N"s
This program is N-inclusive. Future development should allow the user to choose whether they would like this option or whether they do not want the motif query to include "N" automatically. (e.g., TGCT will match TGNT).

## Resources 

see info on re https://docs.python.org/3/howto/regex.html

see info on using variables in re  https://stackoverflow.com/questions/6930982/how-to-use-a-variable-inside-a-regular-expression

see info on how to write a readme 
 https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/

see info on pycairo https://pycairo.readthedocs.io/en/latest/

see info on nucleotide notation https://en.wikipedia.org/wiki/Nucleic_acid_notation 