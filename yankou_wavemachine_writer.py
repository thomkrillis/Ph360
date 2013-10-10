#Robert Yankou, Wave Machine writer, last updated: 3 Aug 2010
#Values are coded in

import math, time
from pygame.locals import *

def slope_th(om):
    sth = om
    return sth

def slope_om(k2,k1,th2,th1,th0,I1):
    som = (k2*(th2-th1)+k1*(th0-th1))/I1
    return som

def check(c, d):
    if c == "":
        c = float(d)
    else:
        c = float(c)
    return c

#This begins section for user-set values
#Different settings for select:
    #1 sends a single pulse from the first rod
    #2 same as 1 for first and last rod
        #sign = -1 for destructive interference
        #sign = 1 for constructive interference
    #3 continuous motion of the first rod
    #4 same as 2 for first and last rod
        #sign = -1 for destructive interference
        #sign = 1 for constructive interference
select = 2
sign = -1
Boundary = 0   #1 sets fixed boundary, 0 sets free boundary
read = 0   #1 to read from a file, 0 not to read from a file
if read == 1:
    file = open('moment','r') 
    line = file.readline()
    n = int(line)   #Number of rods
else:
    n = 41   #Number of rods
t = float(0)   #Initial time
tf = float(50)   #Final time
h = float(.1)
C = 1   #Constant (Rotational Inertia = Constant times Length)
A = 1
freq = 0.29
W = 500   #Width of screen
H = 310   #Height of screen
xscale = W/(n+1)   #For x-coordinates of rods, do not change

th = [0]*(n+2)   #Sets up a list for the theta of each rod plus the two walls
om = [0]*(n+2)   #Sets up a list for the omega of each rod plus the two walls
k = [75]*(n+1)   #Sets up a list for the spring constants
p = [0]*(n*2)   #Sets up a list for the endpoints of each rod
endp = [0]*4
#q = [0]*(n*2+4)
L = [100]*n   #Sets up a list for the length of each rod
I = [100]*n   #Sets up a list for the moment of inertia of each rod
M1 = [0]*(n+2)
K1 = [0]*(n+2)
M2 = [0]*(n+2)
K2 = [0]*(n+2)
M3 = [0]*(n+2)
K3 = [0]*(n+2)
M4 = [0]*(n+2)
K4 = [0]*(n+2)

#Initial conditions for specific cases
if Boundary == 0:
    k[0] = 0
    k[n] = 0

#Keep th[0]=0,th[n+1]=0,om[0]=0,om[n+1]=0
th[0]=0
th[n+1]=0
om[0]=0
om[n+1]=0
#th[int((n+1)/2)] = -math.pi/2   #int((n+1)/2) is the middle rod
#om[int((n+1)/2)] = 100   #int((n+1)/2) is the middle rod

#Change rod lengths (from original length: 100)
if read == 1:
    for i in range(n):
        line = file.readline()
        L[i] = int(line)   
    file.close()
#else:   #use this section to make non-uniform rod lengths without reading in a data file
#    for i in range(int((n+1)/2)):
#        L[i+int(n/2)] = 300

#Calculate moment of inertia from length
for i in range(n):
    I[i] = C*L[i]

#Angles of rotation
anglea = 1*math.pi/6   #Rotation about the z-axis
angleb = 1*math.pi/6   #Rotation about the y-axis
anglec = 0*math.pi/6   #Rotation about the x-axis

#This ends section for user-set values

#Endpoints for rods
for i in range(n):   #Need to define L[i]
    xp = xscale*(i-(n-1)/2)
    yp = L[i]*math.sin(th[i+1])/2
    zp = L[i]*math.cos(th[i+1])/2
    p[i] = (xp,yp,zp)
    p[i+n] = (xp,-yp,-zp)
#    p[i] = (xscale*(i-(n-1)/2),L[i]*math.sin(th[i+1])/2,L[i]*math.cos(th[i+1])/2)
#    p[i+n] = (xscale*(i-(n-1)/2),-L[i]*math.sin(th[i+1])/2,-L[i]*math.cos(th[i+1])/2)

#v = th[int((n+1)/2)]

#Endpoints for coordinate axes
xp = xscale*((1-n)/2)
yp = 0
zp = 0
endp[0] = (xp,yp,zp)
xp = xscale*((n-1)/2)
endp[1] = (xp,yp,zp)
xp = 0
endp[2] = (xp,yp,zp)
yp = L[0]*math.sin(th[0])
zp = L[0]*math.cos(th[0])
endp[3] = (xp,yp,zp)
"""
p[n*2+2] = (0,0*L[0]*math.sin(th[0]),0*L[0]*math.cos(th[0]))   #Use maximum L value, find above
p[n*2+3] = (0,L[0]*math.sin(th[0]),L[0]*math.cos(th[0]))
"""

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

file = open("wavedata", 'w')
file.write(str(n))
file.write("\n")
file.write(str(W))
file.write("\n")
file.write(str(H))
file.write("\n")
file.write(str(t))
file.write("\n")
file.write(str(tf))
file.write("\n")
file.write(str(h))
file.write("\n")

#Multiply matrices together
for i in range(4):   #Endpoints of x-axis
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

    file.write(str(endp[i][0]))
    file.write("\n")
    file.write(str(endp[i][1]))
    file.write("\n")
    file.write(str(endp[i][2]))
    file.write("\n")

for i in range(n*2):   #Endpoints of rods
    if anglea != 0:
        xp = p[i][0]*a[0][0]+p[i][1]*a[0][1]+p[i][2]*a[0][2]
        yp = p[i][0]*a[1][0]+p[i][1]*a[1][1]+p[i][2]*a[1][2]
        zp = p[i][0]*a[2][0]+p[i][1]*a[2][1]+p[i][2]*a[2][2]

        p[i] = (xp,yp,zp)

    if angleb != 0:
        xp = p[i][0]*b[0][0]+p[i][1]*b[0][1]+p[i][2]*b[0][2]
        yp = p[i][0]*b[1][0]+p[i][1]*b[1][1]+p[i][2]*b[1][2]
        zp = p[i][0]*b[2][0]+p[i][1]*b[2][1]+p[i][2]*b[2][2]

        p[i] = (xp,yp,zp)

    if anglec != 0:
        xp = p[i][0]*c[0][0]+p[i][1]*c[0][1]+p[i][2]*c[0][2]
        yp = p[i][0]*c[1][0]+p[i][1]*c[1][1]+p[i][2]*c[1][2]
        zp = p[i][0]*c[2][0]+p[i][1]*c[2][1]+p[i][2]*c[2][2]

        p[i] = (xp,yp,zp)

    file.write(str(p[i][0]))
    file.write("\n")
    file.write(str(p[i][1]))
    file.write("\n")
    file.write(str(p[i][2]))
    file.write("\n")

#Energy
"""e = 0
for i in range(n):
    e += (I[i]*om[i+2]**2+k[i]*(th[i+1]-th[i])**2)
#print(e/2)
eo = e"""

if select == 1:
#Start select 1
#Loop containing RK4 for n second order initial value equations
    while abs(t) < tf:        

        if t*freq < math.pi:
            th[1] = -A*math.sin(t*freq)
            M1[1] = 0
        else:
            M1[1] = slope_th(om[1])
            K1[1] = slope_om(k[1],k[0],th[2],th[1],th[0],I[0])        
        for i in range(n-1):
            M1[i+2] = slope_th(om[i+2])
            K1[i+2] = slope_om(k[i+2],k[i+1],th[i+3],th[i+2],th[i+1],I[i+1])
    
        if t*freq < math.pi:
            th[1] = -A*math.sin((t+h/2)*freq)
            M2[1] = 0
        elif t*freq < 2*math.pi:
            th[1] = 0
            om[1] = 0
            M2[1] = 0
        else:
            M2[1] = slope_th(om[1]+K1[1]*h/2)
            K2[1] = slope_om(k[1],k[0],th[2]+M1[2]*h/2,th[1]+M1[1]*h/2,th[0]+M1[0]*h/2,I[0])        
        for i in range(n-1):   #Necessary to split into several 'for' statements to have updated values such as M1[i+2]
            M2[i+2] = slope_th(om[i+2]+K1[i+2]*h/2)
            K2[i+2] = slope_om(k[i+2],k[i+1],th[i+3]+M1[i+3]*h/2,th[i+2]+M1[i+2]*h/2,th[i+1]+M1[i+1]*h/2,I[i+1])
    
        if t*freq < math.pi:
            th[1] = -A*math.sin((t+h/2)*freq)
            M3[1] = 0
        elif t*freq < 2*math.pi:
            th[1] = 0
            om[1] = 0
            M3[1] = 0
        else:
            M3[1] = slope_th(om[1]+K2[1]*h/2)
            K3[1] = slope_om(k[1],k[0],th[2]+M2[2]*h/2,th[1]+M2[1]*h/2,th[0]+M2[0]*h/2,I[0])        
        for i in range(n-1):
            M3[i+2] = slope_th(om[i+2]+K2[i+2]*h/2)
            K3[i+2] = slope_om(k[i+2],k[i+1],th[i+3]+M2[i+3]*h/2,th[i+2]+M2[i+2]*h/2,th[i+1]+M2[i+1]*h/2,I[i+1])

        if t*freq < math.pi:
            th[1] = -A*math.sin((t+h)*freq)
            M4[1] = 0
        elif t*freq < 2*math.pi:
            th[1] = 0
            om[1] = 0 
            M4[1] = 0
        else:
            M4[1] = slope_th(om[1]+K3[1]*h)
            K4[1] = slope_om(k[1],k[0],th[2]+M3[2]*h,th[1]+M3[1]*h,th[0]+M3[0]*h,I[0])        
        for i in range(n-1):
            M4[i+2] = slope_th(om[i+2]+K3[i+2]*h)
            K4[i+2] = slope_om(k[i+2],k[i+1],th[i+3]+M3[i+3]*h,th[i+2]+M3[i+2]*h,th[i+1]+M3[i+1]*h,I[i+1])
        for i in range(n):        
            th[i+1] += (M1[i+1]+2*M2[i+1]+2*M3[i+1]+M4[i+1])*h/6   
            om[i+1] += (K1[i+1]+2*K2[i+1]+2*K3[i+1]+K4[i+1])*h/6
        t += h
        
        for i in range(n):
            xp = xscale*(i-(n-1)/2)
            yp = L[i]*math.sin(th[i+1])/2
            zp = L[i]*math.cos(th[i+1])/2
            p[i] = (xp,yp,zp)
            p[i+n] = (xp,-yp,-zp)

        for i in range(n*2):
            xp = p[i][0]
            yp = p[i][1]
            zp = p[i][2]
            
            if anglea != 0:
                xp = p[i][0]*a[0][0]+p[i][1]*a[0][1]+p[i][2]*a[0][2]
                yp = p[i][0]*a[1][0]+p[i][1]*a[1][1]+p[i][2]*a[1][2]
                zp = p[i][0]*a[2][0]+p[i][1]*a[2][1]+p[i][2]*a[2][2]
    
                p[i] = (xp,yp,zp)
    
            if angleb != 0:
                xp = p[i][0]*b[0][0]+p[i][1]*b[0][1]+p[i][2]*b[0][2]
                yp = p[i][0]*b[1][0]+p[i][1]*b[1][1]+p[i][2]*b[1][2]
                zp = p[i][0]*b[2][0]+p[i][1]*b[2][1]+p[i][2]*b[2][2]
    
                p[i] = (xp,yp,zp)
    
            if anglec != 0:
                xp = p[i][0]*c[0][0]+p[i][1]*c[0][1]+p[i][2]*c[0][2]
                yp = p[i][0]*c[1][0]+p[i][1]*c[1][1]+p[i][2]*c[1][2]
                zp = p[i][0]*c[2][0]+p[i][1]*c[2][1]+p[i][2]*c[2][2]
    
                p[i] = (xp,yp,zp)
        
            file.write(str(xp))
            file.write("\n")
            file.write(str(yp))
            file.write("\n")
            file.write(str(zp))
            file.write("\n") 
    
    """    e = 0
        for i in range(n):
            e += (I[i]*om[i+2]**2+k[i]*(th[i+1]-th[i])**2)
        print(e/2)"""
#End select 1

if select == 2:
#Start select 2
#Loop containing RK4 for n second order initial value equations
    while abs(t) < tf:        

        if t*freq < math.pi:
            th[1] = -A*math.sin(t*freq)
            M1[1] = 0
            th[n] = sign*-A*math.sin(t*freq)
            M1[n] = 0
        else:
            M1[1] = slope_th(om[1])
            K1[1] = slope_om(k[1],k[0],th[2],th[1],th[0],I[0])
            M1[n] = slope_th(om[n])
            K1[n] = slope_om(k[n],k[n-1],th[n+1],th[n],th[n-1],I[n-1])
        for i in range(n-2):
            M1[i+2] = slope_th(om[i+2])
            K1[i+2] = slope_om(k[i+2],k[i+1],th[i+3],th[i+2],th[i+1],I[i+1])
    
        if t*freq < math.pi:
            th[1] = -A*math.sin((t+h/2)*freq)
            M2[1] = 0
            th[n] = sign*-A*math.sin((t+h/2)*freq)
            M2[n] = 0
        elif t*freq < 2*math.pi:
            th[1] = 0
            om[1] = 0
            M2[1] = 0
            th[n] = 0
            om[n] = 0
            M2[n] = 0
        else:
            M2[1] = slope_th(om[1]+K1[1]*h/2)
            K2[1] = slope_om(k[1],k[0],th[2]+M1[2]*h/2,th[1]+M1[1]*h/2,th[0]+M1[0]*h/2,I[0])
            M2[n] = slope_th(om[n]+K1[n]*h/2)
            K2[n] = slope_om(k[n],k[n-1],th[n+1]+M1[n+1]*h/2,th[n]+M1[n]*h/2,th[n-1]+M1[n-1]*h/2,I[n-1]) 
        for i in range(n-2):   #Necessary to split into several 'for' statements to have updated values such as M1[i+2]
            M2[i+2] = slope_th(om[i+2]+K1[i+2]*h/2)
            K2[i+2] = slope_om(k[i+2],k[i+1],th[i+3]+M1[i+3]*h/2,th[i+2]+M1[i+2]*h/2,th[i+1]+M1[i+1]*h/2,I[i+1])
    
        if t*freq < math.pi:
            th[1] = -A*math.sin((t+h/2)*freq)
            M3[1] = 0
            th[n] = sign*-A*math.sin((t+h/2)*freq)
            M3[n] = 0
        elif t*freq < 2*math.pi:
            th[1] = 0
            om[1] = 0
            M3[1] = 0
            th[n] = 0
            om[n] = 0
            M3[n] = 0
        else:
            M3[1] = slope_th(om[1]+K2[1]*h/2)
            K3[1] = slope_om(k[1],k[0],th[2]+M2[2]*h/2,th[1]+M2[1]*h/2,th[0]+M2[0]*h/2,I[0])
            M3[n] = slope_th(om[n]+K2[n]*h/2)
            K3[n] = slope_om(k[n],k[n-1],th[n+1]+M2[n+1]*h/2,th[n]+M2[n]*h/2,th[n-1]+M2[n-1]*h/2,I[n-1])  
        for i in range(n-2):
            M3[i+2] = slope_th(om[i+2]+K2[i+2]*h/2)
            K3[i+2] = slope_om(k[i+2],k[i+1],th[i+3]+M2[i+3]*h/2,th[i+2]+M2[i+2]*h/2,th[i+1]+M2[i+1]*h/2,I[i+1])

        if t*freq < math.pi:
            th[1] = -A*math.sin((t+h)*freq)
            M4[1] = 0
            th[n] = sign*-A*math.sin((t+h)*freq)
            M4[n] = 0
        elif t*freq < 2*math.pi:
            th[1] = 0
            om[1] = 0 
            M4[1] = 0
            th[n] = 0
            om[n] = 0 
            M4[n] = 0
        else:
            M4[1] = slope_th(om[1]+K3[1]*h)
            K4[1] = slope_om(k[1],k[0],th[2]+M3[2]*h,th[1]+M3[1]*h,th[0]+M3[0]*h,I[0])
            M4[n] = slope_th(om[n]+K3[n]*h)
            K4[n] = slope_om(k[n],k[n-1],th[n+1]+M3[n+1]*h,th[n]+M3[n]*h,th[n-1]+M3[n-1]*h,I[n-1])
        for i in range(n-2):
            M4[i+2] = slope_th(om[i+2]+K3[i+2]*h)
            K4[i+2] = slope_om(k[i+2],k[i+1],th[i+3]+M3[i+3]*h,th[i+2]+M3[i+2]*h,th[i+1]+M3[i+1]*h,I[i+1])
        for i in range(n):        
            th[i+1] += (M1[i+1]+2*M2[i+1]+2*M3[i+1]+M4[i+1])*h/6   
            om[i+1] += (K1[i+1]+2*K2[i+1]+2*K3[i+1]+K4[i+1])*h/6
        t += h
        
        for i in range(n):
            xp = xscale*(i-(n-1)/2)
            yp = L[i]*math.sin(th[i+1])/2
            zp = L[i]*math.cos(th[i+1])/2
            p[i] = (xp,yp,zp)
            p[i+n] = (xp,-yp,-zp)

        for i in range(n*2):
            xp = p[i][0]
            yp = p[i][1]
            zp = p[i][2]
            
            if anglea != 0:
                xp = p[i][0]*a[0][0]+p[i][1]*a[0][1]+p[i][2]*a[0][2]
                yp = p[i][0]*a[1][0]+p[i][1]*a[1][1]+p[i][2]*a[1][2]
                zp = p[i][0]*a[2][0]+p[i][1]*a[2][1]+p[i][2]*a[2][2]
    
                p[i] = (xp,yp,zp)
    
            if angleb != 0:
                xp = p[i][0]*b[0][0]+p[i][1]*b[0][1]+p[i][2]*b[0][2]
                yp = p[i][0]*b[1][0]+p[i][1]*b[1][1]+p[i][2]*b[1][2]
                zp = p[i][0]*b[2][0]+p[i][1]*b[2][1]+p[i][2]*b[2][2]
    
                p[i] = (xp,yp,zp)
    
            if anglec != 0:
                xp = p[i][0]*c[0][0]+p[i][1]*c[0][1]+p[i][2]*c[0][2]
                yp = p[i][0]*c[1][0]+p[i][1]*c[1][1]+p[i][2]*c[1][2]
                zp = p[i][0]*c[2][0]+p[i][1]*c[2][1]+p[i][2]*c[2][2]
    
                p[i] = (xp,yp,zp)
        
            file.write(str(xp))
            file.write("\n")
            file.write(str(yp))
            file.write("\n")
            file.write(str(zp))
            file.write("\n") 
    
    """    e = 0
        for i in range(n):
            e += (I[i]*om[i+2]**2+k[i]*(th[i+1]-th[i])**2)
        print(e/2)"""
#End select 2

elif select == 3:
#Start select 3
#Loop containing RK4 for n second order initial value equations
    while abs(t) < tf:

        th[1] = -A*math.sin(t*freq)
        M1[1] = 0
        for i in range(n-2):
            M1[i+2] = slope_th(om[i+2])
            K1[i+2] = slope_om(k[i+2],k[i+1],th[i+3],th[i+2],th[i+1],I[i+1])
    
        th[1] = -A*math.sin((t+h/2)*freq)
        M2[1] = 0       
        for i in range(n-2):   #Necessary to split into several 'for' statements to have updated values such as M1[i+2]
            M2[i+2] = slope_th(om[i+2]+K1[i+2]*h/2)
            K2[i+2] = slope_om(k[i+2],k[i+1],th[i+3]+M1[i+3]*h/2,th[i+2]+M1[i+2]*h/2,th[i+1]+M1[i+1]*h/2,I[i+1])
    
        th[1] = -A*math.sin((t+h/2)*freq)
        M3[1] = 0       
        for i in range(n-2):
            M3[i+2] = slope_th(om[i+2]+K2[i+2]*h/2)
            K3[i+2] = slope_om(k[i+2],k[i+1],th[i+3]+M2[i+3]*h/2,th[i+2]+M2[i+2]*h/2,th[i+1]+M2[i+1]*h/2,I[i+1])

        th[1] = -A*math.sin((t+h)*freq)
        M4[1] = 0        
        for i in range(n-2):
            M4[i+2] = slope_th(om[i+2]+K3[i+2]*h)
            K4[i+2] = slope_om(k[i+2],k[i+1],th[i+3]+M3[i+3]*h,th[i+2]+M3[i+2]*h,th[i+1]+M3[i+1]*h,I[i+1])
        for i in range(n):        
            th[i+1] += (M1[i+1]+2*M2[i+1]+2*M3[i+1]+M4[i+1])*h/6   
            om[i+1] += (K1[i+1]+2*K2[i+1]+2*K3[i+1]+K4[i+1])*h/6
        t += h
        
        for i in range(n):
            xp = xscale*(i-(n-1)/2)
            yp = L[i]*math.sin(th[i+1])/2
            zp = L[i]*math.cos(th[i+1])/2
            p[i] = (xp,yp,zp)
            p[i+n] = (xp,-yp,-zp)

        for i in range(n*2):
            xp = p[i][0]
            yp = p[i][1]
            zp = p[i][2]
            
            if anglea != 0:
                xp = p[i][0]*a[0][0]+p[i][1]*a[0][1]+p[i][2]*a[0][2]
                yp = p[i][0]*a[1][0]+p[i][1]*a[1][1]+p[i][2]*a[1][2]
                zp = p[i][0]*a[2][0]+p[i][1]*a[2][1]+p[i][2]*a[2][2]
    
                p[i] = (xp,yp,zp)
    
            if angleb != 0:
                xp = p[i][0]*b[0][0]+p[i][1]*b[0][1]+p[i][2]*b[0][2]
                yp = p[i][0]*b[1][0]+p[i][1]*b[1][1]+p[i][2]*b[1][2]
                zp = p[i][0]*b[2][0]+p[i][1]*b[2][1]+p[i][2]*b[2][2]
    
                p[i] = (xp,yp,zp)
    
            if anglec != 0:
                xp = p[i][0]*c[0][0]+p[i][1]*c[0][1]+p[i][2]*c[0][2]
                yp = p[i][0]*c[1][0]+p[i][1]*c[1][1]+p[i][2]*c[1][2]
                zp = p[i][0]*c[2][0]+p[i][1]*c[2][1]+p[i][2]*c[2][2]
    
                p[i] = (xp,yp,zp)

            file.write(str(xp))
            file.write("\n")
            file.write(str(yp))
            file.write("\n")
            file.write(str(zp))
            file.write("\n") 
    
    """    e = 0
        for i in range(n):
            e += (I[i]*om[i+2]**2+k[i]*(th[i+1]-th[i])**2)
        print(e/2)"""
#End select 3
    
elif select == 4:
#Start select 4
#Loop containing RK4 for n second order initial value equations
    while abs(t) < tf:

        th[1] = -A*math.sin(t*freq)
        M1[1] = 0
        th[n] = sign*-A*math.sin(t*freq)
        M1[n] = 0 
        for i in range(n-1):
            M1[i+2] = slope_th(om[i+2])
            K1[i+2] = slope_om(k[i+2],k[i+1],th[i+3],th[i+2],th[i+1],I[i+1])
    
        th[1] = -A*math.sin((t+h/2)*freq)
        M2[1] = 0       
        th[n] = sign*-A*math.sin((t+h/2)*freq)
        M2[n] = 0
        for i in range(n-1):   #Necessary to split into several 'for' statements to have updated values such as M1[i+2]
            M2[i+2] = slope_th(om[i+2]+K1[i+2]*h/2)
            K2[i+2] = slope_om(k[i+2],k[i+1],th[i+3]+M1[i+3]*h/2,th[i+2]+M1[i+2]*h/2,th[i+1]+M1[i+1]*h/2,I[i+1])
    
        th[1] = -A*math.sin((t+h/2)*freq)
        M3[1] = 0       
        th[n] = sign*-A*math.sin((t+h/2)*freq)
        M3[n] = 0       
        for i in range(n-1):
            M3[i+2] = slope_th(om[i+2]+K2[i+2]*h/2)
            K3[i+2] = slope_om(k[i+2],k[i+1],th[i+3]+M2[i+3]*h/2,th[i+2]+M2[i+2]*h/2,th[i+1]+M2[i+1]*h/2,I[i+1])

        th[1] = -A*math.sin((t+h)*freq)
        M4[1] = 0        
        th[n] = sign*-A*math.sin((t+h)*freq)
        M4[n] = 0        
        for i in range(n-1):
            M4[i+2] = slope_th(om[i+2]+K3[i+2]*h)
            K4[i+2] = slope_om(k[i+2],k[i+1],th[i+3]+M3[i+3]*h,th[i+2]+M3[i+2]*h,th[i+1]+M3[i+1]*h,I[i+1])
        for i in range(n):        
            th[i+1] += (M1[i+1]+2*M2[i+1]+2*M3[i+1]+M4[i+1])*h/6   
            om[i+1] += (K1[i+1]+2*K2[i+1]+2*K3[i+1]+K4[i+1])*h/6
        t += h
        
        for i in range(n):
            xp = xscale*(i-(n-1)/2)
            yp = L[i]*math.sin(th[i+1])/2
            zp = L[i]*math.cos(th[i+1])/2
            p[i] = (xp,yp,zp)
            p[i+n] = (xp,-yp,-zp)

        for i in range(n*2):
            xp = p[i][0]
            yp = p[i][1]
            zp = p[i][2]
            
            if anglea != 0:
                xp = p[i][0]*a[0][0]+p[i][1]*a[0][1]+p[i][2]*a[0][2]
                yp = p[i][0]*a[1][0]+p[i][1]*a[1][1]+p[i][2]*a[1][2]
                zp = p[i][0]*a[2][0]+p[i][1]*a[2][1]+p[i][2]*a[2][2]
    
                p[i] = (xp,yp,zp)
    
            if angleb != 0:
                xp = p[i][0]*b[0][0]+p[i][1]*b[0][1]+p[i][2]*b[0][2]
                yp = p[i][0]*b[1][0]+p[i][1]*b[1][1]+p[i][2]*b[1][2]
                zp = p[i][0]*b[2][0]+p[i][1]*b[2][1]+p[i][2]*b[2][2]
    
                p[i] = (xp,yp,zp)
    
            if anglec != 0:
                xp = p[i][0]*c[0][0]+p[i][1]*c[0][1]+p[i][2]*c[0][2]
                yp = p[i][0]*c[1][0]+p[i][1]*c[1][1]+p[i][2]*c[1][2]
                zp = p[i][0]*c[2][0]+p[i][1]*c[2][1]+p[i][2]*c[2][2]
    
                p[i] = (xp,yp,zp)

            file.write(str(xp))
            file.write("\n")
            file.write(str(yp))
            file.write("\n")
            file.write(str(zp))
            file.write("\n") 
    
    """    e = 0
        for i in range(n):
            e += (I[i]*om[i+2]**2+k[i]*(th[i+1]-th[i])**2)
        print(e/2)"""
#End select 4

#Energy
"""e = 0
for i in range(n):
    e += (I[i]*om[i+2]**2+k[i]*(th[i+1]-th[i])**2)
print(h)
print((e-eo)/2)"""

file.close()

print("Done.")
