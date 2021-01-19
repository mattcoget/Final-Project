"""Interactive flask/plotly dashboard"""
from flask import Flask, render_template,request , send_file, send_from_directory, make_response, Response
import os
import io
import pandas as pd
import numpy as np
import webbrowser
from threading import Timer
import logging
from dashboard_plots import *

budget = pd.read_csv('data/clean_budget.csv')
satellite = pd.read_csv('data/clean_satellite.csv')
df = budget

app = Flask(__name__)
UPLOAD_FOLDER = '/static/client'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    bar = create_plot(df)
    table = create_table(df)
    return render_template('index.html', table=table, plot=bar)

@app.route('/plot', methods=['GET', 'POST'])
def change_features():

    feature = request.args['selected']

    if feature == 'Satellite' or feature == 'Budget':
        df = budget if feature == 'Budget' else satellite
        tableJSON= create_table(df)
        return tableJSON


@app.route('/download', methods=['GET', 'POST'])
def download():
    # stream the response as the data is generated
    print("download oi")
    file_type = request.args.get('type')
    
    try:
        if file_type == 'csv':
            response = make_response(df.to_csv())
            response.headers["Content-Disposition"] = "attachment; filename=budget.csv"
            response.headers["Content-Type"] = "text/csv"
            
        else:
            
            out = io.BytesIO()
            writer = pd.ExcelWriter(out, engine='xlsxwriter')
            df.to_excel(excel_writer=writer, index=False, sheet_name='Example')
            writer.save()
            writer.close()
            file_name = 'budget.xlsx'
            response = make_response(out.getvalue())
            response.headers["Content-Disposition"] = "attachment; filename=%s" % file_name
            response.headers["Content-type"] = "application/x-xls"

        return response
    
    except Exception as e:
        print(e)

            
def open_browser():
    webbrowser.open_new('http://127.0.0.1:2000/')

def run_app():
    Timer(1, open_browser).start();
    app.logger.setLevel(logging.DEBUG)
    app.run(port=2000)