** Problems of current cxxtest

- `createSuite` and `destroySuite`.
- Only one test suite per file / algorithm supported (apart from performance tests).
- Cannot (temporarily) disable test by commenting / `#if 0`, need to rename it since test discovery is based on string parsing.
