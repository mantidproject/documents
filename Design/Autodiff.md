Automatic Differentiation
=========================

Introduction
------------
Automatic differentiation can be used as an alternative to numeric differentiation when analytical derivatives are not available or are hard to implement. In contrast to numeric differentiation this method comes with a relatively small overhead and gives partial derivatives that are exact within machine precision. More about the method can be found at [Wikipedia](http://en.wikipedia.org/wiki/Automatic_differentiation) or [http://www.autodiff.org/](http://www.autodiff.org/).

There are generally two ways to implement this method, source code transformation, which would be an additional build step. The other is operator overloading, which requires no additional build step, but using special types provided by the respective libraries.

Being able to use this would be very useful, as one would not be required to write analytical derivatives anymore, without suffering from the performance hit of numerical derivatives. In the cases where this is also too slow, analytical derivatives can still be applied.

Scope
-----
Since functions need to use special variable types (instead of double), this feature can only be used in new functions or old functions that have been adapted.

Because of the special POLDI-fit, a new sub-type of IFunction had to be created recently (IFunction1DSpectrum, Ticket #9531) and all POLDI-related functions will be derived from this interface.

My suggestion is to keep autodiff within this "sandbox" at first, to see how it works out and so that it does not impact other functionality. If others find it useful, the scope can be extended to other areas as well.


The adept library
-----------------
For the operator overloading method, several libraries are available. I personally found [adept](http://www.met.reading.ac.uk/clouds/adept/) easiest to use. It is developed at the University of Reading and seems to have its origin in large scale simulations and is distributed under GPLv3. On the site the author links to his papers on the library, one of which also contains benchmark data suggesting that adept performs better in most situation than the other libraries.

It basically consists of two file, adept.h and adept.cpp, so it is very small. Some tests are included in the distribution as well.


Integrating it as a third-party library
---------------------------------------
Since adept does not seem to be available in the Ubuntu repositories (have not checked the other distros), it would have to be included in Mantid. The library is apparently not released too often (there's more than a year beween the last two releases), so keeping track of this as an upstream dependency seems doable.

The library is intended to be built and used in Unix/Linux-systems. I tried to build a small sample project in Visual Studio (copying adept.h and adept.cpp into the project directory) and adding two extra #define-statements was enough to make it compile. The results produced by that code were correct.

Since I don't have access to Mac OS X, I can not test it there.

What would be the best way to integrate this third-party library into Mantid?