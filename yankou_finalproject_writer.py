#Robert Yankou, Final Project, last updated: 3 Sept 2010
#Wave Surface using array of particles connected by springs

import math, time, pygame, struct
from pygame.locals import *

def slope_y(v):
    slo_y = v
    return slo_y

def slope_v(y11,y10,y12,y01,y21,mass11,xhor00,xhor01,xvert00,xvert10,dhor00,dhor01,dvert00,dvert10,khor00,khor01,kvert00,kvert10,):   #x = sqrt(d**2+delta_y**2)
    slo_v = (((y10-y11)*khor00*(xhor00-dhor00)/xhor00)+((y12-y11)*khor01*(xhor01-dhor01)/xhor01)+((y01-y11)*kvert00*(xvert00-dvert00)/xvert00)+((y21-y11)*kvert10*(xvert10-dvert10)/xvert10))/mass11
    return slo_v

def driving_one(time):
    driv1 = -A*math.sin((time)*omega)
    return driv1

def driving_two(time):
    driv2 = A*math.sin((time)*omega)
    return driv2

#m by n array of particles, m+2 by n+2 array to include walls, springs connecting adjacent particles and walls (4 springs attached to each particle)
n = 41   #Number of Columns
m = 41   #Number of Rows
mass = [[1 for col in range(n+2)] for row in range(m+2)]   #Sets up an array for the mass of each particle plus the two walls
y = [[0 for col in range(n+2)] for row in range(m+2)]   #Sets up an array for the position of each particle plus the two walls
v = [[0 for col in range(n+2)] for row in range(m+2)]   #Sets up an array for the velocity of each particle plus the two walls
k_hor = [[0.5 for col in range(n+1)] for row in range(m)]   #Sets up an array for the horizontal spring constants
k_vert = [[0.5 for col in range(n)] for row in range(m+1)]   #Sets up an array for the verticle spring constants
#The closer the following d-values are to zero, the better, since the restoring force is only the y-component of the spring force
d_hor = [[0.001 for col in range(n+1)] for row in range(m)]   #Sets up an array for the distance between horizontally adjacent particles
d_vert = [[0.001 for col in range(n)] for row in range(m+1)]   #Sets up an array for the distance between vertically adjacent particles
delta_y_hor = [[0 for col in range(n+1)] for row in range(m)]
delta_y_vert = [[0 for col in range(n)] for row in range(m+1)]
x_hor = [[1 for col in range(n+1)] for row in range(m)]
x_vert = [[1 for col in range(n)] for row in range(m+1)]
p = [[0 for col in range(n+2)] for row in range(m+2)]   #Sets up an array for the axis coordinates of each particle
endp = [0]*6

#This makes a free boundary system, to fix the boundary comment out the following section
for i in range(m):
    k_hor[i][0] = 0
    k_hor[i][n] = 0
for i in range(n):
    k_vert[0][i] = 0
    k_vert[m][i] = 0

t = 0
tf = 60
h = 0.1
A = -100   #Amplitude for driving sinusoidal motion
omega = 0.5   #Omega for driving sinusoidal motion
W = 500   #Width of the screen/graphics window
H = 500   #Height of the screen/graphics window
mag = 100   #This currently does nothing
xscale = W/(n+1)   #For x-coordinates of particles, do not change
zscale = H/(m+1)   #For z-coordinates of particles, do not change

#Angles of rotation
anglea = 0*math.pi/6   #Rotation about the z-axis
angleb = 0*math.pi/4   #Rotation about the y-axis
anglec = 1*math.pi/4   #Rotation about the x-axis

#Controls where the two driving particles are placed on the grid
midrow = int((m+1)/2)
col = int((n+1)/8)
col1 = midrow - col
col2 = midrow + col

file = open("surfwave", 'wb')
file.write(struct.pack('i', n))
#file.write("\n")
file.write(struct.pack('i', m))
#file.write("\n")
file.write(struct.pack('i', W))
#file.write("\n")
file.write(struct.pack('i', H))
#file.write("\n")
file.write(struct.pack('i', t))
#file.write("\n")
file.write(struct.pack('i', tf))
#file.write("\n")
file.write(struct.pack('f', h))
#file.write("\n")
file.write(struct.pack('f', anglea))
#file.write("\n")
file.write(struct.pack('f', angleb))
#file.write("\n")
file.write(struct.pack('f', anglec))
#file.write("\n")

#Sets up positions of particles
for j in range(n):
    for i in range(m):
        xp = int(xscale*(j-(n-1)/2))
        yp = y[i+1][j+1]
        zp = int(zscale*(i-(m-1)/2))
        p[i+1][j+1] = (xp,yp,zp)

#Define coordinate axes
xp = 0
yp = 300
zp = 0
endp[0] = (xp,yp,zp)
endp[1] = (xp,-yp,zp)
xp = 0
yp = 0
zp = 300
endp[2] = (xp,yp,zp)
endp[3] = (xp,yp,-zp)
xp = 300
yp = 0
zp = 0
endp[4] = (xp,yp,zp)
endp[5] = (-xp,yp,zp)

for i in range(6):
    file.write(struct.pack('i', int(endp[i][0])))
#    file.write("\n")
    file.write(struct.pack('i', int(endp[i][1])))
#    file.write("\n")
    file.write(struct.pack('i', int(endp[i][2])))
#    file.write("\n")

for j in range(n):
    for i in range(m):
        file.write(struct.pack('i', int(p[i+1][j+1][0])))
#        file.write("\n")
        file.write(struct.pack('i', int(p[i+1][j+1][2])))
#        file.write("\n")

for j in range(n):
    for i in range(m):
        file.write(struct.pack('i', int(p[i+1][j+1][1])))
#        file.write("\n")

M1 = [[0 for col in range(n+2)] for row in range(m+2)]
K1 = [[0 for col in range(n+2)] for row in range(m+2)]
M2 = [[0 for col in range(n+2)] for row in range(m+2)]
K2 = [[0 for col in range(n+2)] for row in range(m+2)]
M3 = [[0 for col in range(n+2)] for row in range(m+2)]
K3 = [[0 for col in range(n+2)] for row in range(m+2)]
M4 = [[0 for col in range(n+2)] for row in range(m+2)]
K4 = [[0 for col in range(n+2)] for row in range(m+2)]

running = True
pygame.init()
screen = pygame.display.set_mode((120,30))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0,0,0))

if pygame.font:
    font = pygame.font.Font(None, 20)
    text = font.render("    % Complete", 1, (0,255,0))
    textpos = text.get_rect(left=1,top=1)
    background.blit(text, textpos)

screen.blit(background, (0, 0))
pygame.display.flip()

marker = 0
old_percent = 101

#Values to reduce division in loop
half_h = h/2
markermultiplier = 100/((tf-t)/h)

while t < tf:    
    for j in range(n):
        for i in range(m):
            delta_y_hor[i][j] = y[i+1][j+1]-y[i+1][j]
            delta_y_vert[i][j] = y[i+1][j+1]-y[i][j+1]
    for j in range(n):
        for i in range(m):
            if i == int((m+1)/2) and j == col1:
                y[i][j] = driving_one(t)
                M1[i][j] = 0                      
            elif i == int((m+1)/2) and j == col2:
                y[i][j] = driving_two(t)
                M1[i][j] = 0
            else:
                x_hor[i][j] = math.sqrt(d_hor[i][j]**2+delta_y_hor[i][j]**2)
                x_vert[i][j] = math.sqrt(d_vert[i][j]**2+delta_y_vert[i][j]**2)
    for j in range(n):
        for i in range(m):
            M1[i+1][j+1] = slope_y(v[i+1][j+1])
            K1[i+1][j+1] = slope_v(y[i+1][j+1],y[i+1][j],y[i+1][j+2],y[i][j+1],y[i+2][j+1],mass[i+1][j+1],x_hor[i][j],x_hor[i][j+1],x_vert[i][j],x_vert[i+1][j],d_hor[i][j],d_hor[i][j+1],d_vert[i][j],d_vert[i+1][j],k_hor[i][j],k_hor[i][j+1],k_vert[i][j],k_vert[i+1][j])

    for j in range(n):
        for i in range(m):
            delta_y_hor[i][j] = y[i+1][j+1]-y[i+1][j]
            delta_y_vert[i][j] = y[i+1][j+1]-y[i][j+1]
    for j in range(n):
        for i in range(m):
            if i == int((m+1)/2) and j == col1:
                y[i][j] = driving_one(t+half_h)
                M2[i][j] = 0                       
            elif i == int((m+1)/2) and j == col2:
                y[i][j] = driving_two(t+half_h)
                M2[i][j] = 0  
            else:
                x_hor[i][j] = math.sqrt(d_hor[i][j]**2+delta_y_hor[i][j]**2)
                x_vert[i][j] = math.sqrt(d_vert[i][j]**2+delta_y_vert[i][j]**2)      
    for j in range(n):
        for i in range(m):
            M2[i+1][j+1] = slope_y(v[i+1][j+1]+K1[i+1][j+1]*half_h)
            K2[i+1][j+1] = slope_v(y[i+1][j+1]+M1[i+1][j+1]*half_h,y[i+1][j]+M1[i+1][j]*half_h,y[i+1][j+2]+M1[i+1][j+2]*half_h,y[i][j+1]+M1[i][j+1]*half_h,y[i+2][j+1]+M1[i+2][j+1]*half_h,mass[i+1][j+1],x_hor[i][j],x_hor[i][j+1],x_vert[i][j],x_vert[i+1][j],d_hor[i][j],d_hor[i][j+1],d_vert[i][j],d_vert[i+1][j],k_hor[i][j],k_hor[i][j+1],k_vert[i][j],k_vert[i+1][j])

    for j in range(n):
        for i in range(m):
            delta_y_hor[i][j] = y[i+1][j+1]-y[i+1][j]
            delta_y_vert[i][j] = y[i+1][j+1]-y[i][j+1]
    for j in range(n):
        for i in range(m):
            if i == int((m+1)/2) and j == col1:
                y[i][j] = driving_one(t+half_h)
                M3[i][j] = 0                     
            if i == int((m+1)/2) and j == col2:
                y[i][j] = driving_two(t+half_h)
                M3[i][j] = 0  
            else:
                x_hor[i][j] = math.sqrt(d_hor[i][j]**2+delta_y_hor[i][j]**2)
                x_vert[i][j] = math.sqrt(d_vert[i][j]**2+delta_y_vert[i][j]**2)        
    for j in range(n):
        for i in range(m):
            M3[i+1][j+1] = slope_y(v[i+1][j+1]+K2[i+1][j+1]*half_h)
            K3[i+1][j+1] = slope_v(y[i+1][j+1]+M2[i+1][j+1]*half_h,y[i+1][j]+M2[i+1][j]*half_h,y[i+1][j+2]+M2[i+1][j+2]*half_h,y[i][j+1]+M2[i][j+1]*half_h,y[i+2][j+1]+M2[i+2][j+1]*half_h,mass[i+1][j+1],x_hor[i][j],x_hor[i][j+1],x_vert[i][j],x_vert[i+1][j],d_hor[i][j],d_hor[i][j+1],d_vert[i][j],d_vert[i+1][j],k_hor[i][j],k_hor[i][j+1],k_vert[i][j],k_vert[i+1][j])

    for j in range(n):
        for i in range(m):
            delta_y_hor[i][j] = y[i+1][j+1]-y[i+1][j]
            delta_y_vert[i][j] = y[i+1][j+1]-y[i][j+1]
    for j in range(n):
        for i in range(m):
            if i == int((m+1)/2) and j == col1:
                y[i][j] = driving_one(t+h)
                M4[i][j] = 0                        
            elif i == int((m+1)/2) and j == col2:
                y[i][j] = driving_two(t+h)
                M4[i][j] = 0  
            else:
                x_hor[i][j] = math.sqrt(d_hor[i][j]**2+delta_y_hor[i][j]**2)
                x_vert[i][j] = math.sqrt(d_vert[i][j]**2+delta_y_vert[i][j]**2)       
    for j in range(n):
        for i in range(m):
            M4[i+1][j+1] = slope_y(v[i+1][j+1]+K3[i+1][j+1]*h)
            K4[i+1][j+1] = slope_v(y[i+1][j+1]+M3[i+1][j+1]*h,y[i+1][j]+M3[i+1][j]*h,y[i+1][j+2]+M3[i+1][j+2]*h,y[i][j+1]+M3[i][j+1]*h,y[i+2][j+1]+M3[i+2][j+1]*h,mass[i+1][j+1],x_hor[i][j],x_hor[i][j+1],x_vert[i][j],x_vert[i+1][j],d_hor[i][j],d_hor[i][j+1],d_vert[i][j],d_vert[i+1][j],k_hor[i][j],k_hor[i][j+1],k_vert[i][j],k_vert[i+1][j])

    for j in range(n):
        for i in range(m):
            y[i+1][j+1] += (M1[i+1][j+1]+2*M2[i+1][j+1]+2*M3[i+1][j+1]+M4[i+1][j+1])*h/6
            v[i+1][j+1] += (K1[i+1][j+1]+2*K2[i+1][j+1]+2*K3[i+1][j+1]+K4[i+1][j+1])*h/6
    t += h

    for j in range(n):
        for i in range(m):
            xp = int(xscale*(j-(n-1)/2))
            yp = y[i+1][j+1]
            zp = int(zscale*(i-(m-1)/2))
            p[i+1][j+1] = (xp,yp,zp)

    for j in range(n):
        for i in range(m):
            file.write(struct.pack('i', int(p[i+1][j+1][1])))

    marker += 1

    percent = int(marker*markermultiplier)

    if percent != old_percent:
        screen.blit(background, (0, 0))
        strp = str(percent)
        if pygame.font:
            font = pygame.font.Font(None, 20)
            text = font.render((strp), 1, (255,0,0))
            textpos = text.get_rect(left=1,top=1)
            screen.blit(text, textpos)

        pygame.display.flip()

    old_percent = percent

file.close()

print("Done.")

pygame.display.quit()
