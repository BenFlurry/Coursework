import numpy as np
import matplotlib.pyplot as plt
import string


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
    """
    :param values list:
    :return tuple:
    """
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


'''
use a while loop until the x coord is less than 0, then add the x = 0 to the list
be able to have the curve start above x = 0, by adding on the starting height to each y coord
'''


# takes in suvat,svt and returns lists of x and y coords
def para_hor_ver_arr(suvat, svt):
    # unpack the lists into their respective variables
    sy, uy, vy, ay, ty = suvat
    sx, vx, tx = svt
    # create coords
    return para_create_coords_lists(uy, ay, vx)


# takes in given parameters and returns lists of x and y coords
def para_vel_angle_arr(velocity, angle, acceleration):
    # calculate the hor, ver components of velocity using trigonometry
    vx = float(velocity * np.cos(angle / 180 * np.pi))
    ay = acceleration
    uy = float(velocity * np.sin(angle / 180 * np.pi))
    # call the create list function
    return para_create_coords_lists(uy, ay, vx)


def para_create_coords_lists(uy, ay, vx):
    # find the number of seconds for which the projectile is in the air to find last point
    max = 2 * uy / -ay
    # create the x,y coords lists
    x_coords = []
    y_coords = []
    # find x,y coords and add to list
    # max * 100 so one point is recorded every 0.01s to make curve smoother
    for t in range(int(max * 100 + 1)):
        # call the suat function to find y coord at t time
        y = suat(0, uy, ay, t / 100, 's')
        # call svt function to find x coord at t time
        x = svt_equation(0, vx, t / 100, 's')
        # add coords to their respective lists
        x_coords.append(x[0])
        y_coords.append(y[0])
    # return the 2 coord lists
    return x_coords, y_coords


# uses matplotlib.pyplot as plt to plot the graph with given coords
def plot_graph(x_coords, y_coords):
    """
    :type x_coords: list
    :type y_coords: list
    """
    plt.plot(x_coords, y_coords)
    plt.show()


# find u, a variables from suvat
def find_sua(values):
    # set empty variables to none, so they can be integers
    for i in range(5):
        if values[i] == '':
            values[i] = None

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


print(find_sua(([1, '', -10, '', 3])))
print(find_v([2, '', 2/3]))

'''
make it so any inputted set of suvat svt can be created into a graph - plot'
use cartesian equations for vel angle acceleration
'''











