
# import packages
import pandas
import numpy
import health_necessary_time_code.auxiliary as aux
from health_necessary_time_code.minwage_settings import location_name, time_name, value_name, datapath


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
############   DATA OJBs   ##############
#########################################

class UsageError(Exception):
	pass

class Data:
	def __init__(self, df, description, source=""):
		assert type(df) is pandas.DataFrame
		assert type(description) is str
		assert type(source) is str
		self._df 			= df
		self.description	= description
		self.source			= source
		self.update_array()

	def update_array(self):
		self._array 	= self._df.to_numpy()

	@property
	def df(self):
		return self._df

	# make sure that numpy array and dataframe are always aligned by not allowing setting array independently
	@df.setter
	def df(self, newdf):
		self._df 		= newdf
		self.update_array()

	@property
	def array(self):
		return self._array

	@array.setter
	def array(self, newarray):
		raise UsageError("the array cannot be updated independently, but must instead be updated by updating the dataframe")


#########################################
########   DATA PROCESSING   ############
#########################################

# Data imports
database_dfs = {}
PennWorldTable_nationaldata_filepath 			= datapath + 'Groningen_Growth_and_Development_Centre/Penn_World_Tables/pwt100-na-data.xlsx'
database_dfs['Penn World Table 10.0 NA data']	= pandas.read_excel( PennWorldTable_nationaldata_filepath, sheet_name='Data' )			# Penn World Table National Account data


########   GET DATA ON DESIRED FORMAT   ########
# population
# requirements on variable
#		- unit should be in 'number of individuals'
dummy_df					= pandas.DataFrame( database_dfs['Penn World Table 10.0 NA data'] )
columns_to_keep 			= { 'countrycode': location_name, 'year': time_name, 'pop': value_name}
columnvalues_to_keep 		= { }
population_df				= aux.process_narrow_to_wide( dummy_df, columnvalues_to_keep, columns_to_keep, location_name, time_name, value_name )
population_df				= population_df * (10**6) # since the input data is in units of 'millions of individuals', and the desired input-unit is in 'number of individuals'
population					= Data( population_df, "Population in units of 'number of individuals'" )

# laborforce
# requirements on variable
#		- unit should be in 'number of individuals'
dummy_df					= pandas.DataFrame( database_dfs['Penn World Table 10.0 NA data'] )
columns_to_keep 			= { 'countrycode': location_name, 'year': time_name, 'emp': value_name}
columnvalues_to_keep 		= { }
laborforce_df				= aux.process_narrow_to_wide( dummy_df, columnvalues_to_keep, columns_to_keep, location_name, time_name, value_name )
laborforce_df 				= laborforce_df * (10**6) # since the input data is in units of 'millions of individuals', and the desired input-unit is in 'number of individuals'
laborforce 					= Data( laborforce_df, "Number of persons engaged (in units of 'numbers of individuals')" )

# Working hours
# requirements on variable
#		- should represent average annual hours actually worked per working person
#		- unit should be in 'hours'
dummy_df					= pandas.DataFrame( database_dfs['Penn World Table 10.0 NA data'] )
columns_to_keep 			= { 'countrycode': location_name, 'year': time_name, 'avh': value_name}
columnvalues_to_keep 		= { }
workhours_annual_avg_df		= aux.process_narrow_to_wide( dummy_df, columnvalues_to_keep, columns_to_keep, location_name, time_name, value_name )
workhours_annual_avg		= Data( workhours_annual_avg_df, "Average annual hours worked per person engaged" )

# GDP at current national prices
# requirements on variable
#		- should represent GDP in units of the national currencies at current prices
dummy_df					= pandas.DataFrame( database_dfs['Penn World Table 10.0 NA data'] )
columns_to_keep 			= { 'countrycode': location_name, 'year': time_name, 'v_gdp': value_name}
columnvalues_to_keep 		= { }
gdp_current_natprices_df	= aux.process_narrow_to_wide( dummy_df, columnvalues_to_keep, columns_to_keep, location_name, time_name, value_name )
gdp_current_natprices_df	= gdp_current_natprices_df * (10**6) # since the input data is in units of 'millions of national currencies', and the desired input-unit is in 'national currencies'
gdp_current_natprices		= Data( gdp_current_natprices_df, "GDP at current national prices (in units of the national currencies)" )

######################################

# Working-age population
# requirements on variable
#		- should represent the percent of the working-age population
workagepop_filepath			= datapath + 'working_age_population/workingage_pop_OECD.csv'
columnvalues_to_keep 		= { }
columns_to_keep 			= { 'LOCATION': location_name, 'TIME': time_name, 'Value': value_name}
workagepop_percent_df		= aux.process_narrow_to_wide( workagepop_filepath, columnvalues_to_keep, columns_to_keep, location_name, time_name, value_name )
workagepop_percent			= Data( workagepop_percent_df, "The working age population (defined as those aged 15 to 64) as percent of total population" )

# Minimum wage
# requirements on variable
#		- should represent the statutory minimum wage in units of national currencies at current prices
minimum_wage_filepath   	= datapath + 'minimum_wage_data/minimum_wage_national_currencies.csv'
columnvalues_to_keep 		= {'Pay period': ['Annual'] }
columns_to_keep 			= { 'COUNTRY': location_name, 'TIME': time_name, 'Value': value_name}
min_grossincome_annual_df	= aux.process_narrow_to_wide( minimum_wage_filepath, columnvalues_to_keep, columns_to_keep, location_name, time_name, value_name )
min_grossincome_annual 		= Data( min_grossincome_annual_df, "Minimum annual income in national currencies at current prices" )


########   GET COMMON DATA AND ESTABLISH SAME SORTING   ########
# 	- Need to make sure that all rows and columns represent the same data (same countries and same years)
#		- Need to find the common countries
#		- Need to find common years
#		- Need to establish data to be only for common years and countries
#		- Need to make sure that the data is sorted the same way, so that apples are compared to apples

# Find common rows and columns

dfs 				= {	'workhours_annual_avg': workhours_annual_avg.df,
						'population': population.df,
						'laborforce': laborforce.df,
						'min_grossincome_annual':min_grossincome_annual.df,
						'workagepop_percent': workagepop_percent.df,
						'gdp_current_natprices': gdp_current_natprices.df,
						}
common_columns 		= population.df.columns			# starting here
common_rows 		= population.df.index
for key in dfs:
	df = dfs[key]
	common_columns 	= common_columns.intersection( df.columns )
	common_rows 	= common_rows.intersection( df.index )

# Discard all except the common rows and columns
for key in dfs:
	df 				= dfs[key]
	df 				= aux.dataframe_with_these_columns( df, list(common_columns ))
	df 				= aux.dataframe_with_these_rows( df, list(common_rows ))
	dfs[key] 		= df.sort_index()

# make sure that the dataframes have the data sorted and organized the same way
for key1 in dfs:
	for key2 in dfs:
		assert list( dfs[key1].columns ) == list( dfs[key2].columns )
		assert list( dfs[key1].index)    == list( dfs[key2].index )

# reassign variable names to dataframes with same rows, columns, and data sorting
population.df 						= dfs['population']
laborforce.df 						= dfs['laborforce']
min_grossincome_annual.df 			= dfs['min_grossincome_annual']
workhours_annual_avg.df 			= dfs['workhours_annual_avg']
workagepop_percent.df 				= dfs['workagepop_percent']
gdp_current_natprices.df 			= dfs['gdp_current_natprices']
