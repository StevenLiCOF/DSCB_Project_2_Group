# General Principles [(PEP20)](https://www.python.org/dev/peps/pep-0020/)
PEP20 is also called “the Zen of Python“. This set of platitudes sums up a lot of the Python philosophy, and can serve as good guideposts as you learn to be a better programmer. 

I’ve included the ones here that I think are particularly relevant, along with Python idioms and examples you can apply in your everyday Python-ing.

## Beautiful is better than ugly
If you’re writing code and something causes you to break style rules (see below) or generally wretch in disgust, that may be a sign that there is a better way to do what you’re trying to do.
Examples: 

* regular expressions hundreds of characters long (see: `re` [verbose mode](http://www.diveintopython.net/regular_expressions/verbose.html))
* bare SQL statements in Python code (see: libraries like SQLAlchemy)


## Explicit is better than implicit
### Unpack values into meaningful names
For list or tuple shaped variables, if you know for sure the length of them Python allows you to “unpack” them into variables separated by commas on the left side of the assignment operator. 

```python
today, tomorrow, today_plus_two = next_three_days(foo)

list_of_pairs = [("Mike","Sally"),("Larry","Gary")]
for index, (name_a, name_b) in enumerate(list_of_pairs):
    ...
```

### Use arguments well
Regular arguments are mandatory and have no default values.
Keyword arguments are optional and have default values.
```python

def swap_random_pairs(data, n_swaps=1):
    …

```

#### Tips
* If most of the time when you pass a value it is the exact same, consider moving it into a keyword argument for brevity.
* Don't anticipate which arguments you think you'll need-- write the function and add them as you need them

### Don't use wildcards except when absolutely necessary
**BAD**
```python
from module import *

def irresponsible(*args):
    x, y, display = args
    ...
```
The better way:
```python
from module import User, Session

def better(x, y, display=False):
    ...
```

## Readability Counts
> Programs must be written for people to read, and only incidentally for machines to execute.
--Abelson & Sussman, Structure and Interpretation of Computer Programs

### Use “in” and "with" when possible
#### Good:
```python
for thing in list:
    ...
```
```python
if "cats" in sentence.split():
    ...
```
```python
with open('file.txt') as file:
    ...
```
#### Bad:
```python
for i in range(len(list)):
    ...
```
```python
file = open('file.txt')
... # this code could raise an exception, leaving the file open
file.close()
```

### Rely on truthiness
```python
if numlist:
    ...
```

instead of

```python
if len(numlist) > 0:
    ...
```
    
False values      | True Values
------------------|------------------
`False`           | `True`
"" (empty string) | any other string
0, 0.0            | any other number
[], (), {}, set() | any other container
None              | almost any object that's not explicitly False

### One statement per line
It's not a contest to make your code as compact as possible. Let it breathe.

**BAD:**

```python
if foo == 'blah': do_something()
do_one(); do_two(); do_three()
```

Good:
```python
if foo == 'blah':
    do_something()
do_one()
do_two()
do_three()
```

## Errors should never pass silently
When things happen that are unexpected, have your code raise an
exception.
[Python standard exceptions](https://docs.python.org/2/library/exceptions.html)

### Never use bare `except:` statements
**BAD:**
```python
try:
    str(x)
except:
    print "¯\_(ツ)_/¯"
```
*Better:*
```python
try:
    str(x)
except TypeError:
    print "x could not be made a string."
		raise
```

## Flat is better than nested
### Make functions liberally.
Functions not only let you reuse shared bits of code, they can help you break complex processes into named, testable steps.

**If you find yourself copy-pasting code from one part of a file to another pretty much EVER, that code should probably be a function.**

### List comprehensions can be useful shorthand
BUT, don’t overdo it. Remember, readability counts. If in doubt, just write a loop.

```python
a = [1,2,3,4,5]

a_squared = [num*num for num in a]
# is equivalent to
a_squared = []
for num in a:
    a_squared.append(num*num)

a_evens = [num for num in a if (num % 2) == 0]
# is equivalent to
a_evens = []
for num in a:
    if (num % 2) == 0:
        a_evens.append[num]
```

# Other Useful Python Idioms
## Don't check for existence of keys- use .get()
```python
dict = {"a": 4, "b": 3}
dict.get("c",None) # 2nd argument is the default value
```

# Code-level Documentation
## Docstrings == How to use code
String literal that occurs as the first statement in a module,
function, class, or method definition. Best practice is to put these in `“””triple double quotes”””`.

* Explain the purpose of the function (even if it seems obvious)
* Describe the parameters expected, the return values, and exceptions raised.
* Explain any other context important to using the class or function

Docstrings get stored on the `.__doc__` attribute of that object. This
means they’re easy to access for people using your function
interactively and also for auto-documentation systems.

```python
def complex(real=0.0, imag=0.0):
    """Form a complex number.

    Keyword arguments:
    real — the real part (default 0.0)
    imag — the imaginary part (default 0.0)
    """
    if imag == 0.0 and real == 0.0:
        return complex_zero
    …
```

## Comments == Why (rationale) & how code works
Comments explain why, and are for the maintainers of code. They’re also good for leaving notes to return to later.

```python
# Entries need to be nonzero to be added to the DB.
for entry in list:
    if entry:
        # TODO: add database code here
        raise NotImplementedError
```

Don’t use comments as a crutch— code that is hard to read but
extensively commented is worse than code that is self evident but not documented.

**Example of over-commented code:**
```python
# loop over the entries in the list
for entry in list:
    # check if entry is zero
    if entry:
        ...
```

# Style Standards [(PEP8)](https://www.python.org/dev/peps/pep-0008/)

## Whitespace
* 4 space indents. 1 line between functions. 2 lines between classes.
* 1 space after “,”s just about everywhere, and after “:”s in dicts.
* No spaces before “,”s or “:”s.
* Spaces around assignments & comparisons (except for arguments).
* No spaces just inside parentheses or just before argument lists.
* No spaces just inside docstrings.

## Naming things
Here are the PEP8 conventions for naming things in Python:
* `joined_lower` for functions, methods, attributes
* `joined_lower` or `ALL_CAPS` for constants
* `StudlyCaps` for classes
* Attributes: `interface`, `_internal`
  * No such thing as private attributes in Python. Throw an _ before
    attributes not intended to be accessed by outside modules.

## Keep lines shorter than 80 chars
Turns out this is actually a holdover habit from the punchcard-era days. But it’s a good guideline, as it makes code readable in terminals and prevents you from making wicked long lines that are hard to read.

The best way to break a long string or tuple over lines is with parens:
```python
my_very_big_string = (
    “For a long time I used to go to bed early. Sometimes, “
    “when I had put out my candle, my eyes would close so “
    “quickly that I had not even time to say ’I’m going to”
    “sleep.’”
)

from some.deep.module.inside.a.module import (
    a_nice_function, another_nice_function,
    yet_another_nice_function)

output = (first + second + third
          + fourth + fifth + sixth)
```

# Laying out a module
This is a good way to organize a module:
```python
“””module docstring”””

# imports
# constants
# exception classes
# interface functions
# classes
# internal functions & classes

def main(…):
    …

if __name__ == ‘__main__’:
    status = main()
    sys.exit(status)
```
