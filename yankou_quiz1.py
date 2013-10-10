#Robert Yankou quiz uncorrected
#Warning: do not run this program; it is in an eternal while loop
#All of the mistakes are at the bottom, the critical one being that t does not increase inside the loop

import pygame, time, math
from pygame.locals import *

def slope_x(vx):
    sx = vx
    return sx

def slope_y(vy):
    sy = vy
    return sy

def slope_z(vz):
    sz = vz
    return sz

def slope_vx(vy,vz,By,Bz):
    svx = vy*Bz-vz*By
    return svx

def slope_vy(vx,vz,Bx,Bz):
    svy = vz*Bx-vx*Bz
    return svy

def slope_vz(vx,vy,Bx,By):
    svz = vx*By-vy*Bx
    return svz

Bx = 0
By = 0
Bz = 10
x = 0
y = 0
z = 0
vx = 1
vy = 1
vz = 1
t = 0
tf = 10
h = 0.05

running = True
W,H = 500,500
pygame.init()
screen = pygame.display.set_mode((W,H))
pygame.draw.line(screen,(128,128,128),(0,H/2),(W,H/2),1)
pygame.draw.line(screen,(128,128,128),(W/2,0),(W/2,H),1)
pygame.display.flip()

xold = W/2 + x
yold = H/2 - y
pygame.draw.circle(screen,(255,0,0),(xold,yold),5,1)

print(x,y,z,vx,vy,vz)
print("KE= ", ((vx**2+vy**2+vz**2)/2))

while abs(t)<tf:
      M1=slope_x(vx)
      J1=slope_vx(vy,vz,By,Bz)
      N1=slope_y(vy)
      K1=slope_vy(vx,vz,Bx,Bz)
      O1=slope_z(vz)
      L1=slope_vz(vx,vy,Bx,By)
      M2=slope_x(vx+J1*h/2)
      J2=slope_vx(vy+K1*h/2,vz+L1*h/2,By,Bz)
      N2=slope_y(vy+K1*h/2)
      K2=slope_vy(vx+J1*h/2,vz+L1*h/2,Bx,Bz)
      O2=slope_z(vz+L1*h/2)
      L2=slope_vz(vx+J1*h/2,vy+K1*h/2,Bx,By)
      M3=slope_x(vx+J2*h/2)
      J3=slope_vx(vy+K2*h/2,vz+L2*h/2,By,Bz)
      N3=slope_y(vy+K2*h/2)
      K3=slope_vy(vx+J2*h/2,vz+L2*h/2,Bx,Bz)
      O3=slope_z(vz+L2*h/2)
      L3=slope_vz(vx+J2*h/2,vy+K2*h/2,Bx,By)
      M4=slope_x(vx+J3*h)
      J4=slope_vx(vy+K3*h,vz+L3*h,By,Bz)
      N4=slope_y(vy+K3*h)
      K4=slope_vy(vx+J3*h,vz+L3*h,Bx,Bz)
      O4=slope_z(vz+L3*h)
      L4=slope_vz(vx+J3*h,vy+K3*h,Bx,By)

      x += (M1+2*M2+2*M3+M4)*h/6
      y += (N1+2*N2+2*N3+N4)*h/6
      z += (O1+2*O2+2*O3+O4)*h/6
      vx += (J1+2*J2+2*J3+J4)*h/6
      vy += (K1+2*K2+2*K3+K4)*h/6
      vz += (L1+2*L2+2*L3+L4)*h/6

      xnew = W/2 + x
      ynew = H/2 - y

      pygame.draw.aaline(screen,(0,0,255),(xold,yold),(xnew,ynew),1)
      pygame.display.flip()

      xold = xnew
      yold = ynew

print(x,y,z,vx,vy,vz)
print("KE= ", ((vx**2+vy**2+vz**2)/2))

while running:
      for event in pygame.event.get()==Quit:
          running = False
pygame.display.quit()

#Left m&q out completely
#Assumed values for vx,vy,vz,Bz,tf&h
#Did not fit or scale graph, assumed values for W&H
#Could have used 2 functions instead of 6
#Did not have to set B's as inputs of functions since they are constant
