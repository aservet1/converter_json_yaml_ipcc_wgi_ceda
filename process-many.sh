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

if [[ -z $1 ]] || [[ -z $2 ]] ; then
	printf " ${RED}usage: $0 <folder con los archivos de JSON> <folder que va a tener los resultados de YAML>${RESET}\n"
	exit 2
fi

# - La forma que este script functiona es que junta todo los files .json en el
# - primer folder y los pasa por mi programa, poniendo  el resultado en el segundo
# - folder. Si no existe el segundo folder, lo crea

src=$1; dest=$2

if [ ! -d $src ]; then
	printf " ${RED}'$src' no existe!! ${RESET}\n"
	exit 1
fi

mkdir -p $dest
printf "${GRN}empezando a procesar files en '$src'${RESET}\n"
for file in $(find $src | grep '\.json' | sort); do
	printf "${BLU} >> procesando $file...${RESET}\n"

	outfile="$dest/${file/$src/}"; outfile=${outfile/.json/\/metadata.yml}
	outdir=${outfile/\metadata.yml/}; mkdir -p $outdir

	python3 src/main.py $file $outfile
done
printf "${GRN}resultados escrito a folder '$dest'${RESET}\n"

