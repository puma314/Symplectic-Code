#Roger Van Peski, 1/13/14
#Created to examine interesting properties of the Theta set of raising operators
from pylab import *
from numpy import *


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



def make_tuple(differences):
    '''take a tuple of differences from
    permutations and gives a partition'''
    l = [differences[0]]
    for i in range(len(differences)-1):
        l.append(l[i]+differences[i+1])
    l = l[::-1] #reverse list
    return l

def reachable_partitions(partition,k):
    '''gives every partition reachable by something in Theta(partition)'''
    S = [partition]
    n = len(partition)
    loop = True
    while loop:
        S_old = S
        for partition1 in S:
            new_reachables = []
            for i in range(n-1):
                if partition1[i] == partition1[i+1] + k:
                    newlist = copy_my_list(partition1)
                    newlist[i] -= 1; newlist[i+1] += 1
                    new_reachables.append(newlist)
            for reachable in new_reachables:
                if reachable not in S:
                    S.append(reachable)
        if S == S_old:
             loop = False
    return S

                    
def vectors(partition,k):
    '''returns the vector versions of all possible
    raising operators in Theta(partition)'''
    S = reachable_partitions(partition,k)
    newset = []
    for s in S:
        newset.append(list(array(s) - array(partition)))
    return newset

def remove_duplicates(i):
  output = []
  for x in i:
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

def difference_list(length,k):
    '''gives data structure to loop over all possibilities +1, +2, +3 ... +k'''
    lists = [[]]
    for i in range(length):
        make_copies(lists,k-1)
        for it in range(len(lists)/k):
            for c in range(k):
                lists[it+c*len(lists)/k].append(c+1) 
    return lists


def make_partitions(n,k):
    differences = difference_list(n-1,k)
    partitions = []
    for d in differences:
        partition = [0]
        for difference in d:
            partition.append(partition[-1]+difference)
        partition = partition[::-1]
        partitions.append(partition)
    return partitions

def make_nonstrict_partitions(n):
    differences = nonstrict_difference_list(n-1)
    partitions = []
    for d in differences:
        partition = [0]
        for difference in d:
            partition.append(partition[-1]+difference)
            partition = partition[::-1]
            partitions.append(partition)
    return partitions    


def standard_thetaset(n):
    '''take the thetaset using our normal notation in terms
    of elementary raising operators, doing them in order of
    last to first (just like regular notation); if the order
    doesn't matter, then it'll just choose the ones closer
    to the front of the string first.'''
    

def distinct_partitions(n,k):
    '''for each element of the theta superset on length n
    gives a representative partition for each possible
    theta set'''
    all_partitions = make_partitions(n,k+1)
    good_partitions = []
    raising_ops = []
    for p in all_partitions:
        v = vectors(p,k)
        if v not in raising_ops:
            good_partitions.append(p)
            raising_ops.append(v)
    return good_partitions
        

def find_thetaset(n,k):
    '''a more efficient version of find_thetaset (old version)'''
    partitions = make_partitions(n,k+1)
    raising_ops = []
    for p in partitions:
        raising_ops.append(vectors(p,k))
    raising_ops = remove_duplicates(raising_ops)
    return raising_ops

def partition_checker(n,k,d):
    '''finds all 'ghost partitions' of length n, considering the k
    last parts, with omegaset difference of d'''
    longpartitions = distinct_partitions(n,d)
    shortpartitions = distinct_partitions(k,d)
    redundant_partitions = []
    for p in longpartitions:
        if p[n-k:n] not in shortpartitions:
            redundant_partitions.append(p)
    return redundant_partitions
        
def thetaset_sequence(k,n):
    '''defines thetaset procedure for difference k, and tests
    size of thetasets up to length n to output a sequence'''
    for i in range(1,n+1):
        print str(len(find_thetaset(i,k)))
    return

##print 'For partitions of length 1:'
##s1 = find_thetaset(1)
##ss1 = parse_thetaset(s1)
##print 'For partitions of length 2:'
##s2 = find_thetaset(2)
##ss2 = parse_thetaset(s2)
##print 'For partitions of length 3:'
##s3 = find_thetaset(3)
##ss3 = parse_thetaset(s3)
##print 'For partitions of length 4:'
##s4 = find_thetaset(4)
##ss4 = parse_thetaset(s4)
##print 'For partitions of length 5:'
##s5 = find_thetaset(5)
##ss5 = parse_thetaset(s5)
##print 'For partitions of length 6:'
##s6 = find_thetaset(6)
##ss6 = parse_thetaset(s6)
##print 'For partitions of length 7:'
##s7 = find_thetaset(7)
##ss7 = parse_thetaset(s7)
##print 'For partitions of length 8:'
##s8 = find_thetaset(8)
##ss8 = parse_thetaset(s8)
##print 'For partitions of length 9:'
##s9 = find_thetaset(9)
##ss9 = parse_thetaset(s9)
##print 'For partitions of length 10:'
##s10 = find_thetaset(10)
##ss10 = parse_thetaset(s10)
##print 'For partitions of length 11:'
##s11 = find_thetaset(11)
##ss11 = parse_thetaset(s11)
##
##
##
##
##
##
##
##
##
##
##    
##
