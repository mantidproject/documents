#include "Point.h"

// ---------------- Point2D ----------------------------
Point2D::Point2D(double x_, double y_) : x(x_), y(y_) {}

double Point2D::norm2() const { return x * x + y * y; }

// ---------------- Point3D ----------------------------
Point3D::Point3D(double x_, double y_, double z_) : x(x_), y(y_), z(z_) {}

double Point3D::norm2() const { return x * x + y * y + z * z; }
