#Roger Van Peski, 2/15/14
#Created to examine interesting properties of the Theta set of raising operators
from pylab import *
from numpy import *
from copy import *

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


def make_tuple(differences):
    '''take a tuple of differences from
    permutations and gives a partition'''
    l = [differences[0]]
    for i in range(len(differences)-1):
        l.append(l[i]+differences[i+1])
    l = l[::-1] #reverse list
    return l

def reachable_partitions(partition,k,d):
    '''gives every partition reachable by something in Theta(partition)'''
    S = [partition]
    n = len(partition)
    loop = True
    while loop:
        S_old = S
        for partition1 in S:
            new_reachables = []
            for i in range(n-1):
##                print partition1
##                print 'done'
##                print type(partition1[i+1])
##                print type(k)
                if partition1[i] == partition1[i+1] + k:
                    newlist = copy_my_list(partition1)
                    newlist[i] -= d; newlist[i+1] += d
                    new_reachables.append(newlist)
            for reachable in new_reachables:
                if reachable not in S:
                    S.append(reachable)
        if S == S_old:
             loop = False
    return S

def adjacent_reachables(partition,k,d):
    reachables = []
    for i in range(len(partition)-1):
            if partition[i] == partition[i+1] + k:
                newpartition = copy_my_list(partition)
                newpartition[i] -= d; newpartition[i+1] += d
                reachables.append(newpartition)
    return reachables

def efficient_reachable_partitions(partition,k,d):
    n = len(partition)
    level = [partition]
    S = []
    counter = 0
    while True:
        S += level
        newlevel = []
        for p in level:
            newlevel += adjacent_reachables(p,k,d)
        if level == newlevel:
            break
        level = newlevel
        newlevel = remove_duplicates(newlevel)
    S = remove_duplicates(S)
    return S

def efficient_reachable_partitions(partition,k,d):
    n = len(partition)
    level = [partition]
    S = []
    counter = 0
    while True:
        S += level
        newlevel = []
        for p in level:
            newlevel += adjacent_reachables(p,k,d)
        if level == newlevel:
            break
        level = newlevel
        newlevel = remove_duplicates(newlevel)
    S = remove_duplicates(S)
    return S



                    
def vectors(partition,k,d):
    '''returns the vector versions of all possible
    raising operators in Theta(partition)'''
    S = reachable_partitions(partition,k,d)
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

def difference_list(length,k,is_strict): #0 for nonstrict, 1 for strict
    '''gives data structure to loop over all possibilities +1, +2, +3 ... +k'''
 #   memory_limit = 8 #point in the sequence at which you need to start compartmentalizing
    lists = [[]]
    for i in range(length):
        make_copies(lists,k-is_strict)
        for it in range(len(lists)/(k+1-is_strict)):
            for c in range(is_strict, k+1):
                lists[it+(c-1)*len(lists)/(k+1-is_strict)].append(c)
    return lists

def reverse_sublists(l):
    '''reverses every list in list of lists l'''
    newlist = []
    for i in l:
        newlist.append(deepcopy(i[::-1]))
    return newlist

def efficient_difference_list(length,k): #incomplete
    '''a more efficient version that takes recursion into
    account and only makes ones in which [12] or [length-1,length]
    is in the raising operators set'''
    lists = [[k-1]]
    for i in range(length-2):
        make_copies(lists,k-1)
        for it in range(len(lists)/k):
            for c in range(k):
                lists[it+c*len(lists)/k].append(c+1)
    for l in lists:
        l.append(k-1)
    return lists


def efficient_make_partitions(n,k):
    differences = efficient_difference_list(n-1,k)
    partitions = []
    for d in differences:
        partition = [0]
        for difference in d:
            partition.append(partition[-1]+difference)
        partition = partition[::-1]
        partitions.append(partition)
    return partitions


def make_partitions(n,k,is_strict): #1 for strict, 0 for nonstrict
    memory_limit = 8 #point in the sequence at which you need to start compartmentalizing
    differences = difference_list(n-1,k,is_strict)
    partitions = []
    for d in differences:
        partition = [0]
        for difference in d:
            partition.append(partition[-1]+difference)
        partition = partition[::-1]
        partitions.append(partition)
    return partitions

def bare_make_partitions(differences):
    '''takes a list of difference lists, turns them into partitions'''
    partitions = []
    for d in differences:
        partition = [0]
        for difference in d:
            partition.append(partition[-1]+difference)
        partition = partition[::-1]
        partitions.append(partition)
    return partitions
    

##def make_nonstrict_partitions(n,k):
##    differences = nonstrict_difference_list(k-1)
##    partitions = []
##    for d in differences:
##        partition = [0]
##        for difference in d:
##            partition.append(partition[-1]+difference)
##            partition = partition[::-1]
##            partitions.append(partition)
##    return partitions    


def standard_thetaset(n):
    '''take the thetaset using our normal notation in terms
    of elementary raising operators, doing them in order of
    last to first (just like regular notation); if the order
    doesn't matter, then it'll just choose the ones closer
    to the front of the string first.'''
    

def distinct_partitions(n,k,d):
    '''for each element of the theta superset on length n
    gives a representative partition for each possible
    theta set'''
    all_partitions = make_partitions(n,k+1)
    good_partitions = []
    raising_ops = []
    for p in all_partitions:
        v = vectors(p,k,d)
        if v not in raising_ops:
            good_partitions.append(p)
            raising_ops.append(v)
    return good_partitions
        

def find_thetaset(n,k,d): #set is_strict to 1 or 0 as desired
    '''a more efficient version of find_thetaset (old version).
    n is length of partition, k is difference condition, d is
    raising strength (number of 1s moved).'''
    memory_limit = 5 #the memory limit, after which we have to start chunking
    raising_ops = [] 
    if n <= memory_limit:
        partitions = make_partitions(n,k+1,1)     
        for p in partitions:
            raising_ops.append(vectors(p,k,d)) 
        raising_ops = remove_duplicates(raising_ops)
        return raising_ops
    else:
        olddiff = difference_list(memory_limit-1,k+1,1) #change to 0 for nonstrict
        newdiff = difference_list(n-memory_limit,k+1,1) #again, change 0 if needed
#        print olddiff
#        print newdiff
        for new in newdiff:
            newolddiff = []
            for i in olddiff:
                for j in newdiff:
                    newolddiff.append(j+i)
 #           print newolddiff
 #           break
            partitions_temp = bare_make_partitions(newolddiff)
            for p in partitions_temp:
                v = vectors(p,k,d)
                raising_ops.append(v)
            newolddiff,partitions_temp = [],[]
#        print raising_ops
        raising_ops = remove_duplicates(raising_ops)
        return raising_ops
        
            
            
        
        


def thetaset_dictionary(n,k,d,olddict):
    '''makes a dictionary that indexes each partition we used by the
    thetaset it gives (given as a tuple, since python won't let you use
    lists as dictionary keys, and takes the dictionary of n-1,k,d as an
    argument to avoid having to compute things multiple times. No guarantees
    that this will work for different values of d.'''
    #make all partitions we need:
    newpartitions = []
    newdict = {}
    for thetaset in olddict:
 #      thetaset = convert_to_lists(thetasettuple,2)
        maxdiff_front = 0
        maxdiff_back = 0
        for raising_op in thetaset:
  #          print raising_op
#            print max(maxdiff_front,raising_op[0])
            maxdiff_front = max(maxdiff_front,raising_op[0])
            maxdiff_back = max(maxdiff_back,raising_op[-1])
        to_add = []
        for partition in olddict[thetaset]:           
            for i in range(k+1,-maxdiff_front,-1):
                to_add.append([partition[0]+i] + partition)
            for i in range(k-1,k-maxdiff_back-1,-1):
                to_add.append(partition + [partition[-1]-i])
 #           print to_add
        newpartitions += to_add
    #whew, now they're made
    #make the new dictionary:
 #   print newpartitions
    for p in newpartitions:
        t = convert_to_tuples(vectors(p,k,d),2)
        if t in newdict:
            newdict[t].append(p)
        else:
            newdict[t] = [p]
    return newdict
        
def convert_to_lists(oldT,d):
    '''takes a tuple of tuples etc. of depth d (d nestings),
    and gives it as a list of lists of lists etc.'''
    if d == 1:
        return list(oldT)
    else:
        T = list(oldT)
        for i in range(len(T)):
            T[i] = convert_to_lists(T[i],d-1)
    return T


    
def convert_to_tuples(oldL,d):
    '''takes a list of lists of lists etc. of depth d,
    and converts to tuple of tuples of tuples.'''
    L = deepcopy(oldL)
    if d == 1: #list contains no lists
        return tuple(L)
    else:
        for i in range(len(L)):
            L[i] = convert_to_tuples(L[i],d-1)
    L = tuple(L)
    return L
            

def efficient_find_thetaset(n,k,d,oldthetasuperset):
    '''takes advantage of recursive nature of thetasets, and
    take the thetaset on length n-1 as an argument'''
    partitions = efficient_make_partitions(n,k+1)
    newset = []
    for thetaset in oldthetasuperset:
        front_concatenate = []
        back_concatenate = []
        for r in thetaset:
            front_concatenate.append([0] + r)
            back_concatenate.append(r + [0])
        newset.append(back_concatenate)
        newset.append(front_concatenate)
 #   for p in partitions: #incomplete


    
def partition_checker(m,n,k,d):
    '''finds all 'ghost partitions' of length m, considering the n
    last parts, with omegaset condition difference of k and
    raising strength d.'''
    longpartitions = distinct_partitions(m,k,d)
    shortpartitions = distinct_partitions(n,k,d)
    redundant_partitions = []
    for p in longpartitions:
        if p[n-k:n] not in shortpartitions:
            redundant_partitions.append(p)
    return redundant_partitions
        
def thetaset_sequence(k,d,n):
    '''defines thetaset procedure for difference k, and tests
    size of thetasets up to length n to output a sequence'''
    for i in range(1,n+1):
        print str(len(find_thetaset(i,k,d)))
    return

def thetadict_sequence(k,d,n):
    '''will keep making theta dictionaries, printing their order,
    and adding them to a list which can be accessed at will.'''
    #make the first dictionary:
    initial_partitions = []
    for i in range(k+1):
        initial_partitions.append([i])
    dictlist = [{convert_to_tuples([[0]],2):initial_partitions}]
    for it in range(2,n):
        newsuperset = thetaset_dictionary(it,k,d,dictlist[-1])
        dictlist.append(newsuperset)
        print len(newsuperset)
    return dictlist

#def thetaset_sequencev2(k,d,n):
    

def fuckyouUma(n,k,d,partition):
    partitions = distinct_partitions(n,k,d)
    n = len(partition)
    matching_partitions = []
    for p in partitions:
        if p[-n:] == partition:
            matching_partitions.append(p)
    return matching_partitions

def fuckyouUmav2(n,k,d):
    partitions = distinct_partitions(n,k,d)
    lilpartitions = distinct_partitions(n-1,k,d)
    nonmatchers = []
    for p in partitions:
        if p[1:] not in lilpartitions:
            nonmatchers.append(p)
    return nonmatchers
    


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
