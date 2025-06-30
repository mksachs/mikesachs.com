#!/bin/zsh
source ~/.zshrc



BASEDIR=$(pwd)

OPTSTRING="rc:"

while getopts ${OPTSTRING} opt; do
    case ${opt} in
        r)
            echo "######### Create a PDF version of the resume #########"

            pyenv deactivate

            pyenv activate mikesachs.com

            cd "$BASEDIR"/python/
            python build_content.py -w
            cd "$BASEDIR"/tex/
            /Library/TeX/texbin/xelatex -synctex=1 -interaction=nonstopmode -output-driver="/Library/TeX/texbin/xdvipdfmx -q -E" "$BASEDIR"/tex/pdf.ltx
            mv "$BASEDIR"/tex/pdf.pdf "$BASEDIR"/pdf/MichaelSachs.pdf

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

            pyenv deactivate
            ;;
        c)
            echo "######### Create a cover letter called ${OPTARG} #########"

            cd "$BASEDIR"/tex/
            cp "$BASEDIR"/tex/templates/cover_letter_boilerplate.ltx "$BASEDIR"/tex/cover_letter_tmp.ltx
            /Library/TeX/texbin/xelatex -synctex=1 -interaction=nonstopmode -output-driver="/Library/TeX/texbin/xdvipdfmx -q -E" "$BASEDIR"/tex/cover_letter_tmp.ltx
            mv "$BASEDIR"/tex/cover_letter_tmp.pdf "$HOME"/Documents/cover_letters/"${OPTARG}".pdf

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

            ;;
        :)
            echo "Option -${OPTARG} requires an argument."
            exit 1
            ;;
        ?)
            echo "Invalid option: -${OPTARG}."
            exit 1
            ;;
    esac
done


#
##
## Synch with the server.
##
#
##rsync -avhL --delete --exclude-from 'exclude-list.txt' "$BASEDIR"/ mksachs@iad1-shared-b8-17.dreamhost.com


