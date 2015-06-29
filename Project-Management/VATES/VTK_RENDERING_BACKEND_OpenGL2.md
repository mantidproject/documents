#Mantid, VATES and OpenGL 2.1

ParaView 5 will include the option to use the new OpenGL 2.1 rendering backend. This new backend is designed for modern graphcis hardware and the VTK developers have shown some massive performance increases with improved image quality. This can only be chosen at compile time. While the older OpenGL1 backend is currently default for all but iOS and Android, we expect it will be soon deprecated as new work focuses on the OpenGL2 rendering backend. 

Most systems built in the last five years should support OpenGL version 2.1, which was released in 2006. In addition, software rendering provided by the Mesa library supports OpenGL 2.1. The [Gallium llvmpipe driver](http://www.mesa3d.org/llvmpipe.html) is currently the fastest software renderer.

Kitware reports massive performance improvements rendering complex geometries containing millions of triangles. They also report **improved** image quality. 

[New OpenGL Rendering in VTK](http://www.kitware.com/source/home/post/144)

Volume rendering 

`vtkImageData` (uniform rectilinear grid) is treated differently from other data types. Most everything else converted to a `vtkUnstructuredGrid` before rendering. Should we give the user the option through either a source or a filter to interpolate their data onto a `vtkImageData` object?

[Volume Rendering Improvements in VTK](http://www.kitware.com/source/home/post/154)

recent VTK paper

[The Visualization Toolkit (VTK): Rewriting the rendering code for modern graphics cards](http://www.sciencedirect.com/science/article/pii/S2352711015000035)

issue: remote access. Many SNS users remotely access "Analysis Workstations" via the NX client. The current server uses
the software renderer MesaGL version 6.4.1 that only supports OpenGL 1.2.

During the Summer 2015 shutdown, these analysis computers will be upgraded to RHEL 7. Remote access will be handled by [thinlinc](https://www.cendio.com/thinlinc/what-is-thinlinc). They [recommend using VirtualGL](https://www.cendio.com/resources/docs/tag/virtualgl.html) with hardware-accelerated 3D applications displayed on a remote client.

ISIS doesn't really having standard things that people use for remote access. 
We might have to get Nick to start discussing how people access things remotely. 
Getting people to switch requires offering something that is going to be far 
better than what they are currently using. 

It's a large enough change that we can't change silently.

potentional solution: VirtualGL http://www.virtualgl.org/

`vglrun ./paraview`

future investigation: check how performance depends on the choice of video card. Would the analysis computers benefit from high performance professional graphics?
