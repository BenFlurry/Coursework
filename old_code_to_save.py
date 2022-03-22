
# find u, a variables from suvat
def find_sua(values, start_height):
    # set empty variables to none, so they can be integers
    for i in range(5):
        if values[i] == '':
            values[i] = None
        else:
            values[i] = int(values[i])

    # unpack the list
    s, u, v, a, t = values

    # find how many suvat variables we have
    num_of_suvat = how_many_suvat_variables(s - start_height, u, v, a, t)

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