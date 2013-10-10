# Robert Yankou June 08 HW Romeo&Juliet

import pygame, math, time
from pygame.locals import *

#Function for change in r-value
def slope_r(t, r, j):
    sr = a*r+b*j
    return sr

#Function for change in j-value
def slope_j(t, r, j):
    sj = c*r+d*j
    return sj

#Function to check for blank values
def check(x, y):
    if x == "":
        x = float(y)
    else:
        x = float(x)
    return x

#Initial values entered by the user
print( "This reveals the complicated relationship between Romeo and Juliet.")
print("To automatically use suggested values, just hit enter.")
print( "The initial r-value is Romeo's initial love for Juliet.")
r = check(input("initial r-value (0): "), 0)
print( "The initial j-value is Juliet's initial love for Romeo.")
j = check(input("initial j-value (1): "), 1)
print( "The following four values directly\ninfluence the magnitude of the change")
print( "in love based on existing love.")
print( "The a-value changes Romeo's love\nfor Juliet based his existing love.")
a = check(input("a-value (0): "), 0)
print( "The b-value changes Romeo's love\nfor Juliet based on Juliet's existing love.")
b = check(input("b-value (1): "), 1)
print( "The c-value changes Juliet's love\nfor Romeo based her existing love.")
c = check(input("c-value (-1): "), -1)
print( "The d-value changes Juliet's love\nfor Romeo based on Romeo's existing love.")
d = check(input("d-value (-0.1): "), -0.1)
print( "The m-value is the magnitude of the graph.")
m = check(input("m-value (200): "), 200)
print( "The h-value is used to approximate.\nSmaller h = better accurracy but slower output.")
h = check(input("h-value (0.05): "), 0.05)
print( "The final t-value is how far the computer goes into the computation.")
tf = check(input("final t-value (70): "), 70)
t = float(0)

#Set up for graphics
running=True
W, H = 500, 500   #Screen size
r_zero, j_zero = W/2, H/2   #Origin
pygame.init()
screen=pygame.display.set_mode((W,H))
pygame.display.set_caption("Romeo&Juliet")
pygame.draw.line(screen, (128,128,128), (0,j_zero), (W,j_zero), 1) #r axis
pygame.draw.line(screen, (128,128,128), (r_zero,0), (r_zero,H), 1) #j axis
pygame.display.flip()
rold = r_zero+m*r   #initial r
jold = j_zero-m*j   #initial j
pygame.draw.circle(screen, (0,0,255), (int(rold),int(jold)), 5, 0)

#Loop containing Runge Kutta 4 & graphics
while abs(t) < tf:
    
    M1 = slope_r(t, r, j)
    K1 = slope_j(t, r, j)
    M2 = slope_r(t+h/2, r+M1*h/2, j+K1*h/2)
    K2 = slope_j(t+h/2, r+M1*h/2, j+K1*h/2)
    M3 = slope_r(t+h/2, r+M2*h/2, j+K2*h/2)
    K3 = slope_j(t+h/2, r+M2*h/2, j+K2*h/2)
    M4 = slope_r(t+h, r+M3*h, j+K3*h)
    K4 = slope_j(t+h, r+M3*h, j+K3*h)

    t += h
    r += (M1+2*M2+2*M3+M4)*h/6
    j += (K1+2*K2+2*K3+K4)*h/6

    pygame.draw.aaline(screen,(255,0,0),(rold,jold),(m*r+W/2,-m*j+H/2),1)
    pygame.display.flip()
    time.sleep(.0)   #adjust this number to speed up/slow the graph
    rold = m*r+W/2
    jold = -m*j+H/2

p = (r**2+j**2)
print()
print("The following value grades the accuracy of the approximation.")
print("The closer it is to one, the better the approximation.")
print(1-p)
print()
print("To quit the Graph, X out or hit escape.")

# Enables the ability to close the graph w/o crashing the program
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
pygame.display.quit()
