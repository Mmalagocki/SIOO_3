from collections import defaultdict as ddict
import numpy as np

'''
Creating main matrix
Array of arrays: Array - Main matrix
'''
def create_sympleks(Array):
    hmc_range = range(0, hmc)

    for i in hmc_range:
        column = get_parameters(constrains[i])
        #print("column => ", column)
        column_range = range(0,len(column))
        for i in column_range:
            Array.append(column[i])
    #print("unpacked =>", Array)
    ''' Stolen from stack'''
    group = ddict(list)

    for xi, value in Array:
        group[xi].append(value)
    Array = [[xi, *values] for xis, values in group.items()]

    ''''''
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
    #chr(ord(letter) + i)
    str_fun = delete_whitespaces(str_fun)
    range_of_search = range(0, hmu)
    last_found = 0
    values_array = []
    for i in range_of_search:
        j = 0
        while str_fun.find(chr(ord(letter) + i), last_found) != -1:
            found_index = str_fun.find(chr(ord(letter) + i), last_found)
            #print('found index =>', found_index)
            parameter_value = str_fun[last_found:found_index]
            #print('parameter_value =>', parameter_value)
            last_found =  found_index + 1
            #print('last_found =>', last_found)
            if j == 0:
                values_array.append(["x[" + str(i) + "]", parameter_value])

                parameter_value
            else:
                print("The given function was incorrect")
                return 0
            j+=1
        if j == 0:
            values_array.append(["x[" + str(i) + "]",0])
    return values_array
    #str_fun.find("")

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
    #print(values_array)
    sympleks = []
    sympleks = create_sympleks(sympleks)
    #print(sympleks)
    TwoPhaseMethod(sympleks, values_array)

def TwoPhaseMethod(sympleks, values_array):
    Initial_XB = []
    hmc_range = range(0, hmc)
    first_row_values = []

    for i in hmc_range:
        Initial_XB.append(["A[" + str(i) + "]", 1])

    sympleks_len = len(sympleks)
    sympleks_range = range(0, sympleks_len - hmc)
    temp_array = []
    for a in hmc_range:
        for i in hmc_range:
            for j in sympleks_range:
                    temp_array.append(sympleks[j][i+1] * Initial_XB[i][1])
        zj_array = []
    
        for j in sympleks_range:
            first_val = float(temp_array[j])
            second = float(temp_array[j + sympleks_len - hmc])
            zj_array.append(first_val + second)
            
        biggest_value = np.max(zj_array)
        biggest_value_index = zj_array.index(max(zj_array))
        xb_div_xi = []
    
        for i in hmc_range:
            xb_div_xi.append(float(sympleks[sympleks_len - hmc + i][1]) / float(sympleks[biggest_value_index][i+1]))
    
        smallest_value_index = xb_div_xi.index(min(xb_div_xi))
        Initial_XB[smallest_value_index] = values_array[biggest_value_index]
        sovling_element = float(sympleks[biggest_value_index][smallest_value_index + 1])
    
        for i in sympleks_range:
            sympleks[i][smallest_value_index + 1] = float (sympleks[i][smallest_value_index + 1])/ sovling_element
    print(Initial_XB)
    print(sympleks)

function = '2a+ 1b'
constrains = []
constrains = ['1a + 1b >= 3','1a + 2b >= 4']
sympleks = []
'''How many uknowns'''
hmu = 2
'''How many constrains'''
hmc = 2

init()
