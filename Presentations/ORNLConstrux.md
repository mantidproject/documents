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

* Be explicit about what is expected of inputs and what will be provided by outputs
* Specify the contract in the code

---

# Design by contract - doxygen [pre](http://www.stack.nl/~dimitri/doxygen/manual/commands.html#cmdpre) and [post](http://www.stack.nl/~dimitri/doxygen/manual/commands.html#cmdpost)

```c++
/**
 * \pre The x-values will be in increasing order
 * \post The data will be correctly rebined or have thrown an exception
 */
void rebin(std::vector<double> x);
```

---

# Design by contract - assert

```c++
#include <cassert>

void rebin(std::vector<double> x) {
  assert(std::is_sorted(x);
  // do the rebinning
  assert(this->y.size() == (x.size() + 1));
}
```

---

# Credits

* Steve Tockey of [Construx](http://www.construx.com/) (he suggests buying his current book [Return on Software](http://www.amazon.com/gp/product/032156149X?keywords=steve%20tockey&qid=1448981669&ref_=sr_1_1&sr=8-1) and is writing another)
* Slideshow render at [Remarkise](https://gnab.github.io/remark/remarkise?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmantidproject%2Fdocuments%2Fmaster%2FPresentations%2FORNLConstrux.md)
