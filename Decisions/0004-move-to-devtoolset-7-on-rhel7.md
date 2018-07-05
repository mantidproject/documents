# 4. Move to devtoolset-7 on Red Hat 7

Date: 2018-06-26

## Status

Accepted

## Context

Red Hat 7's default compiler is gcc 4.8. This is not C++14 compliant and prevents access to more modern C++ features.

## Decision

As part of the maintenance cycle after release 3.13 we will move Red Hat 7 compilers over to use
gcc 7 as part of the [devtoolset-7](https://www.softwarecollections.org/en/scls/rhscl/devtoolset-7/) tools provided by Red Hat.

## Consequences

Combined with the move to Visual Studio 2017 this will allow us to set a minimum standard of C++14 across the project.
