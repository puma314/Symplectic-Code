#Roger Van Peski, 9/29/13
#new_coefficients.py

def copy_my_goddamn_list(l): #this is probs unnecessary, but python was being bitchy about multiple references and stuff
    newlist = []
    for i in range(len(l)):
        newlist.append(l[i])
    return newlist

def triple_list(l): #see above comment
    length = len(l)
    for i in range(length):
        l.append(copy_my_goddamn_list(l[i]))
    for i in range(length):
        l.append(copy_my_goddamn_list(l[i]))
    return
    

def config_list(length):
    '''gives data structure to loop over all possibilities of chain
    and slice, and automatically removes illegal configurations'''
    lists = [[]]
    for i in range(length):
        triple_list(lists)
        for it in range(len(lists)/3):
            lists[it].append(0) #this corresponds to choosing the chain
            lists[it+len(lists)/3].append(1) #corresponds to choosing first (left-sided) entry of property list
            lists[it+2*len(lists)/3].append(2) #corresponds to choosing second (right-sided) entry of property list
    for config in lists: #this is where we get rid of illegal configs
        for i in range(length-1):
            if config[i] == 2 and config[i+1] == 1:
                lists.remove(config)
                break
    return lists
            
            
def property_set(row1,row2): #pretty self-explanatory
    propertyset = []
    for index in range(len(row2)):
        entryset = [0,0,0] #first term is chain coefficient, second is left slice, third is right slice
        if row2[index] == row1[index] or row2[index] == row1[index+1]:
            entryset[0] = '0'
        if row2[index] != row1[index] and row2[index] != row1[index+1]:
            entryset[0] = '(1-t)(1-q)'
        if row2[index] == row1[index]:
            entryset[1] = '(-q)'
        if row2[index] == row1[index]-1:
            entryset[1] = 't'
        if row2[index] < row1[index]-1:
            entryset[1] = '0'
        if row2[index] == row1[index+1]:
            entryset[2] = '1'
        if row2[index] == row1[index+1]+1:
            entryset[2] = '(-q*t)'
        if row2[index] > row1[index+1]+1:
            entryset[2] = '0'
        propertyset.append(entryset)
    return propertyset
    

        
def coefficient(row1,row2):
    '''takes as input top row and second row of a GT
    pattern, outputs coefficient using new method'''
    length = len(row2)
    configs = config_list(length)
    propertyset = property_set(row1,row2)
    coeff_string = 'Expand['
    for i in range(len(configs)): #chooses a configuration of chain and slice terms
        config = configs[i]
        coefficient = ''
        for it in range(len(config)):
            coefficient += str(propertyset[it][config[it]])
            if it != len(config)-1:
                coefficient += '*'
        coeff_string += coefficient
        if i != len(configs)-1:
                 coeff_string += '+'
    coeff_string += ']'
    return coeff_string
        
    
    
