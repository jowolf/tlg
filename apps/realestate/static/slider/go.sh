res=200;for i in *.jpg; do convert "$i" -resize $res $res/"$i"; done
