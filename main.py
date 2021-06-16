from collections import defaultdict as ddict
import numpy as np
import copy
from tkinter import *



########################## GUI #############################
def main_programm():
    Label(frame, text="Please provide required data").grid(row = 0)
    
    Label(frame, text="Function:").grid(row = 1)
    function_input = Entry(frame, width = 20, cursor = 'hand2')
    function_input.insert(0,'2a+ 1b')
    function_input.grid(row=1 , column=1, pady = 10)
    
    Label(frame, text="How many uknowns:").grid(row = 2)
    hmu_imput = Entry(frame, width = 20, cursor = 'hand2')
    hmu_imput.insert(0,'2')
    hmu_imput.grid(row = 2 , column=1, pady = 10)
    
    Label(frame, text="Pass the constrains(seperate them with ','):").grid(row = 3)
    constrains_input = Entry(frame, width = 20, cursor = 'hand2')
    constrains_input.insert(0,'1a + 1b >= 3,1a + 2b >= 4,')
    constrains_input.grid(row = 3 , column = 1, pady = 10)

    Button_submit = Button(frame, text = "Submit", command = lambda: set_and_init(function_input.get(), 
                                                                               hmu_imput.get(), 
                                                                               constrains_input.get(),
                                                                               ))
    Button_submit.grid(row=6 , column=1)

def choose_main_condition(chosen_condition):
    if (chosen_condition == "Two constrains"):
        set_hmc(2)
        main_programm()
    elif(chosen_condition == "Three constrains") :
        set_hmc(3)
        main_programm()
    elif(chosen_condition == "Four constrains") :
        set_hmc(4)
        main_programm()
    else:
        something_went_wront(chosen_condition)

def something_went_wront(chosen_condition):
    Label(frame, text="Sorry! Something went wrong. Here is the codition: " + chosen_condition).grid(row=0)

def set_function(input_string):
    global function
    function = input_string

def set_hmu(n):
    global hmu
    hmu = int(n)

def set_hmc(n):
    global hmc
    hmc = int(n)

def set_constrains(n):
    global constrains
    constrains = get_constrains(n)
    print("constrains", constrains)

def set_and_init(function_str, hmu_str, constrains_str):
    set_function(function_str)
    set_hmu(hmu_str)
    set_constrains(constrains_str)
    init()

########### COMPUTING ########## 
'''
Geting values from given fun
'''
def get_constrains(constrains_str):
    constrains_str = delete_whitespaces(constrains_str)
    range_of_search = range(0, hmc)
    last_found = 0
    constrains_array = []
    while constrains_str.find(',', last_found) != -1:
        found_index = constrains_str.find(',', last_found)
        constrain = constrains_str[last_found:found_index]
        last_found =  found_index + 1
        constrains_array.append(constrain)
    return constrains_array
    
'''
Geting values from given fun
'''
def get_values_from_initial_function():
    letter = 'a'
    str_fun = delete_whitespaces(function)
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
    for i in range_of_search:
        values_array.append(["S[" + str(i+1) + "]",0])
    return values_array

'''
Creating main matrix
Array of arrays: Array - Main matrix
'''
def create_sympleks(Array):
    hmc_range = range(0, hmc)
    print("HOW MANY HMC?", hmc)
    for i in hmc_range:
        column = get_parameters(constrains[i])
        column_range = range(0,len(column))
        for i in column_range:
            Array.append(column[i])

    group = ddict(list)

    for xi, value in Array:
        group[xi].append(value)
    Array = [[xi, *values] for xis, values in group.items()]
    Array_len = len(Array)
    Array_range = range(0, Array_len)
    
    for i in Array_range:
        string = "x[" + str(i) + "]"
        Array[i][0] = string
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
    print("Moving to the second phase")
    values_array = []
    values_array = get_values_from_initial_function()
    Initial_XB = get_parameters(function)
    cjzj_array = [1]
    max_value = max(cjzj_array)
    while( max_value > 0):
        sympleks_len = len(sympleks) - hmc
        sympleks_range = range(0, sympleks_len )
        column_values = []
        for j in sympleks_range:
            temp_array = []
            for i in hmc_range:
                temp_array.append(float(float(sympleks[j][i+1]) * float(Initial_XB[i][1])))
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
        if(max(cjzj_array) <= 0):
            print("********** I HAVE FINISHED CALCULATING **********")
            print("After changing values => ", sympleks)
            print(Initial_XB)
            print("cjzj_array =>",cjzj_array)
            return Initial_XB
        for i in hmc_range:
            xb_div_xi_reulst = float(sympleks[sympleks_len + i][1]) / float(sympleks[biggest_value_column][i+1])
            if(xb_div_xi_reulst > 0):
                xb_div_xi.append(xb_div_xi_reulst)
            else:
                #do nothing
                continue
        smallest_value_row = xb_div_xi.index(min(xb_div_xi))
        RE = float(sympleks[biggest_value_column][smallest_value_row + 1])
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
        print("cjzj_array =>",cjzj_array)
        max_value = np.max(cjzj_array)
    print("After changing values => ", sympleks)
    print(Initial_XB)
    print("cjzj_array =>",cjzj_array)

########### DEBUGGING ########## 
#function = '2a+ 1b' 
#constrains = []
#constrains = ['1a + 1b >= 3','1a + 2b >= 4']
#sympleks = []
#'''How many uknowns'''
#hmu = 2
#'''How many constrains'''
#hmc = 2

#init()

########### SELECT MENU ###########
root = Tk()
root.geometry("1200x900")
root.title("MM&MJ")

frame = Frame(root)
B = Button(root, text = "Submit", command = lambda: choose_main_condition(tkvarq.get()) )

options = ["How many constrains",
           "Two constrains",
           "Three constrains",
           "Four constrains",
           ]

## SELECT MENU
tkvarq = StringVar(root)
tkvarq.set(options[1])
question_menu = OptionMenu(root, tkvarq, *options)
question_menu.pack()
B.pack()
frame.pack()
### DISPLAYS CHOSEN VERSION
root.mainloop()
