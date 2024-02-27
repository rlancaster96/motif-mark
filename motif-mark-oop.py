#!/usr/bin/env python

# imports # 
from __future__ import annotations
import cairo
import math
import bioinfo
import argparse
# info on re https://docs.python.org/3/howto/regex.html #
import re
from re import finditer

#set up argparse
def get_args():
    parser = argparse.ArgumentParser(description="Takes a FASTA file with exons denoted in CAPS, and a motif file. Outputs one .png with one image per sequence of motif positions on the sequence.")
    parser.add_argument("-f", "--fastafile", help="FASTA file to read", required=True, type=str)
    parser.add_argument("-m", "--motiffile", help="Motif text file to read", required=True, type=str)
    return parser.parse_args()

args = get_args()
motiffile = args.motiffile
fastafile = args.fastafile
onelinefastafile = "oneline" + fastafile

# define classes #

class Sequence:
    def __init__(self, sequence:str, header:str):
        # Data # 
        self.sequence = sequence # sequence containing upper and lower case. use for finding exon positions
        self.gensequence = sequence.lower() # general sequence only containing lower case. use for finding motif positions
        self.header = header
        self.length: list = [(0, len(sequence))]
        self.exons = None

    def __repr__(self):
        return(f'{self.header}')
    
    def findexons(self):
        exonlist: list = []
        for a in finditer("[A-Z]+", self.sequence): 
            exonlist += [(a.span())]
            self.exons = exonlist

class Motif:
    def __init__(self, motifsequence:str):
        # Data # 
        self.sequence = motifsequence.lower()
        self.position = None
        self.regex = None
    
    def __repr__(self):
        return(f'{self.sequence}')

    # Methods #
    def regexify(self):
       oglist = [*(self.sequence)] # split up the sequence into a list of individual characters
       regstring = "" # make an empty string to append to
       for a in oglist: # iterate over the list of characters and append to regex-friendly string
           if a == "y":
               regstring += "[ct]"
           else:
               regstring += "[" + a + "]" 
       self.regex = regstring
       return
    
    #def draw(self, somethingelse):
    #    call context here to draw with cairo


# define functions # 

# func to read in motifs into list # 
def parse_motif(motiffile: str) -> list:
    motifs = []
    with open(motiffile) as fh:
        for line in fh:
            line = line.strip()
            motifs.append(line)
    return motifs

# func to read in sequences into dictionary {sequence : header} # 
def parse_fasta(onelinefastafile: str) -> dict:
    sequences = {}
    with open(onelinefastafile) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(">"): # get header
                header = line[1:]
            else: # get sequence             
                sequence = line
                sequences[sequence] = header # put in dictionary
    return sequences

# main # 

if __name__ == "__main__":
    
    # convert from multiple line fasta to one line fasta #
    bioinfo.oneline_fasta(fastafile, onelinefastafile)
    # intake motif and sequence information from files and store in memory # 
    motifs: list = parse_motif(motiffile) # list of motifs ['motif1', 'motif2', 'motif3', ...]
    sequences: dict = parse_fasta(onelinefastafile) # dictionary of sequences {'sequence1':'header1', 'sequence2':'header2', ...}

    # Make motif objects # 
    motif_obj_list: list = []
    motif_obj_list += [Motif(a) for a in motifs] #for each motif create object Motif(motif) and store in list

    # Make sequence objects # 
    sequence_obj_list: list = []
    for a in sequences: # for each sequence and header, store in list of sequence objects
        seq = a
        header = sequences[a]
        sequence_obj_list += [Sequence(seq, header)]

    # find positions of motifs in sequences , just 1 to start with # 
    currentseq = sequence_obj_list[0]
    currentseq.findexons()
    currentmotif = motif_obj_list[0]
    currentmotif.regexify()


    # find where motifs (regex matches) are positionally in sequence #
    rawpositions = []
    for a in finditer(currentmotif.regex, currentseq.gensequence): 
        rawpositions += [a.span()] # "a" is a match object with "span" (position) and "match" (matched sequence) attributes
    # raw positions for the motifs 
    print(currentseq.exons)
    print(currentseq.length)


    


# findseq = currentmotif.sequence
# oglist = [*findseq]
# looklist = []
# for a in looklist:
#     if a == 'y':
#         looklist.append(['ct'])
#     elif a == 

# print(looklist)

# degenerate bases 





# draw the image 

