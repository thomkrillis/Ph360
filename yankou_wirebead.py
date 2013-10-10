# Robert Yankou Bead on a String
# The x & y position of the bead is shown at the top left of the Graph
# All values are coded in
# After running, only click on the graph to place the bead
# Several string(path) alternatives left commented out under x & y functions
# The winsound works correctly but sounds pretty bad (since to sound good, it would slow down the simulation)

import pygame, math, time, pygame.time, winsound
from pygame.locals import *

#Function for x(t)
def x_t(t):
    #if t > 0:
    #    xt = -t+3
    #else:
    #    xt = t+3
    #xt = 10*(math.cos(t))*(math.e**math.cos(t) - 2*math.cos(4*t) - math.sin(t/12)**5)
    #xt = 100*math.cos(t)
    xt = t

    return xt

#Function for y(t)
def y_t(t):
    #if t > 0:
    #    yt = -(t-3)**2+9
    #else:
    #    yt = (t+3)**2-9
    #yt = 10*(math.sin(t))*(math.e**math.cos(t) - 2*math.cos(4*t) - math.sin(t/12)**5)
    #yt = 100*math.sin(t)
    yt = t**2

    return yt

#Function for slope of p
def slope_p(q):
    sp = q
    return sp

#Function for slope of q
def slope_q(k,q):
    sq = -(k/(1+k**2)**(1/2))-q*b/m
    return sq

#Note: pl refers to position calculated from parametric equations, p is position calculated by RK4
#Function to find pl item corresponding to p
def find_k(A, value, low, high):
    if A[int(low)] >= value:
        return 1
    if A[int(high)] <= value:
        return n
    while A[int(low)] < A[int(high)]:
        mid = (low + high) / 2
        if A[int(mid)] > value:
            if int(mid) == n:
                high = mid - 1
            else:
                if A[int(mid + 1)] < value:
                    high = mid
                else:
                    high = mid - 1
        elif A[int(mid)] < value:
            if int(mid) == 0:
                low = mid + 1
            else:
                if A[int(mid + 1)] > value:
                    low = mid
                else:
                    low = mid + 1
        else:
            if int(mid) == 0:
                return int(mid) + 1
            else:
                return int(mid)
    if A[int(low)] == A[int(high)]:
        if A[int(low)] > value:
            return int(low)
        elif A[int(low)] < value:
            if int(low) == n:
                return n
            else:
                return int(low) + 1
        elif A[int(low)] == value:
            if int(low) == 0:
                return 1
            elif int(low) == n:
                return n
            else:
                return int(low)

#Function to check for blank values
def check(r, j):
    if r == "":
        r = float(j)
    else:
        r = float(r)
    return r

#Values for the curve
t = float(-10)   #Initial t for curve
tf = 10   #Final t for curve
h = 0.01   #For curve
n = int((tf-t)/h)

#Lists
tl = [0]*(int(((tf-t)/h)+1))
xl = [0]*(int(((tf-t)/h)+1))
yl = [0]*(int(((tf-t)/h)+1))
pl = [0]*(int(((tf-t)/h)+1))

#Values
tl[0] = t   #Initial tl
b = 0   #Coefficient for friction
m = 1   #Mass of the bead
mag = 5   #Magnification of the graph
p = float(0)   #Initial p
q = float(0)   #Initial q/Initial tangential speed of bead
xl[0] = x_t(tl[0])   #Initial x
yl[0] = y_t(tl[0])   #Initial y
pl[0] = p   #Initial pl

#Defines all items in the lists
for i in range(int((tf-t)/h)):
    tl[i+1] = tl[i]+h
    xl[i+1] = x_t(tl[i+1])
    yl[i+1] = y_t(tl[i+1])
    pl[i+1] = pl[i]+((xl[i+1]-xl[i])**2+(yl[i+1]-yl[i])**2)**(1/2)

#Set-up graphics
running = 1
running2 = 1
pygame.init()
W,H = 500,500
screen = pygame.display.set_mode((W,H))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0,0,0))
pygame.draw.line(background,(128,128,128),(0,H/2),(W,H/2),1)
pygame.draw.line(background,(128,128,128),(W/2,0),(W/2,H),1)

#Draw curve
for i in range(int((tf-t)/h)):
    pygame.draw.aaline(background, (255,255,255), (mag*xl[i]+W/2,-mag*yl[i]+H/2), (mag*xl[i+1]+W/2,-mag*yl[i+1]+H/2), 1)
    pygame.display.flip()

#Create 'position' box in top left
if pygame.font:
    font = pygame.font.Font(None, 18)
    text = font.render("Position:", 1, (255,0,0))
    textpos = text.get_rect(left=1,top=1)
    background.blit(text, textpos)

screen.blit(background, (0, 0))
pygame.display.flip()

#Reset Values for the bead
tn = float(0)   #Initial t for bead
tfn = 20   #Final t for bead
hn = 0.01   #For bead

while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    elif event.type == pygame.MOUSEBUTTONDOWN:
        clicx,clicy = event.pos
        running = 0

c = 1000000
for i in range(int((tf-t)/h)):
    xdist = abs(clicx-mag*xl[i]-W/2)
    ydist = abs(clicy+mag*yl[i]-H/2)
    if xdist+ydist < c:
        f = i
        c = xdist+ydist

p = pl[f]   #Initial p for bead

d = find_k(pl, p, 0, n)
x = xl[d-1]
y = yl[d-1]

pygame.draw.circle(screen, (0,0,255), (int(mag*x+W/2), int(-mag*y+H/2)), 5, 0)
pygame.display.flip()

ener = m*(q**2+y)/2

g = 50

#Loop containing Runge Kutta 4
#Need to figure out issue with k-value
while abs(tn) < tfn:

    screen.blit(background, (0, 0))

    d = find_k(pl, p, 0, n)
    k = (yl[d]-yl[d-1])/(xl[d]-xl[d-1])
    M1 = slope_p(q)
    if xl[d] >= xl [d-1]:
        K1 = slope_q(k,q)
    elif xl[d] < xl[d-1]:
        K1 = slope_q(-k,q)

    d = find_k(pl, p+M1*hn/2, 0, n)
    k = (yl[d]-yl[d-1])/(xl[d]-xl[d-1])
    M2 = slope_p(q+K1*hn/2)
    if xl[d] >= xl [d-1]:
        K2 = slope_q(k,q+K1*hn/2)
    elif xl[d] < xl[d-1]:
        K2 = slope_q(-k,q+K1*hn/2)

    d = find_k(pl, p+M2*hn/2, 0, n)
    k = (yl[d]-yl[d-1])/(xl[d]-xl[d-1])
    M3 = slope_p(q+K2*hn/2)
    if xl[d] >= xl [d-1]:
        K3 = slope_q(k,q+K2*hn/2)
    elif xl[d] < xl[d-1]:
        K3 = slope_q(-k,q+K2*hn/2)

    d = find_k(pl, p+M3*hn, 0, n)
    k = (yl[d]-yl[d-1])/(xl[d]-xl[d-1])
    M4 = slope_p(q+K3*hn)
    if xl[d] >= xl [d-1]:
        K4 = slope_q(k,q+K3*hn)
    elif xl[d] < xl[d-1]:
        K4 = slope_q(-k,q+K3*hn)

    tn += hn
    p += (M1+2*M2+2*M3+M4)*hn/6
    q += (K1+2*K2+2*K3+K4)*hn/6

    d = find_k(pl, p, 0, n)
    x = xl[d]
    y = yl[d]

    background.fill((0,0,0),(60,1,440,14))
    strp = str((int(x),int(y)))
    if pygame.font:
        font = pygame.font.Font(None, 18)
        text = font.render((strp), 1, (255,0,0))
        textpos = text.get_rect(left=60,top=1)
        background.blit(text, textpos)


    pygame.draw.circle(screen, (0,0,255), (int(mag*x+W/2), int(-mag*y+H/2)), 5, 0)
    pygame.display.flip()

# v is the value being used for winsound
# If the print statement is uncommented, you can see that it corresponds to the velocity of the bead
    v = abs(int(g*q))+37
#    print(v)
    winsound.Beep(v,1)

    #time.sleep(0.01)

#enerf = m*(q**2+y)/2
#print(h, hn, enerf-ener)

#Close graph
while running2:
    for event in pygame.event.get():
        if event.type == QUIT:
            running2 = 0
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running2 = 0
pygame.display.quit()

#To Add:
#Prompt to select the x(t) & y(t)
#Autoscaling of graphics, driven by the bead, not the curve
#Spring to push/pull on bead from a point
#Warning when bead reaches one end of the curve, currently waits there until velocity reverses direction
