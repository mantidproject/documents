# Splitting TimeSeriesProperty

TimeSeriesProperty `P` has entries (t0, v0), (t1, v1), ..., (tn, vn).
It is split by a set of N-1 splitters, such as (T\_0, T\_1, w\_0), (T\_1, T\_2, w\_1), ... and (T\_(N-1), T\_N, w\_(N-1)).

## Split TimeSeriesProperty use case 1

In this case, there are more than 1 entry of TimeSeriesPrperty `P` between the start and stop time of a splitter i, i..e,  T\_(i-1), and T\_i, respectively. 
The split entries will be written to a new TimeSeriesProperty indexed as w\_(i-1)).
Hence there will have entries of `P` such that t\_(j-1) <= T\_(i-1) < t\_j, and t\_(k-1) < T\_i <= t\_k, where j < k.
The split-out TimeSeriresProperty by this splitter shall have the entries as (t\_(i-1), t\_i, ..., t\_k) and
be written to output TimeSeriesProperty indexed as w\_(i-1).

![alt text](tsp_split_1.png)


## Split TimeSeriesProperty use case 2

In this case, some splitters i, i+1, i+2, .., i+b, are used to split `P`.
For these splitters, there is an entry j in `P` such that t\_j < T\_i < T\_(i+b+1) < t\_(j+1).
Then no splitting is required for `P` under this situation.

![alt text](tsp_split_2.png)


## Special case: Proton charge

The sum of split proton charge logs shall be same as the original proton charge. 
The algorithms for use case 1 and 2 are not fit.
