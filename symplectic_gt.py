#Roger Van Peski, 2/16/14

def copy_my_list(l): #this is a deep copy, since for some reason the regular deep copy wasn't working...
    newlist = []
    for i in range(len(l)):
        newlist.append(l[i])
    return newlist

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
            l.append(copy_my_list(l[i]))
    return

def nest_partitions(toprow):
    '''makes all possible strict partitions nesting in toprow'''
    rows = [[]]
    newrows = []
    for i in range(len(toprow)-1):
        old_length = len(rows)
        d = toprow[i]-toprow[i+1]+1
        make_copies(rows,d-1)
        choices = range(toprow[i+1],toprow[i]+1)
        for a in range(d):
            for b in range(old_length*a,old_length*(a+1)):
                rows[b].append(choices[a])
    for row in rows:
        if is_strict(row):
            newrows.append(row)            
    return newrows

def make_rows(toprow,barred):
    '''nests a row to toprow, treating it as either barred or nonbarred'''
    if barred:
        return nest_partitions(toprow)
    else:
        return nest_partitions(toprow + [0])

def all_patterns(toprow)
    
