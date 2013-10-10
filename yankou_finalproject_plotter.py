#Robert Yankou, Final Project, last updated: 3 Sept 2010
#Wave Surface using array of particles connected by springs
#Note: to speed up display, replace set_at with pygame.Surfarray

import pygame, math, time, winsound, struct
from pygame.locals import *

datafile = input("Data File Name? ")

print()
print("Please wait for the graphics window to open.")

circle_radius = 1
intensity = 10

file = open(datafile,'rb')
intsize = struct.calcsize('i')
line = file.read(intsize)
tup = struct.unpack('i', line)
n = tup[0]
intsize = struct.calcsize('i')
line = file.read(intsize)
tup = struct.unpack('i', line)
m = tup[0]
intsize = struct.calcsize('i')
line = file.read(intsize)
tup = struct.unpack('i', line)
W = tup[0]
intsize = struct.calcsize('i')
line = file.read(intsize)
tup = struct.unpack('i', line)
H = tup[0]
intsize = struct.calcsize('i')
line = file.read(intsize)
tup = struct.unpack('i', line)
t = tup[0]
intsize = struct.calcsize('i')
line = file.read(intsize)
tup = struct.unpack('i', line)
tf = tup[0]
floatsize = struct.calcsize('f')
line = file.read(floatsize)
tup = struct.unpack('f', line)
h = tup[0]
floatsize = struct.calcsize('f')
line = file.read(floatsize)
tup = struct.unpack('f', line)
anglea = tup[0]
floatsize = struct.calcsize('f')
line = file.read(floatsize)
tup = struct.unpack('f', line)
angleb = tup[0]
floatsize = struct.calcsize('f')
line = file.read(floatsize)
tup = struct.unpack('f', line)
anglec = tup[0]

#The following section can redefine the rotational angles written into the writer program
#"""
#Angles of rotation
anglea = 0*math.pi/6   #Rotation about the z-axis
angleb = 0*math.pi/4   #Rotation about the y-axis
anglec = 0.05*math.pi/2   #Rotation about the x-axis
#"""

endp = [0]*6
p = [[0 for col in range(int((tf-t)/h+1))] for row in range(int(m*n))]
gp = [[0 for col in range(int((tf-t)/h+1))] for row in range(int(m*n))]
x = [0]*int(m*n)
z = [0]*int(m*n)

for i in range(6):
    intsize = struct.calcsize('i')
    line = file.read(intsize)
    tup = struct.unpack('i', line)
    xp = tup[0]
    intsize = struct.calcsize('i')
    line = file.read(intsize)
    tup = struct.unpack('i', line)
    yp = tup[0]
    intsize = struct.calcsize('i')
    line = file.read(intsize)
    tup = struct.unpack('i', line)
    zp = tup[0]
    endp[i] = (xp,yp,zp)

for i in range(int(m*n)):
    intsize = struct.calcsize('i')
    line = file.read(intsize)
    tup = struct.unpack('i', line)
    xp = tup[0]
    intsize = struct.calcsize('i')
    line = file.read(intsize)
    tup = struct.unpack('i', line)
    zp = tup[0]
    x[i] = xp
    z[i] = zp

for j in range(int((tf-t)/h+1)):
    for i in range(int(m*n)):
#        intsize = struct.calcsize('i')
#        line = file.read(intsize)
#        tup = struct.unpack('i', line)
#        xp = tup[0]
        intsize = struct.calcsize('i')
        line = file.read(intsize)
        tup = struct.unpack('i', line)
        yp = tup[0]
#        intsize = struct.calcsize('i')
#        line = file.read(intsize)
#        tup = struct.unpack('i', line)
#        zp = tup[0]
        p[i][j] = yp
        gp[i][j] = (x[i],p[i][j],z[i])

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

for i in range(6):
    if anglea != 0:
        xp = endp[i][0]*a[0][0]+endp[i][1]*a[0][1]+endp[i][2]*a[0][2]
        yp = endp[i][0]*a[1][0]+endp[i][1]*a[1][1]+endp[i][2]*a[1][2]
        zp = endp[i][0]*a[2][0]+endp[i][1]*a[2][1]+endp[i][2]*a[2][2]

        endp[i] = (xp,yp,zp)

    if angleb != 0:
        xp = endp[i][0]*b[0][0]+endp[i][1]*b[0][1]+endp[i][2]*b[0][2]
        yp = endp[i][0]*b[1][0]+endp[i][1]*b[1][1]+endp[i][2]*b[1][2]
        zp = endp[i][0]*b[2][0]+endp[i][1]*b[2][1]+endp[i][2]*b[2][2]

        endp[i] = (xp,yp,zp)

    if anglec != 0:
        xp = endp[i][0]*c[0][0]+endp[i][1]*c[0][1]+endp[i][2]*c[0][2]
        yp = endp[i][0]*c[1][0]+endp[i][1]*c[1][1]+endp[i][2]*c[1][2]
        zp = endp[i][0]*c[2][0]+endp[i][1]*c[2][1]+endp[i][2]*c[2][2]

        endp[i] = (xp,yp,zp)

for j in range(int((tf-t)/h+1)):
    for i in range(int(m*n)):
        if anglea != 0:
            xp = x[i]*a[0][0]+p[i][j]*a[0][1]+z[i]*a[0][2]
            yp = x[i]*a[1][0]+p[i][j]*a[1][1]+z[i]*a[1][2]
            zp = x[i]*a[2][0]+p[i][j]*a[2][1]+z[i]*a[2][2]

            gp[i][j] = (xp,yp,zp)

        if angleb != 0:
            xp = x[i]*b[0][0]+p[i][j]*b[0][1]+z[i]*b[0][2]
            yp = x[i]*b[1][0]+p[i][j]*b[1][1]+z[i]*b[1][2]
            zp = x[i]*b[2][0]+p[i][j]*b[2][1]+z[i]*b[2][2]

            gp[i][j] = (xp,yp,zp)

        if anglec != 0:
            xp = x[i]*c[0][0]+p[i][j]*c[0][1]+z[i]*c[0][2]
            yp = x[i]*c[1][0]+p[i][j]*c[1][1]+z[i]*c[1][2]
            zp = x[i]*c[2][0]+p[i][j]*c[2][1]+z[i]*c[2][2]

            gp[i][j] = (xp,yp,zp)

print()
print("Controls:")
print("Pause/Play - Spacebar")
print("Restart - 'r' key")
print("Speed up - 'f' key or up arrow")
print("Slow down - 's' key or down arrow")
print("Quit - 'q' key or 'e' key or click the 'X' at the top right corner of the window")
print()
print("Note:")
print("Can restart or quit while paused")
print("If cannot run faster, beep will sound")
print()
print("Window on loop separated by 1 second pause")

running = True
pygame.init()
screen = pygame.display.set_mode((W,H))

#Values to set up loops
sleeptime = 0
quitter = 1
loop = 1
#Values to reduce division in loop
half_H = H/2
half_W = W/2

while loop == 1:

    j = 0

    while j < int((tf-t)/h+1):

        if quitter == 1:

#            screen.fill((0,0,0))

            pygame.draw.aaline(screen, (255,0,0), (endp[2][0]+W/2,endp[2][2]+H/2), (endp[3][0]+W/2,endp[3][2]+H/2), 1)
            pygame.draw.aaline(screen, (255,0,0), (endp[4][0]+W/2,endp[4][2]+H/2), (endp[5][0]+W/2,endp[5][2]+H/2), 1)
            pygame.draw.aaline(screen, (0,255,0), (endp[0][0]+W/2,endp[0][2]+H/2), (endp[1][0]+W/2,endp[1][2]+H/2), 1)
            for i in range(m*n):
                b = int(125 + intensity*p[i][j])
                r = int(125 - intensity*p[i][j])
                if r <= 0:
                    r = 0
                if b <= 0:
                    b = 0
                if r >= 255:
                    r = 255
                if b >= 255:
                    b = 255
#                print(b,r)
                pygame.draw.circle(screen, (255,b,0), (int(gp[i][j][0]+half_W),int(gp[i][j][2]+half_H)), circle_radius, 0)
#                pygame.draw.circle(screen, (255,255,255), (int(gp[i][j][0]+half_W),int(gp[i][j][2]+half_H)), circle_radius, 0)
#                screen.set_at((int(gp[i][j][0]+half_W),int(gp[i][j][2]+half_H)), (r,0,b))
            pygame.display.flip()
            for i in range(m*n):
#                screen.set_at((int(gp[i][j][0]+half_W),int(gp[i][j][2]+half_H)), (0,0,0))
                pygame.draw.circle(screen, (0,0,0), (int(gp[i][j][0]+half_W),int(gp[i][j][2]+half_H)), circle_radius, 0)

            time.sleep(sleeptime)

            pause = 1

            for event in pygame.event.get():
                while pause == 1:
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        while pause == 1:
                            for event in pygame.event.get():
                                if event.type == KEYDOWN and event.key == K_SPACE:
                                    pause = 0
                                elif event.type == QUIT or event.type == KEYDOWN and event.key == K_q or event.type == KEYDOWN and event.key == K_e:
                                    pause = 0
                                    quitter = 0
                                    i = int(((tf-t)/h)+2)
                                    loop = 0
                                    pygame.display.quit()
                                elif event.type == KEYDOWN and event.key == K_r:
                                    pause = 0
                                    j = 0
                    elif event.type == QUIT or event.type == KEYDOWN and event.key == K_q or event.type == KEYDOWN and event.key == K_e:
                        pause = 0
                        quitter = 0
                        i = int(((tf-t)/h)+2)
                        loop = 0
                        pygame.display.quit()
                    elif event.type == KEYDOWN and event.key == K_s or event.type == KEYDOWN and event.key == K_DOWN:
                        pause = 0
                        sleeptime += 0.01
                    elif event.type == KEYDOWN and event.key == K_f or event.type == KEYDOWN and event.key == K_UP:
                        pause = 0
                        sleeptime -= 0.01
                        if sleeptime <= 0:
                            sleeptime = 0
                            winsound.Beep(500,10)
                    elif event.type == KEYDOWN and event.key == K_r:
                        pause = 0
                        j = 0
                    else:
                        pause = 0

        j += 1

    time.sleep(1)
