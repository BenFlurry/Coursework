import numpy as np

# HORIZONTAL COMPONENT EQUATIONS

# s = vt
def svt_equation(s, v, t, to_be_found):
    if to_be_found == 's':
        found = v * t
    elif to_be_found == 'v':
        found = s / t
    elif to_be_found == 't':
        found = s / v
    return found,


# VERTICAL COMPONENT EQUATIONS

# s = ut + 0.5at^2
def suat(s, u, a, t, to_be_found):
    if to_be_found == 's':
        found = u * t + ((a * t) ** 2 / 2)
    elif to_be_found == 'u':
        found = (s - 0.5 * a * t ** 2) / t
    elif to_be_found == 'a':
        found = 2 * (s - u * t) / t ** 2
    if to_be_found == 't':
        found = ((-u + np.sqrt(u ** 2 + 2 * a * s)) / a, (-u - np.sqrt(u ** 2 + 2 * a * s)) / a)
        return found
    else:
        return found,


# s = vt - 0.5at^2
def svat(s, v, a, t, to_be_found):
    # INHERINTLY WRONG
    if to_be_found == 's':
        found = v * t - (a * t) ** 2 / 2
    elif to_be_found == 'v':
        found = (-s + 0.5 * a * t ** 2) / t
    elif to_be_found == 'a':
        found = 2 * (-s + v * t) / t ** 2
    if to_be_found == 't':
        # using quadratic formula with re arranged equation
        found = ((v + np.sqrt(v ** 2 - 2 * a * s)) / a, (v - np.sqrt(v ** 2 - 2 * a * s)) / a)
        return found
    else:
        return found,


# s = t(u + v) / 2
def suvt(s, u, v, t, to_be_found):
    if to_be_found == 's':
        found = (u + v) / (2 * t)
    elif to_be_found == 'u':
        found = (2 * s - v) / t
    elif to_be_found == 'v':
        found = (2 * s - u) / t
    elif to_be_found == 't':
        found = (2 * s) / (u + v)
    return found,


# v^2 = u^2 + 2as
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


# v = u + at
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


# main function
def suvat(values):
    """
    :param list values [s,u,v,a,t]:
    :return tuple (value1,value2):
    """
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
            to_be_found = i
        # set the values that will be used to int
        else:
            values[i] = float(values[i])

    # get the individual suvat values from the list
    s, u, v, a, t = values
    # find the missing suvat letter
    suvat_list = ['s', 'u', 'v', 'a', 't']
    to_be_found = suvat_list[to_be_found]

    # finding missing variable, execute correct equation
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


def svt(values):
    """
    :param values list:
    :return tuple:
    """
    for i in range(3):
        # check for unknown value
        if values[i] == '?':
            # set to 0
            values[i] = 0
            values[i] = float(values[i])
            to_be_found = i
        # set the values to integers
        else:
            values[i] = float(values[i])

    # get individual svt values from the list
    s, v, t = values
    suvat_list = ['s', 'v', 't']
    to_be_found = suvat_list[to_be_found]

    # find missing variable, execute correct equation
    return svt_equation(s, v, t, to_be_found)


values = ['10', '1', '?']

# call the main function
print(svt(values))
