#!/usr/bin/env python

from __future__ import annotations
import cairo
import math
import bioinfo
import argparse

# picture of a sequence: positions of exons, introns, and motifs, to scale 

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

# define classes 

# read in info from files #

# convert from multiple line fasta to one line fasta #
bioinfo.oneline_fasta(fastafile, onelinefastafile)

# read in motifs into list # 
def parse_motif(motiffile: str) -> list:
    motifs = []
    with open(motiffile) as fh:
        for line in fh:
            line = line.strip()
            motifs.append(line)
    return motifs

# read in sequences into list # 
def parse_fasta(onelinefastafile: str) -> dict:
    # {sequence : header}
    sequences = {}
    with open(onelinefastafile) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(">"):
                header = line[1:]
            else:            
                sequence = line
                sequences[sequence] = header
    return sequences

motifs = parse_motif(motiffile)
sequences = parse_fasta(onelinefastafile)


# degenerate bases 





# draw the image 

