# Gnuplot script for plotting blitz and bullet performance data vs hour of the
# day using lines.
# Run using: gnuplot> load blitz_bullet_wLines.gnu

# Customize the axes 
set title "Performance data for blitz and bullet games"
set xtic 1,1,24
set xrange [0:25]
set yrange [-3:3]
set xlabel "Hour of the Day" font ",12"
set ylabel "Avg. rating gain per game" font ",12"
set border 3 lw 2
set tics nomirror
set grid
set key box width 2 font ",12"
set terminal GNUTERM size 800,800

# Plot the blitz and bullet data
plot "perf.dat" index 0 title "blitz" lw 2 w l, \
     "perf.dat" index 1 title "bullet" lw 2 w l, \
     0 lc -1 notitle
