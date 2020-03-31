#!/bin/bash

# pyenv activate mikesachs.com

#
# Create the web version of the PDF resume.
#
cd /Users/mike/odrive/Dropbox/mikesachs.com/python/
python to_xetex.py -w
cd /Users/mike/odrive/Dropbox/mikesachs.com/tex/
/Library/TeX/texbin/xelatex -synctex=1 -interaction=nonstopmode -output-driver="/Library/TeX/texbin/xdvipdfmx -q -E" /Users/mike/odrive/Dropbox/mikesachs.com/tex/pdf_web.xetex
mv /Users/mike/odrive/Dropbox/mikesachs.com/tex/pdf_web.pdf /Users/mike/odrive/Dropbox/mikesachs.com/pdf/MichaelSachs.pdf

#
# Create the mini web version of the PDF resume.
#
cd /Users/mike/odrive/Dropbox/mikesachs.com/python/
python to_xetex.py -w -m
cd /Users/mike/odrive/Dropbox/mikesachs.com/tex/
/Library/TeX/texbin/xelatex -synctex=1 -interaction=nonstopmode -output-driver="/Library/TeX/texbin/xdvipdfmx -q -E" /Users/mike/odrive/Dropbox/mikesachs.com/tex/pdf_web.xetex
mv /Users/mike/odrive/Dropbox/mikesachs.com/tex/pdf_web.pdf /Users/mike/odrive/Dropbox/mikesachs.com/pdf/MichaelSachsMini.pdf

#
# Create the print version of the PDF resume.
#
cd /Users/mike/odrive/Dropbox/mikesachs.com/python/
python to_xetex.py -p
cd /Users/mike/odrive/Dropbox/mikesachs.com/tex/
/Library/TeX/texbin/xelatex -synctex=1 -interaction=nonstopmode -output-driver="/Library/TeX/texbin/xdvipdfmx -q -E" /Users/mike/odrive/Dropbox/mikesachs.com/tex/pdf_print.xetex
mv /Users/mike/odrive/Dropbox/mikesachs.com/tex/pdf_print.pdf /Users/mike/odrive/Dropbox/mikesachs.com/pdf/MichaelSachsPrint.pdf

#
# Create the mini print version of the PDF resume.
#
cd /Users/mike/odrive/Dropbox/mikesachs.com/python/
python to_xetex.py -p -m
cd /Users/mike/odrive/Dropbox/mikesachs.com/tex/
/Library/TeX/texbin/xelatex -synctex=1 -interaction=nonstopmode -output-driver="/Library/TeX/texbin/xdvipdfmx -q -E" /Users/mike/odrive/Dropbox/mikesachs.com/tex/pdf_print.xetex
mv /Users/mike/odrive/Dropbox/mikesachs.com/tex/pdf_print.pdf /Users/mike/odrive/Dropbox/mikesachs.com/pdf/MichaelSachsPrintMini.pdf

#
# Synch with the server.
#
cd /Users/mike/odrive/Dropbox/mikesachs.com/

rsync -avhL --delete --exclude-from 'exclude-list.txt' /Users/mike/odrive/Dropbox/mikesachs.com/ mksachs@habersham.dreamhost.com:mikesachs.com