Agenda
======

* [DataProcessorWidget in Python](https://github.com/mantidproject/mantid/pull/18922)


Questions
=========

* Does anyone use Visual Studio 2017 with Mantid yet?
  
  
>There are some issues around this - @DavidFair: 
>  * Requires us to use new MS tool *VSWhere* to find VS installation. This can also be used to find VS2015 instead of using *"%VS140COMNTOOLS%* - [Gist with new visual-studio.bat code](https://gist.github.com/DavidFair/995285a0b6bc8afc0d91b1f55a2d98b2). 
>  * Boost has not been officially tested against 2017 so emits warnings (though these can be suppressed) 
>  * Currently fails to compile a typedef vector in a templated class (FortranVector.h). 
