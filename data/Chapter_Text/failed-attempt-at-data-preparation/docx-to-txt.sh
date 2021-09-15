#!/bin/bash
for d in $(ls Chapter*.docx)
do
	echo ' )) 'starting $d
	pandoc $d -o ${d/.docx/.txt}
	echo ' (( 'done with $d
done
