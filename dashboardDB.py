"""Data prepration for dashboard"""
import pandas as pd
import numpy as np


class DashboardDB:
 
    def __init__(self):
        self.budget = pd.read_csv('data/budget_cleaned.csv')
        self.satellite = pd.read_csv('data/satellites_cleaned.csv')
        
        self.indicator = 'Budget'
        self.features = list(self.budget.columns)
        
        self.budget_coordinates = pd.read_csv('data/boo.csv', index_col='Unnamed: 0')

        self.filteredBudget = self.budget.copy()
        self.filteredBudgetCoor = self.budget_coordinates.copy()
        self.filteredSatellite = self.satellite.copy()
        
    def getIndicator(self):
        """
        Returns indicator(satellite/budget)
        """
        return self.indicator
    
    def get_features(self):
        """
        Returns features(selected column)
        """
        return list(self.features)
    
    def getDataFrame(self):
        """
        Returns dataframe filtered by year,program_type
        Inputs - dataframe=data,columns:(year,program_type)
        """
        df = self.budget if self.indicator == 'Budget' else self.satellite
        return df[self.features]
    
    def getCountries(self):
        """
        Returns list of all countries in budget dataframe
        """
        return list(self.budget.country.unique())
    
    def getPrograms(self):
        """
        Returns list of all program type in budget dataframe
        """
        return list(self.budget.program_type.unique())
    
    def getFilteredBudgetCoor(self,program,app,year):   
        """
        Returns dataframe filtered by year,application and program_type
        Inputs - dataframe=budget_coordinate,columns:(year,program_type,application)
        """
        self.filteredBudgetCoor = self.budget_coordinates[(self.budget_coordinates['program_type']==program)&(self.budget_coordinates['application']==app)
                            &(self.budget_coordinates['year']==int(year))].copy()
        return self.filteredBudgetCoor
    
    def getFilteredBudget(self, countries, programs):
        """
        Returns dataframe filtered by selected programs or countries (multi selection)
        Inputs - dataframe=budget,filter:(countries or program_types)
        """
        df = self.budget.copy()
        self.filteredBudget = pd.concat([df.loc[(df["country"] == ft1) & (df["program_type"] == ft2)] 
           for ft1 in countries for ft2 in programs], join='inner')
        return self.filteredBudget
    
    def getFilteredData(self):
        """
        Returns dataframe filtered by selected programs or countries (multi selection)
        """
        return self.filteredBudget
    
    def getFilteredSatellites(self,name,app):
        """
        Filter dataframe(satellite) by selected columns 
        Inputs - selected country=name application=app
        """
        if app=="all":
            df = self.satellite[self.satellite['country']==name].copy()
        else:
            df = self.satellite[(self.satellite['country']==name)&(self.satellite['Application']==app)].copy()
        self.filteredSatellite = df
        return self.getSatellites(df)
    
    def getSatellites(self,df):
        """
        Return satellites sorted by year
        Inputs - filtered dataframe = df
        """
        df = df[['Launch year','satellite_Name']].copy()
        dict_ = {}
        for year in df.sort_values('Launch year')['Launch year'].unique():
            dict_[year] = list(df[df['Launch year']==year]['satellite_Name'])

        data = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in dict_.items() ]))
        data.fillna(" ", inplace=True)
        
        return data
    
    def getSatelliteDF(self):
        return self.filteredSatellite
     
        
    def setIndicator(self, indicator):
        """
        Change dataframe to satellites_cleaned.csv or budget_cleaned.csv
        Inputs - indicator satellite/budget
        """
        self.indicator = indicator
        df = self.budget if self.indicator == 'Budget' else self.satellite
        self.features = list(df.columns)
        
    def setFeatures(self,columns):
        """
        Filter dataframe(satellite/budget) selected columns 
        Inputs - selected columns=columns
        """
        self.features = columns.strip(',').split(',')
        
    
   
    
    
    
    
    
            
    