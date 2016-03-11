class: center, middle

# Using the C++ standard library with lambda expressions

Mantid developer meeting 2016

michael.wedel@esss.se

---

## What is a lambda expression?

```cpp
[=] (double x) { return 2.0 * a * x; }
```
--

### Components
- `[=]` Capturing variables from surrounding scope (by value)
- `(double x)` Function arguments
- `{ return 2.0 * a * x; }` Function body, `a` captured from surrounding scope
--


### Behind the scenes
- Compiled to *closure*, basically functor with `operator()()`
- Can be stored as `std::function`
- Usable with many standard library algorithms

---

## I want to lambda, but where?

**Replace following `for`-loop:**

```cpp
void ConfigServiceImpl::setFacility(const std::string &facilityName) {
  bool found = false;

  std::vector<FacilityInfo *>::const_iterator it = m_facilities.begin();
  for (; it != m_facilities.end(); ++it) {
    if ((**it).name() == facilityName) {
      found = true;
      setString("default.facility", facilityName);
    }
  }
  if (found == false) {
    throw Exception::NotFoundError("Facilities", facilityName);
  }
}
```
--

- Iterates over entire vector (even if first item matches)
- Uses extra variable to track state
- Actual work in the middle of "search"-loop

---

## Implementation using lambda expression

- Function from standard library: `std::find_if(begin, end, pred)`
- Returns `iterator` to element where `pred` returns `true`
- `pred`: Unary function `bool pred(const T &)`.
--


```cpp
void ConfigServiceImpl::setFacility(const std::string &facilityName) {
  auto facilityMatch = 
          std::find_if(m_facilities.begin(), m_facilities.end(),
                       [=](FacilityInfo *facility) {
                         return facility->name() == facilityName;
                       });

  if (facilityMatch != m_facilities.end()) {
    setString("default.facility", facilityName);
  } else {
    throw Exception::NotFoundError("Facilities", facilityName);
  }
}
```

- `m_facilities` contains `FacilityInfo *`-elements
- Comparison function against `std::string` using `::name()`.
- Lambda captures `facilityName` by value automatically

---

## Some guidelines

- Use lambdas together with standard library functions
- Keep the lambdas short (rule of thumb: 5 lines)
- Careful with default capture modes (`this` is captured when methods are used in a lambda)!
- Prefer to capture by value if you want to store the closure to avoid dangling reference problems
- Replace lambdas with named functions or functors when you use them more than once!
--


.right[*I suppose it is tempting, if the only tool you have is a hammer, to treat everything as if it were a nail.*]

.right[— A. Maslow]

---

## Algorithm overview

If you have to sort, filter, sum, generate, fill, ... a container and are about to type `for`, check this page:
    
> http://en.cppreference.com/w/cpp/algorithm
    
Many algorihtms have overloads which accept one or two functions, which can be Lambdas!
--

### Algorithms I wish I had known/used sooner:

- `std::inner_product` (combine & accumulate two containers!)
- `std::accumulate` (overload with combine function)
- `std::transform` (transform one or two containers simultaneously with arbitrary function!)
