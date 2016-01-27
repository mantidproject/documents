class: center, middle

# Non-member Fuctions

---

## Some links

* [Dr Dobbs](http://www.drdobbs.com/cpp/how-non-member-functions-improve-encapsu/184401197)
* [!DOL](http://codeidol.com/cpp/effective-cpp/Designs-and-Declarations/Item-23-Prefer-non-member-non-friend-functions-to-member-functions/)

Putting all convenience functions in multiple header files — but one
namespace — also means that clients can easily extend the set of
convenience functions. All they have to do is add more non-member
non-friend functions to the namespace.

---

## A reminder of `AlignAndFocusPowder`

```C
// set up a progress bar with the "correct" number of steps
m_progress = new Progress(this, 0., 1., 22);

if (m_inputEW) {
  double tolerance = getProperty("CompressTolerance");
  if (tolerance > 0.) {
    g_log.information() << "running CompressEvents(Tolerance=" << tolerance
                        << ")\n";
    API::IAlgorithm_sptr compressAlg = createChildAlgorithm("CompressEvents");
    compressAlg->setProperty("InputWorkspace", m_outputEW);
    compressAlg->setProperty("OutputWorkspace", m_outputEW);
    compressAlg->setProperty("OutputWorkspace", m_outputEW);
    compressAlg->setProperty("Tolerance", tolerance);
    compressAlg->executeAsChildAlg();
    m_outputEW = compressAlg->getProperty("OutputWorkspace");
    m_outputW = boost::dynamic_pointer_cast<MatrixWorkspace>(m_outputEW);
  } else {
    g_log.information() << "Not compressing event list\n";
    doSortEvents(m_outputW); // still sort to help some thing out
  }
}
m_progress->report();
```

---

## A simpler version

```C
// set up a progress bar with the "correct" number of steps
m_progress = new Progress(this, 0., 1., 22);

if (m_inputEW) {
  double tolerance = getProperty("CompressTolerance");
  if (tolerance > 0.) {
    g_log.information() << "running CompressEvents(Tolerance=" << tolerance
                        << ")\n";
    CompressEvents::execAsChild(m_outputEW, m_outputEW, tolerance);
    m_outputW = boost::dynamic_pointer_cast<MatrixWorkspace>(m_outputEW);
  } else {
    g_log.information() << "Not compressing event list\n";
    doSortEvents(m_outputW); // still sort to help some thing out
  }
}
m_progress->report();
```