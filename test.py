import math
import random
import string
"""
3 variable suvat
2 variable svt
x, y, vx, uy, a, h -> vel, angle, point, acceleration + height
suvat: s, u, v, a
svt: s, v

y, u, a : x, v
y = u(x/v) + 0.5*a*(x/v)^2 + h   finds y
u = (y - 0.5a(x/v)^2 - h)v / x   finds u
a = 2(y - h - u(x/v))v^2 / x^2  finds a
x2(a/2v2) + x(u/v) - y+h = 0     finds x
v2(y-h) -v(ux)) - 0.5xa = 0     finds v

y, u, a
x, v

case where t can be found from svt and then used in suvat or vice versa


y, x, angle, accel, vel, height
y = x, angle, accel, height, vel
y = y
u = vel(sin(angle))
v 
a = accel
t

x = x
v = vel(cos(angle))
t

y = xtan + (ax^2)/2v^2 cos^2     finds y
x^2(a/2u^2cos^2) + x(tan) -y+h   finds x
a = (2v^2cos^2(y-h-xtan))/x^2    finds a 
v = sqrt(ax^2 / 2(y - xtan)cos^2 finds v


s 
u
v
a
t
"""
x = (1,2)
print(list(x))
