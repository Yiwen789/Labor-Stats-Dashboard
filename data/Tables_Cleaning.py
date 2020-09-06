import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np

#-----------------------------------------------------------------------
#data information
#-----------------------------------------------------------------------


#scrape_table

def scrape_table(table_url):
	#get table
	page = requests.get(table_url)
	page_content = page.content
	soup = BeautifulSoup(page_content, 'html.parser')
	table = soup.find_all('table', {'class': 'regular'})

	#read scraped data into list
	all_rows = []
	for t in table:
		rows = t.find_all('tr')
		for row in rows:
			value = row.get_text()
			all_rows.append(value)

	#convert list to dataframe
	df = pd.DataFrame(all_rows)
	return df

#split dataframe
def split_table(df):
		df = df[0].str.split('\n', expand = True)
		return df

#==========================================================================================================================
#state data
#==========================================================================================================================

#data source url
all_url = {}
for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10','11', '12', '13', '14', '15', '16']:
	new_key = 'a_' + str(i)
	all_url[new_key] = 'https://www.bls.gov/news.release/empsit.t' + str(i) + '.htm'

#data index

all_index = {
			'a_01': [['TOTAL',
					'Men, 16 years and over',
					'Men, 20 years and over',
					'Women, 16 years and over',
					'Women, 20 years and over',
					'Both sexes, 16 to 19 years'],
					['Civilian noninstitutional population'],
					['Civilian labor force',
					'Not in labor force'],
					['Employed',
					'Unemployed',
					'Not in labor force']],
			'a_02': [['WHITE',
					'BLACK OR AFRICAN AMERICAN',
					'ASIAN'],
					 ['Total',
					 'Men, 20 years and over',
					'Women, 20 years and over',
					'Both sexes, 16 to 19 years'],
					 ['Employed',
					 'Unemployed']],
			'a_03': [['HISPANIC OR LATINO ETHNICITY'],
					['Total',
					'Men, 20 years and over',
					'Women, 20 years and over',
					'Both sexes, 16 to 19 years'],
					['Employed',
					'Unemployed']],
			'a_04': [['Less than a high school diploma',
					'High school graduates, no college',
					'Some college or associate degree',
					'Bachelor\'s degree and higher'],
					['Employed',
					'Unemployed']],
			'a_05': [['VETERANS, 18 years and over',
					 'Gulf War-era II veterans',
					 'Gulf War-era I veterans',
					 'World War II, Korean War, and Vietnam-era veterans',
					 'Veterans of other service periods',
					 'NONVETERANS, 18 years and over'],
					 ['Civilian labor force',
					 'Not in labor force'],
					 ['Employed',
					 'Unemployed',
					 'Not in labor force']],
			'a_06': [['TOTAL, 16 years and over',
					'Men, 16 to 64 years',
					 'Women, 16 to 64 years',
					 'Both sexes, 65 years and over'],
					 ['Civilian labor force',
					 'Not in labor force'],
					 ['Employed',
					 'Unemployed',
					 'Not in labor force']],
			'a_07': [['Foreign born, 16 years and over',
					'Native born, 16 years and over'],
					['Civilian labor force',
					'Not in labor force'],
					['Employed',
					'Unemployed',
					'Not in labor force']],
			'a_08_1': [['Agriculture and related industries',
					 'Nonagricultural industries'],
					 ['Wage and salary workers',
					 'Self-employed workers, unincorporated',
					 'Unpaid family workers'],
					 ['Wage and salary workers',
					 'Self-employed workers, unincorporated',
					 'Unpaid family workers',
					 'Government',
					 'Private industries'],
					 ['Wage and salary workers',
					 'Self-employed workers, unincorporated',
					 'Unpaid family workers',
					 'Government',
					 'Private households',
					 'Other industries']],
			'a_08_2': [['All industries',
					 'Nonagricultural industries'],
					 ['Part time for economic reasons',
					 'Part time for noneconomic reasons'],
					 ['Slack work or business conditions',
					 'Could only find part-time work',
					 'Part time for noneconomic reasons']],
			'a_09_1': [['Total, 16 years and over',
					 'Men, 16 years and over',
					 'Women, 16 years and over'],
					 ['16 to 19 years',
					 '20 years and over'],
					 ['16 to 17 years',
					 '18 to 19 years',
					 '20 to 24 years',
					 '25 years and over'],
					 ['16 to 17 years',
					 '18 to 19 years',
					 '20 to 24 years',
					 '25 to 54 years',
					 '55 years and over'],
					 ['16 to 17 years',
					 '18 to 19 years',
					 '20 to 24 years',
					 '25 to 34 years',
					 '35 to 44 years',
					 '45 to 54 years',
					 '55 years and over']],
			'a_09_2': [['MARITAL STATUS',
					 'FULL- OR PART-TIME STATUS',
					 'MULTIPLE JOBHOLDERS',
					 'SELF-EMPLOYMENT'],
					 ['Married men, spouse present',
					 'Married women, spouse present',
					 'Women who maintain families',
					 'Full-time workers',
					 'Part-time workers',
					 'Total multiple jobholders',
					 'Self-employed workers, incorporated',
					 'Self-employed workers, unincorporated']],
			'a_10_1': [['Total, 16 years and over',
					 'Men, 16 years and over',
					 'Women, 16 years and over'],
					 ['Total, 16 years and over',
					 'Men, 16 years and over',
					 'Women, 16 years and over'],
					 ['16 to 17 years',
					 '18 to 19 years',
					 '20 to 24 years',
					 '25 years and over'],
					 ['16 to 17 years',
					 '18 to 19 years',
					 '20 to 24 years',
					 '25 to 54 years',
					 '55 years and over'],
					 ['16 to 17 years',
					 '18 to 19 years',
					 '20 to 24 years',
					 '25 to 34 years',
					 '35 to 44 years',
					 '45 to 54 years',
					 '55 years and over']],
			'a_10_2': [['MARITAL STATUS',
					 'FULL- OR PART-TIME STATUS'],
					 ['Married men, spouse present',
					 'Married women, spouse present',
					 'Women who maintain families',
					 'Full-time workers',
					 'Part-time workers']],
			'a_11': [['Job losers and persons who completed temporary jobs',
					'Job leavers',
					'Reentrants',
					'New entrants'],
					['On temporary layoff',
					 'Not on temporary layoff',
					 'Job leavers', 'Reentrants',
					 'New entrants'],
					 ['On temporary layoff',
					 'Permanent job losers',
					 'Persons who completed temporary jobs',
					 'Job leavers', 'Reentrants',
					 'New entrants']],
			'a_12': [['NUMBER OF UNEMPLOYED',
					'PERCENT DISTRIBUTION'],
					['Less than 5 weeks',
					 '5 to 14 weeks',
					 '15 weeks and over',
					 'Average (mean) duration, in weeks',
					 'Median duration, in weeks'],
					 ['Less than 5 weeks',
					 '5 to 14 weeks',
					 '15 to 26 weeks',
					 '27 weeks and over',
					 'Average (mean) duration, in weeks',
					 'Median duration, in weeks'
					 ]],
			'a_13': [['Management, professional, and related occupations',
					 'Service occupations',
					 'Sales and office occupations',
					 'Natural resources, construction, and maintenance occupations',
					 'Production, transportation, and material moving occupations'],
					 ['Management, business, and financial operations occupations',
					 'Professional and related occupations',
					 'Service occupations',
					 'Sales and related occupations',
					 'Office and administrative support occupations',
					 'Farming, fishing, and forestry occupations',
					 'Construction and extraction occupations',
					 'Installation, maintenance, and repair occupations',
					 'Production occupations',
					 'Transportation and material moving occupations']],
			'a_14': [['Nonagricultural private wage and salary workers',
					 'Agriculture and related private wage and salary workers',
					 'Government workers',
					 'Self-employed workers, unincorporated, and unpaid family workers'],
					 ['Mining, quarrying, and oil and gas extraction',
					 'Construction',
					 'Manufacturing:Durable goods',
					 'Manufacturing: Nondurable goods',
					 'Wholesale and retail trade',
					 'Transportation and utilities',
					 'Information',
					 'Financial activities',
					 'Professional and business services',
					 'Education and health services',
					 'Leisure and hospitality',
					 'Other services',
					 'Agriculture and related private wage and salary workers',
					 'Government workers',
					 'Self-employed workers, unincorporated, and unpaid family workers']
					 ],
			'a_15': [['U-1', 'U-2', 'U-3', 'U-4', 'U-5', 'U-6'],
					['U-1 Persons unemployed 15 weeks or longer, as a percent of the civilian labor force',
					 'U-2 Job losers and persons who completed temporary jobs, as a percent of the civilian labor force',
					 'U-3 Total unemployed, as a percent of the civilian labor force (official unemployment rate)',
					 'U-4 Total unemployed plus discouraged workers, as a percent of the civilian labor force plus discouraged workers',
					 'U-5 Total unemployed, plus discouraged workers, plus all other persons marginally attached to the labor force, as a percent of the civilian labor force plus all persons marginally attached to the labor force',
					 'U-6 Total unemployed, plus all persons marginally attached to the labor force, plus total employed part time for economic reasons, as a percent of the civilian labor force plus all persons marginally attached to the labor force']
					],
			'a_16': [['NOT IN THE LABOR FORCE',
					'MULTIPLE JOBHOLDERS'],
					['Total not in the labor force',
					 'Persons who currently want a job',
					 'Total multiple jobholders',
					 'Percent of total employed',
					 'Primary job full time, secondary job part time',
					 'Primary and secondary jobs both part time',
					 'Primary and secondary jobs both full time',
					 'Hours vary on primary or secondary job']]

			}

#multi-level table codes
all_index_codes = {
					'a_01': [np.repeat([0, 1, 2, 3, 4, 5], 3).tolist(),
							np.repeat([0], 18).tolist(),
							np.tile([0, 0, 1], 6).tolist(),
							np.tile([0, 1, 2], 6).tolist()],
					'a_02': [[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
							[0, 0, 1, 1, 2, 2, 3, 3, 0, 0, 1, 1, 2, 2, 3, 3, 0, 0],
							[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]],
					'a_03': [np.repeat([0, 0], 4),
							np.repeat([0, 1, 2, 3], 2),
							np.tile([0, 1], 4)],
					'a_04': [np.repeat([0, 1, 2, 3], 2),
							np.tile([0, 1], 4)],
					'a_05': [np.repeat([0, 1, 2, 3, 4, 5], 3),
							np.tile([0, 0, 1], 6),
							np.tile([0, 1, 2], 6)],
					'a_06': [np.repeat([0, 1, 2, 3], 3),
							np.tile([0, 0, 1], 4),
							np.tile([0, 1, 2], 4)],
					'a_07': [np.repeat([0, 1], 3),
							np.tile([0, 0, 1], 2),
							np.tile([0, 1, 2], 2)],
					'a_08_1': [[0, 0, 0, 1, 1, 1, 1, 1],
							  [0, 1, 2, 0, 0, 0, 1, 2],
							  [0, 1, 2, 3, 4, 4, 1, 2],
							  [0, 1, 2, 3, 4, 5, 1, 2]],
					'a_08_2': [np.repeat([0, 1], 3),
							  np.tile([0, 0, 1], 2),
							  np.tile([0, 1, 2], 2)],
					'a_09_1': [np.repeat([0, 1, 2], 7),
							  np.tile([0, 0, 1, 1, 1, 1, 1], 3),
							  np.tile([0, 1, 2, 3, 3, 3, 3], 3),
							  np.tile([0, 1, 2, 3, 3, 3, 4], 3),
							  np.tile([0, 1, 2, 3, 4, 5, 6], 3)],
					'a_09_2': [[0, 0, 0, 1, 1, 2, 3, 3],
							  [0, 1, 2, 3, 4, 5, 6, 7]],
					'a_10_1': [np.repeat([0, 1, 2], 7),
							   np.tile([0, 0, 1, 1, 1, 1, 1], 3),
							   np.tile([0, 1, 2, 3, 3, 3, 3], 3),
							   np.tile([0, 1, 2, 3, 3, 3, 4], 3),
							   np.tile([0, 1, 2, 3, 4, 5, 6], 3)],
					'a_10_2': [[0, 0, 0, 1, 1],
							   [0, 1, 2, 3, 4]],
					'a_11': [[0, 0, 0, 1, 2, 3],
							 [0, 1, 1, 2, 3, 4],
							 [0, 1, 2, 3, 4, 5]],
					'a_12': [[0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
							 [0, 1, 2, 2, 3, 4, 0, 1, 2, 2],
							 [0, 1, 2, 3, 4, 5, 0, 1, 2, 3]],
					'a_13': [[0, 0, 1, 2, 2, 3, 3, 3, 4, 4],
							 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]],
					'a_14': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3],
							 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]],
					'a_15': [[0, 1, 2, 3, 4, 5],
							 [0, 1, 2, 3, 4, 5]],
					'a_16': [[0, 0, 1, 1, 1, 1, 1, 1],
							 [0, 1, 2, 3, 4, 5, 6, 7]]
					}

#multi-level table level number
all_index_levels = {'a_01': 4,
					'a_02': 3,
					'a_03': 3,
					'a_04': 2,
					'a_05': 3,
					'a_06': 3,
					'a_07': 3,
					'a_08_1': 4,
					'a_08_2': 3,
					'a_09_1': 5,
					'a_09_2': 2,
					'a_10_1': 5,
					'a_10_2': 2,
					'a_11': 3,
					'a_12': 3,
					'a_13': 2,
					'a_14': 2,
					'a_15': 2,
					'a_16': 2}

#multi-level table level names
all_level_names = {}
for i in ['01', '02', '03', '04', '05', '06', '07', '08_1', '08_2', '09_1', '09_2', '10_1', '10_2', '11', '12', '13', '14', '15', '16']:
	all_level_names['a_' + i] = ['data_level_' + str(j) for j in range(1, all_index_levels['a_' + str(i)] + 1)]


month_5 = '07/01/2020'
month_4 = '06/01/2020'
month_3 = '05/01/2020'
month_2 = '04/01/2020'
month_1 = '03/01/2020'
month_prev = '07/01/2019'

#multi-level table columns
all_columns = {
				'a_01': [['Not seasonally adjusted',
						'Seasonally adjusted'],
					   [month_prev,
					   month_1,
					   month_2,
					   month_3,
					   month_4,
					   month_5]],
				'a_02': [['Not seasonally adjusted',
						'Seasonally adjusted'],
						[month_prev,
						month_1,
						month_2,
						month_3,
						month_4,
						month_5]],
				'a_03': [['Not seasonally adjusted',
						'Seasonally adjusted'],
						[month_prev,
						month_1,
						month_2,
						month_3,
						month_4,
						month_5]],
				'a_04': [['Not seasonally adjusted',
						'Seasonally adjusted'],
						[month_prev,
						month_1,
						month_2,
						month_3,
						month_4,
						month_5]],
				'a_05': [['Total',
						'Men',
						'Women'],
						[month_prev,
						month_5]],
				'a_06': [['Persons with a disability',
						'Persons with no disability'],
						[month_prev, month_5]],
				'a_07': [['Total',
						'Men',
						'Women'],
						[month_prev,
						month_5]],
				'a_08_1': [['Not seasonally adjusted',
						'Seasonally adjusted'],
						[month_prev,
						month_1,
						month_2,
						month_3,
						month_4,
						month_5]],
				'a_08_2': [['Not seasonally adjusted',
						'Seasonally adjusted'],
						[month_prev,
						month_1,
						month_2,
						month_3,
						month_4,
						month_5]],
				'a_09_1': [['Not seasonally adjusted',
							'Seasonally adjusted'],
						[month_prev,
						month_1,
						month_2,
						month_3,
						month_4,
						month_5]],
				'a_09_2': [['Not seasonally adjusted',
						'Seasonally adjusted'],
						[month_prev,
						month_1,
						month_2,
						month_3,
						month_4,
						month_5]],
				'a_10_1': [['Number of unemployed persons(in thousands)',
						'Unemployment rates'],
						[month_prev,
						month_1,
						month_2,
						month_3,
						month_4,
						month_5]],
				'a_10_2': [['Not seasonally adjusted',
						'Seasonally adjusted'],
						[month_prev,
						month_1,
						month_2,
						month_3,
						month_4,
						month_5]],
				'a_11': [['Not seasonally adjusted',
						'Seasonally adjusted'],
						[month_prev,
						month_1,
						month_2,
						month_3,
						month_4,
						month_5]],
				'a_12': [['Not seasonally adjusted',
						'Seasonally adjusted'],
						[month_prev,
						month_1,
						month_2,
						month_3,
						month_4,
						month_5]],
				'a_13': [['Employed',
						'Unemployed',
						'Unemployment rates'],
						[month_prev,
						month_5]],
				'a_14': [['Number of unemployed persons (in thousands)',
						'Unemployment rates'],
						[month_prev,
						month_5]],
				'a_15': [['Not seasonally adjusted',
						'Seasonally adjusted'],
						[month_prev,
						month_1,
						month_2,
						month_3,
						month_4,
						month_5]],
				'a_16': [['Total',
						'Men',
						'Women'],
						['May 2019',
						month_5]]}

#multi-level column codes
all_column_codes = {
					'a_01': [[0, 0, 0, 1, 1, 1, 1, 1, 1],
							[0, 4, 5, 0, 1, 2, 3, 4, 5]],
					'a_02': [[0, 0, 0, 1, 1, 1, 1, 1, 1],
							[0, 4, 5, 0, 1, 2, 3, 4, 5]],
					'a_03': [[0, 0, 0, 1, 1, 1, 1, 1, 1],
						   [0, 4, 5, 0, 1, 2, 3, 4, 5]],
					'a_04': [[0, 0, 0, 1, 1, 1, 1, 1, 1],
						   [0, 4, 5, 0, 1, 2, 3, 4, 5]],
					'a_05': [np.repeat([0, 1, 2], 2),
							np.tile([0, 1], 3)],
					'a_06': [np.repeat([0, 1], 2),
							np.tile([0, 1], 2)],
					'a_07': [np.repeat([0, 1, 2], 2),
							np.tile([0, 1], 3)],
					'a_08_1': [[0, 0, 0, 1, 1, 1, 1, 1, 1],
							  [0, 4, 5, 0, 1, 2, 3, 4, 5]],
					'a_08_2': [[0, 0, 0, 1, 1, 1, 1, 1, 1],
							  [0, 4, 5, 0, 1, 2, 3, 4, 5]],
					'a_09_1': [[0, 0, 0, 1, 1, 1, 1, 1, 1],
							  [0, 4, 5, 0, 1, 2, 3, 4, 5]],
					'a_09_2': [[0, 0, 0, 1, 1, 1, 1, 1, 1],
							  [0, 4, 5, 0, 1, 2, 3, 4, 5]],
					'a_10_1': [[0, 0, 0, 1, 1, 1, 1, 1, 1],
							   [0, 4, 5, 0, 1, 2, 3, 4, 5]],
					'a_10_2': [[0, 0, 0, 1, 1, 1, 1, 1, 1],
							   [0, 4, 5, 0, 1, 2, 3, 4, 5]],
					'a_11': [[0, 0, 0, 1, 1, 1, 1, 1, 1],
							 [0, 4, 5, 0, 1, 2, 3, 4, 5]],
					'a_12': [[0, 0, 0, 1, 1, 1, 1, 1, 1],
							 [0, 4, 5, 0, 1, 2, 3, 4, 5]],
					'a_13': [np.repeat([0, 1, 2], 2),
							 np.tile([0, 1], 3)],
					'a_14': [np.repeat([0, 1], 2),
							 np.tile([0, 1], 2)],
					'a_15': [[0, 0, 0, 1, 1, 1, 1, 1, 1],
							 [0, 4, 5, 0, 1, 2, 3, 4, 5]],
					'a_16': [np.repeat([0, 1, 2], 2),
							 np.tile([0, 1], 3)]}

#multilevel table function
def multi_level(split_df, table_id):
	#index
	index = pd.MultiIndex(levels = all_index[table_id],
						codes = all_index_codes[table_id],
						names = ['data_level_' + str(i) for i in range(1,all_index_levels[table_id] + 1)])

	#columns
	columns = pd.MultiIndex(levels = all_columns[table_id],
							codes = all_column_codes[table_id])

	#value

	all_values = {'a_01': (split_df[(split_df[1] == 'Employed') | (split_df[1] == 'Unemployed') |
			  (split_df[1] == 'Not in labor force')].iloc[:, 2:11].values.tolist()),
				'a_02': (split_df[(split_df[1] == 'Employed') | (split_df[1] == 'Unemployed')].iloc[:, 2:11].values.tolist()),
				'a_03': (split_df[(split_df[1] == 'Employed') | (split_df[1] == 'Unemployed')].iloc[:, 2:11].values.tolist()),
				'a_04': (split_df[(split_df[1] == 'Employed') | (split_df[1] == 'Unemployed')].iloc[:, 2:11].values.tolist()),
				'a_05': (split_df[(split_df[1] == 'Employed') | (split_df[1] == 'Unemployed') | (split_df[1] == 'Not in labor force')].iloc[:, 2:8].values.tolist()),
				'a_06': (split_df[(split_df[1] == 'Employed') | (split_df[1] == 'Unemployed') | (split_df[1] == 'Not in labor force')].iloc[:, 2:6].values.tolist()),
				'a_07': (split_df[(split_df[1] == 'Employed') | (split_df[1] == 'Unemployed') | (split_df[1] == 'Not in labor force')].iloc[:, 2:8].values.tolist()),
				'a_08_1': (split_df.iloc[4:7, 2:11].values.tolist()
					+ split_df.iloc[9:10, 2:11].values.tolist()
					+ split_df.iloc[11:15, 2:11].values.tolist()),
				'a_08_2': (split_df[(split_df[1] == 'Slack work or business conditions')
				  | (split_df[1] == 'Could only find part-time work')
				  | (split_df[1] == 'Part time for noneconomic reasons(4)')].iloc[:, 2:11].values.tolist()),
				'a_09_1': (split_df[(split_df[1] == '16 to 17 years')
				  | (split_df[1] == '18 to 19 years')
				  | (split_df[1] =='20 to 24 years')
				  |(split_df[1] == '25 to 34 years')
				  | (split_df[1] == '35 to 44 years')
				  | (split_df[1] =='45 to 54 years')
				  | (split_df[1] =='55 years and over')].iloc[:, 2:11].values.tolist()),
				'a_09_2': (split_df.iloc[43:46, 2:11].values.tolist()
					+ split_df.iloc[48:50, 2:11].values.tolist()
					+ split_df.iloc[52:53, 2:11].values.tolist()
					+ split_df.iloc[56:58, 2:11].values.tolist()),
				'a_10_1': (split_df[(split_df[1] == '16 to 17 years')
				  | (split_df[1] == '18 to 19 years')
				  | (split_df[1] == '20 to 24 years')
				  |(split_df[1] ==  '25 to 34 years')
				  | (split_df[1] == '35 to 44 years')
				  | (split_df[1] =='45 to 54 years')
				  | (split_df[1] =='55 years and over')].iloc[:, 2:11].values.tolist()),
				'a_10_2': (split_df.iloc[43:46, 2:11].values.tolist()
					+ split_df.iloc[48:50, 2:11].values.tolist()),
				'a_11': (split_df.iloc[4:5, 2:11].values.tolist()
					+ split_df.iloc[6:8, 2:11].values.tolist()
					+ split_df.iloc[8:11, 2:11].values.tolist()),
				'a_12': (split_df[(split_df[1] == 'Less than 5 weeks')
				  | (split_df[1] == '5 to 14 weeks')
				  | (split_df[1] == '15 to 26 weeks')
				  |(split_df[1] ==  '27 weeks and over')
				  | (split_df[1] == 'Average (mean) duration, in weeks')
				  | (split_df[1] =='Median duration, in weeks')].iloc[:, 2:11].values.tolist()),
				'a_13': (split_df[(split_df[1] == 'Management, professional, and related occupations')
				  | (split_df[1] == 'Professional and related occupations')
				  | (split_df[1] == 'Service occupations')
				  |(split_df[1] ==  'Sales and related occupations')
				  | (split_df[1] == 'Office and administrative support occupations')
				  | (split_df[1] =='Farming, fishing, and forestry occupations')
				  | (split_df[1] == 'Construction and extraction occupations')
				  |(split_df[1] ==  'Installation, maintenance, and repair occupations')
				  | (split_df[1] == 'Production occupations')
				  | (split_df[1] =='Transportation and material moving occupations')].iloc[:, 2:8].values.tolist()),
				'a_14': (split_df.iloc[4:6, 2:6].values.tolist()
					+ split_df.iloc[7:20, 2:6].values.tolist()),
				'a_15': (split_df.iloc[2:8, 2:11].values.tolist()),
				'a_16': (split_df.iloc[4:6, 2:8].values.tolist()
					+ split_df.iloc[10:16, 2:8].values.tolist())

	}

	data = []

	value = all_values[table_id]

	for i in value:
		i = [int(float(item.replace(',', ''))) for item in i if item != '-']
		data.append(i)

	df = pd.DataFrame(data, index = index, columns = columns)

	return df

df_dict = {}
for i in ['01', '02', '03', '04', '05', '06', '07', '08_1', '08_2', '09_1', '09_2', '10_1', '10_2', '11', '12', '13', '14', '15', '16']:
	id = 'a_' + str(i)
	split_df = split_table(scrape_table(all_url[id[:4]]))
	df_dict[id] = (multi_level(split_df, id))
	# df_dict[id].to_csv('cps_{id}.csv'.format(id = id), index = False)
	df_dict[id].to_pickle('cps_{id}.pkl'.format(id = id))
	print(id)

#==========================================================================================================================
#state data
#==========================================================================================================================

#data url
laus_url = {'state_01': 'https://www.bls.gov/news.release/laus.t01.htm',
			'city_01': 'https://www.bls.gov/news.release/laus.t01.htm',
			'state_03': 'https://www.bls.gov/news.release/laus.t03.htm'}
# for i in range(1, 5):
#     new_key = 'state_0' + str(i)
#     state_url[new_key] = 'https://www.bls.gov/news.release/laus.t0' + str(i) + '.htm'

#state and city list
state_list = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia',
              'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
              'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
              'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
              'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
              'West Virginia', 'Wisconsin', 'Wyoming', 'Puerto Rico']
state_list_t3 = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
                  'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana',
                 'Iowa','Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
                  'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
                  'New York', 'North Carolina', 'North Dakota', 'Ohio','Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
                  'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                  'West Virginia', 'Wisconsin', 'Wyoming', 'Puerto Rico', 'Virgin Islands']
city_list_raw = ['Los Angeles-Long Beach-Glendale(1)',  'Miami-Miami Beach-Kendall(1)', 'Chicago-Naperville-Arlington Heights(1)',
            'Detroit-Warren-Dearborn(2)', 'New York City', 'Cleveland-Elyria(2)', 'Seattle-Bellevue-Everett(1)']
city_list = ['Los Angeles-Long Beach-Glendale',  'Miami-Miami Beach-Kendall', 'Chicago-Naperville-Arlington Heights',
            'Detroit-Warren-Dearborn', 'New York City', 'Cleveland-Elyria', 'Seattle-Bellevue-Everett']

#data index
laus_index = {
			'state_01': [state_list, ['Civilian labor force', 'Unemployed']],
			'city_01': [city_list, ['Civilian labor force', 'Unemployed']],
			'state_03': state_list
			}


#multi-level codes
laus_index_codes = {
			'state_01': [np.repeat(range(0, len(state_list)), 2),
                     np.tile([0, 1], len(state_list))],
            'city_01': [np.repeat(range(0, len(city_list)), 2),
                     np.tile([0, 1], len(city_list))],
			'state_03': [],
}

#multi-level level number
laus_levels = {
			'state_01': 2,
			'city_01': 2,
			'state_03': 1
}

#multi-level level names
laus_level_names = {}
for i in ['state_01', 'city_01', 'state_03']:
	laus_level_names[i] = ['data_level_' + str(j) for j in range(1, laus_levels[i] + 1)]

#multi-level columns
industry_list = ['Total', 'Construction', 'Manufacturing', 'Trade, transportation, and utilities',
			'Financial activities', 'Professional and business services', 'Education and health services',
			'Leisure and hospitality', 'Government']
laus_columns = {
			'state_01': ['May 2019', 'Mar 2020', 'Apr 2020', 'May 2020'],
			'city_01': ['May 2019', 'Mar 2020', 'Apr 2020', 'May 2020'],
			'state_03': [industry_list,
			['May 2019', 'Mar 2020', 'Apr 2020', 'May 2020']]
			}

#multi-level column codes
laus_column_codes = {
			'state_01': [],
			'city_01': [],
			'state_03': [np.repeat(range(0, len(industry_list)), 4),
						np.tile(range(0, 4), len(industry_list))]
}

def get_val3(split_df):
		    val = []
		    for i in state_list:
		        df = pd.concat([split_df[split_df[1] == i].iloc[:,2:6], split_df[split_df[1] == i].iloc[:,6:10], split_df[split_df[1] == i].iloc[:,10:14]], axis = 1)
		        val.append(df.iloc[0].values.tolist() + df.iloc[1].values.tolist() + df.iloc[2].values.tolist())
		    return val

def laus_multi_level(split_df, table_id):

	# #columns
	# columns = pd.MultiIndex(levels = laus_columns[table_id],
	# 						codes = laus_column_codes[table_id])
	if table_id == 'state_01':
		columns = laus_columns[table_id]
		index = pd.MultiIndex(levels = laus_index[table_id],
							codes = laus_index_codes[table_id],
							names = laus_level_names[table_id])
		val = []
		for i in state_list:
		    val.extend(
		       split_df[split_df[1] == i].iloc[:,2:6].values.tolist()
		    )
		    val.extend(
		        split_df[split_df[1] == i].iloc[:,6:10].values.tolist()
		    )
	elif table_id == 'city_01':
		columns = laus_columns[table_id]
		index = pd.MultiIndex(levels = laus_index[table_id],
							codes = laus_index_codes[table_id],
							names = laus_level_names[table_id])
		val = []
		for i in city_list_raw:
		    val.extend(
		       split_df[split_df[1] == i].iloc[:,2:6].values.tolist()
		    )
		    val.extend(
		        split_df[split_df[1] == i].iloc[:,6:10].values.tolist()
		    )

	elif table_id == 'state_03':
		columns = pd.MultiIndex(levels = laus_columns[table_id],
								codes = laus_column_codes[table_id])
		index = state_list

		split_df[1].replace('Delaware(2)', 'Delaware', inplace = True)
		split_df[1].replace('District of Columbia(2)', 'District of Columbia', inplace = True)
		split_df[1].replace('Hawaii(2)', 'Hawaii', inplace = True)
		split_df[1].replace('Virgin Islands(3)', 'Virgin Islands', inplace = True)
		split_df[1].replace('Virgin Islands(1)', 'Virgin Islands', inplace = True)

		val = get_val3(split_df)

	# #data
	# val_1 = []
	# for i in state_list:
	#     val_1.extend(
	#        split_df[split_df[1] == i].iloc[:,2:6].values.tolist()
	#     )
	#     val_1.extend(
	#         split_df[split_df[1] == i].iloc[:,6:10].values.tolist()
	#     )
	# val_2 = []
	# for i in city_list:
	#     val_1.extend(
	#        split_df[split_df[1] == i].iloc[:,2:6].values.tolist()
	#     )
	#     val_1.extend(
	#         split_df[split_df[1] == i].iloc[:,6:10].values.tolist()
	#     )
	#val_3 = get_val3(split_df)

	#value
	# values = {
	# 		'state_01': val_1,
	# 		'city_01': val_2,
	# 		'state_03': []
	# }


	data = []

	#value = values[table_id]

	for i in val:
		i = [int(float(item.replace(',', ''))) for item in i if item != '-']
		data.append(i)

	df = pd.DataFrame(data, index = index, columns = columns)

	return df

area_df_dict = {}
for i in ['state_01', 'city_01', 'state_03']:
	split_df = split_table(scrape_table(laus_url[i]))
	area_df_dict[i] = laus_multi_level(split_df, i)
	print(i)

# df = laus_multi_level(split_table(scrape_table(laus_url['city_01'])), 'city_01')
# print(df)
