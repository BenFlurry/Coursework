"""
3 variable suvat
2 variable svt
x, y, vx, uy, a, h -> vel, angle, point, acceleration + height
suvat: s, u, v, a
svt: s, v

y, u, a : x, v
t = x/v
y = u(x/v) + 0.5*(x/v)^2 + h
x2(1/v2) + x(u/v) - y+h = 0     -> actual y = y-h
v2(y-h) -v(ux)) - 0.5x = 0

case where t can be found from svt and then used in suvat or vice versa
"""
x = 3,
print(type(x))

# # if the calculated variable is t and both positive, account for both values
# if check_variable == 'ty' and found_suvat[0] > 0 and found_suvat[1] > 0:
#     if found_suvat[0] == check_value[0] and found_suvat[1] == check_value[1]:
#         return True, found_suvat[0], found_suvat[1]
#     elif found_suvat[0] == check_value[1] and found_suvat[1] == check_value[0]:
#         return True, found_suvat[0], found_suvat[1]
#     else:
#         return False, found_suvat[0], found_suvat[1]
#
# # otherwise account for only 1 value input
# else:
#     if found_suvat[0] == check_value:
#         return True, found_suvat[0]
#     else:
#         return False, found_suvat


