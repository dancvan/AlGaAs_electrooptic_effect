#!/bin/bash
a=0
for i in *.TXT; do 
  new=$(printf "%02d.TXT" "$a")
  mv -i -- "$i" "$new"
  let a=a+1
done
