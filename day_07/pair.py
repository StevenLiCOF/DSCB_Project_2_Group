denominations = [(.01, "penny"),
                 (.05, "nickel"),
                 (.10, "dime"),
                 (.25, "quarter"),
                 (1, "dollar bill"),
                 (5, "five dollar bill"),
                 (10, "ten dollar bill"),
                 (20, "twenty dollar bill")]

denominations=dict(denominations)

def calculateChange(price, given):
    price=float(price)
    given=float(given)
    if given<price:
        return "Not enough money"
    changemoney={}
    changeamount=given-price
    for denom in sorted(denominations.keys(),reverse=True):
        if int(changeamount/denom)>0:
            changemoney[denominations[denom]]=int(changeamount/denom)
        changeamount=round(changeamount % denom, 2)
        #changemoney=sorted(changemoney,key=denominations)
    return changemoney

print calculateChange(20, 20.00)
print calculateChange(14.28, 20.00)
print calculateChange(21, 20.00)
print calculateChange(0, 20.00)
