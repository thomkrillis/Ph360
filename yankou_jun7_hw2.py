# Robert Yankou June 07 HW 2
# Note: frictionless system, max t = 1

from math import sin
from math import sqrt

def slope(t, x, u):
    s = -(k/m)*x+(A/m)*sin(t)
    return s

m = float(input("m-value: "))
k = float(input("k-value: "))
A = float(input("A-value: "))
h = float(input("h-value: "))
tf = float(input("final t-value: "))
x = float(input("initial x-value: "))
u = float(input("initial u-value: "))
t = float(0)
w = sqrt(k/m)

while t < tf:

    M1 = u
    K1 = slope(t, x, u)
    M2 = u+K1*h/2
    K2 = slope(t+h/2, x+M1*h/2, u+K1*h/2)
    M3 = u+K2*h/2
    K3 = slope(t+h/2, x+M2*h/2, u+K2*h/2)
    M4 = u+K3*h
    K4 = slope(t+h, x+M3*h, u+K3*h)

    t += h
    x += (M1+2*M2+2*M3+M4)*h/6
    u += (K1+2*K2+2*K3+K4)*h/6

    print("t-value: ", t, "\tx-value: ", x, "\tu-value: ", u)
