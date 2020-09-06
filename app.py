# -*- coding: utf-8 -*-
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
#import dash_daq as daq
import plotly.graph_objs as go

from dash.dependencies import Input, Output

#from Tables_Cleaning import *
from state_data_csv import *
#from metro_data import *

external_stylesheets = [
    'https://codepen.io/yluo789/pen/xxZqOOX.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

states_code_to_name_dict = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
							 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia', 'FL': 'Florida',
							 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana',
							 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine',
							 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
							 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire',
							 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota',
							 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
							 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
							 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin',
							 'WY': 'Wyoming'}

app = dash.Dash(__name__)
# app.css.append_css({
#     "external_stylesheets": "https://codepen.io/chriddyp/pen/bWLwgP.css"
# })

# Create global chart template
# mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75Iahttps://codepen.io/yluo789/pen/xxZqOOX?editors=1100.css
# layout = dict(
#     autosize=True,
#     automargin=True,
#     margin=dict(l=30, r=30, b=20, t=40),
#     hovermode="closest",
#     plot_bgcolor="#F9F9F9",
#     paper_bgcolor="#F9F9F9",
#     legend=dict(font=dict(size=10), orientation="h"),
#     title="Satellite Overview",
#     mapbox=dict(
#         accesstoken=mapbox_access_token,
#         style="light",
#         center=dict(lon=-78.05, lat=42.54),
#         zoom=7,
#     ),
# )

server = app.server
app.config["suppress_callback_exceptions"] = True


#==============================================================================================================================================================================

def build_banner():
	return html.Div([
				html.Div(
				id = 'banner',
				children = [
				html.Div([
					html.Img(src = app.get_asset_url('logo.jpg'), style={'height':'60px', 'width':'auto'}),
				], className = 'one column' ),
				html.Div(
					id = 'banner_text',
					children = [
					#html.Img(src = app.get_asset_url('logo.jpg'), style={'height':'60px', 'width':'auto'}),
					html.H3('Labormatics COVID Labor Market Dashboard'),
					], className = 'nine columns'),
				html.Div(
					id = 'banner_logo',
					children = [
						html.A(
						html.Button(id = 'learn_more_button', children = 'LEARN MORE', n_clicks = 0),
						href = 'https://labormatics.com/',
						target = '_blank'
						),

					], className = 'two columns'),

				html.Div([
					html.P('Welcome to the Laboratics COVID Dashboard. \
					This dashboard displays economic data related to the impact of COVID-19 on the US labor market. \
					The data were gathered from a variety of sources including the Department of Commerce, \
					Department of Labor, and the Federal Reserve.'),
					html.P(''),
					html.P('Feedback and suggestions are welcome!'),
					], className = 'twelve columns'),

				])
	])

#==============================================================================================================================================================================

def build_summary():
	return html.Div([
				html.Div([
					html.Div([
						html.H6('Summary'),
					],  className = 'text-container'),
					# html.P('Below are employment and unemployment rates. \
					# If you want to display state employment and unemployment,\
					#  scroll down to the map and click on the state of interest \
					#  and the graphs will update automatically. To reset to \
					#  national data, click the browser refresh button.'),
					html.Div([
						dcc.Markdown('''
						Below are employment and unemployment rates.If you want to display state employment and unemployment, scroll down to the map and click on the state of interest and the graphs will update automatically. To reset national data, click the browser refresh button.
						'''),
					], className = 'descript-container'),
					html.P(id = 'summary_title'),
				], className = 'twelve columns'),
				html.Div([
					dcc.Graph(id = 'summary_1')
				], className = 'four columns'),
				html.Div([
					dcc.Graph(id = 'summary_2')
				], className = 'four columns'),
				html.Div([
					dcc.Graph(id = 'summary_3')
				], className = 'four columns'),
				# html.Div([
				# 	dcc.Graph(id = 'summary_4')
				# ], className = 'four columns')
				html.Div([
					html.Div([
						dcc.Markdown('''
							*Source: US Bureau of Labor Statistics*
						''')
					])
				], className = 'twelve columns')

	])

@app.callback(
[Output(component_id = 'summary_1', component_property = 'figure'),
Output(component_id = 'summary_2', component_property = 'figure'),
Output(component_id = 'summary_3', component_property = 'figure'),
Output(component_id = 'summary_title', component_property = 'children')],
[Input(component_id = 'state_map', component_property = 'clickData')]
)
def update_summary_plots(clicked_state):
	if clicked_state == None:
		df_filtered = df_state
		df_filtered['time'] = pd.to_datetime(df_state['month_year'])
		df_filtered = df_state.groupby('time')[['Civilian non-institutional population', 'Civilian labor force', 'Employed', 'Unemployed']].sum()
		title = 'National Employment Summary'

	else:
		state = clicked_state['points'][0]['location']
		df_filtered = df_state[df_state['code'] == state]
		df_filtered['time'] = pd.to_datetime(df_filtered['month_year'])
		df_filtered.set_index('time', inplace = True)
		title = '{state} Employment Summary'.format(state = states_code_to_name_dict[state])


		# #lines
		# df_filtered = df_state[df_state['State'] == 'Minnesota']
		# df_filtered['time'] = pd.to_datetime(df_filtered['month_year'])
		# df_filtered.set_index('time', inplace = True)
		# fig = go.Figure()

	#fig1=====================================================================================
	#lines
	fig1 = go.Figure()
	fig1.add_trace(
	    go.Scatter(x = list(df_filtered.index),
	               y = list(df_filtered['Unemployed']),
	               name = 'Unemployed',
	               yaxis = 'y',
	               line={"width": 2.5},
	                mode="lines",
	                hovertemplate = 'y: %{y}',
	                showlegend=True
	              )
	)
	fig1.add_trace(
	    go.Scatter(x = list(df_filtered.index),
	               y = list(df_filtered['Unemployed']/df_filtered['Civilian labor force']),
	               name = 'Unemployement Rate',
	               yaxis = 'y2',
	               line={"width": 2.5},
	                mode="lines",
	               hovertemplate = 'y: %{y:.1%}',
	                showlegend=True
	              )
	)
	#yearly marks
	fig1.add_trace(
	    go.Scatter(x = list(df_filtered.resample('AS').first().index),
	               y = list(df_filtered.resample('AS').first()['Unemployed']),
	               yaxis = 'y',
	                marker={"size": 5, "line": dict(width =  1, color = 'DarkSlateGrey'), "color": "white"},
	                hoverinfo = 'skip',
	               mode = 'markers',
	               showlegend = False,
	              )
	)
	fig1.add_trace(
	    go.Scatter(x = list(df_filtered.resample('AS').first().index),
	               y = list(df_filtered.resample('AS').first()['Unemployed']/df_filtered.resample('AS').first()['Civilian labor force']),
	               yaxis = 'y2',
	               marker={"size": 5, "line": dict(width =  1, color = 'DarkSlateGrey'), "color": "white"},
	               mode = 'markers',
	                hoverinfo = 'skip',
	               showlegend = False
	              )
	)
	fig1.update_layout(
	    hovermode = 'x unified',
	    hoverdistance = 200,
	    spikedistance = 200,
		legend=dict(
			    orientation="h",
			    yanchor="bottom",
			    y=1.08,
			    xanchor="right",
			    x=1.1
			),
		margin = dict(
				l = 10,
				r = 10,
				t = 10,
				b = 10,
				pad = 0,
		),
		width = 450,
		height = 300,
	    xaxis=dict(
	        range=["1975-01-01 00:00:00", "2021-05-01 00:00:00"],
	         showspikes = True,
	          spikemode = 'across',
	        rangeselector=dict(
	            buttons=list([
	                dict(count=1,
	                     label="1m",
	                     step="month",
	                     stepmode="backward"),
	                dict(count=6,
	                     label="6m",
	                     step="month",
	                     stepmode="backward"),
	                dict(count = 5,
	                     label = "5y",
	                     step = "year",
	                     stepmode = "backward"),
	                dict(step="all")
	            ]),
				xanchor = 'right',
				x = 1.1,
				y = 1.03,
	        ),
	        rangeslider=dict(
	            visible=True,
	            autorange=False,
	            range=["1975-01-01 00:00:00", "2021-05-01 00:00:00"], #the actual range is ["1976-01-01 00:00:00", "2020-05-01 00:00:00"]
	            thickness = 0.05
	        ),
	        type="date",
			showgrid = False
	    ),
	    yaxis = dict(
	       # range = [0, 0.8*10**6],
	        zeroline = True,
			showgrid = False,
	    ),
	    yaxis2 = dict(
	        #range = [0, 0.2],
	        side = 'right',
	        overlaying = 'y',
	        scaleanchor="y",
	        scaleratio=1,
			gridcolor = 'rgb(159, 197, 232)'
			#showgrid = False
	    ),
		plot_bgcolor = 'rgb(242, 242, 242)',
        paper_bgcolor = 'rgb(242, 242, 242)',
	)

	#fig2=====================================================================================
	fig2 = go.Figure()
	fig2.add_trace(
		go.Scatter(
				x = list(df_filtered.index),
			   	y = list(df_filtered['Civilian labor force']),
			   	name = 'Civilian Labor Force',
			   	yaxis = 'y',
			   	line={"width": 2.5},
				mode="lines",
				hovertemplate = 'y: %{y}',
				showlegend=True
				)
	)
	fig2.add_trace(
		go.Scatter(
				x = list(df_filtered.index),
			    y = list(df_filtered['Unemployed']/df_filtered['Civilian labor force']),
			    name = 'Unemployement Rate',
			    yaxis = 'y2',
			    line={"width": 2.5},
			    mode="lines",
			    hovertemplate = 'y: %{y:.1%}',
			    showlegend=True
				)
	)
	#yearly marks
	fig2.add_trace(
		go.Scatter(x = list(df_filtered.resample('AS').first().index),
	               y = list(df_filtered.resample('AS').first()['Civilian labor force']),
	               yaxis = 'y',
	                marker={"size": 5, "line": dict(width =  1, color = 'DarkSlateGrey'), "color": "white"},
	                hoverinfo = 'skip',
	               mode = 'markers',
	               showlegend = False,
	              )
	)
	fig2.add_trace(
		go.Scatter(x = list(df_filtered.resample('AS').first().index),
	               y = list(df_filtered.resample('AS').first()['Unemployed']/df_filtered.resample('AS').first()['Civilian labor force']),
	               yaxis = 'y2',
	               marker={"size": 5, "line": dict(width =  1, color = 'DarkSlateGrey'), "color": "white"},
	               mode = 'markers',
	                hoverinfo = 'skip',
	               showlegend = False
	              )
	)

	fig2.update_layout(
		hovermode = 'x unified',
		hoverdistance = 200,
		spikedistance = 200,
		legend=dict(
			    orientation="h",
			    yanchor="bottom",
			    y=1.08,
			    xanchor="right",
			    x=1.1
			),
		margin = dict(
				l = 10,
				r = 10,
				t = 10,
				b = 10,
				pad = 0,
		),
		width = 450,
		height = 300,
		xaxis=dict(
			range=["1975-01-01 00:00:00", "2021-05-01 00:00:00"],
			 showspikes = True,
			  spikemode = 'across',
			rangeselector=dict(
				buttons=list([
					dict(count=1,
						 label="1m",
						 step="month",
						 stepmode="backward"),
					dict(count=6,
						 label="6m",
						 step="month",
						 stepmode="backward"),
					dict(count = 5,
						 label = "5y",
						 step = "year",
						 stepmode = "backward"),
					dict(step="all")
				]),
				xanchor = 'right',
				x = 1.1,
				y = 1.03,
			),
			rangeslider=dict(
				visible=True,
				autorange=False,
				range=["1975-01-01 00:00:00", "2021-05-01 00:00:00"], #the actual range is ["1976-01-01 00:00:00", "2020-05-01 00:00:00"]
				thickness = 0.05
			),
			type="date",
			showgrid = False,
		),
		yaxis = dict(
			#range = [0, 0.8*10**6],
			zeroline = True,
			showgrid = False
		),
		yaxis2 = dict(
			#range = [0, 0.2],
			side = 'right',
			overlaying = 'y',
			scaleanchor="y",
			scaleratio=1,
			gridcolor = 'rgb(159, 197, 232)',
			#showgrid = False
		),
		plot_bgcolor = 'rgb(242, 242, 242)',
        paper_bgcolor = 'rgb(242, 242, 242)',
	)
	#fig3=====================================================================================
	#line
	fig3 = go.Figure()
	fig3.add_trace(
		go.Bar(
                x = df_filtered.index,
                y = df_filtered['Employed'],
                name = i
        )
	)

	fig3.add_trace(
		go.Bar(
                x = df_filtered.index,
                y = (-1)*df_filtered[i],
                name = i
        )
	)
	#yearly marks

	fig3.update_layout(
		barmode = 'relative',
	    hovermode = 'x unified',
	    hoverdistance = 200,
	    spikedistance = 200,
		legend=dict(
			    orientation="h",
			    yanchor="bottom",
			    y=1.08,
			    xanchor="right",
			    x=1
			),
		margin = dict(
				l = 10,
				r = 10,
				t = 10,
				b = 10,
				pad = 0,
		),
		width = 450,
		height = 300,
	    xaxis=dict(
	        range=["2005-01-01 00:00:00", "2021-05-01 00:00:00"],
	         showspikes = True,
	          spikemode = 'across',
	        rangeselector=dict(
	            buttons=list([
	                dict(count=1,
	                     label="1m",
	                     step="month",
	                     stepmode="backward"),
	                dict(count=6,
	                     label="6m",
	                     step="month",
	                     stepmode="backward"),
	                dict(count = 5,
	                     label = "5y",
	                     step = "year",
	                     stepmode = "backward"),
	                dict(step="all")
	            ]),
				xanchor = 'right',
				x = 1,
				y = 1.03,
	        ),
	        rangeslider=dict(
	            visible=True,
	            autorange=False,
	            range=["1975-01-01 00:00:00", "2021-05-01 00:00:00"], #the actual range is ["1976-01-01 00:00:00", "2020-05-01 00:00:00"]
	            thickness = 0.05
	        ),
	        type="date"
	    ),
	    yaxis = dict(
	        #range = [0, 4*10**6],
	        zeroline = True,
			showgrid = True,
			gridcolor = 'rgb(159, 197, 232)',

	    ),
	    # yaxis2 = dict(
	    #     #range = [0, 0.2],
	    #     side = 'right',
	    #     overlaying = 'y',
	    #     scaleanchor="y",
	    #     scaleratio=1,
		# 	showgrid = False
	    # ),
		plot_bgcolor = 'rgb(242, 242, 242)',
        paper_bgcolor = 'rgb(242, 242, 242)',
	)

	# #fig4=====================================================================================
	# #line
	# df_ui = pd.read_csv('C:\\Users\\Yiwen L\\Documents\\Work\\Labormatics\\asa_conference\\ui_claims\\ui_cleaned_for_dashboard.csv')
	#
	# df_ui['initial claims'] = df_ui['initial claims'].str.replace(',', '')
	# df_ui['continued claims'] = df_ui['continued claims'].str.replace(',', '')
	# df_ui['initial claims'] = pd.to_numeric(df_ui['initial claims'])
	# df_ui['continued claims'] = pd.to_numeric(df_ui['continued claims'])
	#
	# # df_ui['week'] = pd.to_datetime(df_ui['week'])
	# # df_ui = df_ui.set_index('week', inplace = True)
	#
	# if clicked_state == None:
	# 	df_filtered_2 = df_ui
	# 	df_filtered_2 = df_ui.groupby('week')[['initial claims', 'continued claims']].sum()
	# 	df_ui['week'] = pd.to_datetime(df_ui['week'])
	# 	df_ui.set_index('week', inplace = True)
	# else:
	# 	state = clicked_state['points'][0]['location']
	# 	df_filtered_2 = df_ui[df_ui['code'] == state]
	# 	df_ui['week'] = pd.to_datetime(df_ui['week'])
	# 	df_ui.set_index('week', inplace = True)
	#
	# fig4 = go.Figure()
	# fig4.add_trace(
	#     go.Scatter(x = list(df_filtered_2.index),
	#                y = list(df_filtered_2['initial claims']),
	#                name = 'Initial Claims',
	#                yaxis = 'y',
	#                line={"width": 2.5},
	#                 mode="lines",
	#                 hovertemplate = 'y: %{y}',
	#                 showlegend=True
	#               )
	# )
	# fig4.add_trace(
	#     go.Scatter(x = list(df_filtered_2.index),
	#                y = list(df_filtered_2['continued claims']),
	#                name = 'Continued Claims',
	#                yaxis = 'y2',
	#                line={"width": 2.5},
	#                 mode="lines",
	#                hovertemplate = 'y: %{y:.1%}',
	#                 showlegend=True
	#               )
	# )
	# #yearly marks
	# fig4.add_trace(
	#     go.Scatter(x = list(df_filtered_2.resample('AS').first().index),
	#                y = list(df_filtered_2.resample('AS').first()['initial claims']),
	#                yaxis = 'y',
	#                 marker={"size": 5, "line": dict(width =  1, color = 'DarkSlateGrey'), "color": "white"},
	#                 hoverinfo = 'skip',
	#                mode = 'markers',
	#                showlegend = False,
	#               )
	# )
	# fig4.add_trace(
	#     go.Scatter(x = list(df_filtered_2.resample('AS').first().index),
	#                y = list(df_filtered_2.resample('AS').first()['continued claims']),
	#                yaxis = 'y2',
	#                marker={"size": 5, "line": dict(width =  1, color = 'DarkSlateGrey'), "color": "white"},
	#                mode = 'markers',
	#                 hoverinfo = 'skip',
	#                showlegend = False
	#               )
	# )
	# fig4.update_layout(
	#     hovermode = 'x unified',
	#     hoverdistance = 200,
	#     spikedistance = 200,
	#     legend=dict(
	#             orientation="h",
	#             yanchor="bottom",
	#             y=1.08,
	#             xanchor="right",
	#             x=1.1
	#         ),
	#     margin = dict(
	#             l = 10,
	#             r = 10,
	#             t = 10,
	#             b = 10,
	#             pad = 0,
	#     ),
	#     width = 450,
	#     height = 300,
	#     xaxis=dict(
	#         range=["1987-01-01 00:00:00", "2021-05-01 00:00:00"],
	#          showspikes = True,
	#           spikemode = 'across',
	#         rangeselector=dict(
	#             buttons=list([
	#                 dict(count=1,
	#                      label="1m",
	#                      step="month",
	#                      stepmode="backward"),
	#                 dict(count=6,
	#                      label="6m",
	#                      step="month",
	#                      stepmode="backward"),
	#                 dict(count = 5,
	#                      label = "5y",
	#                      step = "year",
	#                      stepmode = "backward"),
	#                 dict(step="all")
	#             ]),
	#             xanchor = 'right',
	#             x = 1.1,
	#             y = 1.03,
	#         ),
	#         rangeslider=dict(
	#             visible=True,
	#             autorange=False,
	#             range=["1987-01-01 00:00:00", "2021-05-01 00:00:00"], #the actual range is ["1976-01-01 00:00:00", "2020-05-01 00:00:00"]
	#             thickness = 0.05
	#         ),
	#         type="date",
	#         showgrid = False
	#     ),
	#     yaxis = dict(
	#        # range = [0, 0.8*10**6],
	#         zeroline = True,
	#         showgrid = False,
	#     ),
	#     yaxis2 = dict(
	#         #range = [0, 0.2],
	#         side = 'right',
	#         overlaying = 'y',
	#         scaleanchor="y",
	#         scaleratio=1,
	#         gridcolor = 'rgb(159, 197, 232)'
	#         #showgrid = False
	#     ),
	#     plot_bgcolor = 'rgb(242, 242, 242)',
	#     paper_bgcolor = 'rgb(242, 242, 242)',
	# )

	return fig1, fig2, fig3, title
#==============================================================================================================================================================================
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
years = range(1976, 2021)
def build_unemp():
	return html.Div([
				html.Div([
					html.Div([
						html.H6('Unemployment'),
						#html.P('Add some intructions here')
					], className = 'text-container'),
					html.Div([
					dcc.Markdown('''
					Click on the map to view trends. Hover mouse over the map to see detailed state data.
					''')
					], className = 'descript-container'),
				], className = 'twelve columns'),
				html.Div([
					html.Div([
						html.P('Select Month', className = 'control-label'),
						dcc.Dropdown(
							id = 'month_dropdown',
							options = [{'label': i, 'value': i} for i in months],
							value = 'Jan',
							className = 'dcc-control',
							#style = dict(display = 'inline-block')
						)
					], className = 'six columns'),
					html.Div([
						html.P('Select Year  (1976 to 2020)', className = 'control-label'),
						dcc.Dropdown(
							id = 'year_dropdown',
							options = [{'label': i, 'value': i} for i in years],
							value = 2020,
							className = 'dcc-control',
							#style = dict(display = 'inline-block')
							)
					], className = 'six columns'),
				], className = 'row'),
				# html.P('Select Value', className = 'control-label'),
				# dcc.RadioItems(id = 'stat_button',
				# 			   options = [{'label': i, 'value': i} for i in ['Unemployment rate', 'Unemployed', 'Employed', 'Civilian labor force', 'Civilian non-institutional population']],
				# 			   value = 'Unemployment rate',
				# 			   labelStyle = dict(display = 'block'))

				html.Div([
					html.H6(id = 'map_title'),
					dcc.Graph(id = 'state_map')
				], className = 'twelve columns'),
				html.Div([
					html.H6(id = 'datatable_title'),
					dash_table.DataTable(
						id = 'area_table',
						#columns=[{"name": i, "id": i} for i in ['State', 'Civilian labor force', 'Unemployed', 'Unemployment rate']],
						data = [],
						#data = df_state.loc[:, ['State', 'Civilian labor force', 'Unemployed', 'Unemployment rate']].to_dict('records'),
						page_action = 'native',
						page_size = 10,
						style_cell_conditional=[
						    {
						        'if': {'column_id': c},
						        'textAlign': 'left'
						    } for c in ['Date', 'Region']
						],
						style_data_conditional=[
						    {
						        'if': {'row_index': 'odd'},
						        'backgroundColor': 'rgb(248, 248, 248)'
						    }
						],
						style_header={
						    'backgroundColor': 'rgb(230, 230, 230)',
						    'fontWeight': 'bold'
						}
					)
				], className = 'twelve columns'),
				html.Div([
					dcc.Markdown('''
						*Source: US Bureau of Labor Statistics*
					''')
				], className = 'twelve columns'),

		])

@app.callback(
	[Output(component_id = 'state_map', component_property = 'figure'),
	Output(component_id = 'map_title', component_property = 'children')],
	[Input('month_dropdown', 'value'),
	Input('year_dropdown', 'value'),
	#Input('stat_button', 'value')
	]
)
def update_map(selected_month, selected_year):
	time = selected_month + ' ' + str(selected_year)
	fig = go.Figure(data = go.Choropleth(
			    locations = df_state['code'],
			    z = df_state[df_state['month_year'] == time]['Unemployed']/df_state[df_state['month_year'] == time]['Civilian labor force'],
				locationmode = 'USA-states',
			    colorscale = 'Blues',
			    colorbar_title = 'Unemployment Rate',
				#colorbar = dict(bgcolor = 'rgb(250, 250, 250)'),
				text=df_state[df_state['month_year'] == time]['text'],
				#geo_bgcolor="#323130"
				))

	fig.update_layout(
		geo = dict(bgcolor = "rgb(242, 242, 242)"),
	    #title_text = '{month}, {year} Unemployment Rate by State'.format(month = selected_month, year = selected_year),
	    geo_scope = 'usa',
		autosize = False,
		 width = 1400,
		 height = 350,
		margin = dict(
			l = 0,
			r = 0,
			b = 50,
			t = 50
		),
		plot_bgcolor = 'rgb(242, 242, 242)',
        paper_bgcolor = 'rgb(242, 242, 242)'
	)

	title = '{month}, {year} Unemployment Rate by State'.format(month = selected_month, year = selected_year)

	return fig, title

month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
              'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
state_codes = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
			   'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM','NY',
			   'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
			   'WI', 'WY']
# @app.callback(
#
# 	#Output(component_id = 'sum_bar', component_property = 'figure'),
# 	Output(component_id = 'time_bar', component_property = 'figure'),
# 	#Output(component_id = 'state_bar', component_property = 'figure')
#
# 	[Input('month_dropdown', 'value'),
# 	Input('year_dropdown', 'value'),
# 	Input('state_map', 'clickData'),
# 	#Input('stat_button', 'value')
# 	]
# )
# def update_sum_bar(selected_month, selected_year, clicked_state):
# 	time = selected_month + ' ' + str(selected_year)
#
# 	colors_1 = []
# 	for i in ['Civilian non-institutional population', 'Civilian labor force', 'Employed', 'Unemployed']:
# 		if i == 'Unemployed':
# 			colors_1.append('rgb(0, 76, 163)')
# 		else:
# 			colors_1.append('rgba(123, 199, 255, 0.4)')
#
# 	colors_2 = []
# 	for i in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
# 		if i == selected_month:
# 			colors_2.append('rgb(0, 76, 163)')
# 		else:
# 			colors_2.append('rgba(123, 199, 255, 0.4)')
#
#
# 	if clicked_state == None:
# 		fig1 = go.Figure(data = go.Bar(
# 			x = ['Civilian Population', 'Civilian labor force', 'Employed', 'Unemployed'],
# 			y = [df_state[df_state['month_year'] == time]['Civilian non-institutional population'].sum(),
# 				df_state[df_state['month_year'] == time]['Civilian labor force'].sum(),
# 				df_state[df_state['month_year'] == time]['Employed'].sum(),
# 				df_state[df_state['month_year'] == time]['Unemployed'].sum()],
# 			marker_color = colors_1
# 		))
# 		title_1 = 'National'
#
# 		#select twelve months to display
# 		# months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# 		# months_to_display = [month + ' ' + str(selected_year - 1) for month in months[months.index(selected_month):]] + [month + ' ' + str(selected_year) for month in months[:months.index(selected_month)]]
# 		filtered_df = df_state[df['Year'] == selected_year]
# 		fig2 = go.Figure(data = go.Bar(
# 			x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
# 			y = filtered_df.groupby('Month').sum()['Unemployed']/filtered_df.groupby('Month').sum()['Civilian labor force'],
# 			marker_color = colors_2
# 		))
# 		title_2 = 'National'
#
# 		fig3 = go.Figure(data = go.Bar(
# 			x = state_codes,
# 			y = df_state[(df_state['Year'].astype(str) == str(selected_year)) & (df_state['Month'] == month_dict[selected_month])].groupby('code').sum()['Unemployed']/df_state[(df_state['Year'].astype(str) == str(selected_year)) & (df_state['Month'] == month_dict[selected_month])].groupby('code').sum()['Civilian labor force'],
# 			marker_color = 'rgba(123, 199, 255, 0.4)'
#
# ))
# 		title_3 = 'Unemployment Rate by State'
#
# 	elif clicked_state != None:
# 		state = clicked_state['points'][0]['location']
#
# 		colors_3 = []
# 		for i in state_codes:
# 			if i == state:
# 				colors_3.append('rgb(0, 76, 163)')
# 			else:
# 				colors_3.append('rgba(123, 199, 255, 0.4)')
#
#
# 		fig1 = go.Figure(data = go.Bar(
# 			x = ['Civilian Population', 'Civilian labor force', 'Employed', 'Unemployed'],
# 			y = [df_state[(df_state['code'] == state) & (df_state['month_year'] == time)]['Civilian non-institutional population'].values[0],
# 				df_state[(df_state['code'] == state) & (df_state['month_year'] == time)]['Civilian labor force'].values[0],
# 				df_state[(df_state['code'] == state) & (df_state['month_year'] == time)]['Employed'].values[0],
# 				df_state[(df_state['code'] == state) & (df_state['month_year'] == time)]['Unemployed'].values[0]],
# 			marker_color = colors_1
# 			))
# 		title_1 = state
#
# 		#select twelve months to display
# 		# months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# 		# if selected_year == 2020:
# 		# 	months_to_display = ['Jan 2020', 'Feb 2020', 'Mar 2020', 'Apr 2020', 'May 2020']
# 		# months_to_display = [month + ' ' + str(selected_year - 1) for month in months[:months.index(selected_month)]] + [month + ' ' + str(selected_year) for month in months[months.index(selected_month):]]
# 		filtered_df = df_state[(df_state['Year'] == selected_year) & (df_state['code'] == state)]
# 		fig2 = go.Figure(data = go.Bar(
# 			x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
# 			y = filtered_df.groupby('Month').sum()['Unemployed']/filtered_df.groupby('Month').sum()['Civilian labor force'],
# 			marker_color = colors_2
# 			))
# 		title_2 = state
#
# 		fig3 = go.Figure(data = go.Bar(
# 			x = state_codes,
# 			y = df_state[(df_state['Year'].astype(str) == str(selected_year)) & (df_state['Month'] == month_dict[selected_month])].groupby('code').sum()['Unemployed']/df_state[(df_state['Year'].astype(str) == str(selected_year)) & (df_state['Month'] == month_dict[selected_month])].groupby('code').sum()['Civilian labor force'],
# 			marker_color = colors_3
# 			))
# 		title_3 = 'Unemployement Rate by State: {state} Highlighted'.format(state = state)
#
# 	fig1.update_layout(
# 		autosize = False,
# 		width = 700,
# 		height = 250,
# 		margin = dict(
# 			l = 50,
# 			r = 50,
# 			b = 50,
# 			t = 50,
# 			pad = 20
# 		),
# 		title={
# 		'text': title_1 + ' ' + 'Employement Statistics',
#         'y':0.95,
#         'x':0.1,
#         'xanchor': 'left',
#         'yanchor': 'top'
# 		},
# 		xaxis = {'showgrid': True, "gridcolor": "rgb(242, 242, 242)"},
# 		yaxis = {'showgrid': True, "gridcolor": "rgb(242, 242, 242)"},
# 		plot_bgcolor = 'rgb(250, 250, 250)',
#         paper_bgcolor = 'rgb(242, 242, 242)',
# 	)
#
# 	fig2.update_layout(
# 		autosize = False,
# 		width = 1400,
# 		height = 250,
# 		margin = dict(
# 			l = 50,
# 			r = 50,
# 			b = 50,
# 			t = 50,
# 			pad = 20
# 		),
# 		title={
# 		'text': title_2 + ' ' + 'Monthly Unemployement Rate',
#         'y':0.95,
#         'x':0.1,
#         'xanchor': 'left',
#         'yanchor': 'top'
# 		},
# 		xaxis = {'showgrid': True, "gridcolor": "rgb(242, 242, 242)"},
# 		yaxis = {'showgrid': True, "gridcolor": "rgb(242, 242, 242)"},
# 		plot_bgcolor = 'rgb(250, 250, 250)',
#         paper_bgcolor = 'rgb(242, 242, 242)'
# 		)
#
#
# 	fig3.update_layout(
# 			autosize = False,
# 			width = 1400,
# 			height = 200,
# 			margin = dict(
# 				l = 50,
# 				r = 50,
# 				b = 50,
# 				t = 50,
# 				pad = 20
# 			),
# 			title={
# 			'text': title_3,
# 	        'y':0.95,
# 	        'x':0.05,
# 	        'xanchor': 'left',
# 	        'yanchor': 'top'
# 			},
# 			xaxis = {'showgrid': True, "gridcolor": "rgb(242, 242, 242)"},
# 			yaxis = {'showgrid': True, "gridcolor": "rgb(242, 242, 242)"},
# 			plot_bgcolor = 'rgb(250, 250, 250)',
# 	        paper_bgcolor = 'rgb(242, 242, 242)'
# 		)
#
#
# 	#fig.update_layout(width = 500)
# 	return fig2

#===============================
#update Unemployment by area table
#===============================

@app.callback(
[Output('datatable_title', 'children'),
Output('area_table', 'columns'),
Output(component_id = 'area_table', component_property = 'data')],
[Input('month_dropdown', 'value'),
Input('year_dropdown', 'value'),
Input('state_map', 'clickData')]
)
def update_table(selected_month, selected_year, clicked_state): #selected_month format 'Jan', 'Feb', ...
	if clicked_state == None:
		title = '{month}, {year} National Labor Statistics'.format(month = selected_month, year = selected_year)
		columns=[{"name": i, "id": i} for i in ['State', 'Civilian labor force', 'Unemployed', 'Unemployment rate']]
		filtered_df = df_state[df_state['month_year'] == '{month} {year}'.format(month = selected_month, year = selected_year)]
		df = filtered_df.loc[:, ['State', 'Civilian labor force', 'Unemployed', 'Unemployment rate']]

		return title, columns, df.to_dict('records')
	else:
		state_code = clicked_state['points'][0]['location']
		state_name = states_code_to_name_dict[state_code]

		title = '{month}, {year} {state} Labor Statistics'.format(month = selected_month, year = selected_year, state = states_code_to_name_dict[state_code])

		month_code = '{month}-{year_2d}'.format(month = selected_month, year_2d = str(selected_year)[-2:])

		file_name_lbf = state_name + '_lbf.csv'
		file_name_unemp = state_name + '_unemp.csv'
		df_lbf = pd.read_csv('data\metro\{state_name}_lbf.csv'.format(state_name = state_name))
		df_unemp = pd.read_csv('data\metro\{state_name}_unemp.csv'.format(state_name = state_name))

		df_metro = pd.DataFrame({'Area': df_lbf.iloc[:, 0], 'Civilian Labor Force':df_lbf[month_code], 'Unemployed': df_unemp[month_code], 'Unemployment Rate': df_unemp[month_code]/df_lbf[month_code]})
		columns=[{'name': i, 'id': i} for i in df_metro.columns]

		return title, columns, df_metro.to_dict('records')
#==============================================================================================================================================================================
df_cpi = pd.read_csv('data\cpi\cpi_t01.csv')
#df_cpi2 = pd.read_csv('cpi_t01.csv')
def build_cpi():
	return html.Div([
				html.Div([
					html.Div([
						html.H6('Consumer Price Index'),
					], className = 'text-container'),
					html.Div([
						dcc.Markdown('''
						A consumer price index measures changes in the price level of a weighted average market basket of consumer goods and services purchased by households.
						''')
					], className = 'descript-container')
				], className = 'twelve columns'),
				# html.Div([
				# 	html.P('Use slider to select a time range'),
				# 	dcc.RangeSlider(
				# 		id = 'line_slider',
				# 		marks={i: str(i) for i in range(2000, 2021)},
				# 		min = 2000,
				# 		max = 2020,
				# 		value = [2010, 2020]
				# 	)
				#
				# ], className = 'twelve columns'),
				html.Div([
					html.Div([
						dcc.Graph(figure = fig_food),
					], className = 'four columns'),
					html.Div([
						dcc.Graph(figure = fig_trans),
					], className = 'four columns'),
					html.Div([
						dcc.Graph(figure = fig_med),
					], className = 'four columns'),
					html.Div([
						dcc.Graph(figure = fig_shelter),
					], className = 'four columns'),
					html.Div([
						dcc.Graph(figure = fig_ec),
					], className = 'four columns'),
					html.Div([
						dcc.Graph(figure = fig_es),
					], className = 'four columns')

				]),
				html.Div([
					dcc.Markdown('''
						*Source: US Bureau of Labor Statistics*
					''')
				], className = 'twelve columns')
		])
# @app.callback(
# 	[Output(component_id = 'food_line', component_property = 'figure'),
# 	Output(component_id = 'trans_line', component_property = 'figure'),
# 	Output(component_id = 'med_line', component_property = 'figure')],
# 	[Input('line_slider', 'value')]
# )
#def update_cpi(selected_range):
def build_cpi_graphs():
	# months = ['Mar 2019', 'Apr 2019', 'May 2019', 'Jun 2019', 'Jul 2019', 'Aug 2019', 'Sep 2019', 'Oct 2019', 'Nov 2019', 'Dec 2019',
	# 		'Jan 2020', 'Feb 2020', 'Mar 2020', 'Apr 2020', 'May 2020', 'Jun 2020']
	# months = ['Jan-17', 'Feb-17', 'Mar-17', 'Apr-17', 'May-17', 'Jun-17',
	# 		'Jul-17', 'Aug-17', 'Sep-17', 'Oct-17', 'Nov-17', 'Dec-17',
	# 		'Jan-18', 'Feb-18', 'Mar-18', 'Apr-18', 'May-18', 'Jun-18',
	# 		'Jul-18', 'Aug-18', 'Sep-18', 'Oct-18', 'Nov-18', 'Dec-18',
	# 		'Jan-19', 'Feb-19', 'Mar-19',  'Apr-19', 'May-19', 'Jun-19',
    #    		'Jul-19', 'Aug-19', 'Sep-19', 'Oct-19', 'Nov-19', 'Dec-19',
	# 		'Jan-20', 'Feb-20', 'Mar-20', 'Apr-20', 'May-20', 'Jun-20']

	df_cpi_food = df_cpi[df_cpi['data_level_1'] == 'Food at home']
	df_cpi_food = df_cpi_food.drop('data_level_1', axis = 1)
	df_cpi_food = df_cpi_food.T
	df_cpi_food = df_cpi_food.iloc[:,:4]
	df_cpi_food.columns = ['Cereals & Bakery', 'Meats & Eggs', 'Dairy & Related', 'Produce']
	df_cpi_food = df_cpi_food.apply(pd.to_numeric, errors='coerce')
	#df_cpi_food[['Cereals and bakery products', 'Meats, poultry, fish, and eggs']] = df_cpi_food[['Cereals and bakery products', 'Meats, poultry, fish, and eggs']].apply(pd.to_numeric)
	#df_cpi_food['Cereals and bakery products'] = df_cpi_food['Cereals and bakery products'].apply(pd.to_numeric, errors='coerce')
	df_cpi_food = df_cpi_food[1:]
	df_cpi_food.index = pd.to_datetime(df_cpi_food.index)


	df_cpi_trans = df_cpi[df_cpi['data_level_1'] == 'Transportation services']
	df_cpi_trans = df_cpi_trans.drop('data_level_1', axis = 1)
	df_cpi_trans = df_cpi_trans.T
	df_cpi_trans.columns = ['Vehicle Maintenance', 'Vehicle Insurance', 'Airline']
	df_cpi_trans = df_cpi_trans[1:]
	df_cpi_trans = df_cpi_trans.apply(pd.to_numeric, errors='coerce')
	df_cpi_trans.index = pd.to_datetime(df_cpi_trans.index)

	df_cpi_med = df_cpi[df_cpi['data_level_1'] == 'Medical care services']
	df_cpi_med = df_cpi_med.drop('data_level_1', axis = 1)
	df_cpi_med = df_cpi_med.T
	df_cpi_med.columns = ['Physicians\' Services', 'Hospital Services']
	df_cpi_med = df_cpi_med[1:]
	df_cpi_med = df_cpi_med.apply(pd.to_numeric, errors='coerce')
	df_cpi_med.index = pd.to_datetime(df_cpi_med.index)

	df_cpi_shelter = df_cpi[df_cpi['data_level_1'] == 'Shelter']
	df_cpi_shelter = df_cpi_shelter.drop('data_level_1', axis = 1)
	df_cpi_shelter = df_cpi_shelter.T
	df_cpi_shelter.columns = ['Rent', 'Owners\' equivalent rent']
	df_cpi_shelter = df_cpi_shelter[1:]
	df_cpi_shelter = df_cpi_shelter.apply(pd.to_numeric, errors='coerce')
	df_cpi_shelter.index = pd.to_datetime(df_cpi_shelter.index)

	df_cpi_ec = df_cpi[df_cpi['data_level_1'] == 'Energy commodities']
	df_cpi_ec = df_cpi_ec.drop('data_level_1', axis = 1)
	df_cpi_ec = df_cpi_ec.T
	df_cpi_ec.columns = ['Fuel oil', 'Motor Fuel']
	df_cpi_ec = df_cpi_ec[1:]
	df_cpi_ec = df_cpi_ec.apply(pd.to_numeric, errors='coerce')
	df_cpi_ec.index = pd.to_datetime(df_cpi_ec.index)

	df_cpi_es = df_cpi[df_cpi['data_level_1'] == 'Energy services']
	df_cpi_es = df_cpi_es.drop('data_level_1', axis = 1)
	df_cpi_es = df_cpi_es.T
	df_cpi_es.columns = ['Electricity', 'Utility Gas']
	df_cpi_es = df_cpi_es[1:]
	df_cpi_es = df_cpi_es.apply(pd.to_numeric, errors='coerce')
	df_cpi_es.index = pd.to_datetime(df_cpi_es.index)
	#food======================

	fig_food = go.Figure()
	fig_trans = go.Figure()
	fig_med = go.Figure()
	fig_shelter = go.Figure()
	fig_ec = go.Figure()
	fig_es = go.Figure()

	#cpi_dict = ['food': df_cpi_food, 'trans': df_cpi_trans]

	for i in df_cpi_food.columns:
		fig_food.add_trace(
		    go.Scatter(x=list(df_cpi_food.index),
		               y=list(df_cpi_food[i]),
		               name = i,
		                line = {"width": 2.5},
		                 mode = 'lines',
		               hovertemplate = 'y',
		              showlegend = True),
		)

	for i in df_cpi_food.columns:
		fig_food.add_trace(
			go.Scatter(x = df_cpi_food.resample('QS').first().index,
						y = df_cpi_food[i].resample('QS').first(),
						marker={"size": 5, "line": dict(width =  1, color = 'DarkSlateGrey'), "color": "white"},
	 	               mode = 'markers',
	 	                hoverinfo = 'skip',
	 	               showlegend = False
			)
		)

	# Add range slider
	fig_food.update_layout(
	title = dict(
		text = 'Food',
		xanchor = 'center',
		x = 0.5,
		yanchor = 'top',
		y = 0.99,
		pad = dict(
			b = 15,
		)
	),
	hovermode = 'x unified',
	hoverdistance = 200,
	spikedistance = 200,
	legend=dict(
	        orientation="h",
	        yanchor="bottom",
	        y= 1,
	        xanchor="right",
	        x=1.1
	    ),
	margin = dict(
	        l = 25,
	        r = 25,
	        t = 25,
	        b = 25,
	        pad = 0,
	),
#	width = 1200,
	height = 300,
	xaxis=dict(
	    range = ["2014-07-01 00:00:00", "2020-12-01 00:00:00"],
	    showspikes = True,
	    spikemode = 'across',
	    rangeselector=dict(
	        buttons=list([
	            dict(count=1,
	                 label="1m",
	                 step="month",
	                 stepmode="backward"),
	            dict(count=6,
	                 label="6m",
	                 step="month",
	                 stepmode="backward"),
	            dict(count=1,
	                 label="1y",
	                 step="year",
	                 stepmode="backward"),
	            dict(step="all")
	        ]),
	        xanchor = 'right',
	        x = 1.1,
	        y = 0.95
	    ),
	    rangeslider=dict(
	        visible=True,
	        autorange = False,
	        range=["2014-01-01 00:00:00", "2021-05-01 00:00:00"],
	        thickness = 0.05
	    ),
	    type = 'date',
		showgrid = False,
	),
	yaxis = dict(
		#range = [0, 4*10**6],
		zeroline = True,
		showgrid = True,
		gridcolor = 'rgb(159, 197, 232)',

	),
	plot_bgcolor = 'rgb(242, 242, 242)',
	paper_bgcolor = 'rgb(242, 242, 242)',
	)

	#transportation===================

	for i in df_cpi_trans.columns:
		fig_trans.add_trace(
		    go.Scatter(x=df_cpi_trans.index,
		               y=df_cpi_trans[i],
		               name = i,
		               line = {"width": 2.5},
		                mode = 'lines',
		              hovertemplate = 'y',
		              showlegend = True),
		)

	for i in df_cpi_trans.columns:
		fig_trans.add_trace(
			go.Scatter(x = df_cpi_trans.resample('QS').first().index,
						y = df_cpi_trans[i].resample('QS').first(),
						marker={"size": 5, "line": dict(width =  1, color = 'DarkSlateGrey'), "color": "white"},
	 	               mode = 'markers',
	 	                hoverinfo = 'skip',
	 	               showlegend = False
			)
		)


	# Add range slider
	fig_trans.update_layout(
	# title_text="Time series with range slider and selectors"
	title = dict(
		text = 'Transportation',
		xanchor = 'center',
		x = 0.5,
		yanchor = 'top',
		y = 0.99,
		pad = dict(
			b = 15,
		)
	),
	hovermode = 'x unified',
	hoverdistance = 200,
	spikedistance = 200,
	legend=dict(
	        orientation="h",
	        yanchor="bottom",
	        y=1,
	        xanchor="right",
	        x=1.1
	    ),
	margin = dict(
	        l = 25,
	        r = 25,
	        t = 25,
	        b = 25,
	        pad = 0,
	),
	# width = 1200,
	height = 300,
	xaxis=dict(
	    range = ["2014-07-01 00:00:00", "2020-12-01 00:00:00"],
	    showspikes = True,
	    spikemode = 'across',
	    rangeselector=dict(
	        buttons=list([
	            dict(count=1,
	                 label="1m",
	                 step="month",
	                 stepmode="backward"),
	            dict(count=6,
	                 label="6m",
	                 step="month",
	                 stepmode="backward"),
	            dict(count=1,
	                 label="1y",
	                 step="year",
	                 stepmode="backward"),
	            dict(step="all")
	        ]),
	        xanchor = 'right',
	        x = 1.1,
	        y = 0.95,

	    ),

	    rangeslider=dict(
	        visible=True,
	        autorange = False,
	        range=["2014-01-01 00:00:00", "2021-05-01 00:00:00"],
	        thickness = 0.05
	    ),
	    type = 'date',
		showgrid = False,
	),
	yaxis = dict(
		#range = [0, 4*10**6],
		zeroline = True,
		showgrid = True,
		gridcolor = 'rgb(159, 197, 232)',
	),
	plot_bgcolor = 'rgb(242, 242, 242)',
	paper_bgcolor = 'rgb(242, 242, 242)',
	)

	#medical===================
	for i in df_cpi_med.columns:
		fig_med.add_trace(
		    go.Scatter(x=df_cpi_med.index,
		               y=df_cpi_med[i],
		               name = i,
		               line = {"width": 2.5},
		                mode = 'lines',
		              hovertemplate = 'y',
		              showlegend = True),
		)

	for i in df_cpi_med.columns:
		fig_med.add_trace(
			go.Scatter(x = df_cpi_med.resample('QS').first().index,
						y = df_cpi_med[i].resample('QS').first(),
						marker={"size": 5, "line": dict(width =  1, color = 'DarkSlateGrey'), "color": "white"},
	 	               mode = 'markers',
	 	                hoverinfo = 'skip',
	 	               showlegend = False
			)
		)

	# Add range slider
	fig_med.update_layout(
	# title_text="Time series with range slider and selectors"
	title = dict(
		text = 'Medical Services',
		xanchor = 'center',
		x = 0.5,
		yanchor = 'top',
		y = 0.99,
		pad = dict(
			b = 15,
		)
	),
	hovermode = 'x unified',
	hoverdistance = 200,
	spikedistance = 200,
	legend=dict(
	        orientation="h",
	        yanchor="bottom",
	        y= 1,
	        xanchor="right",
	        x=1.1
	    ),
	margin = dict(
	        l = 25,
	        r = 25,
	        t = 25,
	        b = 25,
	        pad = 0,
	),
	# width = 1200,
	height = 300,
	xaxis=dict(
	    range = ["2014-07-01 00:00:00", "2020-12-01 00:00:00"],
	    showspikes = True,
	    spikemode = 'across',
	    rangeselector=dict(
	        buttons=list([
	            dict(count=1,
	                 label="1m",
	                 step="month",
	                 stepmode="backward"),
	            dict(count=6,
	                 label="6m",
	                 step="month",
	                 stepmode="backward"),
	            dict(count=1,
	                 label="1y",
	                 step="year",
	                 stepmode="backward"),
	            dict(step="all")
	        ]),
	        xanchor = 'right',
	        x = 1.1,
	        y = 0.95,

	    ),
	    rangeslider=dict(
	        visible=True,
	        autorange = False,
	        range=["2014-01-01 00:00:00", "2021-05-01 00:00:00"],
	        thickness = 0.05
	    ),
	    type = 'date',
		showgrid = False,
	),
	yaxis = dict(
		#range = [0, 4*10**6],
		zeroline = True,
		showgrid = True,
		gridcolor = 'rgb(159, 197, 232)',

	),
	plot_bgcolor = 'rgb(242, 242, 242)',
	paper_bgcolor = 'rgb(242, 242, 242)',
	)

	#Shelter ================
	for i in df_cpi_shelter.columns:
		fig_shelter.add_trace(
		    go.Scatter(x=df_cpi_shelter.index,
		               y=df_cpi_shelter[i],
		               name = i,
		               line = {"width": 2.5},
		                mode = 'lines',
		              hovertemplate = 'y',
		              showlegend = True),
		)

	for i in df_cpi_shelter.columns:
		fig_shelter.add_trace(
			go.Scatter(x = df_cpi_shelter.resample('QS').first().index,
						y = df_cpi_shelter[i].resample('QS').first(),
						marker={"size": 5, "line": dict(width =  1, color = 'DarkSlateGrey'), "color": "white"},
	 	               mode = 'markers',
	 	                hoverinfo = 'skip',
	 	               showlegend = False
			)
		)

	# Add range slider
	fig_shelter.update_layout(
	# title_text="Time series with range slider and selectors"
	title = dict(
		text = 'Shelter',
		xanchor = 'center',
		x = 0.5,
		yanchor = 'top',
		y = 0.99,
		pad = dict(
			b = 15,
		)
	),
	hovermode = 'x unified',
	hoverdistance = 200,
	spikedistance = 200,
	legend=dict(
	        orientation="h",
	        yanchor="bottom",
	        y=1,
	        xanchor="right",
	        x=1.1
	    ),
	margin = dict(
	        l = 25,
	        r = 25,
	        t = 25,
	        b = 25,
	        pad = 0,
	),
	# width = 1200,
	height = 300,
	xaxis=dict(
	    range = ["2014-07-01 00:00:00", "2020-12-01 00:00:00"],
	    showspikes = True,
	    spikemode = 'across',
	    rangeselector=dict(
	        buttons=list([
	            dict(count=1,
	                 label="1m",
	                 step="month",
	                 stepmode="backward"),
	            dict(count=6,
	                 label="6m",
	                 step="month",
	                 stepmode="backward"),
	            dict(count=1,
	                 label="1y",
	                 step="year",
	                 stepmode="backward"),
	            dict(step="all")
	        ]),
	        xanchor = 'right',
	        x = 1.1,
	        y = 0.95,

	    ),
	    rangeslider=dict(
	        visible=True,
	        autorange = False,
	        range=["2014-01-01 00:00:00", "2021-05-01 00:00:00"],
	        thickness = 0.05
	    ),
	    type = 'date',
		showgrid = False,
	),
	yaxis = dict(
		#range = [0, 4*10**6],
		zeroline = True,
		showgrid = True,
		gridcolor = 'rgb(159, 197, 232)',

	),
	plot_bgcolor = 'rgb(242, 242, 242)',
	paper_bgcolor = 'rgb(242, 242, 242)',
	)

	#energy commodities================
	for i in df_cpi_ec.columns:
		fig_ec.add_trace(
		    go.Scatter(x=df_cpi_ec.index,
		               y=df_cpi_ec[i],
		               name = i,
		               line = {"width": 2.5},
		                mode = 'lines',
		              hovertemplate = 'y',
		              showlegend = True),
		)

	for i in df_cpi_ec.columns:
		fig_ec.add_trace(
			go.Scatter(x = df_cpi_ec.resample('QS').first().index,
						y = df_cpi_ec[i].resample('QS').first(),
						marker={"size": 5, "line": dict(width =  1, color = 'DarkSlateGrey'), "color": "white"},
	 	               mode = 'markers',
	 	                hoverinfo = 'skip',
	 	               showlegend = False
			)
		)

	# Add range slider
	fig_ec.update_layout(
	# title_text="Time series with range slider and selectors"
	title = dict(
		text = 'Energy commodities',
		xanchor = 'center',
		x = 0.5,
		yanchor = 'top',
		y = 0.99,
		pad = dict(
			b = 15,
		)
	),
	hovermode = 'x unified',
	hoverdistance = 200,
	spikedistance = 200,
	legend=dict(
	        orientation="h",
	        yanchor="bottom",
	        y=1,
	        xanchor="right",
	        x=1.1
	    ),
	margin = dict(
	        l = 25,
	        r = 25,
	        t = 25,
	        b = 25,
	        pad = 0,
	),
	# width = 1200,
	height = 300,
	xaxis=dict(
	    range = ["2014-07-01 00:00:00", "2020-12-01 00:00:00"],
	    showspikes = True,
	    spikemode = 'across',
	    rangeselector=dict(
	        buttons=list([
	            dict(count=1,
	                 label="1m",
	                 step="month",
	                 stepmode="backward"),
	            dict(count=6,
	                 label="6m",
	                 step="month",
	                 stepmode="backward"),
	            dict(count=1,
	                 label="1y",
	                 step="year",
	                 stepmode="backward"),
	            dict(step="all")
	        ]),
	        xanchor = 'right',
	        x = 1.1,
	        y = 0.95,

	    ),
	    rangeslider=dict(
	        visible=True,
	        autorange = False,
	        range=["2014-01-01 00:00:00", "2021-05-01 00:00:00"],
	        thickness = 0.05
	    ),
	    type = 'date',
		showgrid = False,
	),
	yaxis = dict(
		#range = [0, 4*10**6],
		zeroline = True,
		showgrid = True,
		gridcolor = 'rgb(159, 197, 232)',

	),
	plot_bgcolor = 'rgb(242, 242, 242)',
	paper_bgcolor = 'rgb(242, 242, 242)',
	)

	#energy services================
	for i in df_cpi_es.columns:
		fig_es.add_trace(
		    go.Scatter(x=df_cpi_es.index,
		               y=df_cpi_es[i],
		               name = i,
		               line = {"width": 2.5},
		                mode = 'lines',
		              hovertemplate = 'y',
		              showlegend = True),
		)

	for i in df_cpi_es.columns:
		fig_es.add_trace(
			go.Scatter(x = df_cpi_es.resample('QS').first().index,
						y = df_cpi_es[i].resample('QS').first(),
						marker={"size": 5, "line": dict(width =  1, color = 'DarkSlateGrey'), "color": "white"},
	 	               mode = 'markers',
	 	                hoverinfo = 'skip',
	 	               showlegend = False
			)
		)

	# Add range slider
	fig_es.update_layout(
	# title_text="Time series with range slider and selectors"
	title = dict(
		text = 'Energy Services',
		xanchor = 'center',
		x = 0.5,
		yanchor = 'top',
		y = 0.99,
		pad = dict(
			b = 15,
		)
	),
	hovermode = 'x unified',
	hoverdistance = 200,
	spikedistance = 200,
	legend=dict(
	        orientation="h",
	        yanchor="bottom",
	        y=1,
	        xanchor="right",
	        x=1.1
	    ),
	margin = dict(
	        l = 25,
	        r = 25,
	        t = 25,
	        b = 25,
	        pad = 0,
	),
	# width = 1200,
	height = 300,
	xaxis=dict(
	    range = ["2014-07-01 00:00:00", "2020-12-01 00:00:00"],
	    showspikes = True,
	    spikemode = 'across',
	    rangeselector=dict(
	        buttons=list([
	            dict(count=1,
	                 label="1m",
	                 step="month",
	                 stepmode="backward"),
	            dict(count=6,
	                 label="6m",
	                 step="month",
	                 stepmode="backward"),
	            dict(count=1,
	                 label="1y",
	                 step="year",
	                 stepmode="backward"),
	            dict(step="all")
	        ]),
	        xanchor = 'right',
	        x = 1.1,
	        y = 0.95,

	    ),
	    rangeslider=dict(
	        visible=True,
	        autorange = False,
	        range=["2014-01-01 00:00:00", "2021-05-01 00:00:00"],
	        thickness = 0.05
	    ),
	    type = 'date',
		showgrid = False,
	),
	yaxis = dict(
		#range = [0, 4*10**6],
		zeroline = True,
		showgrid = True,
		gridcolor = 'rgb(159, 197, 232)',

	),
	plot_bgcolor = 'rgb(242, 242, 242)',
	paper_bgcolor = 'rgb(242, 242, 242)',
	)
	return fig_food, fig_trans, fig_med, fig_shelter, fig_ec, fig_es

fig_food, fig_trans, fig_med, fig_shelter, fig_ec, fig_es = build_cpi_graphs()

#==============================================================================================================================================================================

def build_ui():
	return html.Div([
		html.Div([
			html.Div([
				html.H6('Unemployment Insurance Claims'),
			], className = 'text-container'),
			html.Div([
				dcc.Markdown('''
				Unemployment insurance filings are the number of unemployment claims filed by people who have been furloughed or let go from their jobs. Click on the map above to see UI filings of a specific state.
				''')
			], className = 'descript-container'),
		], className = 'twelve columns'),
		html.Div([
			html.P('')
		], className = 'three columns'),
		html.Div([
			html.Div([
				dcc.Graph(id = 'ui_line')
			]),
		], className = 'six columns'),
		html.Div([
			dcc.Markdown('''
				*Source: US Department of Labor*
			''')
		], className = 'twelve columns')
	])


df_ui = pd.read_csv('data\\ui_claims\\ui.csv')
df_ui = df_ui.set_index('Filed week ended')
df_ui.index = pd.to_datetime(df_ui.index)

@app.callback(
	Output(component_id = 'ui_line', component_property = 'figure'),
	[Input(component_id = 'state_map', component_property = 'clickData')]
)
def update_ui(clicked_state):
	#fig_cliams ======================
	if clicked_state == None:
		fig_claims = go.Figure()
		df_ui_national = df_ui.groupby('Reflecting Week Ended').sum()
		df_ui_national.index = pd.to_datetime(df_ui_national.index)
		df_ui_national = df_ui_national.sort_index()
		for i in ['Initial Claims', 'Continued Claims']:
		    fig_claims.add_trace(
		        go.Scatter(x=df_ui_national.index,
		                   y=df_ui_national[i],
		                   name = i,
		                   line = {"width": 2.5},
		                    mode = 'lines',
		                  hovertemplate = 'y',
		                  showlegend = True),
		    )

		for i in ['Initial Claims', 'Continued Claims']:
		    fig_claims.add_trace(
		        go.Scatter(x = df_ui_national.resample('AS').first().index,
		                    y = df_ui_national[i].resample('AS').first(),
		                    marker={"size": 5, "line": dict(width =  1, color = 'DarkSlateGrey'), "color": "white"},
		                   mode = 'markers',
		                    hoverinfo = 'skip',
		                   showlegend = False
		        )
		    )

		# Add range slider
		fig_claims.update_layout(
			title = dict(
	 	        text = 'National Unemployment Insurance Claims',
	 	        xanchor = 'center',
	 	        x = 0.5,
	 	        yanchor = 'top',
	 	        y = 0.95,
	 	    ),
			hovermode = 'x unified',
			hoverdistance = 200,
			spikedistance = 200,
			legend=dict(
			        orientation="h",
			        yanchor="bottom",
			        y=1.1,
			        xanchor="right",
			        x=1.1
			    ),
			# margin = dict(
			#         l = 10,
			#         r = 10,
			#         t = 10,
			#         b = 10,
			#         pad = 0,
			# ),
			# width = 1200,
			height = 400,
			xaxis=dict(
			    range = ["1986-06-01 00:00:00", "2020-12-01 00:00:00"],
			    showspikes = True,
			    spikemode = 'across',
			    rangeselector=dict(
			        buttons=list([
			            dict(count=1,
			                 label="1m",
			                 step="month",
			                 stepmode="backward"),
			            dict(count=6,
			                 label="6m",
			                 step="month",
			                 stepmode="backward"),
			            dict(count=1,
			                 label="1y",
			                 step="year",
			                 stepmode="backward"),
			            dict(step="all")
			        ]),
			        xanchor = 'right',
			        x = 1.1,
			        y = 0.95,

			    ),
			    rangeslider=dict(
			        visible=True,
			        autorange = False,
			        range=["1986-01-01 00:00:00", "2021-05-01 00:00:00"],
			        thickness = 0.05
			    ),
			    type = 'date',
			    showgrid = False,
			),
			yaxis = dict(
			    #range = [0, 4*10**6],
			    zeroline = True,
			    showgrid = True,
			    gridcolor = 'rgb(159, 197, 232)',

			),
			plot_bgcolor = 'rgb(242, 242, 242)',
			paper_bgcolor = 'rgb(242, 242, 242)',
		)
	else:
		state_code = clicked_state['points'][0]['location']
		state = states_code_to_name_dict[state_code]

		fig_claims = go.Figure()

		df_ui_filtered = df_ui[df_ui['State'] == state]

		for i in ['Initial Claims', 'Continued Claims']:
		    fig_claims.add_trace(
		        go.Scatter(x=df_ui_filtered.index,
		                   y=df_ui_filtered[i],
		                   name = i,
		                   line = {"width": 2.5},
		                    mode = 'lines',
		                  hovertemplate = 'y',
		                  showlegend = True),
		    )

		for i in ['Initial Claims', 'Continued Claims']:
		    fig_claims.add_trace(
		        go.Scatter(x = df_ui_filtered.resample('AS').first().index,
		                    y = df_ui_filtered[i].resample('AS').first(),
		                    marker={"size": 5, "line": dict(width =  1, color = 'DarkSlateGrey'), "color": "white"},
		                   mode = 'markers',
		                    hoverinfo = 'skip',
		                   showlegend = False
		        )
		    )

		# Add range slider
		fig_claims.update_layout(
			title = dict(
	 	        text = '{State} Unemployment Insurance Claims'.format(State = state),
	 	        xanchor = 'center',
	 	        x = 0.5,
	 	        yanchor = 'top',
	 	        y = 0.95,
	 	    ),
			hovermode = 'x unified',
			hoverdistance = 200,
			spikedistance = 200,
			legend=dict(
			        orientation="h",
			        yanchor="bottom",
			        y=1.1,
			        xanchor="right",
			        x=1.1
			    ),
			# margin = dict(
			#         l = 10,
			#         r = 10,
			#         t = 10,
			#         b = 10,
			#         pad = 0,
			# ),
			# width = 1200,
			height = 400,
			xaxis=dict(
			    range = ["1986-06-01 00:00:00", "2020-12-01 00:00:00"],
			    showspikes = True,
			    spikemode = 'across',
			    rangeselector=dict(
			        buttons=list([
			            dict(count=1,
			                 label="1m",
			                 step="month",
			                 stepmode="backward"),
			            dict(count=6,
			                 label="6m",
			                 step="month",
			                 stepmode="backward"),
			            dict(count=1,
			                 label="1y",
			                 step="year",
			                 stepmode="backward"),
			            dict(step="all")
			        ]),
			        xanchor = 'right',
			        x = 1.1,
			        y = 0.95,

			    ),
			    rangeslider=dict(
			        visible=True,
			        autorange = False,
			        range=["1986-01-01 00:00:00", "2021-05-01 00:00:00"],
			        thickness = 0.05
			    ),
			    type = 'date',
			    showgrid = False,
			),
			yaxis = dict(
			    #range = [0, 4*10**6],
			    zeroline = True,
			    showgrid = True,
			    gridcolor = 'rgb(159, 197, 232)',

			),
			plot_bgcolor = 'rgb(242, 242, 242)',
			paper_bgcolor = 'rgb(242, 242, 242)',
		)
	#fig_cover ======================
	fig_cover = go.Figure()

	return fig_claims

#==============================================================================================================================================================================
def build_spending():
		return html.Div([
			html.Div([
				html.Div([
					html.H6('Consumer Spending'),
				], className = 'text-container'),
				html.Div([
					dcc.Markdown('''
					The national level consumer disposable income is displayed using the blue bars on top and consumer savings is displayed in red on the bottom.
					''')
				], className = 'descript-container')
			], className = 'twelve columns'),
			html.Div([
				html.P('')
			], className = 'three columns'),
			html.Div([
				html.Div([
					dcc.Graph(figure = fig)
				])
			], className = 'six columns'),
			html.Div([
				dcc.Markdown('''
				*Source: US Department of Commerce*
				''')
			])
		])
df_spending = pd.read_csv('data\consumer_spending\consumer_spending_cleaned.csv')
df_spending['date'] = pd.to_datetime(df_spending['date'])
df_spending = df_spending.set_index('date')
df_spending = df_spending.apply(pd.to_numeric)

def build_spending_graphs():
	fig = go.Figure()
	fig.add_trace(
	    go.Bar(
	        x = df_spending.index,
	        y = df_spending['disposable_income'],
	        name = 'Disposable Income',
	    )
	)
	fig.add_trace(
	    go.Bar(
	        x = df_spending.index,
	        y = (-1)*df_spending['saving'],
	        name = 'Saving'
	    )
	)

	fig.update_layout(
	    title = dict(
	        text = 'Average Monthly Personal Income and Disposition',
	        xanchor = 'center',
	        x = 0.5,
	        yanchor = 'top',
	        y = 1,
	        pad = dict(
				t = 1,
	            b = 1,
	        )
	    ),
	    barmode = 'relative',
	    hovermode = 'x unified',
	        hoverdistance = 200,
	        spikedistance = 200,
	        legend=dict(
	                orientation="h",
	                yanchor="bottom",
	                y=1,
	                xanchor="right",
	                x=1
	            ),
	        margin = dict(
	                l = 10,
	                r = 10,
	                t = 10,
	                b = 10,
	                pad = 0,
	        ),
	        #width = 450,
	        height = 300,
	        xaxis=dict(
	            range=["2018-07-01 00:00:00", "2021-01-01 00:00:00"],
	             showspikes = True,
	              spikemode = 'across',
	            rangeslider=dict(
	                visible=True,
	                autorange=False,
	                range=["2018-01-01 00:00:00", "2021-05-01 00:00:00"], #the actual range is ["1976-01-01 00:00:00", "2020-05-01 00:00:00"]
	                thickness = 0.05
	            ),
	            type="date"
	        ),
	        yaxis = dict(
	            #range = [0, 4*10**6],
	            zeroline = True,
	            showgrid = True,
	            gridcolor = 'rgb(159, 197, 232)',
	            tickmode = 'array',
	            tickvals = [-5000, 0, 5000, 10000, 15000, 20000],
	            ticktext = ['5k', 0, '5k', '10k', '15k', '20k']

	        ),
	        # yaxis2 = dict(
	        #     #range = [0, 0.2],
	        #     side = 'right',
	        #     overlaying = 'y',
	        #     scaleanchor="y",
	        #     scaleratio=1,
	        # 	showgrid = False
	        # ),
	        plot_bgcolor = 'rgb(242, 242, 242)',
	        paper_bgcolor = 'rgb(242, 242, 242)',
	)

	return fig

fig = build_spending_graphs()

#==============================================================================================================================================================================
df_jolts = pd.read_csv("data\jolts\jolts_05mb.csv")
def build_jolts():
	return html.Div([
		html.Div([
			html.Div([
				html.H6('Job Openings and Labor Turnover'),
			], className = 'text-container'),
			html.P('Add some introductions here'),
		], className = 'twelve columns'),
		html.Div([
			html.P('Select Start Year'),
			dcc.Dropdown(id = 'jolts_start_dropdown',
						options = [{'label': i, 'value': i} for i in df_jolts.columns.values.tolist()[1:]],
						value = 'Jan-20'
						),
		], className = 'six columns'),
		html.Div([
			html.P('Select End Year'),
			dcc.Dropdown(id = 'jolts_end_dropdown',
						options = [{'label': i, 'value': i} for i in df_jolts.columns.values.tolist()[1:]],
						value = 'Apr-20')
		], className = 'six columns'),
		html.Div([
			dcc.Graph(id = 'jolts_line_1')
		], className = 'twelve columns')
	])
@app.callback(
	[Output(component_id = 'jolts_start_dropdown', component_property = 'options'),
	Output(component_id = 'jolts_end_dropdown', component_property = 'options'),
	Output(component_id = 'jolts_line_1', component_property = 'figure')],
	[Input('jolts_start_dropdown', 'value'),
	Input('jolts_end_dropdown', 'value')]
)
def update_jolts(selected_start, selected_end):
	months = df_jolts.columns.values.tolist()[1:]
	options_start = [{'label': i, 'value': i} for i in months]
	options_end = [{'label': i, 'value': i} for i in months[months.index(selected_start)+ 1:]]

	fig = go.Figure()
	for i in df_jolts.industry.values.tolist():
		fig.add_trace(go.Scatter(x = months[months.index(selected_start): months.index(selected_end)],
								y = df_jolts[df_jolts.industry == i].loc[:,selected_start:selected_end].values.tolist()[0],
								name = i,
								line=dict(width=1)
								))
	fig.update_layout(
		title_text = 'Layoff Estimation by Industry',
		margin = dict(
			l = 30,
			r = 30,
			b = 30,
			t = 30
		),
		plot_bgcolor = 'rgb(250, 250, 250)',
		#paper_bgcolor = 'rgb(250, 250, 250)'
	)
	return options_start, options_end, fig



#==============================================================================================================================================================================
def build_news():
	return html.Div([
		html.Div([
			html.Div([
				html.H6('Labor Market News'),
			], className = 'text-container'),
			html.P('Add some introductions here'),
		], className = 'twelve columns')
	])
#==============================================================================================================================================================================
all_sectors = ['Basic_Materials_Sector', 'Communication_Services_Sector', 'Consumer_Cyclical_Sector', 'Consumer_Defensive_Sector', 'Energy_Sector',
         'Financial_Services_Sector', 'Healthcare_Sector', 'Industrials_Sector', 'Real_Estate_Sector', 'Technology_Sector',
         'Utilities_Sector']
sector_type_options = [{'label': i, 'value': i} for i in all_sectors]

dict_sector_shortnames = {'Basic_Materials_Sector': 'bm', 'Communication_Services_Sector':'comm', 'Consumer_Cyclical_Sector':'conc', 'Consumer_Defensive_Sector':'cond','Energy_Sector':'energy',
         'Financial_Services_Sector': 'fin', 'Healthcare_Sector':'hc', 'Industrials_Sector':'ind', 'Real_Estate_Sector':'real', 'Technology_Sector': 'tech',
         'Utilities_Sector': 'u'}
def build_stock():
	return html.Div([
		html.Div([
			html.Div([
				html.H6('Stock Market'),
			], className = 'text-container'),
		], className = 'twelve columns'),
		html.Div([
			html.P("Filter by Sector:"),
	        dcc.RadioItems(
	            id="sector_type_selector",
	            options=[
	                {"label": "All ", "value": "all"},
	               {"label": "Default ", "value": "most"},
	                {"label": "Customize ", "value": "custom"},
	            ],
	            value="most",
	            labelStyle={"display": "inline-block"},
	            className="dcc_control",
	        ),
			dcc.Dropdown(
			                id="sector_types",
			                options=sector_type_options,
			                multi=True,
			                value= ['Technology_Sector', 'Healthcare_Sector'],
			                # className="dcc_control",
			            ),
		], className = 'four columns'),

		html.Div([
			dcc.Graph(id = 'stock_line')
		], className = 'eight columns'),
		html.Div([
			dcc.Markdown('''
			*Source: Yahoo Finance*
			''')
		], className = 'twelve columns'),
	])

@app.callback(
Output('sector_types', 'value'),
[Input('sector_type_selector', 'value')]
)
def update_sector_dropdown(selected_type):
	if selected_type == 'all':
		return all_sectors
	if selected_type == 'most':
		return ['Energy_Sector']
	if selected_type == 'custom':
		return None


@app.callback(
Output('stock_line', 'figure'),
[Input('sector_types', 'value')]
)
def update_stock(sector_types):
	if sector_types == None:
		sector_palette = {'Basic_Materials_Sector': 'rgba(160, 160, 160, 0.2)', 'Communication_Services_Sector': 'rgba(160, 160, 160, 0.2)', 'Consumer_Cyclical_Sector':'rgba(160, 160, 160, 0.2)',
						'Consumer_Defensive_Sector': 'rgba(160, 160, 160, 0.2)', 'Energy_Sector': 'rgba(160, 160, 160, 0.2)',
						'Financial_Services_Sector':'rgba(160, 160, 160, 0.2)', 'Healthcare_Sector': 'rgba(160, 160, 160, 0.2)', 'Industrials_Sector': 'rgba(160, 160, 160, 0.2)',
						'Real_Estate_Sector':'rgba(160, 160, 160, 0.2)', 'Technology_Sector': 'rgba(160, 160, 160, 0.2)', 'Utilities_Sector':'rgba(160, 160, 160, 0.2)'}
	else:
		sector_palette = {'Basic_Materials_Sector': 'rgb(15, 76, 129)', 'Communication_Services_Sector': 'rgb(141, 0, 69)', 'Consumer_Cyclical_Sector':'rgb(214, 165, 0)',
					'Consumer_Defensive_Sector': 'rgb(0, 141, 155)', 'Energy_Sector': 'rgb(221, 167, 155)',
					'Financial_Services_Sector':'rgb(240, 150, 12)', 'Healthcare_Sector': 'rgb(20, 57, 79)', 'Industrials_Sector': 'rgb(187, 216, 104)',
					'Real_Estate_Sector':'rgb(73, 12, 137)', 'Technology_Sector': 'rgb(19, 97, 125)', 'Utilities_Sector':'rgb(230, 212, 200)'}


	fig = go.Figure()
	colors = sector_palette
	for sec in all_sectors:
		if sector_types == None:
			pass
		elif sec in sector_types:
			pass
		else:
			colors[sec] = 'rgba(160, 160, 160, 0.2)'
	for sec in all_sectors:
		file_name = 'df_{sec_short}.pkl'.format(sec_short = dict_sector_shortnames[sec])
		df = pd.read_pickle('data\stock_revenue\{file_name}'.format(file_name = file_name))
		fig.add_trace(go.Scatter(
		    x = df.groupby('Date')['standardized_open'].mean().index,
		    y = df.groupby('Date')['standardized_open'].mean(),
		    line = dict(color = colors[sec]),
		    name = sec,
			hoverinfo = 'skip'
		 ))

	fig.update_layout(
	   title = dict(
	        text = 'Standardized Stock Value by Sectors',
	        xanchor = 'center',
	        x = 0.5,
	        yanchor = 'top',
	        y = 1,
	        # pad = dict(
	        #     # b = 15,
			# 	# t = 15
	        # )
	    ),
	#     marker = dict(line = dict(color = colors)),
	    hovermode = 'x unified',
	    hoverdistance = 200,
	    spikedistance = 200,
	    legend=dict(
	            orientation="h",
	            yanchor="bottom",
	            y= 1,
	            xanchor="right",
	            x=1.1
	        ),
	    margin = dict(
	            l = 25,
	            r = 25,
	            t = 25,
	            b = 25,
	            pad = 0,
	    ),
	    height = 400,
	    xaxis=dict(
	        range = ["2019-03-01 00:00:00", "2020-12-01 00:00:00"],
	        showspikes = True,
	        spikemode = 'across',
	        rangeselector=dict(
	            buttons=list([
	                dict(count=1,
	                     label="1m",
	                     step="month",
	                     stepmode="backward"),
	                dict(count=6,
	                     label="6m",
	                     step="month",
	                     stepmode="backward"),
	                dict(count=1,
	                     label="1y",
	                     step="year",
	                     stepmode="backward"),
	                dict(step="all")
	            ]),
	            xanchor = 'left',
	            x = 0.9,
	            y = 0.9
	        ),
	        rangeslider=dict(
	            visible=True,
	            autorange = False,
	            range=["2015-01-01 00:00:00", "2021-05-01 00:00:00"],
	            thickness = 0.05
	        ),
	        type = 'date',
	        showgrid = False,
	    ),
	    yaxis = dict(
	        #range = [0, 4*10**6],
			title = 'Standardized Average Price',
	        zeroline = True,
	        showgrid = True,
	        gridcolor = 'rgb(159, 197, 232)',

	    ),
	    plot_bgcolor = 'rgb(242, 242, 242)',
	    paper_bgcolor = 'rgb(242, 242, 242)',
	)

	return fig
#
# @app.callback(
# Output('stock_line', 'figure'),
# [Input('intermediate_colors_dict', 'children')]
# )
# def update_colors(hovered_sector):
# 	fig.update_traces(line = dict(color = 'firebrick'),
# 					selector = dict(name = 'colors_dict'))
# 	return fig

# @app.callback(
# Output('intermediate_colors_dict', 'children'),
# [Input('stock_line', 'hoverData')]
# )
# def update_stock(hover_data):
# 	if hover_data == None:
# 		sector_name = 'temp'
# 	else:
# 		sector_id = hover_data['points'][0]['curveNumber']
# 		sector_name = all_sectors[sector_id]
# 	colors = {}
# 	for sec in all_sectors:
# 		if sec == sector_name:
# 			colors[sec] = 'firebrick'
# 		else:
# 			colors[sec] = 'rgba(160, 160, 160, 0.2)'
#
# 	return colors

# def build_tabs():
#     return html.Div([
#             dcc.Tabs(
#                 id="app_tabs",
#                 value="tab1",
#                 #className="custom-tabs",
#                 children=[
#                 	dcc.Tab(
#                         id="summary_tab",
#                         label="National Labor Statistics",
#                         value="tab1",
#                         #className="custom-tab",
#                         #selected_className="custom-tab--selected",
#                     ),
#                     dcc.Tab(
#                         id="unemp_tab",
#                         label="CES data",
#                         value="tab2",
#                         #className="custom-tab",
#                         #selected_className="custom-tab--selected",
#                     ),
#                     dcc.Tab(
#                         id="ui_tab",
#                         label="State Data",
#                         value="tab3",
#                         #className="custom-tab",
#                         #selected_className="custom-tab--selected",
#                     ),
#                     dcc.Tab(
#                         id="stock_tab",
#                         label="City Data",
#                         value="tab4",
#                         #className="custom-tab",
#                         #selected_className="custom-tab--selected",
#                     ),
#                     dcc.Tab(
#                         id="spending_tab",
#                         label="Industries",
#                         value="tab5",
#                         #className="custom-tab",
#                         #selected_className="custom-tab--selected",
#                     ),
#                     dcc.Tab(
#                         id="cpi_tab",
#                         label="occupations",
#                         value="tab6",
#                         #className="custom-tab",
#                         #selected_className="custom-tab--selected",
#                     ),
#
#                 ],
#             ),
#         ], className = 'twelve columns'
#     )
# @app.callback(
# 	Output(component_id = 'app_content', component_property = 'children'),
# 	[Input('app_tabs', 'value')])
# def render_tab_content(tab_switch):
# 	if tab_switch == 'tab1':
# 		return build_summary()
# 	if tab_switch == 'tab2':
# 	 	return build_unemp()
# 	if tab_switch == 'tab3':
# 	 	return build_ui()
# 	if tab_switch == 'tab4':
# 		return build_stock()
# 	if tab_switch == 'tab5':
# 		return build_spending()
# 	if tab_switch == 'tab6':
# 		return build_cpi()

app.layout = html.Div([
		html.Div([
		build_banner(),
		build_summary(),
		build_unemp(),
		build_ui(),
		build_stock(),
		build_spending(),
		build_cpi(),
		# build_jolts(),
		# build_news(),
		])
	])


# app.layout = html.Div(
# 	id = 'big_app_container',
# 	children = [build_banner(),
#
# 				html.Div(
# 					id = 'app_container',
# 					children = [
# 						build_tabs(),
# 						#main_app
# 						html.Div(id = 'app_content'),
# 					]
# 				),
#
#
# 				html.Hr(),
# 				#html.Div(id = 'display_selected_values')
#
# 	], className = 'mainContainer',
# 	style = {'display': 'flex', 'flex-direction': 'column'},
# )



if __name__ == '__main__':
	app.run_server(debug = True, port = 1110)
