#This script is meant to be used with Sage, and computes stuff related to our matrix
from pylab import *
from numpy import *

R, (q, t) = PolynomialRing(RationalField(), 2, 'qt').objgens()
#^makes sage computer algebra work; rerun this if you set q and t to a given value and want them as an indeterminate again

#This is code from new_coefficients.py:

def copy_my_list(l): #this is a deep copy, since for some reason the regular deep copy wasn't working...
    newlist = []
    for i in range(len(l)):
        newlist.append(l[i])
    return newlist

def make_copies(l,n):
    '''makes n copies of every list in list of lists l'''
    length = len(l)
    for index in range(n):
        for i in range(length):
            l.append(copy_my_list(l[i]))
    return
            

def make_rows(toprow): #makes all possible second rows
    rows = [[]]
    for i in range(len(toprow)-1):
        old_length = len(rows)
        d = toprow[i]-toprow[i+1]+1
        make_copies(rows,d-1)
        choices = range(toprow[i+1],toprow[i]+1)
        for a in range(d):
            for b in range(old_length*a,old_length*(a+1)):
                rows[b].append(choices[a])
    return rows
                   

def is_strict(row):
    for i in range(len(row)-1):
        if row[i] == row[i+1]:
            return False
    return True

#end of code copied from new_coefficients

##def zero_mat(n): #creates nxn zero matrix, with elements in the polynomial ring so stuff doesn't get screwed up
##    A = []
##    for i in range(n):
##        l = []
##        for j in range(n):
##            l.append(0*q)
##        A.append(l)
##    M = matrix(A)
##    return M
##            

def property_set(row1,row2): #pretty self-explanatory, uncomment the first lines if you want to set q and t to a specific value
    #q=1
    #t=1
    propertyset = []
    for index in range(len(row2)):
        entryset = [0,0,0] #first term is c coefficient, second is left slice, third is right slice
        if row2[index] == row1[index] or row2[index] == row1[index+1]:
            entryset[0] = 0
        if row2[index] != row1[index] and row2[index] != row1[index+1]:
            entryset[0] = (1-t)*(1-q)
        if row2[index] > row1[index]: #outward
            entryset[1] = 0
        if row2[index] == row1[index]:
            entryset[1] = (-q)
        if row2[index] == row1[index]-1:
            entryset[1] = t
        if row2[index] < row1[index]-1:
            entryset[1] = 0
        if row2[index] < row1[index+1]: #outward
            entryset[2] = 0
        if row2[index] == row1[index+1]:
            entryset[2] = 1
        if row2[index] == row1[index+1]+1:
            entryset[2] = (-q*t)
        if row2[index] > row1[index+1]+1:
            entryset[2] = 0
        propertyset.append(entryset)
    return propertyset



def coef_matrix(row1,row2):
    '''creates the coefficient matrix M(row1;row2)'''
    if len(row1) != len(row2)+1:
        return 'Your rows are the wrong sizes, sir'
    n = len(row2)
    M = zero_matrix(R,n,n)
    prop_set = property_set(row1,row2)
    for i in range(n-1):
        M[i,i+1] = 1
    differences = []
    for i in range(n-1):
        difference = prop_set[i][2]*prop_set[i+1][1]
        M[i+1,i] = difference
    for i in range(n):
        c = prop_set[i][0]
        dl = prop_set[i][1]
        dr = prop_set[i][2]
        M[i,i] = c+dl+dr
    return M

def all_matrices(toprow):
    '''makes a list of all matrices associated to
    GT2 patterns of a given top row'''
    rows = make_rows(toprow)
    matrices = []
    for row in rows:
        M = coef_matrix(toprow,row)
        matrices.append(M)
    return matrices

def display_matrices(toprow): #displays all possible GT2 patterns and associated matrices of a given top row
    rows = make_rows(toprow)
    matrices = all_matrices(toprow)
    for i in range(len(rows)):
        print 'GT2 pattern: '
        print str(toprow)
        print str(rows[i])
        print 'Associated matrix: '
        print str(matrices[i])
        print ''
    return

def wedgerow(row1,row2): #takes the product of wedges of a GT2 pattern
    p = 1
    for i in range(len(row2)):
        a = row1[i]
        b = row1[i+1]
        c = row2[i]
        if c == a and c == b+1: #lar
            p *= -q*(1+t)
        if c == a and not c == b+1: #l
            p *= -q
        if c == a-1 and c == b: #alr
            p *= (1+t)
        if c == a-1 and c == b+1: #alar
            p *= (1-q)
        if c == a-1 and c > b+1: #al
            p *= (1-q+q*t)
        if c < a-1 and c == b: #r
            p *= 1
        if c < a-1 and c == b+1: #ar
            p *= (1-q-t)
        if c < a-1 and c > b+1: #s
            p *= (1-q)*(1-t)
    return p
        
###############################################
#Here is the code from Theta_stuff
########################################
def copy_my_list(l): #this is a deep copy, since for some reason the regular deep copy wasn't working...
    newlist = []
    for i in range(len(l)):
        newlist.append(l[i])
    return newlist

def make_copies(l,n):
    '''makes n copies of every list in list of lists l'''
    length = len(l)
    for index in range(n):
        for i in range(length):
            l.append(copy_my_list(l[i]))
    return

def make_copies2(l,n):
    '''makes n copies of every list in list of lists l'''
    length = len(l)
    for index in range(n):
        for i in range(length):
            l.append(copy_my_list(l[i]))
    return l


def permutation_list(length,s): 
    '''gives data structure to loop over all possibilities of
    differences between consecutive terms. length is the number
    of pairs of consecutive entries in the tuple, so n-1 for an
    n-tuple. s is a set of possible differences between consecutive
    terms, put in whatever works.'''
    n = len(s)
    lists = [[]]
    for i in range(length):
        make_copies(lists,n-1)
        for it in range(len(lists)/n):
            for a in range(n):
                lists[it+a*len(lists)/n].append(s[a])
    return lists

def make_tuple(differences):
    '''take a tuple of differences from
    permutations and gives a partition'''
    l = [differences[0]]
    for i in range(len(differences)-1):
        l.append(l[i]+differences[i+1])
    l = l[::-1] #reverse list
    return l

def theta_set(partition):
    '''takes a partition as a list, outputs the set of
    everything in \Theta(\lambda) for that partition'''
    raising_ops = set([])
    raised_partitions = set([partition])
    while loopagain == True:
        loopagain = False
        for partition in raised_partitions:
            for i in range(len(differences)-2):
                if partition[i] == partition[i+1]:
                    newlist = copy_my_list(partition)
                    newlist[i] -= 1; newlist[i+1] += 1
                    raised_partitions.add(newlist)
                    raising_ops.add('[' + str(i+1) + str(i+2) + ']')
                    loopagain = True


def old_reachable_partitions(partition): #used at first, but misses some
    '''gives every partition reachable by something in Theta(partition)'''
    S = [partition]
    n = len(partition)
    loop = True
    while loop:
        loop = False
        for partition1 in S:
            for i in range(n-1):
                if partition1[i] == partition1[i+1] + 2:
                    newlist = copy_my_list(partition1)
                    newlist[i] -= 1; newlist[i+1] += 1
                    if newlist not in S:
                        loop = True
                    else:
                        break
                    S.append(newlist)
    return S

def reachable_partitions(partition):
    '''gives every partition reachable by something in Theta(partition)'''
    S = [partition]
    n = len(partition)
    loop = True
    while loop:
        S_old = S
        for partition1 in S:
            new_reachables = []
            for i in range(n-1):
                if partition1[i] == partition1[i+1] + 2:
                    newlist = copy_my_list(partition1)
                    newlist[i] -= 1; newlist[i+1] += 1
                    new_reachables.append(newlist)
            for reachable in new_reachables:
                if reachable not in S:
                    S.append(reachable)
        if S == S_old:
             loop = False
    return S
                    







    
                    
def vectors(partition):
    '''returns the vector versions of all possible
    raising operators in Theta(partition)'''
    S = reachable_partitions(partition)
    newset = []
    for s in S:
        newset.append(list(array(s) - array(partition)))
    return newset

    

def remove_duplicates(input):
  output = []
  for x in input:
    if x not in output:
      output.append(x)
  return output

##def sort_randoms(n,bunch): #this is a stupidass script, use the one below
##    '''makes a bunch of (strict) partitions of length n within reasonable limits,
##    and gives you each distinct vector version of theta set found'''
##    partitions = [] 
##    for it in range(bunch):
##        partition = []
##        partition.append(3*n)
##        for i in range(1,n):
##            r = randint(n-1-i,partition[-1])
##            partition.append(r)
##        partitions.append(partition)
##    partitions = remove_duplicates(partitions) #removes duplicates
##    raising_ops = []
##    for p in partitions:
##        raising_ops.append(vectors(p))
##    raising_ops = remove_duplicates(raising_ops)
##    return raising_ops

def recursive_partition_filler(partitions,n): #this is needed for the next one
    '''partitions is a list of partitions (lists) of the same length,
    n is the length we want the partition to get to'''
    p = partitions[0]
    if len(p) == n:
        return partitions
    elif len(p) < n:
        newpartitions = []
        for partition in partitions:
            part_list = make_copies2([partition],partition[-1]-1) 
            for a in range(len(part_list)):
                t = part_list[a]
                t.append(a)
            newpartitions += part_list
        return recursive_partition_filler(newpartitions,n)
                



##def find_thetaset(n):
##    '''finds the theta set on partitions of length n
##    with less stupid methods than the previous (random) one'''
##    partitions = recursive_partition_filler([[3*n]],n)
##    raising_ops = []
##    for p in partitions:
##        raising_ops.append(vectors(p))
##    raising_ops = remove_duplicates(raising_ops)
##    return raising_ops
##    
    
def parse_thetaset(thetaset):
    newthetaset = []
    counter = 0
    max_length = 0
    for element in thetaset:
        max_length = max(max_length,len(element))
    print 'maximum length: ' + str(max_length)
    for i in range(1,max_length+1):
        newset = []
        for e in thetaset:
            if len(e) == i:
                newset.append(e)
        newthetaset.append(newset)
        print 'The number of theta sets with ' + str(i) + ' elements is ' + str(len(newset))
    return newthetaset

def triple_list(l): #see above comment
    length = len(l)
    for i in range(length):
        l.append(copy_my_list(l[i]))
    for i in range(length):
        l.append(copy_my_list(l[i]))
    return


def difference_list(length):
    '''gives data structure to loop over all possibilities +1, +2, +3'''
    lists = [[]]
    for i in range(length):
        triple_list(lists)
        for it in range(len(lists)/3):
            lists[it].append(1) 
            lists[it+len(lists)/3].append(2)
            lists[it+2*len(lists)/3].append(3) 
    return lists


def find_thetaset(n):
    '''a more efficient version of find_thetaset'''
    differences = difference_list(n-1)
    partitions = []
    raising_ops = []
    for d in differences:
        partition = [0]
        for difference in d:
            partition.append(partition[-1]+difference)
        partition = partition[::-1]
        partitions.append(partition)
    for p in partitions:
        raising_ops.append(vectors(p))
    raising_ops = remove_duplicates(raising_ops)
    return raising_ops
####################################
#end of the code from Theta_stuff
####################################

def length(r):
    '''length of a raising operator in vector form'''
    l = len(r)
    rlength = 0
    counter = 0
    for i in range(l):
        rlength += i*r[i]
        counter += r[i]
    if counter != 0:
        print "this is not a valid raising operator"
    return rlength
            
def cool_coef(row1,row2):
    '''gives you the total coefficient, accounting for
    the action of omega on row2 and the raising t^len(phi),
    and automatically takes all the determinants and multiplies
    by the correct factor to just give a coefficient'''
    omega = vectors(row2)
    coefficient = 0
    for raising_op in omega:
        l = length(raising_op)
        newrow2 = list(array(row2)+array(raising_op))
        M = coef_matrix(row1,newrow2)
        det = M.det()
        coefficient += (t**l)*det
    return coefficient

def swag_coef(row1,row2):
    '''gives you the total coefficient, NOT accounting for omega,
    and automatically takes all the determinants and multiplies
    by the correct factor to just give a coefficient'''
    M = coef_matrix(row1,row2)
    det = M.det()
    return det

def total_coef(L):
    '''takes a GT pattern, gives coefficient, NOT accounting for omega'''
    coef = 1
    for i in range(len(L)-1):
        coef *= swag_coef(L[i],L[i+1])
    return coef

def reverse_coef(row2,row3):
    coef = 0
    if row2[0] != row3[0] and row2[1] != row3[0]:
        coef += (1-q)*(1-t)
    if row2[0] == row3[0]:
        coef +=1
    elif row2[0] == row3[0] + 1:
        coef += -q*t
    elif row2 > row3[0]+1:
        coef += 0
    if row2[1] == row3[0]:
        coef +=-q
    elif row2[1] == row3[0] -1:
        coef += t
    elif row2[1] < row3[0]-1:
        coef += 0
    return coef
        

def crazy_coef(row1,row2,row3): #implement's vineet's procedure, ask him
    coef = swag_coef(row1,row2)*reverse_coef(row2,row3)
    return coef

def crazy_coef2(row1,row2,row3): #like crazy_coef but accounts for omega
    coef = cool_coef(row1,row2)*reverse_coef(row2,row3)
    return coef


def wedge(left,right,bottom):
    coef = 0
    if bottom != left and bottom != right:
        coef += (1-q)*(1-t)
    if bottom == left:
        coef +=1
    elif bottom == left - 1:
        coef += -q*t
    if bottom == right:
        
        
def new_coef(row1,row2,row3):
    row1 = row1+[0]
    coef = crazy_coef2(row1,row2,row3)
    row3 = row3+[0]
    coef2 = 0
    if row2[0] != row3[0] and row2[1] != row3[0]:
        coef2 = (1-q)*(1-t)
    if row2[0] == row3[0]:
        coef1 +=1
    elif row2[0] == row3[0] + 1:
        coef1 += -q*t
    elif row2 > row3[0]+1:
        coef1 += 0
    if row2[1] == row3[0]:
        coef1 +=-q
    elif row2[1] == row3[0] -1:
        coef1 += t
    elif row2[1] < row3[0]-1:
        coef1 += 0
    
