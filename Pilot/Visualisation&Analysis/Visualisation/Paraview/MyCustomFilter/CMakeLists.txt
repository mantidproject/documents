
# create a paraview plugin containing server manager xml and the server
# manager classes to build
# this plugin can be loaded on the server side
cmake_minimum_required(VERSION 2.8)
ADD_PARAVIEW_PLUGIN(MyCustomFilter "1.0"
  SERVER_MANAGER_XML MyCustomFilter.xml 
  SERVER_MANAGER_SOURCES vtkMyCustomFilter.cxx)
