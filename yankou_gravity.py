#Robert Yankou 2D Gravity 2 Masses
#Values entered by User upon running, suggested values shown
#Graphing window automatically fits to graph image

import pygame, math, time
from pygame.locals import *

#Function for slopes of x&y coordinates for M1&M2
def slope_x(m):
    sx = m
    return sx

#Function for slope of x-component of velocity for M1
def slope_vxm1(xm1, xm2, r):
    svxm1 = k*(xm2-xm1)/r
    return svxm1

#Function for slope of x-component of velocity for M2
def slope_vxm2(xm1, xm2, r):
    svxm2 = l*(xm1-xm2)/r
    return svxm2

#Function for slope of y-component of velocity for M1
def slope_vym1(ym1, ym2, r):
    svym1 = k*(ym2-ym1)/r
    return svym1

#Function for slope of y-component of velocity for M2
def slope_vym2(ym1, ym2, r):
    svym2 = l*(ym1-ym2)/r
    return svym2

#Function to check for blank values
def check(c, d):
    if c == "":
        c = float(d)
    else:
        c = float(c)
    return c

#Initial values and constants, some defined by the user
print("This program creates a graph showing the motion of")
print("two masses attracting each other by gravity in 2D.")
print("To automatically use suggested values, just hit enter.")
m1 = check(input("Mass m1(1,000,000,000): "), 1000000000)   #Mass 1
m2 = check(input("mass m2(100,000,000): "), 100000000)   #Mass 2
print("h-value is the step size for integration.")
print("As h approaches zero, the program runs")
print("More accurately but more slowly as well.")
h = check(input("h-value(0.01): "), 0.01)
print("Initial t-value is zero.")
tf = check(input("final t-value(50): "), 50)
W = check(input("Width of Graph(500): "), 500)
H = check(input("Height of Graph(500): "), 500)
print("Sleep time makes the Graph run more slowly.")
print("Sleep time should not exceed 0.05 seconds.")
sleeptime = check(input("Sleep time(0): "), 0)
xm1 = check(input("initial x-coordinate for M1(0): "), 0)
x1 = xm1
ym1 = check(input("initial y-coordinate for M1(0): "), 0)
y1 = ym1
vxm1 = check(input("initial x-component of velocity for M1(0): "), 0)
vx1 = vxm1
vym1 = check(input("initial y-component of velocity for M1(0): "), 0)
vy1 = vym1
xm2 = check(input("initial x-coordinate for M2(1): "), 1)
x2 = xm2
ym2 = check(input("initial y-coordinate for M2(1): "), 1)
y2 = ym2
vxm2 = check(input("initial x-component of velocity for M2(-0.1): "), -0.1)
vx2 = vxm2
vym2 = check(input("initial y-component of velocity for M2(0.1): "), 0.1)
vy2 = vym2
xmax = -1000000000
xmin = 1000000000
ymax = -1000000000
ymin = 1000000000
t = float(0)
G = float(6.673*pow(10, -11))   #Gravitational Constant
k = m2*G
l = m1*G

q = m1*(xm1*vym1-ym1*vxm1)+m2*(xm2*vym2-ym2*vxm2)

#print(m1*(xm1*vym1-ym1*vxm1)+m2*(xm2*vym2-ym2*vxm2))
#print((m1*(vxm1**2+vym1**2)+m2*(vxm2**2+vym2**2))/2-G*m1*m2/((xm1-xm2)**2+(ym1-ym2)**2)**(1/2))

while abs(t) < tf:

    r = pow(pow((xm1-xm2),2) + pow((ym1-ym2),2), 3/2)

    M11 = slope_x(vxm1)
    K11 = slope_vxm1(xm1, xm2, r)
    M21 = slope_x(vxm2)
    K21 = slope_vxm2(xm1, xm2, r)
    M31 = slope_x(vym1)
    K31 = slope_vym1(ym1, ym2, r)
    M41 = slope_x(vym2)
    K41 = slope_vym2(ym1, ym2, r)
    M12 = slope_x(vxm1+K11*h/2)
    K12 = slope_vxm1(xm1+M11*h/2, xm2+M21*h/2, r)
    M22 = slope_x(vxm2+K21*h/2)
    K22 = slope_vxm2(xm1+M11*h/2, xm2+M21*h/2, r)
    M32 = slope_x(vym1+K31*h/2)
    K32 = slope_vym1(ym1+M31*h/2, ym2+M41*h/2, r)
    M42 = slope_x(vym2+K41*h/2)
    K42 = slope_vym2(ym1+M31*h/2, ym2+M41*h/2, r)
    M13 = slope_x(vxm1+K12*h/2)
    K13 = slope_vxm1(xm1+M12*h/2, xm2+M22*h/2, r)
    M23 = slope_x(vxm2+K22*h/2)
    K23 = slope_vxm2(xm1+M12*h/2, xm2+M22*h/2, r)
    M33 = slope_x(vym1+K32*h/2)
    K33 = slope_vym1(ym1+M32*h/2, ym2+M42*h/2, r)
    M43 = slope_x(vym2+K42*h/2)
    K43 = slope_vym2(ym1+M32*h/2, ym2+M42*h/2, r)
    M14 = slope_x(vxm1+K13*h)
    K14 = slope_vxm1(xm1+M13*h, xm2+M23*h, r)
    M24 = slope_x(vxm2+K23*h)
    K24 = slope_vxm2(xm1+M13*h, xm2+M23*h, r)
    M34 = slope_x(vym1+K33*h)
    K34 = slope_vym1(ym1+M33*h, ym2+M43*h, r)
    M44 = slope_x(vym2+K43*h)
    K44 = slope_vym2(ym1+M33*h, ym2+M43*h, r)

    t += h
    xm1 += (M11+2*M12+2*M13+M14)*h/6
    vxm1 += (K11+2*K12+2*K13+K14)*h/6
    xm2 += (M21+2*M22+2*M23+M24)*h/6
    vxm2 += (K21+2*K22+2*K23+K24)*h/6
    ym1 += (M31+2*M32+2*M33+M34)*h/6
    vym1 += (K31+2*K32+2*K33+K34)*h/6
    ym2 += (M41+2*M42+2*M43+M44)*h/6
    vym2 += (K41+2*K42+2*K43+K44)*h/6

    #print(m1*(xm1*vym1-ym1*vxm1)+m2*(xm2*vym2-ym2*vxm2))
    #print((m1*(vxm1**2+vym1**2)+m2*(vxm2**2+vym2**2))/2-G*m1*m2/((xm1-xm2)**2+(ym1-ym2)**2)**(1/2))

    #print(m1*(xm1*vym1-ym1*vxm1)+m2*(xm2*vym2-ym2*vxm2))
    #print((m1*(vxm1**2+vym1**2)+m2*(vxm2**2+vym2**2))/2-G*m1*m2/((xm1-xm2)**2+(ym1-ym2)**2)**(1/2))

    if xmax < xm1:
        xmax = xm1
    if xmax < xm2:
        xmax = xm2
    if xmin > xm1:
        xmin = xm1
    if xmin > xm2:
        xmin = xm2
    if ymax < ym1:
        ymax = ym1
    if ymax < ym2:
        ymax = ym2
    if ymin > ym1:
        ymin = ym1
    if ymin > ym2:
        ymin = ym2
    #print(xmax)
    #print(xmin)
    #print(ymax)
    #print(ymin)
    #print(".")

p = m1*(xm1*vym1-ym1*vxm1)+m2*(xm2*vym2-ym2*vxm2)
#print(q-p)

#print(ymax, ymin)
mx = W/(xmax-xmin)
bx = -W*xmin/(xmax-xmin)
my = H/(ymin-ymax)
by = -H*ymax/(ymin-ymax)
#print(my, by)
xm1 = x1
ym1 = y1
vxm1 = vx1
vym1 = vy1
xm2 = x2
ym2 = y2
vxm2 = vx2
vym2 = vy2
t = float(0)

#Set up for graphics
running = True
xm1_zero, ym1_zero = W/2, H/2   #Origin
xm2_zero, ym2_zero = W/2, H/2   #Origin
pygame.init()
screen = pygame.display.set_mode((int(W),int(H)))
pygame.display.set_caption("Gravity")
pygame.draw.line(screen, (128,128,128), (0,by), (W,by), 1) #x axis
pygame.draw.line(screen, (128,128,128), (bx,0), (bx,H), 1) #y axis
pygame.display.flip()
xm1old = mx*xm1+bx   #initial xm1
ym1old = my*ym1+by   #initial ym1
xm2old = mx*xm2+bx   #initial xm2
ym2old = my*ym2+by   #initial ym2
#print(ym1old, ym2old)
pygame.draw.circle(screen, (255,255,0), (int(xm1old),int(ym1old)), 5, 0)
pygame.draw.circle(screen, (0,0,255), (int(xm2old),int(ym2old)), 5, 0)

#Main Loop containing RK4 and graphing
while abs(t) < tf:

    r = pow(pow((xm1-xm2),2) + pow((ym1-ym2),2), 3/2)

    M11 = slope_x(vxm1)
    K11 = slope_vxm1(xm1, xm2, r)
    M21 = slope_x(vxm2)
    K21 = slope_vxm2(xm1, xm2, r)
    M31 = slope_x(vym1)
    K31 = slope_vym1(ym1, ym2, r)
    M41 = slope_x(vym2)
    K41 = slope_vym2(ym1, ym2, r)
    M12 = slope_x(vxm1+K11*h/2)
    K12 = slope_vxm1(xm1+M11*h/2, xm2+M21*h/2, r)
    M22 = slope_x(vxm2+K21*h/2)
    K22 = slope_vxm2(xm1+M11*h/2, xm2+M21*h/2, r)
    M32 = slope_x(vym1+K31*h/2)
    K32 = slope_vym1(ym1+M31*h/2, ym2+M41*h/2, r)
    M42 = slope_x(vym2+K41*h/2)
    K42 = slope_vym2(ym1+M31*h/2, ym2+M41*h/2, r)
    M13 = slope_x(vxm1+K12*h/2)
    K13 = slope_vxm1(xm1+M12*h/2, xm2+M22*h/2, r)
    M23 = slope_x(vxm2+K22*h/2)
    K23 = slope_vxm2(xm1+M12*h/2, xm2+M22*h/2, r)
    M33 = slope_x(vym1+K32*h/2)
    K33 = slope_vym1(ym1+M32*h/2, ym2+M42*h/2, r)
    M43 = slope_x(vym2+K42*h/2)
    K43 = slope_vym2(ym1+M32*h/2, ym2+M42*h/2, r)
    M14 = slope_x(vxm1+K13*h)
    K14 = slope_vxm1(xm1+M13*h, xm2+M23*h, r)
    M24 = slope_x(vxm2+K23*h)
    K24 = slope_vxm2(xm1+M13*h, xm2+M23*h, r)
    M34 = slope_x(vym1+K33*h)
    K34 = slope_vym1(ym1+M33*h, ym2+M43*h, r)
    M44 = slope_x(vym2+K43*h)
    K44 = slope_vym2(ym1+M33*h, ym2+M43*h, r)

    t += h
    xm1 += (M11+2*M12+2*M13+M14)*h/6
    vxm1 += (K11+2*K12+2*K13+K14)*h/6
    xm2 += (M21+2*M22+2*M23+M24)*h/6
    vxm2 += (K21+2*K22+2*K23+K24)*h/6
    ym1 += (M31+2*M32+2*M33+M34)*h/6
    vym1 += (K31+2*K32+2*K33+K34)*h/6
    ym2 += (M41+2*M42+2*M43+M44)*h/6
    vym2 += (K41+2*K42+2*K43+K44)*h/6

    #print(m1*(xm1*vym1-ym1*vxm1)+m2*(xm2*vym2-ym2*vxm2))
    #print((m1*(vxm1**2+vym1**2)+m2*(vxm2**2+vym2**2))/2-G*m1*m2/((xm1-xm2)**2+(ym1-ym2)**2)**(1/2))
    #print(ym1old, ym2old)
    pygame.draw.aaline(screen,(255,0,0),(xm1old,ym1old),(mx*xm1+bx,my*ym1+by),1)
    pygame.draw.aaline(screen,(255,0,0),(xm2old,ym2old),(mx*xm2+bx,my*ym2+by),1)
    pygame.display.flip()
    time.sleep(sleeptime)
    xm1old = mx*xm1+bx
    ym1old = my*ym1+by
    xm2old = mx*xm2+bx
    ym2old = my*ym2+by

print("To quit the Graph, X out or hit escape.")

# Enables the ability to close the graph w/o crashing the program
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
pygame.display.quit()
