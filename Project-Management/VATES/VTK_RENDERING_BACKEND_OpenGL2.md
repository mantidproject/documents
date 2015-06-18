ParaView 5 includes the option to use the new OpenGL2 rendering backend. This can only be chosen at compile time.

Most systems built in the last five years should support version 2.1, which was released in 2006. 
In addition, software rendering provided by Mesa supports OpenGL 2.1 (optionally accelerated using LLVM/Gallium).

significant performance enhancements. improved image quality. 

[New OpenGL Rendering in VTK](http://www.kitware.com/source/home/post/144)

~~DModule_vtkRenderingVolumeOpenGLNew=ON~~ not necessary after VTK v6.1

[Volume Rendering Improvements in VTK](http://www.kitware.com/source/home/post/154)

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
