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
from dashboardDB import *


db = DashboardDB()

app = Flask(__name__)

def create_selector(columns):
    """
    Return selector(list of features) in html format for selected indicator
    Input features name = columns
    """
    origin_columns = db.budget.columns if db.getIndicator() == 'Budget' else db.satellite.columns
    
    selector = ""
    for name in origin_columns:
        checked = 'checked' if name in columns else 'unchecked'
        active = 'active' if name in columns else ''
        selector += f'<label class="selector-btn btn btn-light {active}"><input value="{name}"  type="checkbox" class="form-check list-group-item columnSelector" {checked}/>{name}</label>'
    return selector

def create_filters(filter_type, lst):
    """
    Return selectors for country and program type in html format
    Input features type = filter_type, selected filters = lst
    """
    all_filter = db.getCountries() if filter_type == "country" else db.getPrograms()
    filters = ""
    for name in all_filter:
        checked = 'checked' if name in lst else 'unchecked'
        filters += f'<li><input value="{name}" type="checkbox" class="{filter_type}" {checked}/>{name} </li>'
    return filters

def create_sat_filters(): 
    """
    Return satellite selectors for country and application in html format
    """
    countries=""
    applications = f'<option value="all">all</option>'

    for name in list(db.satellite.country.unique()):
        countries += f'<option value="{name}">{name}</option>'
    for app_name in list(db.satellite.Application.unique()):
        applications += f'<option value="{app_name}">{app_name}</option>'
    return countries, applications 

def create_bubble_filters(): 
    """
    Return selectors for programs and application in html format
    """
    programs=""
    applications=""

    for name in list(db.budget_coordinates.program_type.unique()):
        programs += f'<option value="{name}">{name}</option>'
    for app_name in list(db.budget_coordinates.application.unique()):
        applications += f'<option value="{app_name}">{app_name}</option>'
    return programs, applications 

@app.route('/')
def index():
    """
    Create html template(index.html + jsons)
    """
    selector = create_selector(db.get_features())
    
    df = db.budget
    #table = create_table(df)
    lineChart = create_lineChart(df)
    
    program_bb, apps_bb = create_bubble_filters()
    bubbleChart = create_bubbleChart(db.getFilteredBudgetCoor('Civil','Earth Observation',2019))
    
    countries = create_filters("country",db.getCountries())
    programs = create_filters("program",db.getPrograms())
    
    satellites = create_satellite_table(db.getFilteredSatellites('China','all'))
    country_sats, apps = create_sat_filters()

    
    return render_template('index.html', selector=selector, 
                           plot=lineChart,  bubbleplot=bubbleChart,     
                           countries=countries, programs=programs, satellites=satellites,
                           countries_sat=country_sats, applications=apps,
                          program_type=program_bb, application_type=apps_bb)

@app.route('/indicator', methods=['GET', 'POST'])
def change_indicator():
    """
    Return list of selected columns(html list) in json format
    Call back from indicator selector(html)
    """
    feature = request.args['selected']
    if feature == 'Satellite' or feature == 'Budget':
        indicator=feature
        db.setIndicator(indicator)
    selector = create_selector(db.get_features())

    return jsonify(selector=selector)

@app.route('/features', methods=['GET', 'POST'])
def change_features():
    """
    Update list of selected columns(html list) in json format
    Call back from features selector(html)
    """
    features = request.args['selected']
    db.setFeatures(features)  
    
    return 'OK'

@app.route('/bubblePlot_filter', methods=['GET', 'POST'])
def change_bubble_filter():
    """
    Return bubbleChart in json format
    Call back from filters(year range, program and application selectors)
    """
    filter_type = request.args['type']
    programs = request.args['program']
    apps = request.args['app']
    year = request.args['year']
    
    df = db.getFilteredBudgetCoor(programs,apps,year)

    bubbles = create_bubbleChart(df)

    return bubbles


@app.route('/linePlot_filter', methods=['GET', 'POST'])
def change_filter():
    """
    Return lineChart and data table in json format
    Call back from filters(country, programs selectors)
    """
    countries = request.args['countries']
    programs = request.args['programs']
    df = db.getFilteredBudget(countries.strip(',').split(','),programs.strip(',').split(','))

    #tableJSON = create_table(df) 
    lineChart = create_lineChart(df)

    return jsonify(plot=lineChart)
    

@app.route('/satellite_filter', methods=['GET', 'POST'])
def change_satellite_filter():
    """
    Return data table in json format
    Call back from filters(country, applications)
    """
    filter_country = request.args['country']
    filter_apps = request.args['app']
    df = db.getFilteredSatellites(filter_country,filter_apps)
    satellites = create_satellite_table(df)

    return jsonify(satellites=satellites)


@app.route('/download', methods=['GET', 'POST'])
def download():
    """
    Return flask make_response (download file)
    Call back from download button in html
    """
    file_type = request.args.get('type')
    filter_type = request.args.get('filter')
    
    indicator = db.getIndicator()
    df = db.getDataFrame() if filter_type == "feature" else db.filteredBudgetCoor if filter_type == 'coor_budget' else db.getSatelliteDF() if filter_type== "satellites" else db.getFilteredData()
    if filter_type== "satellites":
        indicator = "satellites"

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