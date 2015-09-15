1. Add functionality to loaddata.py that loads the data from files in the `data\metacritic` folder similarly to how the code we wrote for boxofficemojo works. Try to reuse as much code from the morning as you can, without copy-pasting it!

2. BoxofficeMojo data has a couple fields `release_date_limited` and `release_date_wide` that are strings in a "YYYY-MM-DD" format. Python has a library called `datetime` for doing useful things with dates. Write a function using the `datetime` library to convert these strings into `datetime.date` objects.

3. Write a function that loads both sources and merges them together, returning as many movies as possible where data is available from both sources.
