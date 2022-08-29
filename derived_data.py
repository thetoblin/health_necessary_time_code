
#############################################
#############     IMPORTS     ###############
#############################################
import pandas
from health_necessary_time_code.minwage_input import   (
                                            workhours_annual_avg,
                                            workagepop_percent,
                                            population,
                                            gdp_current_natprices,
                                            laborforce,
                                            )
from health_necessary_time_code.settings import weeks_per_year, workhours_per_week
from health_necessary_time_code.livwage_input       import livwage_USstates_hourly_df


#####################################################
#############     DATA PROCESSING     ###############
#####################################################


# Working hours
workhours_weekly_avg_df                         = workhours_annual_avg.df / weeks_per_year

# Working-age population (in units of 'number of individuals')
workagepop_df                                   = (workagepop_percent.df / 100) * population.df

# Productivity (GDP per hour worked in units of 'national currencies at current prices per hour')
workhours_annual_total_df                       = workhours_annual_avg.df * laborforce.df
productivity_df                                 = gdp_current_natprices.df / workhours_annual_total_df

# Annual living costs based on living wage
liv_grossincome_USstates_annual_df              = livwage_USstates_hourly_df * weeks_per_year * workhours_per_week
