
# import packages
import pandas
import numpy

import seaborn
import matplotlib.pyplot as plt
import itertools

import os


#########################################
########   DATA PROCESSING   ############
#########################################

def dataframe_keep_rows_with_columnvalues( df, colval_to_keep ):
	# takes a dataframe and only keeps the values that are specified by the user
	# input:
	#			df 					: the pandas.DataFrame to process
	#			colval_to_keep		: dictionary of the format {column_name: [list_of_values_to_keep]} that specifies the column values that should not be discarded
	# output:
	#			df				: pandas.DataFrame with only specified values remaining
	assert type(df) is pandas.DataFrame
	assert type(colval_to_keep) is dict
	for col in colval_to_keep:
		assert type(colval_to_keep[col]) is list

	for col in colval_to_keep:
		val = colval_to_keep[col]
		df = df[ df[col].isin(val) ]

	return df

def dataframe_remove_rows_with_NaN_values( df ):
	is_NaN = df.isnull()
	row_has_NaN = is_NaN.any(axis=1)
	rows_with_NaN = df[row_has_NaN]
	df = df.drop( index=rows_with_NaN.index )
	return df

def dataframe_with_these_rows( df, rows ):
	# takes a dataframe and removes all except the specified rows
	# input:
	#			df 				: the pandas.DataFrame to process
	#			rows			: list specifying the rows to keep
	# output:
	#			df				: pandas.DataFrame with only specified rows remaining
	assert type(df) is pandas.DataFrame
	assert type(rows) is list
	allrows = list(df.index)
	rows_to_remove = [x for x in allrows if x not in rows]
	df = df.drop( index=rows_to_remove )
	return df


def dataframe_with_these_columns( df, columns ):
	# takes a dataframe and removes all except the specified columns
	# input:
	#			df 				: the pandas.DataFrame to process
	#			columns			: list specifying the columns to keep
	# output:
	#			df				: pandas.DataFrame with only specified columns remaining
	assert type(df) is pandas.DataFrame
	assert type(columns) is list
	allcolumns = list(df.columns)
	columns_to_remove = [x for x in allcolumns if x not in columns]
	df = df.drop( columns=columns_to_remove )
	return df


def process_narrow_to_wide( input, colval_to_keep, cols_to_keep, location_name, time_name, value_name ):
	# takes a dataframe (or a filepath to a csv datafile), processes it, and puts it on desired format
	# input:
	#			input 				: string specifying the filepath (including filetype, e.g. '<name>.csv')
	#			colval_to_keep		: dictionary of the format {column_name: [values_to_keep]} that specifies the column values (as specified in the original datafile) that should not be discarded
	#			cols_to_keep		: dictionary {column_name: new_column_name} that specifies the columns that should not be discarded (in the datafile), mapped to the names that the columns should have in the output dataframe
	#			input_format		: string specifying whether the input data is in narrow or long format. See https://en.wikipedia.org/wiki/Wide_and_narrow_data
	#			location_name		: the string value that the input dataframe should have for the column with the countrycodes
	#			time_name			: the string value that the input dataframe should have for the column with the time entries (years)
	#			value_name			: the string value that the input dataframe should have for the column with the data values
	#
	import pandas
	assert type(colval_to_keep) is dict
	for key in colval_to_keep:
		assert type( colval_to_keep[key]) is list
	assert type(cols_to_keep) is dict
	for key in cols_to_keep:
		assert not type(cols_to_keep[key]) is list
		assert not type(cols_to_keep[key]) is tuple
	assert type(location_name) is str
	assert type(time_name) is str
	assert type(value_name) is str

	# determine input-type and read input from file if necessary
	if type(input) is str:
		df = pandas.read_csv( input )
	elif type(input) is pandas.DataFrame:
		df = input
	else:
		raise ValueError("unexpected value of 'input': must be str or pandas.Dataframe")

	# keep only specified values
	df = dataframe_keep_rows_with_columnvalues( df, colval_to_keep)

	# keep only specified columns
	cols_to_keep_list = list(cols_to_keep.keys())
	df = dataframe_with_these_columns( df, cols_to_keep_list )

	# rename columns to specified names
	df = df.rename(cols_to_keep, axis='columns')

	# transform to wide format
	df = pandas.pivot( df, index=location_name, columns=time_name, values=value_name )

	return df


######################################################
#####		METHODS TO CALCULATE METADATA		######
######################################################

# METHODS
def ppp_median_posttax_income_from_current_prices_and_PPP_data( median_annual_income_current_prices, ppp_conversion, countries ):
	# input:
	#		median_annual_income_current_prices: 			dictionary[country][year] = median annual income_at_current_prices_and_national_currency (such as Euro) unit: [national_currency]
	#		ppp_conversion							dictionary[country][year] = national_currency_per_USD
	out = {}

	for country in countries:
		out[country] = {}
		for year in median_annual_income_current_prices[country]:
			med_incom_curr_prices = median_annual_income_current_prices[country][year]
			ppp_conv = ppp_conversion[country][year]
			median_incom_ppp = med_incom_curr_prices / ppp_conv

			out[country][year] = median_incom_ppp
	return out


def get_pre_tax_income( incomes, tax_rates, countries ):
	pre_tax_income = {}

	for country in countries:
		pre_tax_income[country] = {}
		for year in incomes[country]:
			income = incomes[country][year]
			tax_rate = tax_rates[country][year]

			pre_tax_income[country][year] = income + income*tax_rate				# since tax rates are given in terms of decimal values like so 0.xx, then: 10*1.2=12 => 10(1 + 0.2)=12 => 10+10*0.2=12
	return pre_tax_income



def USD_fromCPI_toCPI( val_from, CPI_from, CPI_to ):
	return val_from* ( CPI_to / CPI_from )


def convert_USD_from_year_to_year_usingCPI( USD_valued_data, from_year, to_year, CPI_avg_data, countries ):
	# input:
	#				USD_valued_data				: dict[country][year] = USD_value_in_YYYYUSD. For example data for several years but all in 2019-USD
	#				from_year					: str representing the USD-year that the data is in
	#				to_year						: str representing the USD-year that the output should be in
	#				CPI_data					: dict[year] = USD_CPI_for_that_year

	# ON USING CPI TO TRANSLATE 2019 DOLLARS TO 2017 DOLLARS: https://www.usinflationcalculator.com/frequently-asked-questions-faqs/#HowInflationCalculatorWorks
	#Example 1:
	#Let’s say you spent $20 to buy some goods or services today. How much money would you have needed in 1980 to buy the same amount of goods or services?
	#The average CPI for 1980 = 82.4
	#The average CPI for 2011 = 224.9
	#The following formula is then used to calculate the price:
	#2011 Price x (1980 CPI / 2011 CPI) = 1980 Price
	#Using the actual numbers:
	#$20.00 x (82.4 /224.9) = $7.33

	CPI_from = CPI_avg_data[ from_year]							# CPI for the year that we are converting FROM
	CPI_to = CPI_avg_data[ to_year ]							# CPI for the year that we are converting TO

	out = {}

	for country in countries:
		out[country] = {}
		for year in USD_valued_data[country]:


			val_from = USD_valued_data[country][year]						# the USD value for the year that we are converting FROM
			val_to = USD_fromCPI_toCPI( val_from, CPI_from, CPI_to )
			out[country][year] = val_to

	return out



############################################
######		PLOTTING FUNCTIONS      ########
############################################


def get_table_dataframe( ):
	# transforms a data dictionary on format dict[country_code][year]=value into a plottable data format
	# input:
	#			data_dict			: dict[country_code][year]=value
	# output:
	# 			out = { column_i_name: [ data_value_at_ij ] } for column index i and row index j. Hence out[column_name][j] is the value of the data at the given column on row j
	out = {}

#	columns = [ 'Country code', 'Req necessary time per worker', 'Avg work time', 'Req necessary time per capita', 'Work time from median income']

	out['Country'] 								= ['USA']
	out['Req necessary\ntime per capita'] 		= [ objectively_required_necessary_time_per_capita_USA2019 ]
	out['Req necessary\ntime per worker'] 		= [ objectively_required_necessary_time_per_worker_USA2019 ]
	out['Subjectively required\ntime (median)'] = [ subjectively_required_time_median_USA2019_using_medincome_for_USA2017 ]
	out['Average work week'] 					= [ weekly_hours_worked_avg_USA2019 ]

	out_df = pandas.DataFrame.from_dict(out)
	return out_df
