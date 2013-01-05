reaction_koma.py
================

This little python script wraps around [Imagemagik's convert unix
tool](http://www.imagemagick.org) and provides a nicer commandline interface to
generate vertical 4koma scripts. This was mainly created to generate locally
[reaction guy's meme
strips](http://knowyourmeme.com/memes/reaction-guys-gaijin-4koma), but you
could actually use it for anything involving four images.

The script accepts all parameters from the commandline, but most of it can be
customized trough a ``.ini`` configuration file. This allows you to keep a set
of default images which you can use quickly with the ``-s`` switch. Here's the
help output of the command:

```
Usage: reaction_koma.py [options]

Options:
  -h, --help            show this help message and exit
  -1 FIRST, --first=FIRST
                        path of the first koma panel
  -2 SECOND, --second=SECOND
                        path of the second koma panel
  -3 THIRD, --third=THIRD
                        path of the third koma panel
  -4 FOURTH, --fourth=FOURTH
                        path of the fourth koma panel
  -c CONVERT_PATH, --convert=CONVERT_PATH
                        path to Imagemagik's convert binary
  -t FIRST, --top=FIRST
                        alias for the first panel
  -b THIRD, --bottom=THIRD
                        alias for the third panel
  -w STRIP_WIDTH, --strip-width=STRIP_WIDTH
                        width for the vertical strip
  -p PHOTOSET, --photoset=PHOTOSET
                        name of the default photoset from ini file
  -o OUTPUT, --output=OUTPUT
                        filename for the strip, will be overwritten
```
And here is the configuration file I use:

```
[global]
convert_path=/usr/local/bin/convert
strip_width=500

[cinema]
second=~/project/python/reaction_koma/sets/cinema/meh.jpg
fourth=~/project/python/reaction_koma/sets/cinema/excited.jpg

[icinema]
fourth=~/project/python/reaction_koma/sets/cinema/meh.jpg
second=~/project/python/reaction_koma/sets/cinema/excited.jpg
```
With these names you can create a meh-excited sequence or the *inverted*
excited-meh sequence easily, you only need to specity the top and bottom images
for each.

Further improvements
====================

Arguably you would want to implement the image processing with the [Python
Imaging Library](http://www.pythonware.com/products/pil/) which could be in
theory more efficient, and since it doesn't depend on unixy software would be
more portable to windows and the like.

But windows user would prefer a tile interface rather than commandline. So
arguably you would implement a GUI. And arguably you would later implement a
text editor. And arguably you would implement an operative system as the last
step.

Arguably.
