#!/usr/bin/env python

import cairo
import math 

seqlength = [(0,548)]
start, finish = seqlength[0]
exonpos = [(276,312)]
exonstart, exonfinish = exonpos[0]
motifpositions = [(89, 93), (106, 110), (176, 180), (297, 301), (338, 342), (342, 346), (365, 369), (376, 380), (429, 433), (443, 447), (467, 471), (530, 534)]
totalsequences = 1
longest_sequence = 771
red = 0.9
green = 0.5
blue = 0.6

header = "INSR chr19:7150261-7150808 (reverse complement)"

sequence1 = 1*100
end = finish + 25 # buffer 

rectangleheight = totalsequences*200 # done 
rectanglewidth = int(longest_sequence+50) # done 



print(seqlength)
print(exonpos)




with cairo.ImageSurface(cairo.FORMAT_RGB24, rectanglewidth, rectangleheight) as surface:
     
    context = cairo.Context(surface)
    
    # fill in a white background #
    context.set_source_rgb(1.0, 1.0, 1.0) # white
    context.rectangle(0,0,rectanglewidth, rectangleheight)
    context.fill()

    # label sequence # 
    context.set_source_rgb(0.0, 0.0, 0.0) # black
    context.set_font_size(11)
    context.select_font_face( 
        "Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.move_to(25, sequence1-50)
    context.show_text(header)
    context.stroke()


    # draw sequence # 
    context.set_source_rgb(0.0, 0.0, 0.0) # black
    context.set_line_width(5)
    context.move_to(25,sequence1)       
    context.line_to(finish, sequence1)
    context.stroke()
    
    # draw exon #
    context.set_source_rgb(0.0, 0.0, 0.0) # black
    context.set_line_width(30)
    context.move_to(exonstart+25, sequence1)       
    context.line_to(exonfinish+25,sequence1)
    context.stroke()


    # draw motif #

    for start,finish in motifpositions:
        context.set_source_rgb(red, green, blue)
        context.set_line_width(18)
        context.move_to(start,sequence1)       
        context.line_to(finish,sequence1)
        context.stroke()

    # save 
    surface.write_to_png("tester.png") 