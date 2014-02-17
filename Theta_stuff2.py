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

def reachable_partitions2(partition):
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
                    

def reachable_partitions1(partition):
    '''gives every partition reachable by something in Theta(partition)'''
    S = [partition]
    n = len(partition)
    loop = True
    while loop:
        S_old = S
        for partition1 in S:
            new_reachables = []
            for i in range(n-1):
                if partition1[i] == partition1[i+1] + 1:
                    newlist = copy_my_list(partition1)
                    newlist[i] -= 1; newlist[i+1] += 1
                    new_reachables.append(newlist)
            for reachable in new_reachables:
                if reachable not in S:
                    S.append(reachable)
        if S == S_old:
             loop = False
    return S


def reachable_partitions0(partition): #like reachable_partitions2 but the condition is that they be 0 apart
    '''gives every partition reachable by something in Theta(partition)'''
    S = [partition]
    n = len(partition)
    loop = True
    while loop:
        S_old = S
        for partition1 in S:
            new_reachables = []
            for i in range(n-1):
                if partition1[i] == partition1[i+1]:
                    newlist = copy_my_list(partition1)
                    newlist[i] -= 1; newlist[i+1] += 1
                    new_reachables.append(newlist)
            for reachable in new_reachables:
                if reachable not in S:
                    S.append(reachable)
        if S == S_old:
             loop = False
    return S


    
                    
def vectors2(partition):
    '''returns the vector versions of all possible
    raising operators in Theta(partition)'''
    S = reachable_partitions2(partition)
    newset = []
    for s in S:
        newset.append(list(array(s) - array(partition)))
    return newset

def vectors1(partition):
    '''returns the vector versions of all possible
    raising operators in Theta(partition)'''
    S = reachable_partitions1(partition)
    newset = []
    for s in S:
        newset.append(list(array(s) - array(partition)))
    return newset

def vectors0(partition):
    '''returns the vector versions of all possible
    raising operators in Theta(partition)'''
    S = reachable_partitions0(partition)
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
                
def nonstrict_partition_filler(partitions,n): #this is needed for the next one
    '''partitions is a list of partitions (lists) of the same length,
    n is the length we want the partition to get to'''
    p = partitions[0]
    if len(p) == n:
        return partitions
    elif len(p) < n:
        newpartitions = []
        for partition in partitions:
            part_list = make_copies2([partition],partition[-1]) 
            for a in range(len(part_list)+1):
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


def nonstrict_difference_list(length):
    '''gives data structure to loop over all possibilities 0, +1, +2,'''
    lists = [[]]
    for i in range(length):
        triple_list(lists)
        for it in range(len(lists)/3):
            lists[it].append(1) 
            lists[it+len(lists)/3].append(2)
            lists[it+2*len(lists)/3].append(0) 
    return lists


def find_thetaset2(n):
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
        raising_ops.append(vectors2(p))
    raising_ops = remove_duplicates(raising_ops)
    return raising_ops


def find_thetaset0(n):
    '''a more efficient version of find_thetaset'''
    differences = nonstrict_difference_list(n-1)
    partitions = []
    raising_ops = []
    for d in differences:
        partition = [0]
        for difference in d:
            partition.append(partition[-1]+difference)
        partition = partition[::-1]
        partitions.append(partition)
    for p in partitions:
        raising_ops.append(vectors0(p))
    raising_ops = remove_duplicates(raising_ops)
    return raising_ops


def find_thetaset(n,k):
    differences = nonstrict_difference_list(n-1,k)
    partitions = []
    raising_ops = []
    for d in differences:
        partition = [0]
        for difference in d:
            partition.append(partition[-1]+difference)
        partition = partition[::-1]
        partitions.append(partition)
    for p in partitions:
        raising_ops.append(vectors(p,k))
    raising_ops = remove_duplicates(raising_ops)
    return raising_ops
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

def reachable_partitions2(partition):
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
                    

def reachable_partitions1(partition):
    '''gives every partition reachable by something in Theta(partition)'''
    S = [partition]
    n = len(partition)
    loop = True
    while loop:
        S_old = S
        for partition1 in S:
            new_reachables = []
            for i in range(n-1):
                if partition1[i] == partition1[i+1] + 1:
                    newlist = copy_my_list(partition1)
                    newlist[i] -= 1; newlist[i+1] += 1
                    new_reachables.append(newlist)
            for reachable in new_reachables:
                if reachable not in S:
                    S.append(reachable)
        if S == S_old:
             loop = False
    return S


def reachable_partitions0(partition): #like reachable_partitions2 but the condition is that they be 0 apart
    '''gives every partition reachable by something in Theta(partition)'''
    S = [partition]
    n = len(partition)
    loop = True
    while loop:
        S_old = S
        for partition1 in S:
            new_reachables = []
            for i in range(n-1):
                if partition1[i] == partition1[i+1]:
                    newlist = copy_my_list(partition1)
                    newlist[i] -= 1; newlist[i+1] += 1
                    new_reachables.append(newlist)
            for reachable in new_reachables:
                if reachable not in S:
                    S.append(reachable)
        if S == S_old:
             loop = False
    return S


def reachable_partitions3(partition): #like reachable_partitions2 but the condition is that they be 0 apart
    '''gives every partition reachable by something in Theta(partition)'''
    S = [partition]
    n = len(partition)
    loop = True
    while loop:
        S_old = S
        for partition1 in S:
            new_reachables = []
            for i in range(n-1):
                if partition1[i] == partition1[i+1]+3:
                    newlist = copy_my_list(partition1)
                    newlist[i] -= 1; newlist[i+1] += 1
                    new_reachables.append(newlist)
            for reachable in new_reachables:
                if reachable not in S:
                    S.append(reachable)
        if S == S_old:
             loop = False
    return S
    
                    
def vectors2(partition):
    '''returns the vector versions of all possible
    raising operators in Theta(partition)'''
    S = reachable_partitions2(partition)
    newset = []
    for s in S:
        newset.append(list(array(s) - array(partition)))
    return newset

def vectors1(partition):
    '''returns the vector versions of all possible
    raising operators in Theta(partition)'''
    S = reachable_partitions1(partition)
    newset = []
    for s in S:
        newset.append(list(array(s) - array(partition)))
    return newset

def vectors0(partition):
    '''returns the vector versions of all possible
    raising operators in Theta(partition)'''
    S = reachable_partitions0(partition)
    newset = []
    for s in S:
        newset.append(list(array(s) - array(partition)))
    return newset

def vectors3(partition):
    '''returns the vector versions of all possible
    raising operators in Theta(partition)'''
    S = reachable_partitions3(partition)
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
                
def nonstrict_partition_filler(partitions,n): #this is needed for the next one
    '''partitions is a list of partitions (lists) of the same length,
    n is the length we want the partition to get to'''
    p = partitions[0]
    if len(p) == n:
        return partitions
    elif len(p) < n:
        newpartitions = []
        for partition in partitions:
            part_list = make_copies2([partition],partition[-1]) 
            for a in range(len(part_list)+1):
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


def difference_list(length,k):
    '''gives data structure to loop over all possibilities +1, +2, +3 ... +k'''
    lists = [[]]
    for i in range(length):
        copy_my_list(lists,k)
        for it in range(len(lists)/k):
            for c in range(k):
                lists[it+c*len(lists)/k].append(c+1) 
    return lists




def find_thetaset0(n):
    '''a more efficient version of find_thetaset'''
    differences = nonstrict_difference_list(n-1)
    partitions = []
    raising_ops = []
    for d in differences:
        partition = [0]
        for difference in d:
            partition.append(partition[-1]+difference)
        partition = partition[::-1]
        partitions.append(partition)
    for p in partitions:
        raising_ops.append(vectors0(p))
    raising_ops = remove_duplicates(raising_ops)
    return raising_ops


def find_thetaset1(n):
    '''a more efficient version of find_thetaset'''
    differences = nonstrict_difference_list(n-1)
    partitions = []
    raising_ops = []
    for d in differences:
        partition = [0]
        for difference in d:
            partition.append(partition[-1]+difference)
        partition = partition[::-1]
        partitions.append(partition)
    for p in partitions:
        raising_ops.append(vectors1(p))
    raising_ops = remove_duplicates(raising_ops)
    return raising_ops

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

def find_thetaset2(n):
    '''a more efficient version of find_thetaset (old version)'''
    partitions = make_partitions(n,3)
    raising_ops = []
    for p in partitions:
        raising_ops.append(vectors2(p))
    raising_ops = remove_duplicates(raising_ops)
    return raising_ops


def find_thetaset3(n):
    partitions = make_partitions(n,4)
    raising_ops = []
    for p in partitions:
        raising_ops.append(vectors3(p))
    raising_ops = remove_duplicates(raising_ops)
    return raising_ops


def standard_thetaset(n):
    '''take the thetaset using our normal notation in terms
    of elementary raising operators, doing them in order of
    last to first (just like regular notation); if the order
    doesn't matter, then it'll just choose the ones closer
    to the front of the string first.'''
    

def distinct_permutations(n):
    '''for each element of the theta superset on length n
    gives a representative partition for each possible
    theta set'''
    all_partitions = make_partitions(n)
    good_partitions = []
    raising_ops = []
    for p in all_partitions:
        v = vectors2(p)
        if v not in raising_ops:
            good_partitions.append(p)
            raising_ops.append(v)
    return good_partitions
        

def partition_checker(n,k):
    longpartitions = distinct_permutations(n)
    shortpartitions = distinct_permutations(k)
    redundant_partitions = []
    for p in longpartitions:
        if p[n-k:n] not in shortpartitions:
            redundant_partitions.append(p)
    return redundant_partitions
        


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
