import os 
import random
import StringIO
from datetime import datetime, date
from flask import Flask, flash, make_response, render_template, request, redirect, url_for, abort, session, send_from_directory
from manipulateData import dateConverter, renderFigure
from myMongoDB import *
import pymongo
import matplotlib
from matplotlib import pyplot, dates
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import csv
import HTML

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = os.urandom(24)

# for index()::
# initialize all list/array storage variables before entering any methods
lunchListDB = []
lunchListToCSV = []

dinnerListDB = []
dinnerListToCSV = []

miscListDB = []
miscListToCSV = []

dateListDB = []
dateListLunch = []
dateListDinner = []
dateListMisc = []
dateListToCSV = []

# for renderFigHere()::
# initialize all list/array storage variables before entering any methods
dateList_L_toPlot = []
dateList_D_toPlot = []
dateList_M_toPlot = []

@app.route('/', methods=['GET', 'POST'])
def index():
	commitMessage = ""
	todayDateFormatNormal = date.today().strftime('%b %d, %Y')
	
	todayDateDropdown = ""
	todayDateDropdownJoined = ""

	rows = []
	header_row = ""

	if request.method == "POST":

		form = request.form

		# tuple for today's date
		todayDateDropdown = [str(form['monthdrop']), str(form['daydrop']), str(form['yeardrop'])]
		todayDateDropdownJoined = ' '.join(todayDateDropdown)

		mealCounterL = 0
		mealCounterD = 0
		mealCounterM = 0

		###########################################
		# DATA INSERTION - ONE DICTIONARY PER MEAL
		###########################################

		session['meal_type'] = str(form['mealdrop'])
	
		entered_data = float(form['mealMoney'])

		if session['meal_type'] == "Lunch":
			mealCounterL = 1
			lunchListDB.append(entered_data)
			lunchListToCSV.append(entered_data)	
			dateListLunch.append(todayDateDropdown)

		elif session['meal_type'] == "Dinner":
			mealCounterD = 1
			dinnerListDB.append(entered_data)
			dinnerListToCSV.append(entered_data)
			dateListDinner.append(todayDateDropdown)
	
		else:
			mealCounterM = 1
			miscListDB.append(entered_data)
			miscListToCSV.append(entered_data)
			dateListMisc.append(todayDateDropdown)
		
		###############
		# WRITE TO CSV
		###############
        
		# only add date to CSV list if it doesn't already exist
		if not todayDateDropdownJoined in dateListDB:
			dateListToCSV.append(todayDateDropdownJoined)
			print "dropdown date is not already here!"
		else:
			print "dropdown date already exists here :("
		
		rows = map(None, dateListToCSV, lunchListToCSV, dinnerListToCSV, miscListToCSV)
		print "rows: %s" % rows

		header_row = ['Date', 'Lunch', 'Dinner', 'Misc']
		with open('foodCSV.csv', 'wb') as f:
			writer = csv.writer(f, delimiter='\t')
			writer.writerow(header_row)
			for row in rows:
				writer.writerow(row)

		f.close()
		
		#############
		# DATABASING
		#############
		
		dateListDB.append(todayDateDropdownJoined)

		# just a construct for properly saving to the database
		# it's also easy to pass everything as one solid dictionary
		DB = {
			 "lunch": lunchListDB,
			 "dinner": dinnerListDB,
			 "misc": miscListDB,
			 "today_date": dateListDB
		      }

		#
		# MongoDB
		#
		# from myMongoDB.py file
		#insertData_to_db(food_entries_local, DB)

		##############

		session['xL'] = list(dateListLunch)
		session['xD'] = list(dateListDinner)
		session['xM'] = list(dateListMisc)
		session['yL'] = list(lunchListDB)
		session['yD'] = list(dinnerListDB)
		session['yM'] = list(miscListDB)
	
		print "session in index is: %s" % session
		
		if session['xL']:
			if session['meal_type'] == "Lunch":
				dateList_L_toPlot.append(dateConverter(session['xL'][-1:]))
		if session['xD']:
			if session['meal_type'] == "Dinner":
				dateList_D_toPlot.append(dateConverter(session['xD'][-1:]))
		if session['xM']:
			if session['meal_type'] == "Miscellaneous":
				dateList_M_toPlot.append(dateConverter(session['xM'][-1:]))

		print ""
		print "dateL: %s (%d)" % (dateList_L_toPlot, len(dateList_L_toPlot))
		print "yL: %s (%d)" % (session['yL'], len(session['yL']))
		print "dateD: %s (%d)" % (dateList_D_toPlot, len(dateList_D_toPlot))
		print "yD: %s (%d)" % (session['yD'], len(session['yD']))
		print "dateM: %s (%d)" % (dateList_M_toPlot, len(dateList_M_toPlot))
		print "yM: %s (%d)" % (session['yM'], len(session['yM']))

		if mealCounterL and mealCounterD and mealCounterM:
			commitMessage = "Money for all three meal types was successfully submitted"
		elif mealCounterL and mealCounterD:
			commitMessage = "Lunch and dinner money was successfully submitted"
		elif mealCounterL and mealCounterM:
			commitMessage = "Lunch and miscellaneous money was successfully submitted"
		elif mealCounterD and mealCounterM:
			commitMessage = "Dinner and miscellaneous money was successfully submitted"
		elif mealCounterL:
			commitMessage = "Lunch money was successfully submitted!"
		elif mealCounterD:
			commitMessage = "Dinner money was successfully submitted!"
		elif mealCounterM:
			commitMessage = "Miscellaneous money was successfully submitted!"
		else:
			commitMessage = "You must have consumed SOME food today :)"
	
	else:
		print "this is a GET, not a POST"

	return render_template("index.html", today_date=todayDateFormatNormal, commitMessage=commitMessage, header_row = header_row, rows = rows)

	
@app.route('/plot', methods = ["GET", "POST"])
#@app.route('/', methods = ["GET", "POST"])
def renderFigHere():
	
    manipulateData.renderFigure()

if __name__ == '__main__':
	food_entries_local = setup_db()
	
	app.run(debug = True)
