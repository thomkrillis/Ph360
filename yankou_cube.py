#Robert Yankou rotated cube
#This program was not assigned, exactly, but it is what I made to get rotation to work for the first time
#White lines are x & y axes, the rest are the cube

import pygame, math, time
from pygame.locals import *

#Create 8 points
#Translate all points according to a,b,c angles about z,y,x axes respectively
#Graph lines connecting adjacent points

#Initialize points

x = [-100,100]
y = [-100,100]
z = [-100,100]

p0 = (x[0],y[0],z[0])
p1 = (x[0],y[0],z[1])
p2 = (x[0],y[1],z[1])
p3 = (x[0],y[1],z[0])
p4 = (x[1],y[1],z[0])
p5 = (x[1],y[0],z[0])
p6 = (x[1],y[0],z[1])
p7 = (x[1],y[1],z[1])
p8 = (-x[1],y[0],z[0])
p9 = (x[1],y[0],z[0])
p10 = (x[0],-y[1],z[0])
p11 = (x[0],y[1],z[0])

p = [p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11]

#Angles of rotation
anglea = 1*math.pi/4
angleb = 0*math.pi/4
anglec = 2*math.pi/4

#Possible pathways for connecting the 8 corners of the cube
#Linear but 3 retraces
#path1: p1>p2>p3>p4>p5>p6>p7>p8>p5>p6>p1>p2>p7>p8>p3

#Nonlinear thus difficult
#path2: p1>p6,p1>p4,p1>p2,p5>p4,p5>p6,p5>p8,p7>p2,p7>p8,p7>p6,p3>p8,p3>p2,p3>p4

#Composite linear/non-linear
#path3:p1>p2>p3>p4>p5>p6>p7>p8>p5,p8>p3,p1>p6,p2>p7


#Defines matrices
a = [[0 for col in range(3)] for row in range(3)]
b = [[0 for col in range(3)] for row in range(3)]
c = [[0 for col in range(3)] for row in range(3)]


#Matrix angle a around z-axis
a[0][0]=math.cos(anglea)
a[0][1]=math.sin(anglea)
a[0][2]=0
a[1][0]=-math.sin(anglea)
a[1][1]=math.cos(anglea)
a[1][2]=0
a[2][0]=0
a[2][1]=0
a[2][2]=1

#Matrix angle b around y-axis
b[0][0]=math.cos(angleb)
b[0][1]=0
b[0][2]=math.sin(angleb)
b[1][0]=0
b[1][1]=1
b[1][2]=0
b[2][0]=-math.sin(angleb)
b[2][1]=0
b[2][2]=math.cos(angleb)

#Matrix angle c around x-axis
c[0][0]=1
c[0][1]=0
c[0][2]=0
c[1][0]=0
c[1][1]=math.cos(anglec)
c[1][2]=math.sin(anglec)
c[2][0]=0
c[2][1]=-math.sin(anglec)
c[2][2]=math.cos(anglec)

#Define [x,y,z]
d = p[0]
#print(a[0][0])

"""[[0 for col in range(1)] for row in range(3)]
d[0][0]=x
d[1][0]=y
d[2][0]=z"""

#Multiply matrices together
for f in range(12):
    if anglea != 0:
        xp = p[f][0]*a[0][0]+p[f][1]*a[0][1]+p[f][2]*a[0][2]
        yp = p[f][0]*a[1][0]+p[f][1]*a[1][1]+p[f][2]*a[1][2]
        zp = p[f][0]*a[2][0]+p[f][1]*a[2][1]+p[f][2]*a[2][2]

        p[f] = (xp,yp,zp)

    if angleb != 0:
        xp = p[f][0]*b[0][0]+p[f][1]*b[0][1]+p[f][2]*b[0][2]
        yp = p[f][0]*b[1][0]+p[f][1]*b[1][1]+p[f][2]*b[1][2]
        zp = p[f][0]*b[2][0]+p[f][1]*b[2][1]+p[f][2]*b[2][2]

        p[f] = (xp,yp,zp)

    if anglec != 0:
        xp = p[f][0]*c[0][0]+p[f][1]*c[0][1]+p[f][2]*c[0][2]
        yp = p[f][0]*c[1][0]+p[f][1]*c[1][1]+p[f][2]*c[1][2]
        zp = p[f][0]*c[2][0]+p[f][1]*c[2][1]+p[f][2]*c[2][2]

        p[f] = (xp,yp,zp)

running = True
W, H = 500, 500   #Screen size
pygame.init()
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption("Cube")
pygame.draw.line(screen, (255,255,255), (p[8][0]+W/2,p[8][1]+H/2), (p[9][0]+W/2,p[9][1]+H/2), 4) #x axis
pygame.draw.line(screen, (255,255,255), (p[10][0]+W/2,p[10][1]+H/2), (p[11][0]+W/2,p[11][1]+H/2), 4) #y axis
pygame.display.flip()

#path2: p1>p6,p1>p4,p1>p2,  p5>p4,p5>p6,p5>p8,  p7>p2,p7>p8,p7>p6,  p3>p8,p3>p2,p3>p4
pygame.draw.aaline(screen,(255,255,0),(p[0][0]+W/2,p[0][1]+H/2),(p[5][0]+W/2,p[5][1]+H/2),1)
pygame.draw.aaline(screen,(255,255,0),(p[0][0]+W/2,p[0][1]+H/2),(p[3][0]+W/2,p[3][1]+H/2),1)
pygame.draw.aaline(screen,(255,255,0),(p[0][0]+W/2,p[0][1]+H/2),(p[1][0]+W/2,p[1][1]+H/2),1)

pygame.draw.aaline(screen,(0,255,255),(p[4][0]+W/2,p[4][1]+H/2),(p[3][0]+W/2,p[3][1]+H/2),1)
pygame.draw.aaline(screen,(0,255,255),(p[4][0]+W/2,p[4][1]+H/2),(p[5][0]+W/2,p[5][1]+H/2),1)
pygame.draw.aaline(screen,(0,255,255),(p[4][0]+W/2,p[4][1]+H/2),(p[7][0]+W/2,p[7][1]+H/2),1)

pygame.draw.aaline(screen,(255,0,255),(p[6][0]+W/2,p[6][1]+H/2),(p[1][0]+W/2,p[1][1]+H/2),1)
pygame.draw.aaline(screen,(255,0,255),(p[6][0]+W/2,p[6][1]+H/2),(p[7][0]+W/2,p[7][1]+H/2),1)
pygame.draw.aaline(screen,(255,0,255),(p[6][0]+W/2,p[6][1]+H/2),(p[5][0]+W/2,p[5][1]+H/2),1)

pygame.draw.aaline(screen,(100,100,100),(p[2][0]+W/2,p[2][1]+H/2),(p[7][0]+W/2,p[7][1]+H/2),1)
pygame.draw.aaline(screen,(100,100,100),(p[2][0]+W/2,p[2][1]+H/2),(p[1][0]+W/2,p[1][1]+H/2),1)
pygame.draw.aaline(screen,(100,100,100),(p[2][0]+W/2,p[2][1]+H/2),(p[3][0]+W/2,p[3][1]+H/2),1)
pygame.display.flip()

# Enables the ability to close the graph w/o crashing the program
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
pygame.display.quit()

"""xold = x_zero+m*x   #initial x
yold = y_zero+m*y   #initial y"""

"""pygame.draw.aaline(screen,(255,255,0),(xold,yold),(m*x+W/2,-m*y+H/2),1)
pygame.draw.aaline(screen,(255,255,0),(0,0),(1,1),1)
pygame.display.flip()
time.sleep(.0)   #adjust this number to speed up/slow the graph
xold = m*x+W/4
yold = m*y+W/4"""

#Multiply product matrix with each point to solve for new points

#Graph new points to output using 2 of three coordinates

