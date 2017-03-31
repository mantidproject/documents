# Exceptions and Error Logging in Algorithms

## Overview

- Many algorithm log and error and then throw and exception with the same or a similar description ([example](https://github.com/mantidproject/mantid/blob/master/Framework/CurveFitting/src/Algorithms/Fit1D.cpp#L431)).
- The base class, `Algorithm`, logs the exception description as an error, unless the algorithm is called as a child algorithm.
- For child algorithms, `Algorithm` just rethrows.
- Algorithms that call other algorithms often catch exception of child algorithm, and either ignore the exception, or throw a new exception (with a potentially different description).

## Problems

- Duplicated code in algorithms for logging and exceptions.
- Exceptions of child algorithms are often lost, since in general the calling algorithms do not log or forward details of the child's exception. This can make debugging more difficult.
- Duplicated error log messages, once from the algorithm itself, and once from the logging of exception messages done by `Algorithm`.

## Proposed solution

1. Change `Algorithm` to log and error with the exception description if there was an exception, *including child algorithms*.
2. Algorithms should generally not log errors but instead include the error message in the exception, if applicable.
3. If a child algorithm fails an algorithm should do one of the following:
  1. log a message stating why the error is ignored
  2. throw an error, maybe with a more context related message (edited)

We can consider logging child-errors as warning (or some other level), so users can avoid getting flooded with messages.
