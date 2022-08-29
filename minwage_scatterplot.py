
import pandas
import numpy
import seaborn
import matplotlib.pyplot

# for adding logotype
from PIL import Image

from health_necessary_time_code.minwage_estimate import minwage_nectime_weekly_perworkingageperson_df
from health_necessary_time_code.derived_data import workhours_weekly_avg_df
from health_necessary_time_code.settings import year_to_plot
import health_necessary_time_code.auxiliary as aux


def plot(show=True):

    # Setup plot dataframe by combining the hene-time and phybehene-time data
    perworkingageperson_plot_df = pandas.DataFrame( minwage_nectime_weekly_perworkingageperson_df[year_to_plot] )
    perworkingageperson_plot_df = perworkingageperson_plot_df.rename( columns={year_to_plot: 'perworkingageperson'} )

    avgworkhours_plot_df 		= pandas.DataFrame( workhours_weekly_avg_df[year_to_plot] )
    avgworkhours_plot_df		= avgworkhours_plot_df.rename( columns={year_to_plot: 'avgworkhours'} )

    plot_df 			        = perworkingageperson_plot_df.join( avgworkhours_plot_df )
    plot_df 			        = aux.dataframe_remove_rows_with_NaN_values( plot_df )

    # Specify markers to use
    #markers = ['o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd', '|', '_', '$\Omega$', '$\Omega$', '$\Omega$', '$\Omega$', '$\Omega$', '$\Omega$']
    #markers = ['s', 'v', '^', '<', '>', 'o', 'X', 'P', 'p', 'd', 'D', '*']
    #from matplotlib.lines import Line2D
    #markers = list( Line2D.filled_markers )
    #markers += ['$'+x+'$' for x in ['£','\$','\%','\clubsuit','\diamondsuit','\spadesuit','\heartsuit','\sigma','😍" />', '\sigma', '\Omega', '\star', '\\bullet']]

    ###   plot   ###
    # set figure size
    matplotlib.pyplot.figure(figsize=(18,12))#(16,12))

    # set style
    seaborn.set(style="darkgrid")

    # set size of plot
    #seaborn.set( rc = {'figure.figsize':(2,8)} )

    # plot
    ax = seaborn.scatterplot( x='perworkingageperson', y='avgworkhours', hue='Country', data = plot_df, s=350)

    # fix legend
    ax.legend(loc='lower right',  ncol=3, fancybox=True, shadow=True)

    # fix axes
    matplotlib.pyplot.xlabel('Average working hours [hours/week]', fontsize=18)
    matplotlib.pyplot.xticks(fontsize=16)
    matplotlib.pyplot.ylabel('Time required per working-age person [hours/week]', fontsize=18)
    matplotlib.pyplot.yticks(fontsize=16)

	###   set title, subtitle, and description   ###
    title_ypos 		= 1.14
    subtitle_ypos 	= 1.04
    descr_ypos		= -0.20
    githublink_ypos	= descr_ypos-0.03        #-0.28

    licence_text	= "MIT License"
    graph_version	= "Graph version 1.0"

    title_text 		= "Time required to provide population with minimum-wage worth of goods and services (" + str(year_to_plot) + ")" + "\n(Scatter plot)"
    subtitle_text	= "Comparing 1) the number of hours required per working-age person (ages 15-64) to provide everyone in the population of a given country\nwith an annual minimum-wage worth of goods and services with the country's average productivity (GDP per hour), and 2) the country's\naverage working hours. For the year " + str(year_to_plot) + "."
    descr_text		= "Sources:\n     - Robert C. Feenstra, Robert Inklaar. “Penn World Table 10.0.” Groningen Growth and Development Centre, 2021. https://doi.org/10.15141/S5Q94M\n     - Feenstra, Robert C., Robert Inklaar, and Timmer Marcel P. “The Next Generation of the Penn World Table.” American Economic Review 105, no. 10 (October 1, 2015): 3150–82.\n        https://doi.org/10.1257/aer.20130954\n     - OECD. “Minimum Wages at Current Prices in NCU (Database),” December 15, 2021. https://stats.oecd.org/Index.aspx?DataSetCode=MW_CURP (accessed 18 April, 2022)\n     - OECD. “Working Age Population.” Accessed June 29, 2022. https://doi.org/10.1787/d339918b-en"
    githublink_text	= licence_text + ". " + graph_version + ". Source code available at https://github.com/thetoblin/health_necessary_time"

	# title
    matplotlib.pyplot.title(
							title_text,
							y			= title_ypos,
							fontsize	= 19,
							loc			= 'left',
							fontweight	= 'bold',
							#style		= 'italic',
							#family		= 'serif'
							)
	# subtitle
    ax.text(x=0.0, y=subtitle_ypos, s=subtitle_text, fontsize=13, ha='left', va='bottom', transform=ax.transAxes) #, family='serif' )#, weight='bold')

	# description
    ax.text(x=0.0, y=descr_ypos, s=descr_text, fontsize=11, ha='left', va='bottom', transform=ax.transAxes) #, family='serif' )#, weight='bold')

	# githublink and license
    ax.text(x=0.0, y=githublink_ypos, s=githublink_text, fontsize=11, ha='left', va='bottom', transform=ax.transAxes) #, family='serif' )#, weight='bold')


    # Standardize axis ranges
    plot_xy_start = 0.0
    plot_xy_stop = 45.0
    ax.set(xlim=(plot_xy_start,plot_xy_stop),ylim=(plot_xy_start,plot_xy_stop))


    # Setup equality line
    plot_xy_delta = plot_xy_stop
    xy_line = list( numpy.arange( plot_xy_start, plot_xy_stop+plot_xy_delta, plot_xy_delta ) )					# list with float values from plot_xy_start to plot_xy_stop
    equilibrium_line_xs = list(xy_line)
    equilibrium_line_ys = list(xy_line)
    matplotlib.pyplot.plot( equilibrium_line_xs, equilibrium_line_ys, color='black')


	# add logotype
    fig 		= matplotlib.pyplot.gcf()					# get current figure
    logo 		= Image.open('logo.png')					# open logo image file
    figsize 	= fig.get_size_inches()*fig.dpi				# get the size of the pyplot figure in pixels
    logo_xpos	= figsize[0]-logo.size[0]-305				# set the logos xposition in pixels
    logo_ypos	= figsize[1]-logo.size[1]+115				# set the logos xposition in pixels
    fig.figimage( logo, xo=logo_xpos, yo=logo_ypos )		# place image in figure

    matplotlib.pyplot.savefig('minwage_scatterplot.png', bbox_inches='tight')

    if show:
        matplotlib.pyplot.show()

    return
