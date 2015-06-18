ParaView 5 will include the option to use the new OpenGL 2.1 rendering backend. This new backend is designed for modern graphcis hardware and the VTK developers have shown some massive performance increases with improved image quality. This can only be chosen at compile time. While the older OpenGL 1 backend is currently default for all but iOS and Android, we expect it will be deprecated as new work focuses on the OpenGL2 rendering backend. 

Most systems built in the last five years should support OpenGL versio 2.1, which was released in 2006. 
In addition, software rendering provided by Mesa supports OpenGL 2.1 (optionally accelerated using LLVM/Gallium).

significant performance enhancements. improved image quality. 

[New OpenGL Rendering in VTK](http://www.kitware.com/source/home/post/144)

~~DModule_vtkRenderingVolumeOpenGLNew=ON~~ not necessary after VTK v6.1

[Volume Rendering Improvements in VTK](http://www.kitware.com/source/home/post/154)

recent VTK paper

[The Visualization Toolkit (VTK): Rewriting the rendering code for modern graphics cards](http://www.sciencedirect.com/science/article/pii/S2352711015000035)

issue: remote access. Many SNS users remotely access "Analysis Workstations" via the NX client. The current server uses
the software renderer MesaGL version ?.?.? that only supports OpenGL 1.2.

ISIS doesn't really having standard things that people use for remote access. 
We might have to get Nick to start discussing how people access things remotely. 
Getting people to switch requires offering something that is going to be far 
better than what they are currently using. 

It's a large enough change that we can't change silently.

potentional solution: VirtualGL http://www.virtualgl.org/

`vglrun ./paraview`

future investigation: check how performance depends on the choice of video card.
