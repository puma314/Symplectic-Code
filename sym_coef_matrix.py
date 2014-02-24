#Roger Van Peski, 2/24/2014
from pylab import *
from numpy import *

R, (q, t) = PolynomialRing(RationalField(), 2, 'qt').objgens()
#^makes sage computer algebra work; rerun this if you set q and t to a given value and want them as an indeterminate again

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

def flipped_prop_set(row1,row2):
    '''gives the 'flipped' property set, i.e. left
    and right,almost left and almost right reversed.'''
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
        if row2[index] == row1[index]: #left
            entryset[1] = 1
        if row2[index] == row1[index]-1: #almost left
            entryset[1] = (-q*t)
        if row2[index] < row1[index]-1: #left_special
            entryset[1] = 0
        if row2[index] < row1[index+1]: #outward
            entryset[2] = 0
        if row2[index] == row1[index+1]: #right
            entryset[2] = (-q)
        if row2[index] == row1[index+1]+1: #almost right
            entryset[2] = t
        if row2[index] > row1[index+1]+1: #right-special
            entryset[2] = 0
        propertyset.append(entryset)
    return propertyset

##def wedge(left,right,bottom):
##    coef = 0
##    if bottom != left and bottom != right:
##        coef += (1-q)*(1-t)
##    if bottom == left:
##        coef +=1
##    elif bottom == left - 1:
##        coef += -q*t
##    if bottom == right:


    


def rvpmatrix1(row1,row2,row3):
    '''conjectural matrix of a secondrowpattern. Uses both ghost zeros,
    and take row1/row2 regular wedges, row2/row3 flipped upside down
    wedges, row1/row2 regular differences, and row2/row3 flipped upside
    down differences.'''
    if len(row1) != len(row2) or len(row2) != len(row3)+1:
        print'Your rows are the wrong sizes, sir'
        return
    k = len(row1)
    n = 2*k-1
    M = zero_matrix(R,n,n)
    for i in range(n-1):
        M[i+1,i] = 1
    prop_set1 = property_set(row1+[0],row2)
    for i in range(k):
        M[i,i] = sum(prop_set1[i]) #initialize first wedge entries, row2 wrt row1
    prop_set2 = flipped_prop_set(row2[1:],row3+[0])
    for i in range(k,n):
        M[i,i] = sum(prop_set2[i-k]) #initialize last wedge entries on diagonal
    #now, on to the differences below the diagonal
    for i in range(k-1):
        M[i,i+1] = prop_set1[i][2]*prop_set1[i+1][1]
    for i in range(k-1,n-1):
        M[i,i+1] = prop_set2[i-k+1][2]*prop_set2[i-k+1][2]
    return M
    
    


##row3flip = [0]+row3[::-1]
##    row2flip = row2[::-1][:-1] #flips and cuts first entry
##    prop_set2 = property_set(row2flip,row3flip)
##    for i in range(k,n):
##        M[i,i] = sum(prop_set2[i-k]) #initialize last wedge entries on diagonal
##    

    
