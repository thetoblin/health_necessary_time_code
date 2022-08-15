import matplotlib
import seaborn
import pandas
from health_necessary_time_code.minwage_estimate import (
								 minwage_nectime_weekly_per_capita_df,
								 minwage_nectime_weekly_perworkingageperson_df,
								 )
from health_necessary_time_code.derived_data import workhours_weekly_avg_df
from health_necessary_time_code.minwage_settings import year_to_plot, location_name, time_name
import health_necessary_time_code.auxiliary as aux


def plot(show=True):
	assert type(show) is bool

	# define legend-texts (visible in plot)
	minwage_nectime_percapita_legendtext				= 'Time per capita required\nto provide population with\nminimum-wage worth of\ngoods and services'
	avg_workhours_legendtext							= 'Average working hours'
	minwage_nectime_perworkingageperson_legendtext		= 'Time per working-age person\nrequired to provide population\nwith minimum-wage worth of\ngoods and services'


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


	# plot
	seaborn.set_theme(style="whitegrid")
	ax = seaborn.catplot( y='value', x=location_name, hue=time_name, data=plot_df,  ci="sd", palette="dark", alpha=.8, kind="bar", height=8 )
	#matplotlib.pyplot.subplots_adjust( hspace=1.8 )
	matplotlib.pyplot.xticks(rotation = 90)
	matplotlib.pyplot.ylabel("Hours per week")
	matplotlib.pyplot.savefig('minwage_estimate_plot.png', bbox_inches='tight')

	# remove the legend title
	ax.legend.set_title('')

	if show:
		matplotlib.pyplot.show()

	return
