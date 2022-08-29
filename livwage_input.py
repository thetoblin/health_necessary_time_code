
# import packages
import pandas
import numpy
import health_necessary_time_code.auxiliary as aux
from health_necessary_time_code.settings import location_name, time_name, value_name, datapath

#########################################
############   DATA FORMAT   ############
#########################################

# DATA FORMAT (CONVENTION)
# All data must be on the following format (where ... represent values).
#
#			2021	2022	2023	2024
# USA		 ...	 ...	 ...	 ...
# MEX		 ...	 ...	 ...	 ...
# SWE 		 ...	 ...	 ...	 ...
# NOR 		 ...	 ...	 ...	 ...
# DEN 		 ...	 ...	 ...	 ...
#
# The purpose of this module is to take data and process it to be in the correct format


#########################################
########   DATA PROCESSING   ############
#########################################

name_of_region_column			= 'Region'
time_name 						= 'Time'
value_name						= 'Value'

# US state population data
population_USstates_path		= datapath + 'US_census_bureau/nst-est2020.csv'
population_USstates_df			= pandas.read_csv( population_USstates_path )
new_column_names 				= {
										'STATE': 'STATE',
										'NAME': name_of_region_column,
										'POPESTIMATE2010': 2010,
										'POPESTIMATE2011': 2011,
										'POPESTIMATE2012': 2012,
										'POPESTIMATE2013': 2013,
										'POPESTIMATE2014': 2014,
										'POPESTIMATE2015': 2015,
										'POPESTIMATE2016': 2016,
										'POPESTIMATE2017': 2017,
										'POPESTIMATE2018': 2018,
										'POPESTIMATE2019': 2019,
										'POPESTIMATE2020': 2020,
										}

population_USstates_df			= population_USstates_df.rename(new_column_names, axis='columns')				# rename columns as specified by dictionary
columns_to_keep					= list(new_column_names.values())
population_USstates_df			= aux.dataframe_with_these_columns( population_USstates_df, columns_to_keep )	# keep only specified columns
population_USstates_df			= population_USstates_df.set_index(name_of_region_column)						# set dataframe index to state column
rows_to_remove					= ['Northeast Region', 'Midwest Region', 'South Region', 'West Region', 'Puerto Rico', 'United States']				# remove region values since they will not be used
population_USstates_df 			= population_USstates_df.drop( labels=rows_to_remove )
population_USstates_df			= population_USstates_df.sort_index()											# sort indices


# Living-wage data for the United States
livwage_USstates_path			= datapath + 'Livingwage_Calculator/livwage_USstates.csv'
livwage_USstates_hourly_df		= pandas.read_csv( livwage_USstates_path )
columnvalues_to_keep 			= { 'indicator': ['1 Adult'] }
columns_to_keep 				= { 'location': name_of_region_column, 'Date': time_name, 'Value': value_name}
livwage_USstates_hourly_df		= aux.process_narrow_to_wide( livwage_USstates_hourly_df, columnvalues_to_keep, columns_to_keep, name_of_region_column, time_name, value_name )


# keep only common rows and columns
dfs = {'population_USstates_df': population_USstates_df, 'livwage_USstates_hourly_df': livwage_USstates_hourly_df }
dfs = aux.get_dfs_with_common_rows_and_columns(dfs)

# reassign variables
population_USstates_df			= dfs['population_USstates_df']
livwage_USstates_hourly_df		= dfs['livwage_USstates_hourly_df']
