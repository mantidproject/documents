Motivation
==========

Currently code (especially workflow algorithms) will be full of things
like

```C
double tolerance = getProperty("CompressTolerance");
m_outputEW = boost::dynamic_pointer_cast<EventWorkspace>(m_outputW);
if ((m_outputEW) && (tolerance > 0.)) {
  g_log.information() << "running CompressEvents(Tolerance=" << tolerance
                      << ")\n";
  API::IAlgorithm_sptr compressAlg = createChildAlgorithm("CompressEvents");
  compressAlg->setProperty("InputWorkspace", m_outputEW);
  compressAlg->setProperty("OutputWorkspace", m_outputEW);
  compressAlg->setProperty("Tolerance", tolerance);
  compressAlg->executeAsChildAlg();
  m_outputEW = compressAlg->getProperty("OutputWorkspace");
  m_outputW = boost::dynamic_pointer_cast<MatrixWorkspace>(m_outputEW);
}
m_progress->report();
```

This boiler-plate code exists (sometimes with copy/paste errors) in
many algorithms.

Alternative 1
=============

Add specific code into algorithms that should be simpler to call. This
would be strongly typed methods on the classes themselves. The code in
the header would be:

```C
static
EventWorkspace_sptr CompressEvents::execAsChild(EventWorkspace_sptr input,
                                                EventWorkspace_sptr output,
                                                double tolerance=1.e-5);
```

The return is the pointer to the resultant output workspace. This is
required because we use copy-on-write (cow) pointers. In the example
above its usage would be

```C
double tolerance = getProperty("CompressTolerance");
m_outputEW = boost::dynamic_pointer_cast<EventWorkspace>(m_outputW);
if ((m_outputEW) && (tolerance > 0.)) {
  g_log.information() << "running CompressEvents(Tolerance=" << tolerance
                      << ")\n";
  m_outputEW = CompressEvents::execAsChild(m_outputEW, m_outputEW, tolerance);
  m_outputW = boost::dynamic_pointer_cast<MatrixWorkspace>(m_outputEW);
}
m_progress->report();
```

While this is much cleaner in client code, every algorithm would need
to modified to add this functionality.

Alternative 2
=============

Initializer lists
([cplusplus](http://www.cplusplus.com/reference/initializer_list/initializer_list/))
or variadic templates
([cplusplus](http://www.cplusplus.com/articles/EhvU7k9E/) ,
[msdn](https://msdn.microsoft.com/en-us/library/dn439779.aspx)), might
do the job well. What this would do internally is call `setProperty(string &, Type &)` for each pair in the list then call `executateAsChild()`. The details of how this would exactly work are a bit fuzzy, but the usage would be:

```C
double tolerance = getProperty("CompressTolerance");
m_outputEW = boost::dynamic_pointer_cast<EventWorkspace>(m_outputW);
if ((m_outputEW) && (tolerance > 0.)) {
  g_log.information() << "running CompressEvents(Tolerance=" << tolerance
                      << ")\n";
  API::IAlgorithm_sptr compressAlg = createChildAlgorithm("CompressEvents");
  compressAlg->execAsChild({"InputWorkspace", m_outputEW},
                           {"OutputWorkspace", m_outputEW},
                           {"Tolerance", tolerance});
  m_outputEW = compressAlg->getProperty("OutputWorkspace");
  m_outputW = boost::dynamic_pointer_cast<MatrixWorkspace>(m_outputEW);
}
m_progress->report();
```

The benefit of this approach is that it needs to be written once and
can be used everywhere. The disadvantage is having to specify
key/value pairs for all parameters.
