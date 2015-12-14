# Suggestions based on course at ORNL

--
**Context**

ORNL hired [Construx](http://www.construx.com/) to provide training December 1-3, 2015 on the topic of "Software Development Best Practices"

---

# What was covered (skipping lots)

1. Design by contract
2. "Better" coding standards
3. Write for others

---

# Design by contract

* Most bugs come from symantic errors rather than syntax errors
* Be explicit about what is expected of inputs and what will be provided by outputs
* Specify the contract in the code
* Make the names (objects, functions, variables) follow the contract

---

# Design by contract - doxygen [pre](http://www.stack.nl/~dimitri/doxygen/manual/commands.html#cmdpre) and [post](http://www.stack.nl/~dimitri/doxygen/manual/commands.html#cmdpost)

```c++
/**
 * \param x Bin boundaries to convert to. This vector will be copied
 * into this.
 * \pre The x-values will be in increasing order
 * \post The data will be correctly rebined or have thrown an exception
 */
void rebin(std::vector<double> x);
```
* Advantages:
  * Puts the contract next to the rest of the code documentation
  * Uses existing tags
* Disavantages:
  * Expects that people read the code before calling it

---

# Design by contract - [assert](http://en.cppreference.com/w/cpp/error/assert) 

```c++
#include <cassert>

void rebin(std::vector<double> x) {
  assert(std::is_sorted(x);
  // do the rebinning
  assert(this->y.size() == (x.size() + 1));
}
```
* Advantages:
  * Enforces the contract at runtime
  * Assertions only apply to debug builds (which is supported by CMake)
* Disadvantages:
  * Calculating assertions can be as expensive as just enforcing them ([sort](http://en.cppreference.com/w/cpp/algorithm/sort) vs [is_sorted](http://en.cppreference.com/w/cpp/algorithm/is_sorted))
  
Related:
* [static_assert](http://en.cppreference.com/w/cpp/language/static_assert) in c++11 (with `message`) and c++17 (without `message`)
* Contracts in c++17? ([reference](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/n4378.pdf) and [reference](http://www.open-std.org/JTC1/SC22/WG21/docs/papers/2015/n4415.pdf))
* Preconditions from CppCoreGuidelines ([i.5](https://github.com/isocpp/CppCoreGuidelines/blob/master/CppCoreGuidelines.md#-i5-state-preconditions-if-any) and [i.7](https://github.com/isocpp/CppCoreGuidelines/blob/master/CppCoreGuidelines.md#-i7-state-postconditions))

---

# Make the names follow the contract

* Read [Clean Code](http://www.amazon.com/gp/product/0132350882?keywords=code%20complete&qid=1450118105&ref_=sr_1_2&s=books&sr=1-2) by Robert “Uncle Bob” Martin
* [The Boy Scout Rule](http://programmer.97things.oreilly.com/wiki/index.php/The_Boy_Scout_Rule): Leave the code better than you found it

---
# "Better" coding standards - [mantid's](http://www.mantidproject.org/Coding_Standards)

* Most bugs are syntactically valid
* Placement of curly braces standards don't really matter

---
# "Better" coding standards - [mantid's](http://www.mantidproject.org/Coding_Standards)

* Most bugs are syntactically valid - compiler warnings
* Placement of curly braces standards don't really matter - [clang-format](http://clang.llvm.org/docs/ClangFormat.html)
* Code complexity is what matters - more difficult to understand
* Enforce as much of the standard as possible with tools

---
# Enforce as much of the standard as possible with tools

Already done:
* compiler warnings
* cppcheck - [mantid report](http://builds.mantidproject.org/view/Static%20Analysis/job/cppcheck-1.71/)
* coverity - [mantid report](https://scan.coverity.com/projects/mantidproject-mantid)
* valgrind (broken) - [mantid report](http://builds.mantidproject.org/view/Static%20Analysis/job/valgrind_core_packages/)
* **bonus** coveralls - [mantid report](https://coveralls.io/github/mantidproject/mantid)

Possibilities - C++
* [oclint](http://oclint.org/) - code complexity
* [copy-paste detector](http://pmd.sourceforge.net/pmd-4.3.0/cpd.html)

Possibilities - python
* [pep8](https://pypi.python.org/pypi/pep8) - easy version of pylint
* [radon](https://pypi.python.org/pypi/radon) - code complexity

---
# Write for others

* Mantid [Iteration30](https://github.com/mantidproject/mantid/releases/tag/Iteration30) was created in 2011
* There are currently [70 contributers](https://github.com/mantidproject/mantid/graphs/contributors)

---

# Credits

* Steve Tockey of [Construx](http://www.construx.com/) (he suggests buying his current book [Return on Software](http://www.amazon.com/gp/product/032156149X?keywords=steve%20tockey&qid=1448981669&ref_=sr_1_1&sr=8-1) and is writing another)
* Slideshow render at [Remarkise](https://gnab.github.io/remark/remarkise?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmantidproject%2Fdocuments%2Fmaster%2FPresentations%2FORNLConstrux.md)
