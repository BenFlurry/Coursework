import numpy as np
import matplotlib.pyplot as plt
from data import Data
import math


# VERTICAL COMPONENT
# 1: s = ut + 0.5at^2
def suat(s, u, a, t, to_be_found):
    # print(f'{s = }, {u = }, {a = }')
    if to_be_found == 's':
        found = (u * t) + ((a * (t ** 2)) / 2)
    elif to_be_found == 'u':
        found = (s - 0.5 * a * t ** 2) / t
    elif to_be_found == 'a':
        found = 2 * (s - u * t) / t ** 2
    if to_be_found == 't':
        found = ((-u + np.sqrt(u ** 2 + 2 * a * s)) / a, (-u - np.sqrt(u ** 2 + 2 * a * s)) / a)
        return found
    else:
        return found,

    # todo handle NaN


# 2: s = vt - 0.5at^2
def svat(s, v, a, t, to_be_found):
    if to_be_found == 's':
        found = v * t - (a * (t ** 2)) / 2
    elif to_be_found == 'v':
        found = (-s + 0.5 * a * t ** 2) / t
    elif to_be_found == 'a':
        found = 2 * (-s + v * t) / t ** 2
    if to_be_found == 't':
        found = ((v + np.sqrt(v ** 2 - 2 * a * s)) / a, (v - np.sqrt(v ** 2 - 2 * a * s)) / a)
        return found
    else:
        return found,


# 3: v^2 = u^2 + 2as
def suva(s, u, v, a, to_be_found):
    if to_be_found == 'v':
        found = np.sqrt(u ** 2 + 2 * a * s)
    elif to_be_found == 's':
        found = (v ** 2 - u ** 2) / (2 * a)
    elif to_be_found == 'u':
        found = np.sqrt(v ** 2 - 2 * a * s)
    elif to_be_found == 'a':
        found = ((v ** 2 - u ** 2) / (2 * s))
    return found,


# 4: v = u + at
def uvat(u, v, a, t, to_be_found):
    if to_be_found == 'v':
        found = u + a * t
    elif to_be_found == 'u':
        found = v - a * t
    elif to_be_found == 'a':
        found = (v - u) / t
    elif to_be_found == 't':
        found = (v - u) / a
    return found,


# 5: s = t(u + v) / 2
def suvt(s, u, v, t, to_be_found):
    if to_be_found == 's':
        found = (u + v) / (2 * t)
    elif to_be_found == 'u':
        found = (2 * s) / t - v
    elif to_be_found == 'v':
        found = (2 * s) / t - u
    elif to_be_found == 't':
        found = (2 * s) / (u + v)
    return found,


# HORIZONTAL COMPONENT
# 6: s = vt
def svt_equation(s, v, t, to_be_found):
    if to_be_found == 's':
        found = v * t
    elif to_be_found == 'v':
        found = s / t
    elif to_be_found == 't':
        found = s / v
    return found,


# main functions
def suvat_main(values):
    # iterate through the inputted values
    for i in range(5):
        # check for the null value
        if values[i] == "":
            # set it to null to convert to int
            values[i] = None
        # check for the unknown value
        elif values[i] == "?":
            # set to 0
            values[i] = 0
            values[i] = float(values[i])
            # set to be found to the index of the list of the target variable
            to_be_found = i
        # set the values that will be used to int
        else:
            values[i] = float(values[i])

    # get the individual suvat values from the list
    s, u, v, a, t = values
    # find the missing suvat letter
    suvat_list = ['s', 'u', 'v', 'a', 't']
    # the content of the suvat_list at index to_be_found is the target variable
    to_be_found = suvat_list[to_be_found]
    choose_suvat_eqn(s, u, v, a, t, to_be_found)
    return s, u, v, a, t


def choose_suvat_eqn(s, u, v, a, t, to_be_found):
    # finding missing variable, execute correct equation passing in target variable and suvat variables
    if s is None:
        return uvat(u, v, a, t, to_be_found)
    elif u is None:
        return svat(s, v, a, t, to_be_found)
    elif v is None:
        return suat(s, u, a, t, to_be_found)
    elif a is None:
        return suvt(s, u, v, t, to_be_found)
    elif t is None:
        return suva(s, u, v, a, to_be_found)
    # return the values returned from the suvat equations


def svt_main(values):
    # iterate through the 3 list indexes
    for i in range(3):
        # check for unknown value as inputted as '?'
        if values[i] == '?':
            # set to 0 in order to set to a float value
            values[i] = 0
            values[i] = float(values[i])
            # set value to be found to the index of the list
            to_be_found = i
            # if the value inputted is nothing, then set the string to nothing data type
        elif values[i] == '':
            values[i] = None
        # set the values to integers
        else:
            values[i] = float(values[i])

    # get individual svt values from the list
    s, v, t = values
    # compare the s,v,t variables to the list to find the variable that needs to be found
    suvat_list = ['s', 'v', 't']
    # the to be found index (as found earlier) in the list will be the variable to be arranged for
    to_be_found = suvat_list[to_be_found]

    # pass the variables, and target variable into the svt equation, and return the result
    return svt_equation(s, v, t, to_be_found)


def para_create_coords_lists(uy, ay, vx, start_height):
    # convert inputs to integers
    uy = float(uy)
    ay = float(ay)
    vx = float(vx)
    start_height = float(start_height)
    # create the x,y coords lists
    x_coords = []
    y_coords = []
    # find x,y coords and add to list
    # set t and y to 0
    t = 0
    y = 0
    # iterate through value of t, until projectile hits ground (y = 0)
    while y >= 0:
        # call the suat function to find y coord at t time
        y = suat(0, uy, ay, t, 's')[0] + start_height
        # call svt function to find x coord at t time
        x = svt_equation(0, vx, t, 's')[0]
        # add coords to their respective lists
        x_coords.append(x)
        y_coords.append(y)
        # increment t
        t += 0.01
    # return the 2 coord lists
    return x_coords, y_coords


# takes in suvat,svt and returns lists of x and y coords
def para_hor_ver_arr(suvat, svt, start_height):
    # unpack the lists into their respective variables
    sy, uy, vy, ay, ty = suvat
    sx, vx, tx = svt
    # create coords
    return para_create_coords_lists(uy, ay, vx, start_height)


# takes in given parameters and returns lists of x and y coords
def para_vel_angle_arr(velocity, angle, acceleration, height):
    # calculate the hor, ver components of velocity using trigonometry
    vx = float(velocity * np.cos(angle / 180 * np.pi))
    ay = acceleration
    uy = float(velocity * np.sin(angle / 180 * np.pi))
    # call the create list function
    return para_create_coords_lists(uy, ay, vx, height)


# makes graphs look nice
def style_graphs():
    # annotate() -> annotate a point x,y with text. might have to convert to numpy array to then find max etc.
    plt.xlabel('Horizontal Displacement (m)')
    plt.ylabel('Vertical Displacement (m)')
    plt.grid(True)
    plt.axis('equal')
    plt.axhline(y=0, color='black', linestyle='-')
    plt.axvline(x=0, color='black', linestyle='-')
    plt.gca().set_aspect("equal")
    # hlines() -> add horizontal lines from xmin to xmax (get a reference of scale)
    # axis() -> set to on to add x and y axis


def find_variables(suvat, svt, h):
    try:
        # get suvat svt masks
        suvat_mask = []
        svt_mask = []
        svt_other = []
        # if suvat[0]:
        #     suvat[0] -= h
        suvat_total = 0
        for i in range(5):
            if suvat[i] == '':
                suvat_mask.append(0)
                suvat[i] = None
            else:
                suvat[i] = float(suvat[i])
                suvat_mask.append(1)
                suvat_total += 1
        for i in range(3):
            if svt[i] == '':
                svt_mask.append(0)
                svt[i] = None
            else:
                svt[i] = float(svt[i])
                svt_mask.append(1)
        # find a
        if suvat_mask[1] == 0:
            # if t needs to be found, find it
            if suvat_total == 2:
                suvat[4] = svt_equation(*svt, 't')[0]
            suvat[1] = choose_suvat_eqn(*suvat, 'u')[0]
        # find u
        if suvat_mask[3] == 0:
            # find t if needed
            if suvat_total == 2:
                suvat[4] = svt_equation(*svt, 't')[0]

            suvat[3] = choose_suvat_eqn(*suvat, 'a')[0]
        # find v
        if svt_mask[1] == 0:
            if svt_mask[1] == [1, 0, 1]:
                svt[1] = svt_equation(*svt, 'v')[0]
            else:
                time = choose_suvat_eqn(*suvat, 't')
                t1 = max(time)
                t2 = min(time)
                print(f'{time = }')
                svt[2] = t1
                svt[1] = svt_equation(*svt, 'v')[0]
                print(f'{svt = }')
                # check the min value of t > 0, if so we can use it
                if t2 > 0:
                    svt_other = []
                    for i in range(3):
                        svt_other.append(svt[i])
                    svt_other[2] = t2
                    svt_other[1] = svt_equation(*svt_other, 'v')[0]
                    print(f'{svt_other[1] = }')
                    print(f'{svt_other = }')

        return suvat, svt, svt_other, h
    # if suvat[0]:
    #     suvat[0] += h
    except Exception as e:
        print(f'Error in finding variables for graph: {e}')
        return False


def graph_main_suvat(values_suvat, values_svt, start_height):
    variables = find_variables(values_suvat, values_svt, start_height)
    print(f'{variables = }')
    if not variables:
        return 'not enough variables to plot graph'
    else:
        suvat, svt, svt_other, h = variables
    # create list of coords
    if not svt_other:
        coords = para_hor_ver_arr(suvat, svt, h)
        plt.plot(coords[0], coords[1])
        style_graphs()
        plt.show()
        return True
    else:
        coords1 = para_hor_ver_arr(suvat, svt, h)
        coords2 = para_hor_ver_arr(suvat, svt_other, h)
        plt.plot(*coords1)
        plt.plot(*coords2)
        style_graphs()
        plt.show()
        return True


# equation to take in x, velocity angle, acceleration and start height and return the y value for each x passed in
def vel_angle_eqn(x, velocity, angle, acceleration, start_height):
    # equation to find y with respect to x
    y = (np.tan(angle) * x) + (
                (acceleration * (x ** 2)) / (2 * (velocity ** 2) * (np.cos(angle) ** 2))) + start_height
    return y


# finds when projectile hits the ground
def vel_angle_x_intercept(velocity, angle, acceleration, start_height):
    # take the ax^2 + bx + c coefficients
    a = acceleration / (2 * (velocity ** 2) * ((np.cos(angle)) ** 2))
    b = np.tan(angle)
    c = start_height
    # find roots
    roots = (np.roots([a, b, c]))
    # return as tuple
    return np.maximum(roots[0], roots[1])


# takes in vel, angle, acceleration, start height and plots the graph
def graph_main_velangle(velocity, angle, acceleration, start_height, x, y):
    if start_height == '':
        start_height = 0

    if angle == '':
        angle = find_theta(x, y, velocity, acceleration, start_height)
        # convert angle from degrees to radians
        angle1 = angle[0] * np.pi / 180
        angle2 = angle[1] * np.pi / 180
        # find where the projectile hits the ground to find end point of projectile curve
        end1 = vel_angle_x_intercept(velocity, angle1, acceleration, start_height)
        end2 = vel_angle_x_intercept(velocity, angle2, acceleration, start_height)
        # create set of x values from 0 to the max end value
        x_coords1 = np.arange(0, end1, 0.01)
        x_coords2 = np.arange(0, end2, 0.01)
        # find the y values respective to x values for each angle
        y_coords1 = vel_angle_eqn(x_coords1, velocity, angle1, acceleration, start_height)
        y_coords2 = vel_angle_eqn(x_coords2, velocity, angle2, acceleration, start_height)
        # plot the x and y coordinates and show graph
        style_graphs()
        plt.plot(x_coords1, y_coords1)
        plt.plot(x_coords2, y_coords2)
        plt.show()

    else:
        # convert angle from degrees to radians
        angle = angle * np.pi / 180
        # find where the projectile hits the ground to find end point of projectile curve
        end = vel_angle_x_intercept(velocity, angle, acceleration, start_height)
        # create set of x values from 0 to the end value
        x_coords = np.arange(0, end, 0.01)
        # find the y values respective to x values
        y_coords = vel_angle_eqn(x_coords, velocity, angle, acceleration, start_height)
        # plot the x and y coordinates and show graph
        style_graphs()
        plt.plot(x_coords, y_coords)
        plt.show()


# finds theta given x,y,u,a,start height
def find_theta(x, y, velocity, acceleration, start_height):
    # make graph start at (0,0)
    y = y - start_height
    # find abc coefficients of atheta^2 + btheta + c = 0
    a = ((-acceleration) * (x ** 2)) / (2 * (velocity ** 2))
    b = -x
    c = ((-acceleration) * (x ** 2)) / (2 * (velocity ** 2)) + y
    # find tan theta roots
    tan_theta = np.array(np.roots([a, b, c]))
    # convert to degrees from radians and wrap as tuple
    theta = tuple((180 / np.pi) * np.arctan(tan_theta))
    # return theta possibilities
    return theta


# round values to 3sf
def to_3sf(value):
    return round(value, 2 - int(math.floor(math.log10(abs(value)))))


# input validate as a string for either
def verify_suvat(inp_suvat, inp_svt, height, check_variable, check_value):
    variables = ['sy', 'uy', 'vy', 'ay', 't', 'sx', 'vx', 'h']
    index = variables.index(check_variable)
    # if the check_variable has a value, remove it to calculate manually
    if index <= 4:
        inp_suvat[index] = ''
    elif 5 <= index <= 7:
        inp_svt[index - 5] = ''

    suvat_mask = [1, 1, 1, 1, 1]
    num_of_suvat = 5

    for i in range(5):
        if inp_suvat[i] == '':
            num_of_suvat -= 1
            suvat_mask[i] = 0

    svt_mask = [1, 1, 1]
    num_of_svt = 3
    for i in range(3):
        if inp_svt[i] == '':
            num_of_svt -= 1
            svt_mask[i] = 0

    if height == '':
        has_height = False
    else:
        has_height = True

    # Case 1: solve suvat on its own
    if num_of_suvat >= 3 and index <= 4:
        suvat = inp_suvat
        for i in range(5):
            if suvat_mask[i] == 1:
                suvat[i] = float(inp_suvat[i])
            if i == index:
                suvat[i] = 0
            elif suvat[i] == '':
                suvat[i] = None

        if has_height:
            suvat[0] += float(height)

        if check_variable == 't' and suvat_mask == [1, 1, 0, 1, 0] or suvat_mask == [1, 0, 1, 1, 0]:
            calculated_t1 = to_3sf(choose_suvat_eqn(*suvat, check_variable[0])[0])
            calculated_t2 = to_3sf(choose_suvat_eqn(*suvat, check_variable[0])[1])
            if calculated_t1 > 0 and calculated_t2 > 0:
                if type(check_value) == tuple and len(check_value) == 2:
                    if calculated_t1 == check_value[0] and calculated_t2 == check_value[1]:
                        return True, (calculated_t1, calculated_t2)
                    elif calculated_t1 == check_value[1] and calculated_t2 == check_value[0]:
                        return True, (calculated_t2, calculated_t1)
                    else:
                        return False, (calculated_t1, calculated_t2)
                else:
                    return False, (calculated_t1, calculated_t2)
            else:
                calculated_value = calculated_t2
        else:
            calculated_value = to_3sf(choose_suvat_eqn(*suvat, check_variable[0])[0])
        if calculated_value == check_value:
            return True, (calculated_value,)
        else:
            return False, (calculated_value,)

    # Case 2: solve svt on its own
    elif num_of_svt >= 2 and 4 <= index <= 6:
        svt = inp_svt
        for i in range(3):
            if svt_mask[i] == 1:
                svt[i] = float(inp_svt[i])
            if i == index:
                svt[i] = 0
            elif svt[i] == '':
                svt[i] = None
        found_svt = to_3sf(svt_equation(*svt, check_variable[0])[0])
        if found_svt == check_value:
            return True, (found_svt,)
        else:
            return False, (found_svt,)

    # Case 3: svt then suvat
    elif num_of_suvat == 2 and num_of_svt == 2 and svt_mask == [1, 1, 0] and index <= 3 and suvat_mask[4] != 1:
        # find t from svt
        b, n, m = inp_svt
        t = b / n
        # add t to the suvat list
        suvat = inp_suvat
        suvat[4] = t
        # setup suvat list for calculation
        for i in range(4):
            if suvat[i] == '':
                suvat[i] = None
            else:
                suvat[i] = float(suvat[i])
        suvat[index] = 0
        # add starting height if given
        if has_height and suvat[0] is not None and check_variable != 'sy':
            suvat[0] += height
        # calculate missing variable
        actual_value = to_3sf(choose_suvat_eqn(*suvat, check_variable[0])[0])
        # account for starting height
        if check_variable == 'sy':
            actual_value += height
        # check if valid and return
        if actual_value == check_value:
            return True, (actual_value,)
        else:
            return False, (actual_value,)

    # Case 4: suvat then svt
    elif num_of_suvat == 3 and num_of_svt == 1 and 5 <= index <= 6 and svt_mask[2] != 1:
        suvat = inp_suvat
        # handle nones
        for i in range(4):
            if suvat[i] == '':
                suvat[i] = None
            else:
                suvat[i] = float(suvat[i])
        # find t from suvat
        t = choose_suvat_eqn(*suvat, 't')
        # if there are 2 valid values for t
        svt = inp_svt
        for i in range(3):
            if svt[i] == '':
                svt[i] = None
            else:
                svt[i] = float(svt[i])
        e, f, _ = svt
        if len(t) == 2 and t[0] > 0 and t[1] > 0:
            # check which variable is missing and calculate the value
            if svt_mask == [1, 0, 0]:
                actual_value = (to_3sf(svt_equation(e, f, t[0], 'v')[0]),
                                to_3sf(svt_equation(e, f, t[1], 'v')[0]))
            else:
                actual_value = (to_3sf(svt_equation(e, f, t[0], 's')[0]),
                                to_3sf(svt_equation(e, f, t[1], 's')[0]))
            # check if correct and return
            if actual_value == check_value and type(check_value) == tuple:
                return True, actual_value
            else:
                return False, actual_value
        # if there is only 1 value of t
        else:
            # take the highest value
            if len(t) == 2:
                t = max(t[0], t[1])
            else:
                t = t[0]
            # and calculate the missing variable
            if svt_mask == [1, 0, 0]:
                actual_value = to_3sf(svt_equation(e, f, t, 'v')[0])
            else:
                actual_value = to_3sf(svt_equation(e, f, t, 's')[0])
            # and check if its correct
            if actual_value == check_value:
                return True, (actual_value,)
            else:
                return False, (actual_value,)

    # Case 5: svt subbed into suvat with only svt[t] given
    elif num_of_suvat >= 3 and num_of_svt == 1 and 5 <= index <= 6 and svt_mask == [0, 0, 1]:
        print('case 5')
        # convert empty string to none
        for i in range(5):
            if inp_suvat[i] == '':
                inp_suvat[i] = None
            else:
                inp_suvat[i] = float(inp_suvat[i])
        for i in range(3):
            if inp_svt[i] == '':
                inp_svt = None
            else:
                inp_svt[i] = float(inp_svt[i])
        # unpack relevant inputs
        x, u, _, a, _ = inp_suvat
        y, v, _ = inp_svt
        h = height
        # if no start height is given, assume 0
        if h == '':
            h = 0

        # need to have x, u, a and y or v so find them if not given
        # if x doesnt exist
        if suvat_mask[0] != 1:
            x = 0
            x = choose_suvat_eqn(*inp_suvat, 's')
        # if u doesnt exist
        elif suvat_mask[1] != 1:
            u = 0
            u = choose_suvat_eqn(*inp_suvat, 'u')
        # if a doesnt exist
        elif suvat_mask[3] != 1:
            a = 0
            a = choose_suvat_eqn(*inp_suvat, 'a')

        # for the x quadratic eqn
        if svt_mask[0] == 1:
            alpha = 0.5 * a / (v ** 2)
            beta = u / v
            gamma = -y + h
            # find roots
            roots = np.roots([alpha, beta, gamma]) - h
            if roots[0] == check_value[0] and roots[1] == check_value[1]:
                return True, (roots[0], roots[1])
            elif roots[0] == check_value[1] and roots[1] == check_value[0]:
                return True, (roots[1], roots[0])
            else:
                return False, (roots[0], roots[1])

        # for the v quadratic eqn
        if svt_mask[1] == 1:
            alpha = y - h
            beta = -u * x
            gamma = -0.5 * x ** 2 * a
            # find roots
            roots = np.roots([alpha, beta, gamma])
            if roots[0] == check_value[0] and roots[1] == check_value[1] and type(check_value) == tuple:
                return True, (roots[0], roots[1])
            elif roots[0] == check_value[1] and roots[1] == check_value[0] and type(check_value) == tuple:
                return True, (roots[1], roots[0])
            else:
                return False, (roots[0], roots[1])

    else:
        return 'invalid',


def tests():
    print('test 1: suvat only')
    inputs = ['3', '10', '', '-10', ''], ['', '', ''], '0', 't', ('1.63', '0.368')
    print(inputs)
    print(f'check value = {inputs[4]}')
    print('calculated value = ', end='')
    print(verify_suvat(*inputs))

    print('\ntest 2: svt only')
    inputs = ['', '', '', 10, 10], [6, 2, ''], '', 't', 3
    print(inputs)
    print(f'check value = {inputs[4]}')
    print('calculated value = ', end='')
    print(verify_suvat(*inputs))

    print('\ntest 3: svt then suvat')
    inputs = ['', 10, '', -10, ''], [6, 2, ''], 15, 'vy', -20
    print(inputs)
    print(f'check value = {inputs[4]}')
    print('calculated value = ', end='')
    print(verify_suvat(*inputs))

    print('\ntest 4: suvat then svt')
    inputs = [-10, 20, '', -10, ''], ['', 1, ''], 15, 'vx', 4.45
    print(inputs)
    print(f'check value = {inputs[4]}')
    print('calculated value = ', end='')
    print(verify_suvat(*inputs))


# tests()


def verify_velangle(values, check_variable, check_value):
    input_mask = []
    for i in range(6):
        if values[i] != '':
            input_mask.append(1)
        else:
            input_mask.append(0)

    x, y, vel, angle, accel, h = values
    if check_variable == 'angle':
        found_angle = find_theta(x, y, vel, accel, h)
        if len(found_angle) == 1 and len(check_value) == 1:
            if found_angle == check_value:
                return True, found_angle
            else:
                return False, found_angle
        elif len(found_angle) == 2 and len(check_value) == 2:
            if found_angle[0] == check_value[0] and found_angle[1] == check_value[1]:
                return True, found_angle[0], found_angle[1]
            elif found_angle[0] == check_value[1] and found_angle[1] == check_value[0]:
                return True, found_angle[1], found_angle[0]
            else:
                return False, found_angle[0], found_angle[1]

    elif check_variable == 'y':
        found_y = vel_angle_eqn(x, vel, angle, accel, h)
        if found_y == check_value:
            return True, found_y
        else:
            return False, found_y

    elif check_variable == 'x':
        angle = angle * np.pi / 180
        alpha = accel / (2 * (vel ** 2) * (np.cos(angle) ** 2))
        beta = np.tan(angle)
        gamma = -y + h
        found_x = np.roots([alpha, beta, gamma])
        # check length of found x
        if found_x[0] == check_value[0] and found_x[1] == check_value[1]:
            return True, found_x[0], found_x[1]
        elif found_x[1] == check_value[0] and found_x[0] == check_value[1]:
            return True, found_x[0], found_x[1]
        else:
            return False, found_x[0], found_x[1]

    elif check_variable == 'accel':
        angle = angle * np.pi / 180
        found_a = (2 * vel ** 2 * np.cos(angle) ** 2 * (y - h - (x * np.tan(angle)))) / x ** 2
        if found_a == check_value:
            return True, found_a
        else:
            return False, found_a

    elif check_variable == 'vel':
        angle = angle * np.pi / 180
        found_vel = np.sqrt((accel * x ** 2) / (2 * (np.cos(angle)) ** 2 * (y - h - (x * np.tan(angle)))))
        if found_vel == check_value:
            return True, found_vel
        else:
            return False, found_vel
