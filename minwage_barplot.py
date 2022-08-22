
from health_necessary_time_code.minwage_estimate import (
								 minwage_nectime_weekly_per_capita_df,
								 minwage_nectime_weekly_perworkingageperson_df,
								 )
from health_necessary_time_code.derived_data import workhours_weekly_avg_df
from health_necessary_time_code.minwage_settings import year_to_plot, location_name, time_name
import health_necessary_time_code.auxiliary as aux

# for plotting
import matplotlib
import seaborn
import pandas

# for adding logotype
from PIL import Image



def plot(show=True):
	assert type(show) is bool

	# define legend-texts (visible in plot)
	minwage_nectime_percapita_legendtext				= 'Time required per\ncapita' 				#'Time per capita required\nto provide population with\nminimum-wage worth of\ngoods and services'
	minwage_nectime_perworkingageperson_legendtext		= 'Time required per\nworking-age person' 	#'Time per working-age person\nrequired to provide population\nwith minimum-wage worth of\ngoods and services'
	avg_workhours_legendtext							= 'Average working\nhours'



	# create new dataframes (so to not mess with the originals)
	years_to_plot 										= [year_to_plot]
	minwage_nectime_weekly_per_capita_plot_df 			= aux.dataframe_with_these_columns( minwage_nectime_weekly_per_capita_df, years_to_plot )
	minwage_nectime_weekly_per_workingageperson_plot_df	= aux.dataframe_with_these_columns( minwage_nectime_weekly_perworkingageperson_df, years_to_plot )
	workhours_weekly_avg_plot_df						= aux.dataframe_with_these_columns( workhours_weekly_avg_df, years_to_plot )


	# format them for plotting so that the countries are an actual datacolumn and not an index (which is needed for plotting)
	minwage_nectime_weekly_per_capita_plot_df			= minwage_nectime_weekly_per_capita_plot_df.reset_index( level=0 )
	minwage_nectime_weekly_per_workingageperson_plot_df	= minwage_nectime_weekly_per_workingageperson_plot_df.reset_index( level=0 )
	workhours_weekly_avg_plot_df						= workhours_weekly_avg_plot_df.reset_index( level=0 )


	# rename year-to-plot column to what the dataframe represents (otherwise it will be confusing when the dataframes are merged - since we will not know what the columns represent)
	minwage_nectime_weekly_per_capita_plot_df		  	= minwage_nectime_weekly_per_capita_plot_df.rename( 		  columns={ year_to_plot: minwage_nectime_percapita_legendtext } )
	minwage_nectime_weekly_per_workingageperson_plot_df	= minwage_nectime_weekly_per_workingageperson_plot_df.rename(columns={ year_to_plot: minwage_nectime_perworkingageperson_legendtext } )
	workhours_weekly_avg_plot_df					  	= workhours_weekly_avg_plot_df.rename(					  columns={ year_to_plot: avg_workhours_legendtext} )


	# merge into new dataframe
	# note that the order of appending the legend texts to data_to_plot determines the order of the columns in the plot
	plot_df = workhours_weekly_avg_plot_df
	data_to_plot = []
	plot_df = pandas.merge( plot_df, minwage_nectime_weekly_per_capita_plot_df, on=location_name )
	data_to_plot.append(minwage_nectime_percapita_legendtext)
	plot_df = pandas.merge( plot_df, minwage_nectime_weekly_per_workingageperson_plot_df, on=location_name )
	data_to_plot.append(minwage_nectime_perworkingageperson_legendtext)
	data_to_plot.append(avg_workhours_legendtext)


	# transform from wide to long format
	plot_df = pandas.melt( plot_df, id_vars=location_name, value_vars=data_to_plot)


	# remove incomplete data (where the original data has NaN instead of real values)
	#plot_df = aux.dataframe_remove_rows_with_NaN_values( plot_df )


	###   plot   ###
	# set figure size
	matplotlib.pyplot.figure(figsize=(18,9))

	seaborn.set_theme(style="whitegrid")
	#seaborn.set_theme(style="darkgrid")

	#ax = seaborn.catplot(y='value', x=location_name, hue=time_name, data=plot_df,  ci="sd", palette="deep", alpha=1.0, kind="bar", height=plot_height, aspect=plot_width/plot_height )
	ax = seaborn.barplot(y='value', x=location_name, hue=time_name, data=plot_df, ci="sd", palette="deep" )

	# fix legend
	matplotlib.pyplot.legend(frameon=False)
	seaborn.move_legend(ax, "center right", bbox_to_anchor=(1.175, 0.5))

	# fix ticks and lables
	matplotlib.pyplot.xlabel(location_name, fontsize=14)
	matplotlib.pyplot.xticks(rotation = 90)
	matplotlib.pyplot.ylabel("Hours per week", fontsize=14)

	###   set title, subtitle, and description   ###
	title_ypos 		= 1.14
	subtitle_ypos 	= 1.04
	descr_ypos		= -0.28
	githublink_ypos	= -0.34

	licence_text	= "MIT License"
	graph_version	= "Graph version 1.0"

	title_text 		= "Time required to provide population with minimum-wage worth of goods and services (" + str(year_to_plot) + ")"
	subtitle_text	= "Comparing 1) the number of hours required (per capita and per person in the working-age population (ages 15-64)) to provide everyone in the population\nof a given country with an annual minimum-wage worth of goods and services with the country's average productivity (GDP per hour), and 2) the country's\naverage working hours. For the year " + str(year_to_plot) + "."
	descr_text		= "Sources:\n     - Robert C. Feenstra, Robert Inklaar. “Penn World Table 10.0.” Groningen Growth and Development Centre, 2021. https://doi.org/10.15141/S5Q94M\n     - Feenstra, Robert C., Robert Inklaar, and Timmer Marcel P. “The Next Generation of the Penn World Table.” American Economic Review 105, no. 10 (October 1, 2015): 3150–82.\n       https://doi.org/10.1257/aer.20130954\n     - OECD. “Minimum Wages at Current Prices in NCU (Database),” December 15, 2021. https://stats.oecd.org/Index.aspx?DataSetCode=MW_CURP (accessed 18 April, 2022)\n     - OECD. “Working Age Population.” Accessed June 29, 2022. https://doi.org/10.1787/d339918b-en"
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

	# remove top and right border of plot
	seaborn.despine(ax=ax)

	# add logotype
	# fig 		= matplotlib.pyplot.gcf()					# get current figure
	# #a 			= fig.add_subplot(111, frameon=False)
	# logo 		= matplotlib.pyplot.imread( 'logo.png' )	# read image
	# logoaxes	= fig.add_axes(								# add new axes (that will be used to scale and position the image)
	# 							ax.get_position(),
	# 							label='image',
	# 							xticks=[], yticks=[],		#remove ticks
	# 							)
	# logoaxes.set_xlim()
	fig 		= matplotlib.pyplot.gcf()					# get current figure
	logo 		= Image.open('logo.png')					# open logo image file
	figsize 	= fig.get_size_inches()*fig.dpi				# get the size of the pyplot figure in pixels

	logo_xpos	= figsize[0]-logo.size[0] - 120				# set the logos xposition in pixels
	logo_ypos	= figsize[1]-logo.size[1] + 200				# set the logos xposition in pixels
	fig.figimage( logo, xo=logo_xpos, yo=logo_ypos )		# place image in figure

	#save the plot to file
	matplotlib.pyplot.savefig('minwage_barplot.png', bbox_inches='tight')

	if show:
		matplotlib.pyplot.show()

	return
