
import pandas
import numpy
import seaborn
import matplotlib.pyplot

from minwage_estimate import phybehene_time_weekly_per_worker_df
from derived_data import workhours_weekly_avg_df
from minwage_settings import year_to_plot
import auxiliary as aux

############################
# PLOT DATA
############################

# Setup plot dataframe by combining the hene-time and phybehene-time data
phybehene_plot_df 	= pandas.DataFrame( phybehene_time_weekly_per_worker_df[year_to_plot] )
phybehene_plot_df	= phybehene_plot_df.rename( columns={year_to_plot: 'Phybehene time'} )

hene_plot_df 		= pandas.DataFrame( workhours_weekly_avg_df[year_to_plot] )
hene_plot_df		= hene_plot_df.rename( columns={year_to_plot: 'Hene time'} )

plot_df 			= phybehene_plot_df.join(hene_plot_df)
plot_df 			= aux.dataframe_remove_rows_with_NaN_values( plot_df )

# Specify markers to use
#markers = ['o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd', '|', '_', '$\Omega$', '$\Omega$', '$\Omega$', '$\Omega$', '$\Omega$', '$\Omega$']
#markers = ['s', 'v', '^', '<', '>', 'o', 'X', 'P', 'p', 'd', 'D', '*']
#from matplotlib.lines import Line2D
#markers = list( Line2D.filled_markers )
#markers += ['$'+x+'$' for x in ['£','\$','\%','\clubsuit','\diamondsuit','\spadesuit','\heartsuit','\sigma','😍" />', '\sigma', '\Omega', '\star', '\\bullet']]

# Create plot
seaborn.set(style="darkgrid")
matplotlib.pyplot.figure(figsize=(10,10))
ax = seaborn.scatterplot( x='Phybehene time', y='Hene time', hue='Country', data = plot_df, s=140) #, palette='gray' )
ax.set(ylabel='Average workweek [hours/week]')
ax.set(xlabel='Time necessary per worker to provide population with\nminimum-income worth of goods and service [hours/week]')
ax.legend(loc='lower right',  ncol=3, fancybox=True, shadow=True)

# Establish title and subtitle
#matplotlib.pyplot.subplots_adjust(top=0.85, bottom=0.09)
#matplotlib.pyplot.title('Freedom of time map (based on average work week)', fontsize=16, weight='bold', pad=60.0)
#matplotlib.pyplot.suptitle('Comparing the average work week with the time per worker that\nis necessary to provide the population with minimum-income worth of goods and services',
#	          fontsize=8, alpha=0.75, color='grey', x=0.15, y=0.915, ha='left')

# Standardize axis ranges
plot_xy_start = 0.0
plot_xy_stop = 40.0
plot_xy_delta = 0.5
ax.set(xlim=(plot_xy_start,plot_xy_stop),ylim=(plot_xy_start,plot_xy_stop))

# Setup equilibrium line
xy_line = list( numpy.arange( plot_xy_start, plot_xy_stop+plot_xy_delta, plot_xy_delta ) )					# list with float values from plot_xy_start to plot_xy_stop
equilibrium_line_xs = list(xy_line)
equilibrium_line_ys = list(xy_line)
matplotlib.pyplot.plot( equilibrium_line_xs, equilibrium_line_ys, color='black')

matplotlib.pyplot.savefig('minwage_scatterplot.png', bbox_inches='tight')
matplotlib.pyplot.show()
