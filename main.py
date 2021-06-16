from collections import defaultdict as ddict
import numpy as np
import copy

'''
Creating main matrix
Array of arrays: Array - Main matrix
'''
def create_sympleks(Array):
    hmc_range = range(0, hmc)

    for i in hmc_range:
        column = get_parameters(constrains[i])
        column_range = range(0,len(column))
        for i in column_range:
            Array.append(column[i])

    group = ddict(list)

    for xi, value in Array:
        group[xi].append(value)
    Array = [[xi, *values] for xis, values in group.items()]

    for i in hmc_range:
        column = ["S[" + str(i) + "]"]
        for k in hmc_range:
            column.append(0)
        column[i+1] = (-1)
        Array.append(column)

    for i in hmc_range:
        column = ["A[" + str(i) + "]"]
        for k in hmc_range:
            column.append(0)
        column[i+1] = (1)
        Array.append(column)

    for i in hmc_range:
        B_values = get_Bs(constrains[i], i)
        Array.append(B_values)

    return Array


'''
Merging arrays
'''
def merge_arrays(Array_to_merge_with, Array):
    Array_to_merge_with.append(Array)

'''
Finding Bs values and creating array of it
string: constrain_str - single constrain string
'''
def get_Bs(constrain_str, i):
    constrain_str = delete_whitespaces(constrain_str)
    j = 0
    if constrain_str.find(">=") != -1:
        searched_index = constrain_str.find(">=")
        B_value = constrain_str[searched_index+2:]
        Bs = ["B[" + str(i) + "]", B_value]
        return Bs
    if constrain_str.find("<=") != -1:
        searched_index = constrain_str.find("<=")
        B_value = constrain_str[searched_index+2:]
        Bs = ["B[" + str(i) + "]", B_value]
        return Bs
    if constrain_str.find("=") != -1:
        searched_index = constrain_str.find("=")
        B_value = constrain_str[searched_index+1:]
        Bs = ["B[" + str(i) + "]", B_value]
        return Bs


'''
Creating additional parameters Si and Ai
'''
def get_addidionalCj():
    hmc_range = range(0, hmc)
    values_array = []
    for i in hmc_range:
        values_array.append(["x[" + str(i) + "]", 0])
    for i in hmc_range:
        # S values Array
        values_array.append(["S[" + str(i) + "]", 0])
    for i in hmc_range:
        # A values Array
        values_array.append(["A[" + str(i) + "]", 1])
    return values_array

'''
Getting fucntion str like ('2x[1] + x[0]') and trying to get its parameters

string: str_fun - function string
'''
def get_parameters(str_fun):
    letter = 'a'
    str_fun = delete_whitespaces(str_fun)
    range_of_search = range(0, hmu)
    last_found = 0
    values_array = []
    for i in range_of_search:
        j = 0
        while str_fun.find(chr(ord(letter) + i), last_found) != -1:
            found_index = str_fun.find(chr(ord(letter) + i), last_found)
            parameter_value = str_fun[last_found:found_index]
            last_found =  found_index + 1
            if j == 0:
                values_array.append(["x[" + str(i+1) + "]", parameter_value])
                parameter_value
            else:
                print("The given function was incorrect")
                return 0
            j+=1
        if j == 0:
            values_array.append(["x[" + str(i+1) + "]",0])
    return values_array


'''
Deletes whitespaces

string: str_fun - function string
'''
def delete_whitespaces(str_fun):
    str_fun = str_fun.replace(" ","")
    return str_fun

'''
Initialization method
'''
def init():
    fun = ''
    '''replacing whitespaces with no space'''
    fun = delete_whitespaces(function)
    '''geting parameters from given function'''
    values_array = []
    values_array = get_addidionalCj()
    sympleks = []
    sympleks = create_sympleks(sympleks)
    TwoPhaseMethod(sympleks, values_array)

def TwoPhaseMethod(sympleks, values_array):
    Initial_XB = []
    hmc_range = range(0, hmc)
    first_row_values = []

    for i in hmc_range:
        Initial_XB.append(["A[" + str(i) + "]", 1])

        ''' First phase '''

    for a in hmc_range:
        sympleks_len = len(sympleks) - hmc
        sympleks_range = range(0, sympleks_len )
        column_values = []
        for j in sympleks_range:
            temp_array = []
            for i in hmc_range:
                temp_array.append(float(float(sympleks[j][i+1]) * Initial_XB[i][1]))
            temp_len = len(temp_array)
            temp_range = range(0, temp_len )
            total = 0
            for i in temp_range:
                total = total + temp_array[i]
            column_values.append(total)
        cjzj_array = []
        cj_len = len(values_array)
        cj_range = range(0, cj_len)
        for i in cj_range:
            cjzj_array.append(float(column_values[i]) - float(values_array[i][1]) )
        biggest_value = np.max(cjzj_array)
        biggest_value_column = cjzj_array.index(max(cjzj_array))
        xb_div_xi = []
        for i in hmc_range:
            xb_div_xi_reulst = float(sympleks[sympleks_len + i][1]) / float(sympleks[biggest_value_column][i+1])
            xb_div_xi.append(xb_div_xi_reulst)
        smallest_value_row = xb_div_xi.index(min(xb_div_xi))
        RE = float(sympleks[biggest_value_column][smallest_value_row + 1])
        for i in sympleks_range:
            if (Initial_XB[smallest_value_row][0] == sympleks[i][0]):
                sympleks.pop(i) 
                values_array.pop(i) 

        sympleks_range = range(0, sympleks_len -1)
        sympleks_len = len(sympleks) - hmc
        Initial_XB[smallest_value_row] = values_array[biggest_value_column]
        temp_value = len(sympleks)
        next_sympleks = copy.deepcopy(sympleks)
        for j in hmc_range:
            if (j == smallest_value_row):
                next_sympleks[sympleks_len +j ][1] = float(sympleks[sympleks_len + j][1])/RE
            else:
                '''
                OE - Old element
                RE - Resolving element
                KRE - Key row element
                KCE - Key column element 
                NE - New element
                '''
                OE = float (sympleks[sympleks_len + j][1])
                KRE = float(sympleks[sympleks_len + smallest_value_row][1])
                KCE = float(sympleks[biggest_value_column][j + 1])
                NE = OE - (KCE * KRE)/ RE
                next_sympleks[sympleks_len + j][1] =float(NE)

            for i in sympleks_range:
                '''
                OE - Old element
                RE - Resolving element
                KRE - Key row element
                KCE - Key column element 
                NE - New element
                '''

                ''' For the RE row'''
                if (j == smallest_value_row):
                    next_sympleks[i][j + 1] = float (sympleks[i][j + 1])/ RE
                else:
                    '''For the rest of the table'''
                    OE = float (sympleks[i][j + 1])
                    KRE = float(sympleks[i][smallest_value_row + 1])
                    KCE = float(sympleks[biggest_value_column][j + 1])
                    NE = OE - (KCE * KRE)/ RE
                    next_sympleks[i][j + 1] = float(NE)
          

        sympleks = copy.copy(next_sympleks)
        print("After changing values => ", sympleks)
        print(Initial_XB)

        ''' Second phase '''

function = '2a+ 1b' 
constrains = []
constrains = ['1a + 1b >= 3','1a + 2b >= 4']
sympleks = []
'''How many uknowns'''
hmu = 2
'''How many constrains'''
hmc = 2

init()
