# Gnuplot script for plotting rapid performance data vs hour of the
# day with lines.
# Run using: gnuplot> load rapid_wLines.gnu

# Customize the axes 
set title "Performance data for rapid games"
set xtic 1,1,24
set xrange [0:25]
set yrange [-36:36]
set xlabel "Hour of the Day" font ",12"
set ylabel "Avg. rating gain per game" font ",12"
set border 3 lw 2
set tics nomirror
set grid
set key box width 2 font ",12"
set terminal GNUTERM size 800,800

# Plot the blitz and bullet data
plot "perf.dat" index 2 title "rapid" lw 2 w l, \
     0 lc -1 notitle
