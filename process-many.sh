#!/bin/bash

# ---- colors ---- #
 RESET="\x1B[0m"
 RED="\x1B[0;31m"
 GRN="\x1B[0;32m"
 YEL="\x1B[0;33m"
 BLU="\x1B[0;34m"
 MAG="\x1B[0;35m"
 CYN="\x1B[0;36m"
 WHT="\x1B[0;37m"
 B_RED="\x1B[1;31m"
 B_GRN="\x1B[1;32m"
 B_YEL="\x1B[1;33m"
 B_BLU="\x1B[1;34m"
 B_MAG="\x1B[1;35m"
 B_CYN="\x1B[1;36m"
 B_WHT="\x1B[1;37m"
# ---------------- #

if [[ -z $1 ]] ; then
	printf " ${RED}usage: $0 <folder con los archivos de JSON> {RESET}\n"
	exit 2
fi

# - La forma que este script functiona es que junta todo los files .json en el
# - folder y los pasa por mi programa, poniendo el resultado en el mismo folder.
# - Las nombres de los nuevos teneran el mismo nombre pero '.yaml' en ves de '.json'

src=$1; dest=$2

if [ ! -d $src ]; then
	printf " ${RED}'$src' no existe!! ${RESET}\n"
	exit 1
fi

python3 src/main.py $src $dest

