#pragma once
#include "DllConfig.h"

class Point2D {
public:
  Point2D(double x_, double y_);
  double norm2() const;
  double x, y;
};

class A_DLL Point3D {
public:
  Point3D(double x_, double y_, double z_);
  double norm2() const;
  double x, y, z;
};
