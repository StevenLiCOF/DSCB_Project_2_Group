autoscale: true
build-lists: true

# [fit] Why Python?

^ I’m not a Python salesman. It’s not universally better than SAS or anything else.
^ Python is first and foremost a programming language. Not a data language, not really specialized for anything
***
## Some of my favorite parts
- Clean, (relatively) straightforward syntax
- “Batteries included”
- Big community
- Versatile

***

> Programs must be written for people to read, and only incidentally for machines to execute.
—Abelson & Sussman, Structure and Interpretation of Computer Programs

^ the obvious beneficiary- your teammates
^ the less obvious one is you- 6 weeks from now, when you completely forget about this code

***
# The reader shouldn’t have to remember much
- Split code into functions that perform single, easily understood tasks
	- Bonus: This makes them easier to test too

***
# Names should be consistent and meaningful
## Examples:

`current_account_balance`
`comment_box_text`
`account.withdraw(20, ‘USD’)`

*** 
# Keep it DRY
## (don’t repeat yourself)

If you’re copy-pasting code,

***

# [fit] STOP

^ break the code out into a new function and call it

***

# Document, but document the right things

Design and intent, not implementation

Bad: 

```python
# loop over movies in the list
for movie in list:
    # add genre to genre counts
    genres.update(movie.genre)
```

***
# Document, but document the right things

Better

```python
# Takes a list of Movie objects and returns a Counter of genre objects
def count_genres():
    …
```

***
# Docstrings even nicer

Docstrings are triple-quoted strings placed after a `def` or `class` that describe the functionality of that thing.

Can be used to automatically generate documentation

```python
def count_genres():
    ˮˮˮTakes: a list of Movie objects 
    returns: a Counter of genre objects
    ˮˮˮ
    …
```

***

##I Revisit *the zen* frequently.

# `import this`

***

# Beautiful is better than ugly
Looks gross? There may be a better way.

***

# Explicit is better than implicit
### Unpack values into meaningful names

```python
today, tomorrow, today_plus_two = next_three_days(foo)

list_of_pairs = [("Mike","Sally"),("Larry","Gary")]
for index, (name_a, name_b) in enumerate(list_of_pairs):
    ...
```

***
# Explicit is better than implicit
### Use arguments well
Regular arguments are mandatory and have no default values.
Keyword arguments are optional and have default values.

```python

def swap_random_pairs(data, n_swaps=1):
    …

```
***
# Explicit is better than implicit
### Use arguments well
* If most of the time when you pass a value it is the exact same, consider moving it into a keyword argument for brevity.
* Don't anticipate which arguments you think you'll need-- write the function and add them as you need them

***
# Readability Counts
## Use “in” and "with" when possible
### Good:
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

***

### Bad:
```python
for i in range(len(list)):
    ...
```
```python
file = open('file.txt')
... # this code could raise an exception, leaving the file open
file.close()
```

***

## Rely on truthiness
```python
if numlist:
    ...
```

instead of

```python
if len(numlist) > 0:
    ...
```

***
### One statement per line
It's not a contest to make your code as compact as possible. Let it breathe.

**BAD:**

```python
if foo == 'blah': do_something()
do_one(); do_two(); do_three()
```

***

**Good:**
```python
if foo == 'blah':
    do_something()
do_one()
do_two()
do_three()
```
***

# Errors should never pass silently
When things happen that are unexpected, have your code raise an exception.

```python
if len(class_list) % 2 != 0:
    raise ValueError(’List should have an even number of elements’)
```

***

## Never use bare `except:` statements
**BAD:**

```python
try:
    str(x)
except:
    print "¯\_(ツ)_/¯"
```
**Better:**

```python
try:
    str(x)
except TypeError:
    print "x could not be made a string."
    raise
```

***
# Flat is better than nested
## Make functions liberally
