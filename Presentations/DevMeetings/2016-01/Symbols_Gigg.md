class: center, middle

# Symbols 101

(Alternate title: Explaining those Visual Studio linker errors)

---

## Problem

```cpp
// Point.h - A.dll
class Point2D {
public:
  Point2D(double x_, double y_);
  double norm2() const;
  double x, y;
};
class Point3D {
public:
  Point3D(double x_, double y_, double z_);
  double norm2() const;
  double x, y, z;
};
```
```cpp
// Point.cpp - A.dll
#include "Point.h"
// ---------------- Point2D ----------------------------
Point2D::Point2D(double x_, double y_) : x(x_), y(y_) {}
double Point2D::norm2() const { return x * x + y * y; }
// ---------------- Point3D ----------------------------
Point3D::Point3D(double x_, double y_, double z_) : x(x_), y(y_), z(z_) {}
double Point3D::norm2() const { return x * x + y * y + z * z; }
```

- A shared library (`A`) contains classes to be used by another library or executable

---

## Solution

- Simple! Just include it and link to the library:

```cpp
#include "A/Point.h"
#include <iostream>

using std::cout;
using std::endl;

int main() {
  Point3D p1(3, 4, 5);
  cout << "p1.norm() = " << p1.norm() << endl;
}
```

---

## Build (gcc/clang)

```remark
> g++ -o libA.so -shared A/Point.cpp
> g++ -o main main.cpp -L$PWD -lA
```

- Run

```remark
> LD_LIBRARY_PATH=$PWD ./main
p1.norm2() = 50
```

---

## Build (Visual Studio)

```remark
> cl /FeA.dll A\Point.cpp /LD
> cl /EHsc /Femain main.cpp A.lib

// Fails!
LINK : fatal error LNK1181: cannot open input file 'A.lib'
```

- Visual Studio separates the API (`.lib`) from the implementations (`.dll`)

```remark
> dir
A.dll
main.cpp
main.obj
Point.dll
Point.obj
```

- Where's the `.lib` file gone ??

---

## Symbol Visibility

- `MSVC` defines all symbols has hidden by default (and you can't change it)
 - All symbols to be used externally must be specially marked
 - Our `A` library has no public symbols and therefore no `.lib` for linking

- `gcc` & `clang` define all symbols as public by default
 - Visibility can be controlled using the `-fvisibility=hidden` compiler flag

```remark
> g++ -o libA.so -fvisibility=hidden -shared A/Point.cpp
> g++ -o main main.cpp -L$PWD -lA

//Fails!
/tmp/ccxOMz34.o: In function `main':
main.cpp:(.text+0x4a): undefined reference to `Point3D::Point3D(double, double, double)'
main.cpp:(.text+0x56): undefined reference to `Point3D::norm2() const'
collect2: error: ld returned 1 exit status
```

---

## Controlling Visibility

- Symbol visibility can be controlled at the source code level via attributes

```remark
// DllConfig.h
#if defined(_WIN32)
  #define DLLExport __declspec(dllexport)
  #define DLLImport __declspec(dllimport)
  #if defined(A_Exports)
    #define A_DLL DLLExport
  #else
    #define A_DLL DLLImport
  #endif
#elif defined(__GNUC__) || defined(__clang__)
  #define DLLExport __attribute__ ((visibility ("default")))
  #define A_DLL
#else
  #define DLLExport
  #define A_DLL
#endif
```

- Visual Studio requires that a symbol is marked `dllexport` when the DLL is being compiled and `dllimport` when being linked against.
  - `A_Exports` is defined at compile time on the command line when the DLL is being built

---

## Controlling Visibility

- Any struct, class and function declarations that are to be made public need to be marked with these attributes. Back to our `Point3D` example:

```cpp
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
```

- Building on `gcc` with `-fvisibility=hidden` is now successful

```remark
> g++ -o libA.so -fvisibility=hidden -shared A/Point.cpp
> g++ -o main main.cpp -L$PWD -lA

Success!
```

---

## Controlling Visibility

- On `MSVC` we need to define the `A_Exports` definition for a successful build.

```remark
> cl /DA_Exports  /FeA.dll A\Point.cpp /LD
> cl /EHsc /Femain main.cpp A.lib

// Success!
```

- Trying to use a symbol not marked as exported now produces the familar error:

```cpp
int main() {
  Point3D p1(3, 4, 5);
  cout << "P3D p1.norm() = " << p1.norm() << endl;
  Point2D p2(3, 4);
  cout << "P2D p2.norm() = " << p2.norm() << endl;
}
```

```remark
> cl /DA_Exports  /FeA.dll A\Point.cpp /LD
> cl /EHsc /Femain main.cpp A.lib

// Fails!

```

---

## Remarks

- We should use `-fvisibility=hidden` on `gcc`/`clang` and define the required macros.

- Advantages:
 - Smaller binaries
 - Consistent linking behaviour across all platforms, i.e. Linux/OSX devs will see symbol errors before hitting the build servers

- It should be low impact as the macros are already in the correct places for `MSVC`
