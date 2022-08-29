
# import packages
import pandas
import numpy

from health_necessary_time_code.settings import weeks_per_year
from health_necessary_time_code.derived_data import (
												workagepop_df,
												productivity_df,
												)
from health_necessary_time_code.minwage_input import (
												population,
												min_grossincome_annual,
				  								)

minwage_goods_and_services_annual_totalpop_df 		 	= min_grossincome_annual.df  * population.df					# the total value of providing everyone in the population with a minimum-wage worth of goods and services

# Physically and behaviorally health-necessary time
minwage_nectime_annual_total_df				 			= minwage_goods_and_services_annual_totalpop_df / productivity_df
minwage_nectime_annual_per_capita_df		 			= minwage_nectime_annual_total_df / population.df
minwage_nectime_annual_perworkingageperson_df 			= minwage_nectime_annual_total_df / workagepop_df

minwage_nectime_weekly_per_capita_df					= minwage_nectime_annual_per_capita_df / weeks_per_year
minwage_nectime_weekly_perworkingageperson_df 			= minwage_nectime_annual_perworkingageperson_df / weeks_per_year
