from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from tqdm import tqdm
from cairosvg import svg2png



for i in tqdm(range(0,2589+1)):
    b = len(str(i))-1 #1-9 returns 0, 10-99 returns 1, 100-999 returns 2...
    zero = "0"*(5-b) #Sony vegas image sequences are name_000000
    name = "a_"+zero + str(i) #an example of name is a_000123 (frame 123)

    svg_filename = 'C:/Users/demor/OneDrive/Documents/python_scripts/bad_apple_penrose/penroses/end/'+name+'.svg'
    png_filename = 'C:/Users/demor/OneDrive/Documents/python_scripts/bad_apple_penrose/penroses/png_end/'+name+'.png'

    svg_code = open(svg_filename, 'rt').read()
    svg2png(bytestring=svg_code,write_to='output.png')

    #drawing = svg2rlg()
    #renderPM.drawToFile(drawing, 'C:/Users/demor/OneDrive/Documents/python_scripts/bad_apple_penrose/penroses/png_end/'+name+'.png', fmt="PNG")
