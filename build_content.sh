#!/bin/zsh
source ~/.zshrc

pyenv activate mikesachs.com

BASEDIR=$(pwd)

#
# Create the web version of the PDF resume.
#
cd "$BASEDIR"/python/
python build_content.py -w
cd "$BASEDIR"/tex/
/Library/TeX/texbin/xelatex -synctex=1 -interaction=nonstopmode -output-driver="/Library/TeX/texbin/xdvipdfmx -q -E" "$BASEDIR"/tex/pdf.ltx
mv "$BASEDIR"/tex/pdf.pdf "$BASEDIR"/pdf/MichaelSachs.pdf

#
# Create the mini web version of the PDF resume.
#
#cd "$BASEDIR"/python/
#python build_content.py -w -m
#cd "$BASEDIR"/tex/
#/Library/TeX/texbin/xelatex -synctex=1 -interaction=nonstopmode -output-driver="/Library/TeX/texbin/xdvipdfmx -q -E" "$BASEDIR"/tex/pdf_web.xetex
#mv "$BASEDIR"/tex/pdf_web.pdf "$BASEDIR"/pdf/MichaelSachsMini.pdf
#
##
## Create the print version of the PDF resume.
##
#cd "$BASEDIR"/python/
#python build_content.py -p
#cd "$BASEDIR"/tex/
#/Library/TeX/texbin/xelatex -synctex=1 -interaction=nonstopmode -output-driver="/Library/TeX/texbin/xdvipdfmx -q -E" "$BASEDIR"/tex/pdf_print.xetex
#mv "$BASEDIR"/tex/pdf_print.pdf "$BASEDIR"/pdf/MichaelSachsPrint.pdf
#
##
## Create the mini print version of the PDF resume.
##
#cd "$BASEDIR"/python/
#python build_content.py -p -m
#cd "$BASEDIR"/tex/
#/Library/TeX/texbin/xelatex -synctex=1 -interaction=nonstopmode -output-driver="/Library/TeX/texbin/xdvipdfmx -q -E" "$BASEDIR"/tex/pdf_print.xetex
#mv "$BASEDIR"/tex/pdf_print.pdf "$BASEDIR"/pdf/MichaelSachsPrintMini.pdf

cd "$BASEDIR"

#
# Cleanup
#
rm tex/*.aux
rm tex/*.log
rm tex/*.out
rm tex/*.synctex.gz
rm tex/*.ltx
rm tex/*.log

#
# Synch with the server.
#

#rsync -avhL --delete --exclude-from 'exclude-list.txt' "$BASEDIR"/ mksachs@iad1-shared-b8-17.dreamhost.com

pyenv deactivate
