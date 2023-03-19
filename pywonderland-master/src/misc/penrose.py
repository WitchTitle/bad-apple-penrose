"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Draw Penrose P3 tiling using substitution rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import cmath
import math
import random

# try:
#     import cairocffi as cairo
# except ImportError:
#     import cairo
import cairo


#IMAGE_SIZE = (1920, 1080)
IMAGE_SIZE = (800, 800)



PHI = (math.sqrt(5) - 1) / 2

RED = (0.697, 0.425, 0.333)
BLUE = (0, 0.4078, 0.5451)


BLACK = (0,0,0)
WHITE = (1,1,1)


def subdivide(triangles):
    result = []
    for color, A, B, C in triangles:
        if color == 0:
            # Subdivide red triangle
            P = A + (B - A) * PHI
            result += [(0, C, P, B), (1, P, C, A)]
        else:
            # Subdivide blue triangle
            Q = B + (A - B) * PHI
            R = B + (C - B) * PHI
            result += [(1, R, C, A), (1, Q, R, B), (0, R, Q, A)]
    return result

#load the bad apple image
from PIL import Image, ImageDraw
import sys
k=sys.argv[1]
#k = 100
b = len(str(k))-1 #1-9 returns 0, 10-99 returns 1, 100-999 returns 2...
zero = "0"*(5-b) #Sony vegas image sequences are name_000000
name = "a_"+zero + str(k) #an example of name is a_000123 (frame 123)

#NUM_ITERATIONS = 7
#NUM_ITERATIONS = 5
k = int(k)
if k < 50:
    NUM_ITERATIONS = 4
elif k < 100:
    NUM_ITERATIONS = 5
elif k < 150:
    NUM_ITERATIONS = 6
elif k < 200:
    NUM_ITERATIONS = 7
else:
    NUM_ITERATIONS = 8


source = Image.open("C:/Users/demor/OneDrive/Documents/python_scripts/bad_apple_penrose/penroses/binarized_square/"+name+".png").convert("L") #the source image in black and white
 

surface = cairo.SVGSurface(r"C:/Users/demor/OneDrive/Documents/python_scripts/bad_apple_penrose/penroses/end/"+ name + '.svg', IMAGE_SIZE[0], IMAGE_SIZE[1])
#surface = cairo.PNGSurface(r"C:/Users/demor/OneDrive/Documents/python_scripts/bad_apple_penrose/penroses/png_end/"+ name + '.png', IMAGE_SIZE[0], IMAGE_SIZE[1])

ctx = cairo.Context(surface)
ctx.translate(IMAGE_SIZE[0] / 2.0, IMAGE_SIZE[1] / 2.0)
wheel_radius = math.sqrt(IMAGE_SIZE[0] ** 2 + IMAGE_SIZE[1] ** 2) / math.sqrt(2)
#ctx.scale(wheel_radius, wheel_radius)
ctx.scale(0.5*wheel_radius, 0.5*wheel_radius)

# Create wheel of red triangles around the origin
triangles = []
for i in range(10):
    B = cmath.rect(1, (2 * i - 1) * math.pi / 10)
    C = cmath.rect(1, (2 * i + 1) * math.pi / 10)
    if i % 2 == 0:
        B, C = C, B  # Make sure to mirror every second triangle
    triangles.append((0, 0j, B, C))

for i in range(NUM_ITERATIONS):
    triangles = subdivide(triangles)

# Determine line width from size of the first triangle
color, A, B, C = triangles[0]
ctx.set_line_width(abs(B - A) / 10.0)
ctx.set_line_join(cairo.LINE_JOIN_ROUND)


from statistics import mean

max_dim = 0 #maximum Real or Imaginary component of any vector
for color, A, B, C in triangles:
    D = B + C - A
    for vec in [A, B, C, D]:
        if abs(vec.real) > max_dim:
            max_dim = abs(vec.real)
        if abs(vec.imag) > max_dim:
            max_dim = abs(vec.imag)
        


# Draw all rhombus
for color, A, B, C in triangles:

    D = B + C - A
    ctx.move_to(A.real, A.imag)
    ctx.line_to(B.real, B.imag)
    ctx.line_to(D.real, D.imag)
    ctx.line_to(C.real, C.imag)
    ctx.close_path()
    #print(f'A,B,C,D = {A} {B} {C} {D}')
    #print(color)

    #points inside the rhombus are A + u(B-A) + v(C-A) where u and v are in [0,1]
    # get 9 points in the interior of the rhombus
    interior_points = []
    for u in [0.25, 0.5, 0.75]:
        for v in [0.25, 0.5, 0.75]:
            interior_points.append(A + u*(B-A) + v*(C-A))

    #get the pixel values of the bad apple image at those coordinates
    pixel_values = []
    for interior_point in interior_points:

        # if abs(interior_point.real) > max_dim / 2 or abs(interior_point.imag) > max_dim / 2:
        #     continue


        #interior_points are complex numbers with real and imaginary parts in [-max_dim, max_dim]
        pixel_x =  source.width / 2 + source.width / 2 * (interior_point.real / max_dim)
        pixel_y =  source.height / 2 + source.height / 2 * (interior_point.imag / max_dim)
        val = source.getpixel( (pixel_x, pixel_y))

        # if abs(interior_point.real) > max_dim or abs(interior_point.imag) > max_dim:
        #     print(f'pixelx pixely = ({pixel_x, pixel_y}), interior_point = {interior_point}, source size is {source.size}, max_dim = {max_dim}')
        pixel_values.append(val)

    avg = mean(pixel_values)
    if avg > 128:
        ctx.set_source_rgb(*WHITE)
    else:
        ctx.set_source_rgb(*BLACK)

    # if color == 0:
    #     ctx.set_source_rgb(*RED)
    # else:
    #     ctx.set_source_rgb(*BLUE)

    ctx.fill_preserve()
    #ctx.set_source_rgb(0.2, 0.2, 0.2)
    ctx.set_source_rgb(0.5, 0.5, 0.5)

    

    ctx.stroke()

# import pickle
# pickle_filename = r'C:\Users\demor\OneDrive\Documents\python_scripts\bad_apple_penrose\pywonderland-master\triangle_data.pickle'
# pickle_out = open(pickle_filename,"wb")
# pickle.dump(triangles, pickle_out)
# pickle_out.close()

#surface.finish()
surface.write_to_png(r"C:/Users/demor/OneDrive/Documents/python_scripts/bad_apple_penrose/penroses/png_end/"+ name + '.png') 
