
#ifndef __vtkMyCustomFilter_h
#define __vtkMyCustomFilter_h

#include "vtkElevationFilter.h"

class VTK_EXPORT vtkMyCustomFilter : public vtkElevationFilter
{
public:
  static vtkMyCustomFilter* New();
  vtkTypeRevisionMacro(vtkMyCustomFilter, vtkElevationFilter);
  void PrintSelf(ostream& os, vtkIndent indent);

protected:
  vtkMyCustomFilter();
  ~vtkMyCustomFilter();

private:
  vtkMyCustomFilter(const vtkMyCustomFilter&);  // Not implemented.
  void operator=(const vtkMyCustomFilter&);  // Not implemented.
};

#endif
