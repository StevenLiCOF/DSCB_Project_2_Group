In project2/modeling.py is some helpful (but not very good) code. 

These challenges involve making improvements to this code. In addition to these specific improvements, please feel free to rename variables and restructure things along the way.

* Take a look at the code and figure out what it does.
Then move it into a function called `k_value_test` that can take any arbitrary set of feature data X and target data Y.
* This code features a lot of copy-pasted functionality. To eliminate duplicated code, write a general function that takes any metric name and call it from your `k_value_test` function.
* Improve your `k_value_test` function by allowing the user to pass the range of K values they want to test as a keyword argument.
* Add another keyword argument that takes a list of metric names to be displayed in the report/plot.
* Make sure your functions have docstrings describing  their arguments and functionality.
* The function as written calls `cross_val_score` 4 separate times to get the 4 different error measures; this re-trains and runs the model 4 times. You can speed up your function by only cross-validating once; look into `cross_val_predict`, the KFold iterator, and the `sklearn.metrics` functions.
* Other algorithms have values like K we might want to experiment with. See if you can generalize the function even further, to work with any given algorithm and parameter.

Once you're happy with your function, try combining all the hospital datasets and running it on the combined data.
