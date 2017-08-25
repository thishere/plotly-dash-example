# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import csv


def readFromCsv(csv_name):
	all_data = []
	with open('%s.csv' % csv_name, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			all_data.append(row)
	return all_data

def getDashData():

	all_data = readFromCsv('campaign_data')

	ig_handles = []
	images = []
	campaigns = []
	post_ids = []
	post_urls = []
	date_posteds = []
	country = []
	likes = []
	comment_nos = []
	post_engagements = []
	expected_engagements = []
	engagement_ratios = []

	for row in all_data[1:]:
		ig_handles.append(row[0])
		images.append(row[1])
		campaigns.append(row[2])
		post_ids.append(row[3])
		date_posteds.append(row[4])
		country.append(row[5])
		likes.append(int(row[6]))
		comment_nos.append(int(row[7]))
		post_engagements.append(float(row[8]))
		expected_engagements.append(float(row[9]))
		engagement_ratios.append(float(row[10]))


	data = {'IG HANDLE': ig_handles,
	        'IMAGE': images,
	        'CAMPAIGN': campaigns,
	        'POST ID': post_ids,
	        'DATE POSTED': date_posteds,
	        'COUNTRY': country,
	        'LIKES': likes,
	        'COMMENTS': comment_nos,
	        'ENGAGEMENT RATE': post_engagements,
	        'EXPECTED ENGAGEMENT': expected_engagements,
	        'ENGAGEMENT RATIO': engagement_ratios}

	return pd.DataFrame(data)

app = dash.Dash()

df = getDashData()

metrics = ["LIKES","COMMENTS","ENGAGEMENT RATE","EXPECTED ENGAGEMENT","ENGAGEMENT RATIO"]
campaigns = ["TFWGucci","DG Millennials","Bridging The Gap"]

colour_dict = {}
colour_dict["TFWGucci"] = 'rgb(240,21,22)'
colour_dict["DG Millennials"] = 'rgb(22,96,185)'
colour_dict["Bridging The Gap"] = 'rgb(6,193,95)'

external_css = [ "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
        "//fonts.googleapis.com/css?family=Raleway:400,300,600",
        "https://cdn.rawgit.com/plotly/dash-app-stylesheets/5047eb29e4afe01b45b27b1d2f7deda2a942311a/goldman-sachs-report.css",
        "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({ "external_url": css })


app.layout = html.Div([
				html.Div([
					html.Div([
						html.H6('Choose Metric:', className = "gs-header gs-text-header padded")
						],
						style={'width': '25%', 'display': 'inline-block'}
					),
					html.Div([
						html.H6('Choose Campaign:', className = "gs-header gs-text-header padded")
						],
						style={'width': '50%', 'display': 'inline-block'}
					),
					html.Div([
						html.H6('Choose Country:', className = "gs-header gs-text-header padded")
						],
						style={'width': '25%', 'display': 'inline-block'}
					),
				]),
				html.Div([
					html.Div([
						dcc.Dropdown(
							id='yaxis-column',
							options=[{'label': i, 'value': i} for i in metrics],
							value='ENGAGEMENT RATIO')
						],
						style={'width': '25%', 'display': 'inline-block'}
					),
					html.Div([
						dcc.Dropdown(
							id='campaign-selection',
							options=[{'label': i, 'value': i} for i in campaigns],
							multi=True,
							value=campaigns)
						],
						style={'width': '50%', 'display': 'inline-block'}
					),
					html.Div([
						dcc.Dropdown(
							id='country-selection',
							value='All')
						],
						style={'width': '25%', 'display': 'inline-block'}
					)
				]),
				html.Div([
					html.Div([
						dcc.Graph(id='main-graph')
						],
						style={'width': '100%', 'display': 'inline-block'}
					),
				],
				className='row'
				),
				html.Div([
					html.Div([
						html.H6('Selected Post:', className = "gs-header gs-text-header padded")
						],
						style={'width': '100%', 'display': 'inline-block'}
					)
				]),
				html.Div([
					html.Div([
						html.A([
							html.Img(id='selected-post-image',
									style={'position': 'relative',
										   'height' : '200',
										   'width' : '200',
										   'left' : '30%',
										   'top' : '30'})
							],
							id='selected-post-hyperlink',
							target='_blank'
						)
					],style={'width': '50%', 'display': 'inline-block'}
					),
					html.Div([
						html.A([
							html.H5(id='selected-ig-handle')
							],
							id='selected-ig-handle-hyperlink',
							target='_blank',
							className='column',
							style={'position': 'relative',
								   'left' : '27%',
								   'top' : '5'}
						),
						html.H5(id='selected-likes',
								className='column',
								style={'position': 'relative',
									   'left' : '25%',
									   'top' : '5'}
						),
						html.H5(id='selected-comments',
								className='column',
								style={'position': 'relative',
									   'left' : '25%',
									   'top' : '5'}
						),
						html.H5(id='selected-engagement-rate',
								className='column',
								style={'position': 'relative',
									   'left' : '25%',
									   'top' : '5'}
						),
						html.H5(id='selected-engagement-ratio',
								className='column',
								style={'position': 'relative',
									   'left' : '25%',
									   'top' : '5'}
						)
					],style={'width': '25%', 'display': 'inline-block','position': 'relative'}
					)
				]),
				html.Div([
					html.Div([
						html.H6('', className = "gs-header gs-text-header padded")
						],
						style={'width': '100%', 'display': 'inline-block','margin-top' : '45'}
					)
				])
			])


@app.callback(
    Output('country-selection', 'options'),
    [dash.dependencies.Input('campaign-selection', 'value')])
def populate_country_selection(campaign_selection):
	country_list = ["All"]
	for campaign in campaign_selection:
		campaign_df = df[df['CAMPAIGN'] == campaign]
		campaign_country_list = campaign_df['COUNTRY'].unique()
		country_list.extend([i for i in campaign_country_list])
	return [{'label': i, 'value': i} for i in country_list]

'''*****************************************************************************************
Selected Post functions
*******************************************************************************************'''	
@app.callback(
    Output('selected-post-image', 'src'),
    [Input('main-graph', 'clickData'),
    dash.dependencies.Input('campaign-selection', 'value'),
     dash.dependencies.Input('country-selection', 'value')])
def display_selected_post_image(clickData,
				 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return df_campaign[df_campaign['POST ID'] == post_id]["IMAGE"].unique()
	return None

@app.callback(
	Output('selected-ig-handle', 'children'),
	[Input('main-graph', 'clickData'),
	dash.dependencies.Input('campaign-selection', 'value'),
	dash.dependencies.Input('country-selection', 'value')])
def display_selected_ig_handle(clickData,
				 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return df_campaign[df_campaign['POST ID'] == post_id]["IG HANDLE"]
	return None

@app.callback(
    Output('selected-ig-handle-hyperlink', 'href'),
    [Input('main-graph', 'clickData'),
    dash.dependencies.Input('campaign-selection', 'value'),
     dash.dependencies.Input('country-selection', 'value')])
def display_selected_ig_handle_hyperlink(clickData,
				 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return "https://www.instagram.com/" + df_campaign[df_campaign['POST ID'] == post_id]["IG HANDLE"]
	return None

@app.callback(
    Output('selected-likes', 'children'),
    [Input('main-graph', 'clickData'),
     dash.dependencies.Input('campaign-selection', 'value'),
     dash.dependencies.Input('country-selection', 'value')])
def display_selected_likes(clickData,
				 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return "{:,}".format(df_campaign[df_campaign['POST ID'] == post_id]["LIKES"].values[0]) + " Likes"
	return None


@app.callback(
    Output('selected-comments', 'children'),
    [Input('main-graph', 'clickData'),
    dash.dependencies.Input('campaign-selection', 'value'),
     dash.dependencies.Input('country-selection', 'value')])
def display_selected_comments(clickData,
				 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return "{:,}".format(df_campaign[df_campaign['POST ID'] == post_id]["COMMENTS"].values[0]) + " Comments"
	return None

@app.callback(
    Output('selected-engagement-rate', 'children'),
    [Input('main-graph', 'clickData'),
    dash.dependencies.Input('campaign-selection', 'value'),
     dash.dependencies.Input('country-selection', 'value')])
def display_selected_engagement_rate(clickData,
				 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return "{:.2f}".format(df_campaign[df_campaign['POST ID'] == post_id]["ENGAGEMENT RATE"].values[0]) + "% Eng. Rate"
	return None

@app.callback(
    Output('selected-engagement-ratio', 'children'),
    [Input('main-graph', 'clickData'),
    dash.dependencies.Input('campaign-selection', 'value'),
     dash.dependencies.Input('country-selection', 'value')])
def display_selected_engagement_ratio(clickData,
				 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return "{:.2f}".format(df_campaign[df_campaign['POST ID'] == post_id]["ENGAGEMENT RATIO"].values[0]) + " Eng. Ratio"
	return None

@app.callback(
    Output('selected-post-hyperlink', 'href'),
    [Input('main-graph', 'clickData'),
    dash.dependencies.Input('campaign-selection', 'value'),
     dash.dependencies.Input('country-selection', 'value')])
def display_selected_post_hyperlink(clickData,
					 				campaign_selection,
				 				country_selection):
	if clickData:
		try:
			post_id = clickData["points"][0]["customdata"]
		except KeyError:
			return None
		if country_selection == 'All':
			df_country = df
		else:
			df_country = df[df['COUNTRY'] == country_selection]
		if campaign_selection:
			df_campaigns = [df_country[df_country['CAMPAIGN'] == i] for i in campaign_selection]
			for df_campaign in df_campaigns:
				if post_id in df_campaign['POST ID'].values:
					return "https://www.instagram.com/p/"+post_id
	return None

'''*****************************************************************************************
Graph functions
*******************************************************************************************'''	

@app.callback(
	dash.dependencies.Output('main-graph', 'figure'),
	[dash.dependencies.Input('yaxis-column', 'value'),
	 dash.dependencies.Input('campaign-selection', 'value'),
	 dash.dependencies.Input('country-selection', 'value'),
	 Input('main-graph', 'clickData')])
def update_graph(yaxis_column_name,
				 campaign_selection,
				 country_selection,
				 clickData):

	if country_selection == 'All':
		df_country = df
	else:
		df_country = df[df['COUNTRY'] == country_selection]

	if campaign_selection:
		if clickData:
			try:
				post_id = clickData["points"][0]["customdata"]
			except KeyError:
				post_id = None
		else:
			post_id = None

		df_campaigns = []
		for campaign in campaign_selection:
			df_campaigns.append(df_country[df_country['CAMPAIGN'] == campaign])

		df_post = pd.DataFrame()
		for df_campaign in df_campaigns:
			if post_id in df_campaign['POST ID'].values:
				df_post = df_campaign[df_campaign['POST ID'] == post_id]
				break

		max_y = 0.0
		min_y = 100000000000000000.0

		data = []
		colour_count = 0
		for df_campaign in df_campaigns:
			data.append(go.Scatter( x=df_campaign["DATE POSTED"],
									y=df_campaign[yaxis_column_name], 
									customdata = df_campaign["POST ID"],
									mode='markers',
									name=campaign_selection[colour_count],
									marker=dict(
										color=colour_dict[campaign_selection[colour_count]],
									),
									text=df_campaign['IG HANDLE'],
									opacity=0.6
								))
			try:
				max_x = max(df_campaign["DATE POSTED"])
				min_x = min(df_campaign["DATE POSTED"])
				average = df_campaign[yaxis_column_name].mean()
				data.append(go.Scatter( x=[min_x,max_x],
										y=[average,average],
										mode='lines',
										name=campaign_selection[colour_count],
										marker=dict(
											color=colour_dict[campaign_selection[colour_count]],
										),
										opacity=0.6,
										showlegend=False
									))
				if df_campaign[yaxis_column_name].max() > max_y: max_y = df_campaign[yaxis_column_name].max()
				if df_campaign[yaxis_column_name].min() < min_y: min_y = df_campaign[yaxis_column_name].min()
			except ValueError:
				pass
			colour_count+=1
		
		y_axis_range = [0.0,1.1*max_y]

		if not df_post.empty:
			data.append(go.Scatter( x=df_post["DATE POSTED"],
									y=df_post[yaxis_column_name],
									customdata = df_post["POST ID"],
									mode='markers',
									name='Selected Post',
									marker=dict(color='rgb(0,0,0)'),
									opacity=1.0,
									showlegend=False))
		figure = {	'data': data,
					'layout': go.Layout(title='',
										showlegend=True,
										hovermode='closest',
										legend=dict(orientation="h",
													x=0,
													y=100),
										yaxis=dict(range=y_axis_range))
				 }
		return figure
	else:
		return None


if __name__ == '__main__':
    app.run_server(debug=True)
