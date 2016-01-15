#pragma once

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
