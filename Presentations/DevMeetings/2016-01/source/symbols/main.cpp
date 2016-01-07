#include "A/Point.h"
#include <iostream>

using std::cout;
using std::endl;

int main() {
  Point3D p1(3, 4, 5);
  cout << "p1.norm2() = " << p1.norm2() << endl;
}
