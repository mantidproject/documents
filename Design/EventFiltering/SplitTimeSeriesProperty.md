# Splitting TimeSeriesProperty

Assume that a TimeSeriesProperty `P` has entries (t\_0, v\_0), (t\_1, v\_1), ..., (t\_n, v\_n).
It is split by a set of (N-1) splitters, (T\_0, T\_1, w\_0), (T\_1, T\_2, w\_1), ... and (T\_(N-1), T\_N, w\_(N-1)).

There are two types of sample logs that are recorded in TimeSeriesProperty.
* TYPE I: The log value within an arbitrary entry is constant. For example, motor position and temperature can be treated as this type of log;
* TYPE II: The log value is a value measured at the beginning of a TimeSeriesProperty entry.  And between start and stop time of the entry, the log value is not measured and cannot be treated as a constant. For example, proton charge is of this type. 

One of our assumption is that any TimeSeriesProperty entry is better to be kept complete during splitting.

## Split TYPE I TimeSeriesProperty Use Case 1

In this case, there are more than 1 entry of TimeSeriesPrperty `P` between the start and stop time of a splitter i, i..e,  T\_(i-1), and T\_i, respectively. 
And The split entries will be written to a new TimeSeriesProperty indexed as w\_(i-1)).
Then in `P`, it can be found an entry j and and entry k, where j < k, such that
t\_(j-1) <= T\_(i-1) < t\_j, and t\_(k-1) < T\_i <= t\_k.
The split-out TimeSeriresProperty by this splitter shall contain the entries as (t\_(j-1), t\_j, ..., t\_k),
which will be written to output TimeSeriesProperty indexed as w\_(i-1).

![alt text](tsp_split_1.png)


## Split TYPE I TimeSeriesProperty Use Case 2

In this case, there are more than 1 consecutive splitters within an entry j of `P`.
Such that t\_j < T\_i < T\_(i+s+1) < t\_(j+1), where s is the number of splitters within entry j.
Then no splitting is required to `P`'s j entry in this situation.

![alt text](tsp_split_2.png)


## Special case: Proton charge (TYPE II)

The value of a proton chage entry is measured at the begining of the entry. 
Its value between 2 adjacent measurements cannot be treated as a constant value but 
rather varies by specific instrument type.

For a **slow** splitter, whose time span is much larger than the time of a proton charge entry,
it is not necessary to consider split any proton charge log entry.

Assume that the total proton charge is `C`.
If this log is split to `P\_ 1`, `P\_2`, ..., `P\_m`, and the total proton charges for 
each split log are `C\_ 1`, `C\_2`, ..., `C\_m`, respectively.
Then the sum of  `C\_ 1`, `C\_2`, ..., `C\_m` can be slightly larger than `C`.

For a **fast** splitter, whose time span is comparable to a proton charge entry,
then it requires detailed information about how to split it in order to normalize
the data correctly. 

We plan to leave it for future till there is a solid use case.
