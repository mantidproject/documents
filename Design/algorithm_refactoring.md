# Cleaning up Mantid Algorithms

## Motivation

See discussions during the developer workshop in January 2016.

This document is meant as a base for discussion and does not (yet) represent a complete design. The results of this and potentially various parts of this document will eventually be used to create documentation for developers on how to write an algorithm.


## N kinds of boilerplate code


### Progress

```cpp
Progress progress(this, 0.0, 1.0, m_numberOfSpectra);
// [...]
progress.report();
```

This can be done in the proposed `Algorithm::transform` method, see below.


### Getters on workspaces

Typically when looping over spectra, one or several getters are used on workspaces, for event lists, spectra, and histograms. For example, `getEventList()`, `getSpectrum()`, and `readX()`, `readY()`, `readE()`.

There may be a way to combine this with what is described in the proposed `Algorithm::transform` method below, but it is not obvious how to get rid of these entirely.


### Looping over spectra

The loop over histograms comprises various kinds of boilerplate:

- The `for`-loop statement itself
- `PARALLEL` macros, which in turn contain:
  - OpenMP pragmas
  - A mechanism for cancellation
  - Parallel exception handling

  Typically there are 4 `PARALLEL` macros for a single loop over spectra.

To get rid of these, we would like to implement something along the lines of `std::transform`. In our case it turns out to be most convenient to make this a member of `Algorithm`, since our `transform` needs access to various members of `Algorithm`, in particular:

- The `PARALLEL` macros access `m_cancel`, `m_parallelException` (which, however, could be made local), and `g_log` (which may not be necessary, strictly speaking).
- We would like to move the `Progress` code into our `transform`, so we need the `this` pointer.

If it were not a member we would need some way of passing all these things into our `transform`, which is cumbersome.

In the simplest case (in-place modification of a single field), this could be implemented along the lines of this:

```cpp
// Note that we need the explicit syntax ELEM (WS::*getter)(IDX), else the compiler cannot resolve (const) overloads
template <class WS, class OP, class ELEM, class IDX>
void transform(WS &workspace, ELEM (WS::*getter)(IDX), const OP &operation) {
  int length = workspace.getNumberHistograms();
  auto progress = Kernel::make_unique<API::Progress>(this, 0.0, 1.0, length);
  auto getArg = std::mem_fn(getter);
  PARALLEL_FOR1((&workspace))
  for (int i = 0; i < length; ++i) {
    PARALLEL_START_INTERUPT_REGION
    operation(getArg(workspace, i));
    progress->report(name());
    PARALLEL_END_INTERUPT_REGION
  }
  PARALLEL_CHECK_INTERUPT_REGION
  workspace.clearMRU();
}
```

Usage would then be, e.g.,

```cpp
transform(ws, &EventWorkspace::getEventList, my_eventlist_rebin);
```

Things to consider in the design:

- We do not want to call `transform` unnecessarily often. Many algorithms consist of various micro-steps. If we do a separate transform for each of those steps we would end up loading all our data from memory many times.

  A common solution to solve this problem are expression templates, but the generic nature of the things we do (i.e., not just chaining of simple operations like `+` and `*`) would probably make this cumbersome.

  Instead, it is probably best to compose a "top-level" function or functor that calls functions or functors implementing the various micro-steps. We would then pass the top-level callable to `transform`.

-  We need to provide means to deal with several in- and outputs, e.g., in the common case of an input and output `MatrixWorkspace`, where we need x, y, and error data for both input and output. There are also cases that are more complex than that


Furthermore, we would probably want to provide overloads for supporting the following cases:

- Transform for all spectra.
- Transform for a range of spectra.
- Transform for a list of spectra.


### Casting of input workspaces to specific workspace types

```cpp
// Check if its an event workspace
EventWorkspace_const_sptr eventW =
    boost::dynamic_pointer_cast<const EventWorkspace>(inputWS);
if (eventW != NULL) {
  this->execEvent();
  return;
}
```

A very nice way to solve this would be to use the **visitor pattern**:

- Add the following method to `Algorithm`:
  ```cpp
  virtual std::string getInputWorkspaceForVisitorPattern() const {
    return std::string{};
  }
   ```
  Algorithm implementations that have an input workspace and support the visitor pattern reimplement this function and return the name of the input workspace property.
- Add a method like this to all Workspace types:
  ```cpp
  void Workspace2D::apply(API::Algorithm &algorithm) {
    algorithm.apply(*this);
  }
  ```
- `Algorithm::Execute()` calls `getInputWorkspaceForVisitorPattern()` to obtain a workspace `ws` and then calls `ws.apply(*this);`
- All algorithms implement `apply` for various workspace types.

The last bullet is where it all starts to fall apart, there is a fatal flaw in this mechanism: Inheritance does not go well with overloading. For the visitor pattern to work we would need to implement `Algorithm::apply` for **all workspace types**. What we would actually like to do is, e.g., implement `Rebin::apply(const MatrixWorkspace &ws)` and `Rebin::apply(const EventWorkspace &ws)`. Calling the algorithm with a `Workspace2D` will then **not** resolve to `Rebin::apply(const MatrixWorkspace &ws)` but `Algorithm::apply(const Workspace2D &ws)`.

The conclusion is that currently there is **no reasonable way for using the visitor pattern** in this case.

- Are there other ways to solve the some problem?
- Reconsider the visitor pattern when redesigning workspaces.


### Creating output `EventWorkspace`

Replace

```cpp
// Make a brand new EventWorkspace
outputWS = boost::dynamic_pointer_cast<EventWorkspace>(
    API::WorkspaceFactory::Instance().create(
        "EventWorkspace", inputWS->getNumberHistograms(), 2, 1));
// Copy geometry over.
API::WorkspaceFactory::Instance().initializeFromParent(inputWS, outputWS,
                                                       false);
// You need to copy over the data as well.
outputWS->copyDataFrom((*inputWS));
```

with

```cpp
outputWS = inputWS->clone();
```


### Code for dealing with input and output workspaces

Apart from the bits covered by the discussion above on casting and creating output event workspaces, there are also others:

- Dealing with the case `inputWS == outputWS`, which is particularly bad in the case of `EventWorkspace`, since it requires even more casting.
- Setting the output workspace property,
  ```cpp
  this->setProperty("OutputWorkspace", outputWS);
   ```


### More potential candidates

#### Ranges or lists of spectra

There seem to be quite a few algorithms which either run on all spectra, a user-defined range of spectra, or a user-defined list of spectra. We should have a generic way to deal with this.


## Library of smaller building blocks

An algorithm implementation that uses a `Algorithm::transform` as described above needs to provide some sort of callable to it. The callable would typically do something to a spectrum, a histogram, or an event list. The callable will typically be specific to the particular algorithm, however, in most cases, it will contain many bits that can be reused. We need to:

- Provide a library of commonly used bits. This can be functions or functors, but probably both.
- Figure out if there is a reasonable way for automatic chaining of those bits to build the top-level callable.
- Have a reasonable way to document and search the existing bits, such that developers will use them in their algorithms.
