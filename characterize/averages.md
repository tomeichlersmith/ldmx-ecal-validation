# Different Kinds of Averages

These notes are just my own thoughts. 
There are many more helpful and more detailed resources available.
Honestly, the [Wikipedia page on Average](https://en.wikipedia.org/wiki/Average)
is a great place to start.

### mean
The "arithmetic mean" (or "mean" for short, there are different kinds of means as well),
is the most common average. Simply add up all the values of the samples and divide by
the number of samples.

**Code**: [`np.mean`](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)

### median
The middle number of the group of samples when ranked in order. If there are an even
number of samples, then take the arithmetic mean of the two samples in the middle.

**Code**: [`np.median`](https://numpy.org/doc/stable/reference/generated/numpy.median.html)

### weighted mean
Sometimes, the different samples should be weighted differently. In the arithmetic mean,
each sample carries the same weight (I think of it as importance). We can slightly augment
the arithmetic mean to consider weights by multipling each sample by its weight, adding these
up, and then dividing by the sum of weights. This is a nice definition since it simplifies
down to the regular arithmetic mean if all the weights are one.

Confusingly, NumPy has decided to implemented the weighted mean in their `average` function.
This is just due to a difference in vocabulary.

**Code**: [`np.average`](https://numpy.org/doc/stable/reference/generated/numpy.average.html)

### iterative mean
To repeat what I said at our meeting, in a lot of the distributions we look at, there 
is a "core" distribution that is Gaussian, but the tails are distorted by other effects.
Sometimes, we only care about the core distribution and we want to intentionally cut away
the distorted tails so that we can study the "bulk" of the distribution. This is where
an iterative approach is helpful. We continue to take means and cut away outliers until
there are no outliers left. The main question then becomes: how do we define an outlier?
A simple definition that works well in our case since we usually have many samples is
to have any sample that is further from the mean by X standard deviations be considered
an outlier.

NumPy does not have a function for this type of mean to my knowledge, so we will construct
our own.

**Code**:
```python
import numpy as np

# first I write my own mean calculation that includes the possibility of weights
#   and returns both the mean and standard deviation
def weightedmean(values, weights = None) :
    """calculate the weighted mean and standard deviation of the input values
    
    If no weights are provided, then we assume they are all one.

    This is definitely slower than the pure-C NumPy implementation when
    the weights are all one, but we want to include the possibility of the 
    weights not being one _and_ the ability to calculate weighted standard
    deviations.
    """

    if weights is None :
        weights = np.full(len(values),1.)

    mean = (weights*values).sum()/(weights.sum())
    stdd = np.sqrt((weights*(values-mean)**2).sum()/(weights.sum()))
    return mean, stdd

# now I can write the iterative mean
def itermean(values, weights = None, *, sigma_cut = 3.0) :
    """calculate an iterative mean and standard deviation

    If no weights are provided, then we assume they are all one.
    The sigma_cut parameter is what defines what an outlier is.
    If a sample is further from the mean than the sigma_cut times
    the standard deviation, it is removed.
    """

    # calculate weights once for ease
    if weights is None :
        weights = np.full(len(values), 1.)

    mean, stdd = weightedmean(values, weights)
    num_included = len(weights)+1 # just to get loop started
    selection = (weights > 0) # first selection is all non-zero weighted samples
    while np.count_nonzero(selection) < num_included :
        # update number included for this mean
        num_included = np.count_nonzero(selection)
        # calculate mean and std dev
        mean, stdd = weightedmean(values[selection], weights[selection])
        # determine new selection
        selection = (values > (mean - sigma_cut*stdd)) & (values < (mean + sigma_cut*stdd)) & (weights > 0)

    # left loop, meaning we settled into a state where nothing it outside sigma_cut standard deviations
    #   from our mean
    return mean, stdd
```

