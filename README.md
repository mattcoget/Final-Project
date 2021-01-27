![Ironhack logo](https://i.imgur.com/1QgrNNw.png)

# EUROCONSULT

**Mahshid AMIR MOAZAMI & Matthieu COGET**

*Data Analytics full-time Paris Jan 2021*

## Overview

Two projects were proposed by Euroconsult, which is a consulting firm specialized in space markets. 

* The first was the creation of an interactive dashboard to have an overview on the satellites activities and budget for every country.
* The second project was the modelling of the budget on satellites per country for the next 10 years from the budgets for the last 22 years.

Two datasets were provided by Euroconsult and were cleaned. Some adaptations were needed (data aggregation, pivot table).

* Datasets provided were:
	* Satellites
		- Launched from 2009  to to be launched by 2028.
		- Application
		- Launch status
		- Range of price
	* Budget by country
		- Year
		- Application
		- Civil or defence

The budget dataset was composed of 97,459 rows and 10 columns with 2 numeric columns, the rest were objects.
The satellites dataset was composed of 2,500 rows and 9 columns with 1 numeric column (dates), the rest were objects. Two columns were price range and weight range of the satellites, so it easily became dummies.

### Libraries used:

Pandas, Numpy, Matplotlib.pyplot, Seaborn

* For the dashboard:
	* Plotly (an interactive graphing library for Python)
	* Flask (a micro web framework written in Python)
* For the :
	* Scikit-Learn (a machine learning for data modelling library on Python)
  
### Dashboard

#### Usage

```bash
$ python app.py
 * Running on http://0.0.0.0:9999/ (Press CTRL+C to quit)
 * Restarting with stat
```

![screenshot of the dashboard](/static/img/dashboard.png)

## Organization
In repository of project you find:

<img src="static/img/folder.png" style="float:left;" width="200" height="300"/>



## Model Training and Evaluation

* To prepare the Machine Learning model, all the budgets have been grouped by year and type of program (Civil or Defence).
* Two models were selected because they : 
	* Linear Regression
	* Support Vector Regression (SVR) with a polynomial factor as some budget evolutions look like a cubic evolution.

During the modelling, we see that the performance were way better on Linear Regression model, compare to SVR which don’t really fit with our data. Moreover the evaluation metrics for SVR were bad for the Defence programs, for some of them, the statistics were worse than an horizontal line.
Even Linear Regression is the best model compare to SVR, it isn't a really good model: it needs more datas to process a better prediction.

## Conclusion

* The dashboard is fully operationnal.
* The model cannot give a good prediction for the moment. It need to be feed with more datas or find another model which need less data give a good prediction.
* The RBF neural networks could be used to go further on the predictive part.
