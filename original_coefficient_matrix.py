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

def zero_mat(n): #creates nxn zero matrix, with elements in the polynomial ring so stuff doesn't get screwed up
    A = []
    for i in range(n):
        l = []
        for j in range(n):
            l.append(0*q)
        A.append(l)
    M = matrix(A)
    return M
            

def property_set(row1,row2): #pretty self-explanatory, uncomment the first lines if you want to set q and t to a specific value
    #q=1
    #t=1
    propertyset = []
    for index in range(len(row2)):
        entryset = [0,0,0] #first term is c coefficient, second is left difference, third is right difference
        if row2[index] == row1[index] or row2[index] == row1[index+1]:
            entryset[0] = 0
        if row2[index] != row1[index] and row2[index] != row1[index+1]:
            entryset[0] = (1-t)*(1-q)
        if row2[index] == row1[index]:
            entryset[1] = (-q)
        if row2[index] == row1[index]-1:
            entryset[1] = t
        if row2[index] < row1[index]-1:
            entryset[1] = 0
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
    M = zero_mat(n)
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
        M[i,i] = c-dl-dr
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
        

