# `rr` - Alternative Debugging Under Gdb

* What is it? - An application execution recorder and replayer integrating with gdb
  * *Apologies to Windows/OS X developers - purely a Linux  tool*
  * Requires intel chip with Nehalem or later arch
  * Most VMs will work but not *VirtualBox* & *Hyper-V* at this time

* Works on real applications with minimal overhead compared to built-in `gdb` recording mechansim

* Move from debugging a *live* application to debugging a pre-recorded, deterministic execution
  * Ideally suited for debugging intermittent failures

---

# Usage

* Start by using rr to record your application:

```


$ rr record /your/application --args
...
FAIL: oh no!
```

* The entire execution, including the failure, was saved to disk. That recording can now be debugged.

```
$ rr replay
GNU gdb (GDB) ...
...
0x4cee2050 in _start () from /lib/ld-linux.so.2
(gdb)
```

---

# Gdb Commands

* Supports common `gdb` commands including  `reverse-continue`, `reverse-step`, `reverse-next` and `reverse-finish`
  * essentially the reverse equivalents of standard forward commands

* Interface feels very familiar and it's pretty quick to get going

* Watch points are now very powerful and survive "rerunning" application as memory addresses stay the same!

---


# Real World Usage

* Used it to debug and fix one of our intermittent test failures: *OptimizeCrystalPlacementTest*

* A test failure could generally be guaranteed within 20-30 consecutive runs
  * Simple bash script to record execution of each run and stop script when a failure occurs
  * Now we have a recording of a *good* run & a *bad* run to compare

* Fire up `rr replay` side-by-side and step through to see divergance

* Ability to reverse step through the code useful
  * e.g. if you accidentally step over a function call

---

# Limitations

* Emulates a single-core machine. So, parallel programs incur the slowdown of running on a single core

* Cannot record processes that share memory with processes outside the recording tree

* Sometimes needs to be updated in response to kernel changes

---


# Links

* http://rr-project.org/
  * good documentation and videos about how `rr` works
