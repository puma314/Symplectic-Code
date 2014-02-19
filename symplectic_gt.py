#Roger Van Peski, 2/16/14
from copy import *




def is_strict(row):
    for i in range(len(row)-1):
        if row[i] == row[i+1]:
            return False
    return True

def make_copies(l,n):
    '''makes n copies of every list in list of lists l'''
    length = len(l)
    for index in range(n):
        for i in range(length):
            l.append(deepcopy(l[i]))
    return

def nest_partitions(toprow,is_barred):
    '''makes all possible strict partitions nesting in toprow;
    is_barred refers to barredness of toprow'''
    rows = [[]]
    newrows = []
    for i in range(len(toprow)-1):
        old_length = len(rows)
        bound = toprow[i+1]
        if is_barred: #accounts for barred row zero analness
            bound = max(1,toprow[i+1])
        d = toprow[i]-bound
        make_copies(rows,d)
        choices = range(bound,toprow[i]+1)
        for a in range(toprow[i]+1-bound):
            for b in range(old_length*a,old_length*(a+1)):
                rows[b].append(choices[a])
    for row in rows:
        if is_strict(row):
            newrows.append(row)            
    return newrows

def make_rows(toprow,is_barred):
    '''nests a row to toprow, treating it as either barred or nonbarred'''
    if is_barred:
        return nest_partitions(toprow,is_barred)
    else:
        return nest_partitions(toprow + [0],is_barred)

def secondrowlists(toprow,is_barred):
    '''makes a list of all possible GT2 patterns of given top row'''
    newrows = make_rows(toprow,is_barred)
    newnewrows = []
    for row in newrows:
        newnewrows.append([deepcopy(toprow),row])
    return newnewrows
        

def all_patterns(toprow):
    '''makes all symplectic gt patterns with given top row'''
    patterns = secondrowlists(toprow,False)
    looping = True
    while looping:
        if len(patterns[0][-1]) == 1 and len(patterns[0][-2]) == 1: #when done
            looping = False
            break
        newnewpatterns = []
        for pattern in patterns:
            is_barred = (len(pattern[-1]) == len(pattern[-2]))
            newrows = make_rows(pattern[-1],is_barred)
            l = len(newrows)
            newpatterns = [pattern]
            make_copies(newpatterns,l-1)
            for i in range(l):
                newpatterns[i] += [newrows[i]]
            newnewpatterns += newpatterns
        patterns = newnewpatterns
    return patterns

def all_secondrowpatterns(toprow):
    '''makes all symplectic secondrows (i.e. lists of first, second, and
    third row so that we can calculate wgt_1(T)'''
    patterns = secondrowlists(toprow,False)
    looping = True
    newnewpatterns = []
    for pattern in patterns:
        is_barred = (len(pattern[-1]) == len(pattern[-2]))
        newrows = make_rows(pattern[-1],is_barred)
        l = len(newrows)
        newpatterns = [pattern]
        make_copies(newpatterns,l-1)
        for i in range(l):
            newpatterns[i] += [newrows[i]]
        newnewpatterns += newpatterns
    patterns = newnewpatterns
    return patterns

def indexed_secondrows(toprow):
    patterns = all_secondrowpatterns(toprow)
    weights = []
    weight_dict = {}
    for pattern in patterns:
        weight = sum(pattern[0]) - 2*sum(pattern[1]) + sum(pattern[2])
        if weight in weight_dict:
            weight_dict[weight].append(pattern)
        else:
            weight_dict[weight] = [pattern]
    for i in range(min(weight_dict),max(weight_dict)+1):
        print 'All patterns for which wgt_1(T) = ' + str(i) + ':'
        for pattern in weight_dict[i]:
            print pattern
    return weight_dict



def indexed_patterns(toprow):
    '''indexes all patterns with given top row by wgt_1(T)'''
    patterns = all_patterns(toprow)
    weights = []
    weight_dict = {}
    for pattern in patterns:
        weight = sum(pattern[0]) - 2*sum(pattern[1]) + sum(pattern[2])
        if weight in weight_dict:
            weight_dict[weight].append(pattern)
        else:
            weight_dict[weight] = [pattern]
    for i in range(min(weight_dict),max(weight_dict)+1):
        print 'All patterns for which wgt_1(T) = ' + str(i) + ':'
        for pattern in weight_dict[i]:
            print pattern
    return weight_dict
        
            
def mathematica_gts(toprow):
    pylist = all_patterns(toprow)
    pystring = str(pylist)
    pystring2 = pystring.replace('[','{')
    pystring3 = pystring2.replace(']','}')
    return pystring3

def mathematica_secondrows(toprow):
    pylist = all_secondrowpatterns(toprow)
    pystring = str(pylist)
    pystring2 = pystring.replace('[','{')
    pystring3 = pystring2.replace(']','}')
    return pystring3

            
    
    
