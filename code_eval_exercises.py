# Compare Points

def compare_points(O,P,Q,R):
    '''Report N, NE, E, SE, S, SW, W, NW, or here,
    depending on (Q,R)'s position relative to (O,P)'''
    if Q==O and R==P:
        print 'here'
    elif Q==O and R>P:
        print 'N'
    elif Q==O and R<P:
        print 'S'
    elif Q<O and R==P:
        print 'W'
    elif Q>O and R==P:
        print 'E'
    elif Q<O and R<P:
        print 'SW'
    elif Q<O and R>P:
        print 'NW'
    elif Q>O and R<P:
        print 'SE'
    elif Q>O and R>P:
        print 'NE'

def compare_points(O,P,Q,R):
    ''' My attempt at more compact script using a library'''
    import numpy as np
    [diffdir=(np.sign(Q-O),np.sign(R-P))]
    dirmap={(-1,-1): 'SW',
        (-1,0): 'W',
        (-1,1): 'NW',
        (0,-1): 'S',
        (0,0): 'here',
        (0,1): 'N',
        (1,-1): 'SE',
        (1,0): 'E',
        (1,1): 'NE'}
    print dirmap[diffdir]

def read_more(lines):
    '''prints inputs text with trimmed lines'''
    for line in lines:
        if len(line)<=55:
            print line
        else:
            line=line[:40]
            print line[:line.rfind(' ')]+'... <Read More>'

def sum_digitssq(n):
    s = 0
    while n:
        s += n**2 % 10
        n /= 10
    return s
def happy(x):
    hist=[]
    while x not in hist and x>1:
        hist.append(x)
        x=sum_digitssq(x)
    if x in hist:
        return 0
    if x==1:
        return 1
