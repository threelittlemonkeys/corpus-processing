awk -v OFS='\t' '{ print length, $0 }' | sort -n -s
