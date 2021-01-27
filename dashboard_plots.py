"""Visualizations(plotly) for flask dashboard."""
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json
import math
import pandas as pd

def get_bubbleSize(data):
    """
    Returns bubble size for selected countries
    Input - dataframe=data
    """
    hover_text = []
    bubble_size = []

    for index, row in data.iterrows():
        hover_text.append(('Country: {country}<br>'+
                           'Region: {region}<br>'+
                          'Budget: {value}<br>'+
                          'Year: {year}').format(country=row['country'],
                                                 region=row['region'],
                                                value=row['value'],
                                                year=row['year']))
        bubble_size.append(math.sqrt(row['value']))

    data['text'] = hover_text
    data['size'] = bubble_size
    return data


def create_bubbleChart(data):
    """
    Returns plotly bubbleChart in json format
    Input - dataframe=data
    """
    
    # Create figure
    fig = go.Figure()
    
    data1=get_bubbleSize(data)   
    
    data1 = data1.sort_values(['region', 'country'])
    region_name = list(data1.region.unique())
    region_data = {region:data1.query("region == '%s'" %region)
                              for region in region_name}

    
    for region_name, region in region_data.items():
        fig.add_trace(go.Scatter(
            x=region['CenterLongitude'], y=region['CenterLatitude'],
            name=region_name, text=region['text'],
            marker_size=region['size'],
            )
          )

    # Tune marker appearance and layout
    if len(data1['size']):
        fig.update_traces(mode='markers', marker=dict(sizemode='area', 
                                                  sizeref=(lambda x: 2.*max(x)/(100**2))(data1['size']), line_width=2), showlegend=True)

    fig.update_layout(
        title='Satellites budget in millions USD',
        xaxis=dict(

            gridcolor='rgb(243, 243, 243)',
            type='linear',
            gridwidth=2,
        ),
        yaxis=dict(
        
        gridcolor='rgb(243, 243, 243)',
        gridwidth=2,
    ),
    #paper_bgcolor='rgb(243, 243, 243)',
    #plot_bgcolor='rgb(243, 243, 243)',
    paper_bgcolor='white',
    plot_bgcolor='white',
    yaxis_range=[-150.0,150.0]
    )

    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
    

def create_table(df):
    """
    Returns plotly data table in json format
    Input - dataframe=df
    """
    table = go.Figure([go.Table(
        columnorder = [1,2,3,4,5,6],
        columnwidth = [140,80,140,140,100,100],
        header=dict(
            values=df.columns.str.replace('_',' '),
            line_color='darkslategray',
            align='left',
            height=40
        ),
        cells=dict(
            values=[df[k].tolist() for k in df.columns],
            align = "left",
            line_color='darkslategray',
            fill_color='whitesmoke',
            font=dict(color='midnightblue', size=12))
        
        )
        
    ])
 
    #table.update_layout(
    #    autosize=True,
    #    height=600,
    #)
    #tableJSON = json.dumps(table, cls=plotly.utils.PlotlyJSONEncoder)

    #return tableJSON
    return table

def get_groupedYearData(country,df):
    """
    Returns dataframe filtered by country and grouped by year (for lineCharts)
    Inputs - country=country, dataframe=data
    """
    grouped_df = df[df['country'] == country].groupby('year')['value'].sum().reset_index()
    return grouped_df

def create_lineChart(df):       
    """
    Returns plotly lineChart in json format
    Input - dataframe=df
    """
    #fig = go.Figure()
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "table"} , {"type": "scatter"}]])

    #table = create_table(df)
    fig.add_trace(
        go.Table(
            columnorder = [1,2,3,4,5,6,7,8],
            columnwidth = [150,120,150,150,150,150,150,150],
            header=dict(
                values=df.columns.str.replace('_',' '),
                line_color='darkslategray', fill_color='#fc5e61',
                align='left', font=dict(color='white', size=10),
                height=40
            ),
            cells=dict(
                values=[df[k].tolist() for k in df.columns],

                align = "left",
                line_color='darkslategray',
                fill_color='white',
                font=dict(color='midnightblue', size=10)

            )
        ), 
        row=1, col=1
    )
               
    for name in list(df.country.unique()):
        data = get_groupedYearData(name,df)
        fig.add_trace(go.Scatter(x=data['year'], y=data['value'],
                    mode='lines',
                    name=name), row=1, col=2)
       


    fig.update_layout(
        title='Evolution of Budget for each country',
        xaxis=dict(

            gridcolor='rgb(243, 243, 243)',
            type='linear',
            gridwidth=2,
        ),
        yaxis=dict(
        
        gridcolor='rgb(243, 243, 243)',
        gridwidth=2,
    ),
     paper_bgcolor='white',
     plot_bgcolor='white',
     height=700
    )
    
    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1year",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def create_satellite_table(df):
    """
    Returns plotly data table in json format
    Input - dataframe=df
    """
    table = go.Figure(data=[go.Table(
      columnorder = [i for i,col in enumerate(list(df.columns))],
      columnwidth = [120 for i,col in enumerate(list(df.columns))],
      header=dict(
        values=[f"<b>{k}<b>" for k in df.columns],

        line_color='rgb(8, 81, 156)', fill_color='#fc5e61',

        align='left', font=dict(color='white', size=10)
      ),
      cells=dict(
        values=[df[k].tolist() for k in df.columns],
        line_color='white', fill_color='white',
        align='left', font=dict(color='#023161', size=10)
      ))
    ])
    table.update_layout(
        autosize=True,
        height=1000,
    )
    
    tableJSON = json.dumps(table, cls=plotly.utils.PlotlyJSONEncoder)

    return tableJSON

    