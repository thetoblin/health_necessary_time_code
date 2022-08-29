# import packages
import pandas
from health_necessary_time_code.settings import weeks_per_year
from health_necessary_time_code.livwage_input import population_USstates_df
from health_necessary_time_code.derived_data import (
														liv_grossincome_USstates_annual_df,
														workagepop_df,
														productivity_df,
														)

livwage_goods_and_services_USstates_annual_totalpop		= liv_grossincome_USstates_annual_df * population_USstates_df    # the annual living-income for the entire US population in 2019-USD

livwage_goods_and_services_US_annual_totpop_df			= pandas.DataFrame(livwage_goods_and_services_USstates_annual_totalpop.sum()).transpose()
livwage_goods_and_services_US_annual_totpop_df			= livwage_goods_and_services_US_annual_totpop_df.rename( {0:'USA'})		# rename the index 0 (of the only row in the dataframe) to 'USA'


# divide the value with the productivity for USA to get the total time required to produce it. Since not all years exist in both dataframes
livwage_nectime_annual_US_totalpop_df					= livwage_goods_and_services_US_annual_totpop_df / productivity_df.loc['USA']

livwage_nectime_weekly_percapita_USA_df					= livwage_nectime_annual_US_totalpop_df / ( population_USstates_df.sum() * weeks_per_year )

livwage_nectime_weekly_perworkingageperson_USA_df		= livwage_nectime_annual_US_totalpop_df / ( workagepop_df.loc['USA'] * weeks_per_year )

livwage_weeklycost_percapita_USA_df						= livwage_goods_and_services_US_annual_totpop_df / ( population_USstates_df.sum() * weeks_per_year)

livwage_annualcost_percapita_USA_df						= livwage_goods_and_services_US_annual_totpop_df / population_USstates_df.sum()
