# Extension interoperability

## The interface contract

A small set of abstract C++ base classes defines what an extension is —
`IExtension` for compute, plus a family of GUI-specific interfaces covered in
[Hosts and registries](03-hosts-and-registries.md). These are plain C++, with
no pybind11 or Python dependency, so core can compile and use them without
Python present at all.

```cpp
struct IExtension {
    virtual std::string name() const = 0;
    virtual Result execute(const Args&) = 0;
    virtual ~IExtension() = default;
};
```

**This is the registry's minimum contract, not the whole bound surface.**
`IExtension` is deliberately narrow — it's the shape the registry needs to
treat anything uniformly for dispatch (find it, name it, run it). The SDK's
binding generator reflects over the *concrete* extension class, not the
abstract interface, and binds everything it finds there:

```cpp
class GaussianFit : public IExtension {
public:
    std::string name() const override { return "GaussianFit"; }
    Result execute(const Args&) override { /* ... */ }

    // extension-specific surface — unrelated to the registry contract,
    // bound to Python just as fully as name() and execute() are
    void setInitialGuess(double mean, double sigma);
    FitReport getReport() const;
    std::vector<double> residuals() const;
};
```

```python
ext.name()                          # from IExtension
ext.execute(args)                   # from IExtension
ext.set_initial_guess(mean, sigma)  # GaussianFit-specific, fully exposed
ext.get_report()
ext.residuals()
```

The registry only ever calls through the narrow `IExtension*` for its own
bookkeeping. `IExtension`'s two methods are the floor every extension must
clear to participate in the registry, not a ceiling on what gets bound — same
relationship as `IWorkspace` to `TableWorkspace` below.

## The pybind11 trampoline: one call path, two possible backings

A single trampoline class per interface (not per extension) lets a Python
subclass satisfy the same C++ interface that native implementations satisfy:

```cpp
struct PyExtensionTrampoline : IExtension, py::trampoline_self_life_support {
    std::string name() const override {
        PYBIND11_OVERRIDE_PURE(std::string, IExtension, name);
    }
    Result execute(const Args& a) override {
        PYBIND11_OVERRIDE_PURE(Result, IExtension, execute, a);
    }
};
```

A caller holding an `IExtension*` never needs to know which backing it has.
Native calls are a plain vtable dispatch, zero overhead. Python calls go
through the trampoline, which acquires the GIL and forwards into the Python
method.

**Granularity matters.** This pattern is cheap at "run this algorithm" /
"fetch this metadata" granularity. It's expensive at "call this per element"
granularity, because every crossing acquires the GIL. Keep interface methods
coarse; keep hot inner loops entirely on one side of the boundary.

## Binding generation is a build byproduct, not hand-written labor

Because extensions are maintained independently and core can't write
everyone's bindings, Python-visibility for C++ extensions is generated as
part of the standard SDK build step, not authored by hand per extension:

- **Build-time codegen** (e.g. a Binder-style, Clang-AST-based generator):
  walks the extension's headers, emits real pybind11 C++ source, which
  compiles into a second shared library alongside the native one. Native
  runtime speed, no extra runtime dependency, at the cost of a build step and
  occasional manual touch-up for unusual signatures.
- **Runtime reflection** (cppyy, built on Cling): no second binary, no codegen
  step at all — Python calls are resolved dynamically against the compiled
  headers. Heavier runtime dependency (Cling/LLVM), some coverage gaps for
  template-heavy code.

Either way: following the SDK's header conventions — already required to
register into the interface system at all — produces Python bindings as a
side effect. Extension authors who skip the conventions simply don't get a
Python module or a registry entry; that's an expected consequence, not a
support gap.

## Binding is not limited to single entrypoints

The `IExtension`/trampoline pattern solves one narrow problem: letting the
registry dispatch uniformly across C++ and Python. It is not the general
binding mechanism. Plain pybind11 class binding exposes as rich a surface as
the class actually has — constructors, arbitrary methods, properties,
operators, Python's iteration/indexing protocols:

```cpp
py::class_<TableWorkspace, IWorkspace, std::shared_ptr<TableWorkspace>>(m, "TableWorkspace")
    .def(py::init<>())
    .def("add_column", &TableWorkspace::addColumn)
    .def("row_count", &TableWorkspace::rowCount)
    .def("__getitem__", &TableWorkspace::getRow)
    .def("__arrow_c_stream__", &TableWorkspace::exportArrowStream);
```

A new workspace type can carry whatever rich API it needs. The trampoline
machinery only matters where Python code needs to *subclass and override* a
C++ interface (algorithms); a type that's merely *called*, like a workspace,
doesn't need one.

**Rich binding of a concrete type is separate from generic ecosystem
interoperability.** For other code — the dispatcher, a GUI view provider, an
unrelated algorithm — to accept a new workspace type without knowing its
concrete class in advance, it needs to satisfy a thin common contract
(`IWorkspace`: name, id, metadata) plus the Arrow export protocol. That thin
contract is what the registry stores as a type descriptor; everything above
it is free to design as needed.

## Data interoperability, solved separately from behavior

Workspaces (e.g. `TableWorkspace`) are backed by Arrow's in-memory format and
exposed via the Arrow C Data Interface / PyCapsule protocol
(`__arrow_c_stream__`). Any Arrow-aware library in either language — pandas,
polars, DuckDB, a C++ consumer — gets zero-copy access without Mantid writing
per-pair converters. This is an adopted standard, not a bespoke protocol.

## Stable ABI foundation, adopted for future-language support

A rewrite of this scale happens rarely, and adding a language later is far
more expensive than building for it now, while every interface is being
defined for the first time. Decided as the default; amendable if a future
contributor consensus judges it not worth carrying.

The actual contract is a plain C vtable, not the C++ abstract class:

```c
typedef struct {
    const char* (*name)(void* self);
    Result      (*execute)(void* self, const Args* args);
    void        (*destroy)(void* self);
} IExtensionVTable;

typedef struct {
    void* self;
    const IExtensionVTable* vtable;
} IExtensionHandle;
```

The C++ `IExtension` class becomes a thin, ergonomic wrapper over this handle
— extension authors still write `class MyAlgorithm : public IExtension` as
before; nothing changes in their day-to-day experience. Python still binds
against that C++ wrapper via pybind11, unchanged. Binder/cppyy still reflect
over the same C++ headers. A future language (Rust, or anything else) can
implement the raw vtable directly, with no C++ compiler or bridge tool
involved at all — it only needs to produce a compatible C ABI.

**Nothing C++ standard-library crosses the boundary.** No `std::string`,
`std::vector`, or `std::shared_ptr` in vtable signatures — those types don't
have a stable ABI even across compilers or standard-library versions of C++
itself. The vtable speaks only C-compatible types (raw pointers, fixed-size
structs, C strings, serialized buffers); the ergonomic wrapper converts at
the boundary, not across it.

The explicit registration entry point (an exported symbol called right after
load, rather than relying on implicit static initializers) is part of this
same ABI — any language that can export a C symbol can register, without
depending on a language-specific load-time convention.

**Cost:** one vtable struct and one thin wrapper, per interface family,
written once — not per extension.