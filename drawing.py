#!/usr/bin/env python

import cairo
import math 

sequence = "atgtccacatgtagtcacgtttgacatcagcaggccgtctctggggaAAAAACCTCTTCAGGCACTGGTGCCGAGGACCCTAGgtatgactcacctgtgcga"
motif1 = "acat"
motif2 = "ggcc"
motif3 = "CCTCTT"




with cairo.ImageSurface(cairo.FORMAT_RGB24, 500, 500) as surface:
     
    context = cairo.Context(surface)
    
    # fill in a white background 
    context.set_source_rgb(1.0, 1.0, 1.0) # white
    context.rectangle(0,0,500,500)
    context.fill()

    # draw line #
    context.set_source_rgb(0.0, 0.0, 0.8) # dark blue 
    context.set_line_width(5)
    context.move_to(25,250)       
    context.line_to(475,250)
    context.stroke()

    #draw a rectangle
    context.set_source_rgb(1.0, 0.569, 0.643) # salmon pink 
    context.rectangle(50,280,200,50)      
    context.fill()

    # save 
    surface.write_to_png("salmon_swimming.png") 