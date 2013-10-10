# Robert Yankou June 07 HW 1

def slope(x,y):
    s = 10*(y-x*x+0.2*x-1)
    return s

h = float(input("h-value: "))
x = float(input("initial x-value: "))
xf = float(input("final x-value: "))
y = float(input("initial y-value: "))

while x < xf:

    K1 = slope(x,y)
    K2 = slope(x+h/2, y+K1*h/2)
    K3 = slope(x+h/2, y+K2*h/2)
    K4 = slope(x+h, y+K3*h)

    x += h
    y += (K1+2*K2+2*K3+K4)*h/6

    print("x-value: ", x, "\ty-value: ", y)
