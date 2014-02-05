pyCopy-Windows
==============

Windows Python file copying

Library Copies files IF the modified time does not match!
NOTE: it does not matter if OLDER OR NEWER, NO MATCH WILL
RESULT IN OVERWRITE - to be fixed later :)

Simple to use,

python pyCopy.py src dst

to use for drag and drop (folder to script)

modify the class constants and specify your defaultdst
then drag your folder onto the script, its equiv to running

python pyCopy.py src

the DST is taken from defaultdst
