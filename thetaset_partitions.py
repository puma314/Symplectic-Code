#Roger Van Peski 3/23/14
#To examine the distribution of thetasets on partitions of integers
from numpy import *
from pylab import *
from copy import *

def partition(number): #taken from stackexchange
    answer = set()
    answer.add((number, ))
    for x in range(1, number):
        for y in partition(number - x):
            answer.add(tuple(sorted((x, ) + y)))
    return answer

def partitions(number):
    partitions = list(partition(number))
    newpartitions = []
    for p in partitions:
        newpartitions.append(list(p)[::-1]+[0])
    return newpartitions

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
                    newlist = deepcopy(partition1)
                    newlist[i] -= d; newlist[i+1] += d
                    new_reachables.append(newlist)
            for reachable in new_reachables:
                if reachable not in S:
                    S.append(reachable)
        if S == S_old:
             loop = False
    return S

def remove_duplicates(i):
  output = []
  for x in i:
    if x not in output:
      output.append(x)
  return output

def vectors(partition,k,d):
    '''returns the vector versions of all possible
    raising operators in Theta(partition)'''
    S = reachable_partitions(partition,k,d)
    newset = []
    for s in S:
        l = list(array(s) - array(partition))
        newset.append(l)
    return newset

def all_partition_thetasets(n,k,d):
    '''returns all possible thetasets on partitions of n,
    with difference condition k, d 1s moved each raising op.'''
    partitionlist = partitions(n)
    thetasets = []
    for p in partitionlist:
        thetasets.append(vectors(p,k,d))
    thetasets = remove_duplicates(thetasets)
    #print 'Number of thetasets on partitions of ' + str(n) + ': ' + str(len(thetasets))
    return thetasets




def partition_sequence(n1,n2,k,d):
    '''takes sequence of number of possible thetasets
    of all possible partitions of k with n1 \leq k \leq n.'''
    partitions = zeros(n2-n1)
    for i in range(n1,n2):
        p = len(all_partition_thetasets(i,k,d))
        partitions[i-n1] = p
        print p
    plot(arange(n1,n2),partitions,'ro') 
    return partitions

def partition_differences(n1,n2,k,d):
    '''takes the difference between the number of thetasets
    on partitions of n and the number of thetasets on
    partitions of n-1.'''
    p1 = len(all_partition_thetasets(n1-1,k,d))
    differences = zeros(n2-n1)
    for i in range(n1,n2):
        p2 = len(all_partition_thetasets(i,k,d))
        diffs = p2-p1
        print str(diffs)
        differences[i-n1] = diffs
        p1=p2
    plot(arange(n1,n2),differences,'ro')
    return differences
    

def conversion_ratio(n1,n2,k,d):
    '''the fraction of partitions which produce unique thetasets'''
    fractions = zeros(n2-n1)
    for i in range(n1,n2):
        fraction = float(len(all_partition_thetasets(i,k,d)))/len(partitions(i))
        fractions[i-n1] = fraction
        print fraction
    plot(arange(n1,n2),fractions,'ro')
    return fractions
    
#if you want to try log scaling the output of any of these, just do plot(arange(len(output)),log(output),'ro')
