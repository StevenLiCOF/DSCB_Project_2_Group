You are writing software for a fancy new robot cash register iPad app. It's totally
gonna disrupt the cash register industry and you're gonna get filthy rich!

You need to write a function called `calculateChange`. It takes a total amount
of money due and the amount of cash given by the customer, and returns a
dictionary with how many of each coin and bill the robot needs to return to give
correct change. The robot has the following coins and bills:

```python
denominations = [(.01, "penny"), 
                 (.05, "nickel"),                  
                 (.10, "dime"),                  
                 (.25, "quarter"),                  
                 (1, "dollar bill"),                  
                 (5, "five dollar bill"),                  
                 (10, "ten dollar bill"),                  
                 (20, "twenty dollar bill")]
```
 So your function should work something like this:

```python
>>> calculateChange(14.26, 20.00)

{"five dollar bill": 1,
 "quarter": 2,
 "dime":2,
 "penny":4
}
```

The best implementations will return the fewest number of bills and coins necessary.
But we're still in beta, so you could always solve the problem by spitting hundreds
of pennies out.

Bonus: write your function to take any arbitrary denomination list, so it's easy to launch this thing in Sweden in a few months.
