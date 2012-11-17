#!/usr/bin/gnuplot
set title ""
set term png

set xlabel "Cache size"
set ylabel "Hit ratio [%]"
#unset key
set output "plot.png" 

set style data linespoints

plot "results/OPT.res" using 2:3  title "OPT", \
     "results/LRU.res" using 2:3  title "LRU", \
     "results/LFU.res" using 2:3  title "LFU", \
     "results/ARC.res" using 2:3  title "ARC"
