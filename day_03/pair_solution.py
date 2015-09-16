def balanced(inputstring):
    negcheck=True
    counter=0
    for char in inputstring:
        if char=='(':
            counter+=1
        elif char==')':
            counter-=1
        if counter<0:
            negcheck=False
    return negcheck and (counter==0)

print balanced('(()()()())')
print balanced('(((())))')
print balanced('(()((())()))')
print balanced('((((((())')
print balanced('()))')
print balanced('(()()))(()')

print balanced('((asd)asg()45)saa)df(ah()')
print balanced('a((e)ger(j)t()s(eg))er')
