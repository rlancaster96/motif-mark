#!/usr/bin/env python

# imports # 
from __future__ import annotations
import cairo
import math
import argparse
from re import finditer
from bioinfo import oneline_fasta


#set up argparse
def get_args():
    parser = argparse.ArgumentParser(description="Takes a FASTA file with exons denoted in CAPS, and a motif text file with one motif per line (case insensitive). Outputs one .png with one image per sequence of motif and exon positions on the sequence. Aware of ambiguous nucleotides and inclusive of 'n's in sequence. e.g., 'ygcy' will match to 'tgnc'")
    parser.add_argument("-f", "--fastafile", help="FASTA file to read", required=True, type=str)
    parser.add_argument("-m", "--motiffile", help="Motif text file to read", required=True, type=str)
    return parser.parse_args()

args = get_args()
motiffile:str = args.motiffile
fastafile:str = args.fastafile
pngfilename:str = fastafile + ".png"
onelinefastafile:str = "oneline" + fastafile

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
        self.label = None 
        
        # attributes for drawing # 
        self.color = None
        self.red:float = None
        self.green:float = None
        self.blue:float = None
    
    def __repr__(self):
        return(f'{self.sequence}')
    
    def shortenlabel(self):
        if len(self.sequence) > 8:
            self.label = self.sequence[:8] + "..." # shorten long motifs to label friendly format
        else:
            self.label = self.sequence

    # Methods #
    
    def regexify(self):
       oglist = [*(self.sequence)] # split up the sequence into a list of individual characters
       regstring = "" # make an empty string to append to
       for a in oglist: # iterate over the list of characters and append to regex-friendly string
           # https://en.wikipedia.org/wiki/Nucleic_acid_notation #
           if a == "y": # pyrimidine
               regstring += "[ctn]"
           elif a == "u": # uracil
               regstring += "[tn]"
           elif a == "w": # weak
               regstring += "[atn]"
           elif a == "s": # strong
               regstring += "[cgn]"
           elif a == "m": # amino
               regstring += "[acn]"
           elif a == "k": # ketone
               regstring += "[gtn]"
           elif a == "r": # purine
               regstring += "[agn]"    
           elif a == "b": # not a
               regstring += "[cgtn]"
           elif a == "d": # not c
               regstring += "[agtn]" 
           elif a == "h": # not g
               regstring += "[actn]"
           elif a == "v": # not t
               regstring += "[acgn]"
           elif a == "n": # any nucleotide
               regstring += "[actgn]"
           else:
               regstring += "[" + a + "n" + "]" 
       self.regex = "?=" + regstring
       return
    
    def colorit(self):
        # generate rgb colors # 
        # self.red:float = 1-((2*(self.number))-2)/10
        # self.green:float = (2*(self.number))/10 
        # self.blue:float = 1-((2*(self.number))-2)/10 
        self.red:float = math.log10(self.number)
        self.green:float = math.log10(self.number)
        self.blue:float = math.log10(self.number)
        return

class Canvas: # the canvas I will be drawing on # 
    def __init__(self, totalsequences, longestsequence):
        self.buffer: int = 25
        self.constant: int = 100
        self.height:int = (totalsequences*self.constant)+self.constant # add extra on the bottom to account for label
        self.width:int = int(longest_sequence+(self.buffer*2))
        # label position information # 
        self.xlabel = ((totalsequences+1)*self.constant)-30
        
# >> define functions << # 

# read in motifs into list # 
def parse_motif(motiffile: str) -> list:
    '''read motifs from a text file with one motif per line into a list'''
    motifs = []
    with open(motiffile) as fh:
        for line in fh:
            line = line.strip()
            motifs.append(line)
    return motifs

# read in sequences into dictionary {sequence : header} # 
def parse_fasta(onelinefastafile: str) -> dict:
    '''read sequences and headers in from a fasta file to a dictionary'''
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

def longest(sequence_obj_list: list) -> int:
    '''determine the longest sequence from a list of sequence objects with attribute "length"'''
    longest: int = 0
    for a in sequence_obj_list: 
        if a.length > longest:
            longest = a.length
    return longest

# def makemotifs(motifs):

# main # 

if __name__ == "__main__":
    
    # convert from multiple line fasta to one line fasta #
    oneline_fasta(fastafile, onelinefastafile)
    # intake motif and sequence information from files and store in memory # 
    motifs: list = parse_motif(motiffile) # list of motifs ['motif1', 'motif2', 'motif3', ...]
    sequences: dict = parse_fasta(onelinefastafile) # dictionary of sequences {'sequence1':'header1', 'sequence2':'header2', ...}
 
    # make motif objects # 
    motif_obj_list: list = []
    motif_obj_list += [Motif(motifsequence, i) for i, motifsequence in enumerate(motifs)] #for each motif create object Motif(motif) and store in list
    for motif in motif_obj_list:
        motif.colorit()
        motif.regexify()
        motif.shortenlabel()

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
    longest_sequence:int = 650 # minimum length for my label to display nicely 
    if longest(sequence_obj_list) > 650:
        longest_sequence = longest(sequence_obj_list)
    drawing_canvas = Canvas(totalsequences, longest_sequence)

    # open cairo image file to draw on. RGB24 is the non-transparent option # 
    # use a 25px margin so add 25 to all width values #
    with cairo.ImageSurface(cairo.FORMAT_RGB24, drawing_canvas.width, drawing_canvas.height) as surface:
        context = cairo.Context(surface)
        # fill in a white background #
        context.set_source_rgb(1.0, 1.0, 1.0) # white
        context.rectangle(0, 0, drawing_canvas.width, drawing_canvas.height)
        context.fill()

        for sequence in sequence_obj_list:
            
            # 1. label sequence # 
            context.set_source_rgb(0.0, 0.0, 0.0) # black
            context.set_font_size(11)
            context.select_font_face("Arial")
            context.move_to(drawing_canvas.buffer, (sequence.number*drawing_canvas.constant)-(drawing_canvas.constant/3))
            context.show_text(sequence.header)
            context.stroke()

            # 2. draw sequence # 
            context.set_source_rgb(0.0, 0.0, 0.0) # black
            context.set_line_width(5)
            context.move_to(drawing_canvas.buffer, sequence.number*drawing_canvas.constant)       
            context.line_to(sequence.length + drawing_canvas.buffer, sequence.number*drawing_canvas.constant)
            context.stroke()

            # 3. draw exon(s) #
            if sequence.exons is None: # if you haven't added any value to the exons attribute
                pass # allows you to plot sequences with no exons 
            else:
                for i in range(len(sequence.exons)):
                    exonstart, exonfinish = sequence.exons[i]
                    context.set_source_rgb(0.0, 0.0, 0.0) # black
                    context.set_line_width(30)
                    context.move_to(exonstart+drawing_canvas.buffer, sequence.number*drawing_canvas.constant)       
                    context.line_to(exonfinish+drawing_canvas.buffer, sequence.number*drawing_canvas.constant)
                    context.stroke()

            # 4. draw motifs # 
            for motif in motif_obj_list:
                # find where motifs (regex matches) are positionally in sequence #
                motifpositions = []
                for match in finditer(motif.regex, sequence.gensequence): 
                    motifpositions += [match.span()] # "match" is a match object with "span" (position) and "match" (matched sequence) attributes
                    for start,finish in motifpositions:
                        context.set_source_rgb(motif.red, motif.green, motif.blue)
                        context.set_line_width(18)
                        context.move_to(start+drawing_canvas.buffer, sequence.number*drawing_canvas.constant)       
                        context.line_to(finish+drawing_canvas.buffer, sequence.number*drawing_canvas.constant)
                        context.stroke()
            
            # 5. add label for motifs # 
            for i,motif in enumerate(motif_obj_list):
                context.set_source_rgb(motif.red, motif.green, motif.blue) # white
                context.rectangle(drawing_canvas.buffer+(i*120),drawing_canvas.xlabel,20,20)
                context.fill()
                context.set_source_rgb(0.0, 0.0, 0.0) # black
                context.set_font_size(11)
                context.select_font_face("Arial")
                context.move_to(drawing_canvas.buffer+(i*120)+22,drawing_canvas.xlabel+12.5)
                context.show_text(motif.label)
                context.stroke()

        
        
        # save #
        surface.write_to_png(pngfilename) 

