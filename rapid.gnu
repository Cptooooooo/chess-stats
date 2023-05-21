# Gnuplot script for plotting rapid performance data vs hour of the 
# day using histograms.

# Customize the axes
set title "Performance data for rapid games" font ",14"
set xtics 1,1,24
set yrange [-30:38]
set xlabel "Hour of the Day" font ",12"
set ylabel "Avg. rating gain per game" font ",12"
set border lw 2
set grid 
set key box width 2 font ",12" at 23.5,36.5
set terminal GNUTERM size 1200,800

# Set histogram
set style data histogram
set style histogram clustered gap 2
set style fill solid border -1
set boxwidth 0.9 relative

# Plot the blitz and bullet data
plot "perf.dat" index 2 using 2:xtic(1) title "rapid", \
     0 lc -1 notitle
