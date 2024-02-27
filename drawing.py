#!/usr/bin/env python

import cairo
import math 

seqlength = [(0,548)]
exonpos = [(276,312)]
totalsequences = 8
longest = 771
red = 0.9
green = 0.5
blue = 0.6

rectangleheight = totalsequences*200
rectanglewidth = int(longest+50)


print(seqlength)
print(exonpos)




with cairo.ImageSurface(cairo.FORMAT_RGB24, rectanglewidth, rectangleheight) as surface:
     
    context = cairo.Context(surface)
    
    # fill in a white background #
    context.set_source_rgb(1.0, 1.0, 1.0) # white
    context.rectangle(0,0,rectanglewidth, rectangleheight)
    context.fill()

    # draw sequence # 
    context.set_source_rgb(1.0, 1.0, 1.0)
    context.set_line_width(5)
    context.move_to(25,250)       
    context.line_to(475,250)
    context.stroke()

    # draw motif #
    context.set_source_rgb(red, green, blue)
    context.set_line_width(5)
    context.move_to(25,250)       
    context.line_to(475,250)
    context.stroke()

    #draw exon
    context.set_source_rgb(1.0, 1.0, 1.0) # salmon pink 
    context.rectangle(50,280,200,50)      
    context.fill()

    # save 
    surface.write_to_png("tester.png") 