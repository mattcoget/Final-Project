"""Visualizations(plotly) for flask dashboard."""
import plotly
import plotly.graph_objs as go
import json

def create_table(df):

    table = go.Figure([go.Table(
        header=dict(
            values=df.columns,
            line_color='darkslategray',
            fill_color='royalblue',
            align=['left','center'],
            font=dict(color='white', size=12),
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
 
    table.update_layout(
        autosize=True,
        height=500,
    )
    tableJSON = json.dumps(table, cls=plotly.utils.PlotlyJSONEncoder)

    return tableJSON

def create_plot(df):    

    plot = go.Figure([go.Scatter( 
        x=df['country'], # assign x as the dataframe column 'x'
        y=df['value'],
        mode='markers') 
    ]) 
    # Add dropdown 
    plot.update_layout( 
        updatemenus=[ 
            dict( 
                buttons=list([ 
                    dict( 
                        args=["type", "scatter"], 
                        label="Scatter Plot", 
                        method="restyle"
                    ), 
                    dict( 
                        args=["type", "bar"], 
                        label="Bar Chart", 
                        method="restyle"
                    ) 
                ]), 
                direction="down", 
            ), 
        ] 
    )

    graphJSON = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON