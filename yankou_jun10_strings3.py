#Robert Yankou Wind-Up System
#An early version of the wave machine, it has only 2 rods.
#The output is in function graph form in terms of theta_1, omega_1,
#theta_2, and omega_2, respectively from top left to bottom right.

import pygame, math, time
from pygame.locals import *

def slope_th1(om1):
    sx = om1
    return sx

def slope_om1(th1, th2):
    sy = -a*th1+c*(th2-th1)
    return sy

def slope_th2(om2):
    sxx = om2
    return sxx

def slope_om2(th1, th2):
    syy = -b*th2+d*(th1-th2)
    return syy

def check(c, d):
    if c == "":
        c = float(d)
    else:
        c = float(c)
    return c
print("This wind up system has two rods that rotate at their centers.")
print("They are connected to each other and 2 walls by a total of 3 springs.")
print("To automatically use suggested values, just hit enter.")
print("Note: it is best to use the suggested values at first.")
print()
print("The I-values are the rotational inertia of each rod.")
I1 = check(input("I1-value(1): "), 1)
I2 = check(input("I2-value(1): "), 1)
print("The k-values are for the springs connecting the rods to the walls.")
k1 = check(input("k1-value(2): "), 2)
k2 = check(input("k2-value(2): "), 2)
print("The a-value is for the spring connecting the two rods.")
a = check(input("a-value(1): "), 1)
print("The m-value controls the scale of the Graph.")
m = check(input("m-value(6): "), 6)
print("h-value is the step size for integration.")
print("As h approaches zero, the program runs")
print("More accurately but more slowly as well.")
h = check(input("h-value(0.05): "), 0.05)
print("Initial t-value is zero.")
tf = check(input("final t-value(20): "), 20)
print("theta and omega are the rotational theta's and omega's of each rod.")
th1 = check(input("initial theta one(10): "), 10)
om1 = check(input("initial omega one(0): "), 0)
th2 = check(input("initial theta two(0): "), 0)
om2 = check(input("initial omega two(10): "), 10)
t = float(0)
a = k1/I1
b = k2/I2
c = a/I1
d = a/I2

print()
print("The graph of theta one vs. time is in the top left.")
print("Top right is omega one, and theta and omega two are below.")

#Set up for graphics
running = True
W, H = 500, 500   #Screen size
t_zero, tt_zero = W/4, 3*W/4
th1_zero, om1_zero, th2_zero, om2_zero = H/4, H/4, 3*H/4, 3*H/4   #Origin
pygame.init()
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption("Theta1, Omega1, Theta2, & Omega2 vs. t")
pygame.draw.line(screen, (128,128,128), (0,H/4), (W,H/4), 1) #t axis
pygame.draw.line(screen, (128,128,128), (0,H/2), (W,H/2), 1) #t axis
pygame.draw.line(screen, (128,128,128), (0,3*H/4), (W,3*H/4), 1) #t axis
pygame.draw.line(screen, (128,128,128), (W/4,0), (W/4,H), 1) #t axis
pygame.draw.line(screen, (128,128,128), (W/2,0), (W/2,H), 1) #x axis
pygame.draw.line(screen, (128,128,128), (3*W/4,0), (3*W/4,H), 1) #t axis
pygame.display.flip()
told = t_zero+m*t   #initial t
ttold = tt_zero+m*t
th1old = th1_zero-m*th1   #initial theta1
om1old = om1_zero-m*om1   #initial omega1
th2old = th2_zero-m*th2   #initial theta2
om2old = om2_zero-m*om2   #initial omega2
pygame.draw.circle(screen, (0,0,255), (int(told),int(th1old)), 5, 0)
pygame.draw.circle(screen, (0,0,255), (int(ttold),int(om1old)), 5, 0)
pygame.draw.circle(screen, (0,0,255), (int(told),int(th2old)), 5, 0)
pygame.draw.circle(screen, (0,0,255), (int(ttold),int(om2old)), 5, 0)

while abs(t) < tf:

    M1 = slope_th1(om1)
    K1 = slope_om1(th1, th2)
    MM1 = slope_th2(om2)
    KK1 = slope_om2(th1, th2)
    M2 = slope_th1(om1+K1*h/2)
    K2 = slope_om1(th1+M1*h/2, th2+MM1*h/2)
    MM2 = slope_th2(om2+KK1*h/2)
    KK2 = slope_om2(th1+M1*h/2, th2+MM1*h/2)
    M3 = slope_th1(om1+K2*h/2)
    K3 = slope_om1(th1+M2*h/2, th2+MM2*h/2)
    MM3 = slope_th2(om2+KK2*h/2)
    KK3 = slope_om2(th1+M2*h/2, th2+MM2*h/2)
    M4 = slope_th1(om1+K3*h)
    K4 = slope_om1(th1+M3*h, th2+MM3*h)
    MM4 = slope_th2(om2+KK3*h)
    KK4 = slope_om2(th1+M3*h, th2+MM3*h)

    t += h
    th1 += (M1+2*M2+2*M3+M4)*h/6
    om1 += (K1+2*K2+2*K3+K4)*h/6
    th2 += (MM1+2*MM2+2*MM3+MM4)*h/6
    om2 += (KK1+2*KK2+2*KK3+KK4)*h/6

    pygame.draw.aaline(screen,(255,0,0),(told,th1old),(m*t+W/4,-m*th1+H/4),1)
    pygame.draw.aaline(screen,(0,255,0),(ttold,om1old),(m*t+3*W/4,-m*om1+H/4),1)
    pygame.draw.aaline(screen,(255,255,255),(told,th2old),(m*t+W/4,-m*th2+3*H/4),1)
    pygame.draw.aaline(screen,(255,255,0),(ttold,om2old),(m*t+3*W/4,-m*om2+3*H/4),1)
    pygame.display.flip()
    time.sleep(.0)   #adjust this number to speed up/slow the graph
    told = m*t+W/4
    ttold = m*t+3*W/4
    th1old = -m*th1+H/4
    om1old = -m*om1+H/4
    th2old = -m*th2+3*H/4
    om2old = -m*om2+3*H/4

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
