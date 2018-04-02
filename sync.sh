#!/bin/bash

pyenv activate mikesachs.com

#
# Create the web version of the PDF resume.
#
cd /Users/michaelsachs/odrive/Dropbox/mikesachs.com/python/
python to_xetex.py -w
cd /Users/michaelsachs/odrive/Dropbox/mikesachs.com/tex/
/Library/TeX/texbin/xelatex -synctex=1 -interaction=nonstopmode -output-driver="/Library/TeX/texbin/xdvipdfmx -q -E" /Users/michaelsachs/odrive/Dropbox/mikesachs.com/tex/pdf_web.xetex
mv /Users/michaelsachs/odrive/Dropbox/mikesachs.com/tex/pdf_web.pdf /Users/michaelsachs/odrive/Dropbox/mikesachs.com/pdf/MichaelSachs.pdf

#
# Create the print version of the PDF resume.
#
cd /Users/michaelsachs/odrive/Dropbox/mikesachs.com/python/
python to_xetex.py -p
cd /Users/michaelsachs/odrive/Dropbox/mikesachs.com/tex/
/Library/TeX/texbin/xelatex -synctex=1 -interaction=nonstopmode -output-driver="/Library/TeX/texbin/xdvipdfmx -q -E" /Users/michaelsachs/odrive/Dropbox/mikesachs.com/tex/pdf_print.xetex
mv /Users/michaelsachs/odrive/Dropbox/mikesachs.com/tex/pdf_print.pdf /Users/michaelsachs/odrive/Dropbox/mikesachs.com/pdf/MichaelSachsPrint.pdf

#
# Synch with the server.
#
cd /Users/michaelsachs/odrive/Dropbox/mikesachs.com/

rsync -avhL --delete --exclude-from 'exclude-list.txt' /Users/michaelsachs/odrive/Dropbox/mikesachs.com/ mksachs@habersham.dreamhost.com:mikesachs.com