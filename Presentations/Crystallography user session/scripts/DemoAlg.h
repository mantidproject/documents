#ifndef DEMOALG_H_
#define DEMOALG_H_

#include "MantidAPI/Algorithm.h"

class DemoAlg : public Mantid::API::Algorithm
{
public:
  /// (Empty) Constructor
  DemoAlg() : Mantid::API::Algorithm() {}
  /// Virtual destructor
  virtual ~DemoAlg() {}
  /// Algorithm's name
  virtual const std::string name() const { return "DemoAlg"; }
  /// Algorithm's version
  virtual const int version() const { return (1); }
  /// Algorithm's category for identification
  virtual const std::string category() const { return "Demos"; }

private:
  /// Initialisation code
  void init();
  ///Execution code
  void exec();

  /// Static reference to the logger class
  static Mantid::Kernel::Logger& g_log;
};

#endif /*DEMOALG_H_*/
