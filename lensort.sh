cat $1 | awk '{ print length, $0 }' | sort -n $2 | cut -d" " -f2-
