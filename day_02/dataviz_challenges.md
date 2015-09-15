1. Fit three different regression models to your data (different feature sets). Plot all of them together on top of the real data. Add a legend so we can see which model is which.

2. For a model that predicts either gross or opening weekend with the budget as the single feature, plot all the movies as points, plot the fitted line of the model, plot your model's best predictions for each movie in the dataset.

3. Continue from previous challenge. Calculate the mean standard error of your model. To each of your prediction points, add an errorbar the size of the mean square error.

4. Try drawing the 95% confidence intervals, using `wls_prediction_std` from statsmodels. This page has an example to get you started.

> Bonus tip after finishing: Check out [some of seaborne's pre-configured plotting functions](http://stanford.edu/~mwaskom/software/seaborn/tutorial/regression.html) to quickly pull off some nice looking graphs. Also check out the [visual aesthetics tutorial](http://stanford.edu/~mwaskom/software/seaborn/tutorial/aesthetics.html#aesthetics-tutorial).
