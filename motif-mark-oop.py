#!/usr/bin/env python

# imports # 
from __future__ import annotations
import cairo
import math
import bioinfo
import argparse
import random # for randomizing motif colors 

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
    def __init__(self, sequence:str, header:str, number):
        # Data # 
        self.sequence = sequence # sequence containing upper and lower case. use for finding exon positions
        self.gensequence = sequence.lower() # general sequence only containing lower case. use for finding motif positions
        self.header = header
        self.length: int = len(sequence)
        # self.lengthrange: list = [(0, len(sequence))] put this in somewhere else 
        self.exons = None
        self.number:int = number+1 # add a sequence number here instead of relying on calling the list of objects 

    def __repr__(self):
        return(f'{self.header}')
    
    # Methods # 
    def findexons(self):
        exonlist: list = []
        for a in finditer("[A-Z]+", self.sequence): 
            exonlist += [(a.span())]
            self.exons = exonlist

class Motif:
    def __init__(self, motifsequence:str, number:int):
        # Data # 
        # attributes for getting positions # 
        self.sequence = motifsequence.lower()
        self.position = None
        self.regex = None
        self.number:int = number+1
        
        # attributes for drawing # 
        self.color = None
        self.red = None
        self.green = None
        self.blue = None
    
    def __repr__(self):
        return(f'{self.sequence}')

    # Methods #
    
    def regexify(self):
       oglist = [*(self.sequence)] # split up the sequence into a list of individual characters
       regstring = "" # make an empty string to append to
       for a in oglist: # iterate over the list of characters and append to regex-friendly string
           # https://en.wikipedia.org/wiki/Nucleic_acid_notation #
           if a == "y": # pyrimidine
               regstring += "[ct]"
           elif a == "u": # uracil
               regstring += "[t]"
           elif a == "w": # weak
               regstring += "[at]"
           elif a == "s": # strong
               regstring += "[cg]"
           elif a == "m": # amino
               regstring += "[ac]"
           elif a == "k": # ketone
               regstring += "[gt]"
           elif a == "r": # purine
               regstring += "[ag]"    
           elif a == "b": # not a
               regstring += "[cgt]"
           elif a == "d": # not c
               regstring += "[agt]" 
           elif a == "h": # not g
               regstring += "[act]"
           elif a == "v": # not t
               regstring += "[acg]"
           elif a == "n": # any nucleotide
               regstring += "[actg]"
           else:
               regstring += "[" + a + "]" 
       self.regex = regstring
       return
    
    def colorit(self):
        # generate three random floats to code for rgb color # 
        self.red = round(random.uniform(0.0, 1.0), 1)
        self.green = round(random.uniform(0.0, 1.0), 1)
        self.blue = round(random.uniform(0.2, 0.8), 1) # limiting 0.2-0.8 guaruntees can't be white (1,1,1) or black (0,0,0)
        self.color = (self.red, self.green, self.blue) # use tuple so order does not change because order = color
        return
        # make sure you include a checking step to ensure that no motifs are the same color. if they are are, reaassign color with colorit
    
    #def draw(self, somethingelse):
    #    call context here to draw with cairo

class Canvas: # the canvas I will be drawing on # 
    def __init__(self, totalsequences, longestsequence):
        self.height:int = totalsequences*200
        self.width:int = int(longest_sequence+50)


# >> define functions << # 

# read in motifs into list # 
def parse_motif(motiffile: str) -> list:
    motifs = []
    with open(motiffile) as fh:
        for line in fh:
            line = line.strip()
            motifs.append(line)
    return motifs

# read in sequences into dictionary {sequence : header} # 
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

# determine the longest sequence from a list of sequence objects with attribute "length" (use to determine width of png) #
def longest(sequence_obj_list: list) -> int:
    longest: int = 0
    for a in sequence_obj_list: 
        if a.length > longest:
            longest = a.length
    return longest

# main # 

if __name__ == "__main__":
    
    # convert from multiple line fasta to one line fasta #
    bioinfo.oneline_fasta(fastafile, onelinefastafile)
    # intake motif and sequence information from files and store in memory # 
    motifs: list = parse_motif(motiffile) # list of motifs ['motif1', 'motif2', 'motif3', ...]
    sequences: dict = parse_fasta(onelinefastafile) # dictionary of sequences {'sequence1':'header1', 'sequence2':'header2', ...}
 
    # make motif objects # 
    motif_obj_list: list = []
    motif_obj_list += [Motif(motifsequence, i) for i, motifsequence in enumerate(motifs)] #for each motif create object Motif(motif) and store in list
    for motif in motif_obj_list:
        motif.colorit()
        motif.regexify()

    # make sequence objects # 
    sequence_obj_list: list = []
    for i, seq in enumerate(sequences): # for each sequence and header, store in list of sequence objects
        header = sequences[seq]
        sequence_obj_list += [Sequence(seq, header, i)]
    for sequence in sequence_obj_list:
        sequence.findexons()

    # set up drawing parameters # 
    # >> determine height << # 
    totalsequences: int = len(sequences) # how many sequences am I graphing? (use to determine height of png)
    # >> determine width << # 
    longest_sequence:int = longest(sequence_obj_list) # determine width of png 
    drawing_canvas = Canvas(totalsequences, longest_sequence)

    # find positions of motifs in sequences , just 1 to start with #



    for i, sequences in enumerate(sequence_obj_list): 
        currentseq = sequence_obj_list[0]
    currentmotif = motif_obj_list[0]


    # find where motifs (regex matches) are positionally in sequence #
    rawpositions = []
    for a in finditer(currentmotif.regex, currentseq.gensequence): 
        rawpositions += [a.span()] # "a" is a match object with "span" (position) and "match" (matched sequence) attributes
    # raw positions for the motifs 
    print(currentseq.exons)
    print(currentseq.length)
    print(rawpositions)
    print(currentseq.header)


    
    


# draw the image see drawing.py 

