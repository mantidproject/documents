
cmake_minimum_required(VERSION 2.6)

project(CustomView)

FIND_PACKAGE(ParaView REQUIRED)
INCLUDE(${PARAVIEW_USE_FILE})

INCLUDE(${ParaView_CMAKE_DIR}/ParaViewBranding.cmake)
INCLUDE(${ParaView_CMAKE_DIR}/ParaViewPlugins.cmake)

SET (SOURCE_FILES 
  Demo.cxx
  MyCustomWindow.cxx
  MyCustomWindow.h
)

QT4_WRAP_CPP(MOC_SRCS
  MyCustomWindow.h
)

INCLUDE_DIRECTORIES(
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${CMAKE_CURRENT_BINARY_DIR})

ADD_EXECUTABLE(CustomView ${SOURCE_FILES} ${MOC_SRCS} ${UI_BUILT_SOURCES})
TARGET_LINK_LIBRARIES(CustomView pqCore pqComponents pqApplicationComponents
${QT_LIBRARIES} )
