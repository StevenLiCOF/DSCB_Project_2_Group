1. Draw a histogram of the residuals for one of the regression models. What do their distribution look like? Does it look normally distributed?

2. Build a Domestic Gross model using all the features. Include every available feature. How does your model do? Is it safe to include all these features?

3. Create a couple of features yourself. Add them as columns in your dataframe. Calculate them from other features. Examples: a) Length of title, b) if it is after 2000 or not (1 if it is, 0 it isn't), number of thaters opened to (opening take/opening per theater), etc. You make others. Put them (among with budget and other features of your choice) in model. See if they look significant. One by one, remove insignificant features and check the residuals. Any change? What is left? (Try different combinations to find a better performing model. Which metric will you use for 'better performance'?)

4. Fitting and checking predictions on the exact same data set can be misleading. Divide your data into two sets: a training and a test set (roughly 75% training, 25% test is a fine split). Fit a model on the training set, check the predictions (by plotting versus actual values) in the test set. 

5. Build a model for predicting gross with multiple features, including budget. Plot a scatterplot with x=budget, y=gross, both for actual values and for predicted values. Predicted values will no longer neatly fall on a line. Why? What's happening?

