#include "DemoAlg.h"

// Register the algorithm into the AlgorithmFactory
DECLARE_ALGORITHM(DemoAlg)

using namespace Mantid::Kernel;
using namespace Mantid::API;
using namespace Mantid::Geometry;

// Get a reference to the logger. It is used to print out information, warning and error messages
Mantid::Kernel::Logger& DemoAlg::g_log = Mantid::Kernel::Logger::get("DemoAlg");

void DemoAlg::init()
{
  // Put your initialisation code (e.g. declaring properties) here...
  
  // Declare two workspace properties and an integer property
  declareProperty(new WorkspaceProperty<>("InputWorkspace","",Direction::Input));
  declareProperty(new WorkspaceProperty<>("OutputWorkspace","",Direction::Output));
  
  declareProperty("AProperty",10);
}

void DemoAlg::exec()
{
  // Retrieve the input properties
  Workspace_sptr inputWorkspace = getProperty("InputWorkspace");
  
  int factor = getProperty("AProperty");
  
  // Create the output workspace
  Workspace_sptr outputWorkspace = WorkspaceFactory::Instance().create(inputWorkspace);

  // Get a handle on the instrument geometrical definition associated with the workspace
  IInstrument_sptr instrument = inputWorkspace->getInstrument();
  // Get the position of the sample
  V3D samplePosition = instrument->getSample()->getPos();

  // Get hold of the mapping between spectrum numbers and UDETs
  SpectraMap_sptr specMap = inputWorkspace->getSpectraMap();

  // Loop over the spectra in the input workspace
  for (int i = 0; i < inputWorkspace->getNumberHistograms(); ++i)
  {
    // Just copy over the bin boundary and error data for this spectrum
    outputWorkspace->dataX(i) = inputWorkspace->dataX(i);
    outputWorkspace->dataE(i) = inputWorkspace->dataE(i);

    // Go via the workspace axis to get the spectrum number for the current index
    int spec = inputWorkspace->getAxis(1)->spectraNo(i);
    // Get a handle on the detector(s) related to the current spectrum
    IDetector_sptr det = specMap->getDetector(spec);

    // Calculate L2 for the current detector
    double l2 = samplePosition.distance(det->getPos());
  
    // Loop over all the entries in the spectrum
    for (int j = 0; j < inputWorkspace->blocksize(); ++j)
    {
      // Set each value in the output to be the input multiplied by L2 and a constant
      outputWorkspace->dataY(i)[j] = inputWorkspace->dataY(i)[j]*l2*factor;
    }

    // Get the value of 2theta for this detector
    double twoTheta = instrument->detectorTwoTheta(det);

    // Print out some information to the log
    g_log.information() << "Detector position: " << l2 << ", " << twoTheta << "\n";
  }

  // Set the value of the OutputWorkspace property to be the outputWorkspace variable
  setProperty("OutputWorkspace",outputWorkspace);

}

