"""Interactive flask/plotly dashboard"""
from flask import Flask, render_template,request , send_file, send_from_directory, make_response, Response, redirect,jsonify
import os
import io
import pandas as pd
import numpy as np
import webbrowser
from threading import Timer
import logging
from dashboard_plots import *


class DashboardDB:
 
    def __init__(self):
        self.indicator = 'Budget'
        self.df=None

    def setDataFrame(self, df1, df2):
        self.budget = df1
        self.df =  df1
        self.satellite = df2
        
    def changeIndicator(self, indicator):
        self.indicator = indicator
        self.df = self.budget if indicator == 'Budget' else self.satellite
        
    def filterDataFrame(self,cols):
        self.df = self.budget[cols] if self.indicator == 'Budget' else self.satellite[cols]
        
    def getIndicator(self):
        return self.indicator
    
    def getDataFrame(self):
        return self.df

    
budget = pd.read_csv('data/clean_budget.csv')
satellite = pd.read_csv('data/clean_satellite.csv')

db = DashboardDB()
db.setDataFrame(budget, satellite)

app = Flask(__name__)

def create_selector(columns):
    indicator = db.getIndicator()
    origin_columns = db.budget.columns if indicator == 'Budget' else db.satellite.columns
    
    selector = ""
    for name in origin_columns:
        checked = 'checked' if name in columns else 'unchecked'
        selector += f'<li><input value="{name}" type="checkbox" class="columnSelector" {checked}/>{name} </li>'
    return selector

@app.route('/')
def index():
    df = db.getDataFrame()
    bar = create_plot(db.budget)
    table = create_table(df)
    selector = create_selector(df.columns)
    return render_template('index.html', table=table, plot=bar, selector=selector)

@app.route('/plot', methods=['GET', 'POST'])
def change_features():
    feature = request.args['selected']
    feature_type = request.args['type']
    print(feature_type)
    print(feature)
    if feature_type == "indicators":

        if feature == 'Satellite' or feature == 'Budget':
            indicator=feature
            db.changeIndicator(indicator)
        df = db.getDataFrame()
        selector = create_selector(df.columns)

        tableJSON = create_table(df)       
        return jsonify(table=tableJSON,selector=selector)
    
    elif feature_type == "attributes":
        columns = request.args['selected'].strip(',').split(",")
        print(columns)
        db.filterDataFrame(columns)     
        df = db.getDataFrame()
        tableJSON = create_table(df)
        
        return tableJSON


@app.route('/download', methods=['GET', 'POST'])
def download():
    # stream the response as the data is generated
    indicator = db.getIndicator()
    df = db.getDataFrame()
    print("download file ...",indicator)
    file_type = request.args.get('type')
    
    try:
        if file_type == 'csv':
            response = make_response(df.to_csv())
            response.headers["Content-Disposition"] = f"attachment; filename={indicator}.csv"
            response.headers["Content-Type"] = "text/csv"
            
        else:
            
            out = io.BytesIO()
            writer = pd.ExcelWriter(out, engine='xlsxwriter')
            df.to_excel(excel_writer=writer, index=False, sheet_name='Example')
            writer.save()
            writer.close()
            response = make_response(out.getvalue())
            response.headers["Content-Disposition"] = f"attachment; filename={indicator}.xlsx"
            response.headers["Content-type"] = "application/x-xls"

        return response
    
    except Exception as e:
        print(e)

            
def open_browser():
    webbrowser.open_new('http://127.0.0.1:2000/')

def run_app():
    Timer(1, open_browser).start();
    app.logger.setLevel(logging.DEBUG)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=2000)