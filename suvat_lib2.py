import numpy as np
import matplotlib.pyplot as plt


# VERTICAL COMPONENT
# 1: s = ut + 0.5at^2
def suat(s, u, a, t, to_be_found):
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


# 2: s = vt - 0.5at^2
def svat(s, v, a, t, to_be_found):
    if to_be_found == 's':
        found = v * t - (a * (t ** 2)) / 2
    elif to_be_found == 'v':
        found = (-s + 0.5 * a * t ** 2) / t
    elif to_be_found == 'a':
        found = 2 * (-s + v * t) / t ** 2
    if to_be_found == 't':
        # using quadratic formula with re arranged equation
        found = ((v + np.sqrt(v ** 2 - 2 * a * s)) / a, (v - np.sqrt(v ** 2 - 2 * a * s)) / a)
        return found
    else:
        return found


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
def suvat(values):
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


def svt(values):
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
    uy = int(uy)
    ay = int(ay)
    vx = int(vx)
    start_height = int(start_height)
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
def para_vel_angle_arr(velocity, angle, acceleration):
    # calculate the hor, ver components of velocity using trigonometry
    vx = float(velocity * np.cos(angle / 180 * np.pi))
    ay = acceleration
    uy = float(velocity * np.sin(angle / 180 * np.pi))
    # call the create list function
    return para_create_coords_lists(uy, ay, vx)


# find u, a variables from suvat
def find_sua(values):
    # set empty variables to none, so they can be integers
    for i in range(5):
        if values[i] == '':
            values[i] = None
        else:
            values[i] = int(values[i])

    # unpack the list
    s, u, v, a, t = values
    # find how many suvat variables we have
    num_of_suvat = how_many_suvat_variables(s, u, v, a, t)

    # check if both u and a are unknown
    if a is None and u is None:
        # if so, set the variable to 0, and pass it through the suvat main function to find u
        u = 0
        u = choose_suvat_eqn(s, u, v, a, t, 'u')[0]
        # now we have 4 variables, main function doesnt work, so we call the suvat eqn itself
        a = 0
        a = suat(s, u, a, t, 'a')[0]
    # if just a is unknown
    elif a is None:
        # if we have 4 known variables call the suvat eqn directly
        if num_of_suvat == 4:
            a = suat(s, u, a, t, 'a')[0]
        # otherwise call the suvat main function to find a
        else:
            a = 0
            a = choose_suvat_eqn(s, u, v, a, t, 'a')[0]
    # same as with a but for u
    elif u is None:
        if num_of_suvat == 4:
            u = uvat(u, v, a, t, 'u')[0]
        else:
            u = 0
            u = choose_suvat_eqn(s, u, v, a, t, 'u')[0]

    # return the list of suvat values
    return [s, u, v, a, t]


# finds the value of v from svt
def find_v(values):
    # set unknown variables to None to allow to convert to int
    for i in range(3):
        if values[i] == '':
            values[i] = None
        else:
            values[i] = int(values[i])
    # unpack the list
    s, v, t = values
    # if v is unknown, call the equation
    if v is None:
        # call the svt function, with v being the target variable
        v = svt_equation(s, v, t, 'v')[0]
    # return the list of svt values
    return [s, v, t]


# to find how many unknown suvat variables there are (will be used in validation)
def how_many_suvat_variables(s, u, v, a, t):
    # pack the variables into a list to iterate
    values = [s, u, v, a, t]
    # set number of unknown variables to 0
    none = 0
    for value in values:
        if value is None:
            # increase num of unknown variables if we have a None value
            none += 1
    # return num of suvat values (5 - num of unknown values)
    return 5 - none


def graph_main_suvat(values_suvat, values_svt, start_height):
    # if uy and ay are unknown
    if values_suvat[1] == '' or values_suvat[3] == '':
        # find the unknown values needed to plot curve
        values_suvat = find_sua(values_suvat)
    # if vx is unknown
    if values_svt[1] == '':
        # find v
        values_svt = find_v(values_svt)
    # create list of coords
    coords = para_hor_ver_arr(values_suvat, values_svt, start_height)
    plt.plot(coords[0], coords[1])
    return coords


# equation to take in x, velocity angle, acceleration and start height and return the y value for each x passed in
def vel_angle_eqn(x, velocity, angle, acceleration, start_height):
    # equation to find y with respect to x
    y = (np.tan(angle) * x) + ((acceleration * x ** 2) / (2 * velocity ** 2 * (np.cos(angle) ** 2))) + start_height
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
        plt.plot(x_coords, y_coords)
        plt.show()


# finds theta given x,y,u,a,start height
def find_theta(x, y, velocity, acceleration, start_height):
    # make graph start at (0,0)
    y = y - start_height
    # find abc coefficients of atheta^2 + btheta + c = 0
    a = ((-acceleration) * (x**2)) / (2 * (velocity**2))
    b = -x
    c = ((-acceleration) * (x**2)) / (2 * (velocity**2)) + y
    # find tan theta roots
    tan_theta = np.array(np.roots([a, b, c]))
    # convert to degrees from radians and wrap as tuple
    theta = tuple((180 / np.pi) * np.arctan(tan_theta))
    # return theta possibilities
    return theta


# makes graphs look nice
def style_graphs():
    # annotate() -> annotate a point x,y with text
    # hlines() -> add horizontal lines from xmin to xmax (get a reference of scale)
    # axis() -> set to on to add x and y axis
    pass


