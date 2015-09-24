Write a function `is_valid_anagram(string1, string2)`, which takes two
strings and checks if they are anagrams of each other. It should
return `True` if they are, and `False` if not. For example, if `string1`
and `string2` are `"meter"` and `"metre"`, it should return `True`. For
`"meter"` and `"mother"`, it should return `False`. It should only
accept full matches, not partial ones, so `"meter"` and `"kilometer"`
is also a `False`. It should ignore capitalization, spaces, punctuation,
etc. So, `"___...M e t e R...___"` and `"metre"` is a `True`.

Here are some examples and what they should return so you can test
your code:

```python
print is_valid_anagram("The eyes", "they see")                     # True 
print is_valid_anagram("Potato", "Elvis lives.")                   # False
print is_valid_anagram("color", "colour")                          # False
print is_valid_anagram("A decimal point", "I'm a dot in place")    # True 
print is_valid_anagram("The Morse Code", "Here come dots...")      # True 
print is_valid_anagram("Election Results", "Lies. Let's recount.") # True 
print is_valid_anagram("Astronomer", "Moon Starer")                # True 
print is_valid_anagram("Snooze alarms", "Alas, no more Z's")       # True 
print is_valid_anagram("Brian", "Brain")                           # True 
print is_valid_anagram("Irmak", "Brad Pitt")                       # False
```

------

Bonus if you have time:

Implement the _guessing game_. Computer picks a number between 1
and 100. Asks you to guess it. You enter a guess, it will tell you if
your guess is too high or too low. If you guess correctly within 6
tries, you win. If you exhaust your 6 guesses without getting the
computer's pick, you lose.

The output may look something like this (you enter the guesses with
the keyboard during the game):

```
guess 1: 60
You guessed too high.
guess 2: 12
You guessed too low.
guess 3: 35
You guessed too high.
guess 4: 20
You guessed too high.
guess 5: 15
You guessed too low.
guess 6: 18
You guessed too high.
YOU FAILED. YOU IDIOT. YOUR 6 GUESSES ARE UP.
It was 16. Haha. So simple. 16. You were close, too.
```

-----

Bonus if you still have more time:

Implement the _guessing game_ again, but this time you are picking the
number and the computer is trying to guess it in 6 tries. It will tell
you its guess and you will input if it's too high or low. No
cheating! Also try to implement a strategy that does not have a
blatant weakness (meaning you shouldn't be able to beat it every time
by picking a specific number).

