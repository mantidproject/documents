## Create .ico files

I used the following steps to create the .ico files from .svg:
* Create a png with transparency using [Inkscape](https://inkscape.org/en/). It is important that the png is 256x256 pixels.
* Use [imagemagick](http://www.imagemagick.org/script/index.php) to create the .ico file with the command
```
convert mantid_python.png -define icon:auto-resize=64,48,32,16 -background transparent mantid_python.ico
```

