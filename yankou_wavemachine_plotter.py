#Robert Yankou, Wave Machine, last updated: 3 Aug 2010

import pygame, math, time, winsound
from pygame.locals import *

datafile = input("Data File Name? ")

file = open(datafile,'r')
line = file.readline()
n = int(line)
line = file.readline()
W = int(line)
line = file.readline()
H = int(line)
line = file.readline()
t = float(line)
line = file.readline()
tf = float(line)
line = file.readline()
h = float(line)

p = [0]*(int(2*n*(((tf-t)/h)+1)))
endp = [0]*4

for v in range(4):
    line = file.readline()
    xp = float(line)
    line = file.readline()
    yp = float(line)
    line = file.readline()
    zp = float(line)
    endp[v] = (xp,yp,zp) 

#while line != "":
for v in range(int(2*n*(((tf-t)/h)+1))):
    line = file.readline()
    #if line != "":
    xp = float(line)
    line = file.readline()
    yp = float(line)
    line = file.readline()
    zp = float(line)
    p[v] = (xp,yp,zp)

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

#Graphics set-up
running = True
pygame.init()
screen = pygame.display.set_mode((W,H))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0,0,0))
pygame.draw.aaline(background,(100,100,100),(endp[0][0]+W/2,endp[0][1]+H/2),(endp[1][0]+W/2,endp[1][1]+H/2),1)
pygame.draw.aaline(background,(200,255,0),(endp[2][0]+W/2,endp[2][1]+H/2),(endp[3][0]+W/2,endp[3][1]+H/2),1)

#print(endp[0][0]+W/2,endp[0][1]+H/2)
#print(endp[1][0]+W/2,endp[1][1]+H/2)

if pygame.font:
    font = pygame.font.Font(None, 20)
    text = font.render("by Robert Yankou (a.k.a. Bobby)", 1, (0,255,0))
    textpos = text.get_rect(left=1,top=1)
    background.blit(text, textpos)

screen.blit(background, (0, 0))
pygame.display.flip()

sleeptime = 0.01
quitter = 1
loop = 1

while loop == 1:

    i = 0

    while i < int(((tf-t)/h)+1):

        if quitter == 1:

            screen.blit(background, (0, 0))

            #Must draw axis line by creating 2-4 more points to be rotated
            #pygame.draw.line(screen,(0,100,0),(p[2*n*i+j][0]+W/2,p[2*n*i+j][1]+H/2),(p[2*n*i+j+n][0]+W/2,p[2*n*i+j+n][1]+H/2),1)
            for j in range(n):
                pygame.draw.line(screen,(100,100,100),(p[2*n*i+j][0]+W/2,p[2*n*i+j][1]+H/2),(p[2*n*i+j+n][0]+W/2,p[2*n*i+j+n][1]+H/2),1)
            for j in range(n):
                pygame.draw.circle(screen,(0,255,0),(int(p[2*n*i+j][0]+W/2),int(p[2*n*i+j][1]+H/2)), 3, 0)
            pygame.display.flip()

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
                                    i = 0
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
                        i = 0
                    else:
                        pause = 0

        i += 1

    time.sleep(1)
