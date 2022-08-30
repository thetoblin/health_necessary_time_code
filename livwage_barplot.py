import matplotlib
import seaborn
import pandas
from health_necessary_time_code.livwage_estimate import (
								 livwage_nectime_weekly_percapita_USA_df,
								 livwage_nectime_weekly_perworkingageperson_USA_df,
								 livwage_annualcost_percapita_USA_df,					# to print in subtitle
								 )

from health_necessary_time_code.derived_data import workhours_weekly_avg_df
from health_necessary_time_code.settings import year_to_plot
import health_necessary_time_code.auxiliary as aux

# for adding logotype
from PIL import Image

livwage_annual_str = f'{round(int(livwage_annualcost_percapita_USA_df[year_to_plot])):,}'		# format so that the annual cost per capita has thousand delimiters, e.g. 20,000 instead of 20000

def plot(show=True):
	livwage_nectime_perworkingageperson_legendtext	= 'Time required\nper working-age\nperson'
	livwage_nectime_percapita_legendtext			= 'Time required\nper capita'
	avg_workhours_legendtext						= 'Average working\nhours'

	plot_dic	= {
			  'Country': ['USA']*3,
			  'Time type': [
			  			livwage_nectime_percapita_legendtext,
						livwage_nectime_perworkingageperson_legendtext,
					   	avg_workhours_legendtext ],
			  #'Time': ['Phybehene-percapita', 'Phybehene-perworker', 'Henetime-median', 'Avg workhours' ],
			  'value': [
			  			float(livwage_nectime_weekly_percapita_USA_df[year_to_plot]),
						float(livwage_nectime_weekly_perworkingageperson_USA_df[year_to_plot]),
						float(workhours_weekly_avg_df[year_to_plot]['USA']) ]
			  }

	plot_df = pandas.DataFrame( plot_dic )

	# plot
	matplotlib.pyplot.figure(figsize=(8,8))
	seaborn.set_theme(style="whitegrid")
	ax = seaborn.barplot(y='value', x='Country', hue='Time type', data=plot_df, ci="sd", palette="deep" )
	#ax = seaborn.catplot( y='value', x='Country', hue='Time type', data=plot_df,  ci="sd", palette="dark", alpha=.8, kind="bar", height=8 )

	# fix legend
	ax.get_legend().set_title(None)
	seaborn.move_legend(ax, "center right", bbox_to_anchor=(1.54, 0.5), fontsize=18, frameon=False)
	#matplotlib.pyplot.legend(frameon=False, fontsize=16)

	# fix axes labels and ticks
	matplotlib.pyplot.ylabel("Hours per week", fontsize=18)
	matplotlib.pyplot.xlabel("")
	matplotlib.pyplot.xticks(fontsize=18)
	matplotlib.pyplot.yticks(fontsize=18)

	###   set title, subtitle, and description   ###
	title_xpos		= -0.08
	title_ypos 		= 1.20

	subtitle_ypos 	= 1.04
	subtitle_xpos	= title_xpos

	descr_ypos		= -0.28
	descr_xpos		= title_xpos

	githublink_ypos	= descr_ypos - 0.05
	githublink_xpos	= title_xpos

	licence_text	= "MIT License"
	graph_version	= "Graph version 1.0"

	title_text 		= "Time required to provide population with living-wage worth of goods and\nservices (USA, "+str(year_to_plot)+")"
	subtitle_text	= "Comparing 1) the number of hours required (per capita and per working-age person (ages 15-64)) to provide\nevery individual in the United States with an annual living-wage worth of goods and services ($"+livwage_annual_str+" per\nyear) with the country's average productivity (GDP per hour), and 2) the country's average working hours.\nThe living wage annual income assumes that each individual has the needs of a single adult, neglecting\neconomies of scale in consumption that arise from e.g. sharing a household. For the year 2019."
	#"Comparing 1) the number of hours required (per capita and per working-age person (ages 15-64)) to provide\nevery individual in the United States with an annual living-wage worth of goods and services with the\ncountry's average productivity (GDP per hour), and 2) the country's average working hours. The living wage\nannual income assumes that each individual has the needs of a single adult, neglecting economies of scale\nin consumption that arise from e.g. sharing a household. For the year 2019."
	#"Comparing 1) the number of hours required (per capita and per working-age person (ages 15-64)) to provide\nevery individual in the United States with an annual living-wage worth of goods and services ($"+livwage_annual_str+" per year) with\nthe country's average productivity (GDP per hour), and 2) the country's average working hours. For the year "+str(year_to_plot)
	descr_text		= "Sources:\n     - Glasmeier, Amy K. “Living Wage Calculator.” Massachusetts Institute of Technology, 2022. livingwage.mit.edu 	(accessed 26 August 2022)\n     - US Census Bureau, Population Division. Dataset “National and State Population Estimates” in database “National Population Totals: 2010-2020”.\n       US Census Bureau, July 2021.\n       https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/national/totals/nst-est2020.csv (retrieved 24 August 2022).\n     - Robert C. Feenstra, Robert Inklaar. “Penn World Table 10.0.” Groningen Growth and Development Centre, 2021. https://doi.org/10.15141/S5Q94M.\n     - Feenstra, Robert C., Robert Inklaar, and Timmer Marcel P. “The Next Generation of the Penn World Table.” American Economic Review 105, no.\n       10 (October 1, 2015): 3150–82. https://doi.org/10.1257/aer.20130954."
	githublink_text	= licence_text + ". " + graph_version + ". Source code available at https://github.com/thetoblin/health_necessary_time"

	# title
	matplotlib.pyplot.title(
								title_text,
								y			= title_ypos,
								x 			= title_xpos,
								fontsize	= 16,
								loc			= 'left',
								fontweight	= 'bold',
								#style		= 'italic',
								#family		= 'serif'
								)
	# subtitle
	ax.text( x=subtitle_xpos, y=subtitle_ypos, s=subtitle_text, fontsize=11, ha='left', va='bottom', transform=ax.transAxes) #, family='serif' )#, weight='bold')

	# description
	ax.text( x=descr_xpos, y=descr_ypos, s=descr_text, fontsize=9, ha='left', va='bottom', transform=ax.transAxes) #, family='serif' )#, weight='bold')

	# githublink and license
	ax.text( x=githublink_xpos, y=githublink_ypos, s=githublink_text, fontsize=9, ha='left', va='bottom', transform=ax.transAxes) #, family='serif' )#, weight='bold')

	# remove top and right border of plot
	seaborn.despine(ax=ax)

	# add logotype
	figquality	= 300
	fig 		= matplotlib.pyplot.gcf()					# get current figure
	logo 		= Image.open('logo2.png')					# open logo image file
	figsize 	= fig.get_size_inches()*figquality #*fig.dpi # get the size of the pyplot figure in pixels
	logo_xpos	= figsize[0]*1.13							# set the logos xposition in pixels
	logo_ypos	= figsize[1]*1.06							# set the logos xposition in pixels
	fig.figimage( logo, xo=logo_xpos, yo=logo_ypos )		# place image in figure

	###################

	matplotlib.pyplot.savefig('livwage_barplot.png', bbox_inches='tight', dpi=figquality)

	if show:
		matplotlib.pyplot.show()

	return
