from flask import Flask
from datetime import datetime, date

def dateConverter(dateStr):
	
	#dateStr_converted = ''

	#print ""
	#print "dateStr: %s" % dateStr
	#print "dateStr[0]: %s" % dateStr[0]
	#print "dateStr[0][0]: %s" % dateStr[0][0]

	if dateStr[0][0] == 'January':
		dateStr[0][0] = 'Jan'
	if dateStr[0][0] == 'February':
		dateStr[0][0] = 'Feb'
	if dateStr[0][0] == 'March':
		dateStr[0][0] = 'Mar'
	if dateStr[0][0] == 'April':
		dateStr[0][0] = 'Apr'
	if dateStr[0][0] == 'June':
		dateStr[0][0] = 'Jun'    
	if dateStr[0][0] == 'July':
		dateStr[0][0] = 'Jul'
	if dateStr[0][0] == 'August':
		dateStr[0][0] = 'Aug'
	if dateStr[0][0] == 'September':
		dateStr[0][0] = 'Sep'
	if dateStr[0][0] == 'October':
		dateStr[0][0] = 'Oct'  
	if dateStr[0][0] == 'November':
		dateStr[0][0] = 'Nov'
	if dateStr[0][0] == 'December':
		dateStr[0][0] = 'Dec'
   
	if dateStr == []:
		dateStr_converted = ''
	else:
		dateStr[0] = ' '.join(dateStr[0])
		print "dateStr[0] amended: %s" % dateStr[0]
		dateStr_converted = datetime.strptime(dateStr[0], '%b %d %Y')
	
	print "dateStr_converted: %s" % dateStr_converted
	return dateStr_converted

# ---> test run
#dateStr = ['October', '24', '2013']
#dateConverter(dateStr)

def renderFigure():
    ############
    # PLOT DATA
    ############
    
	fig = ""
	fig1 = ""
	fig2 = ""
	fig3 = ""
	response = ""
	response1 = ""
	response2 = ""
	response3 = ""
    
	#if request.method == "POST":
	print "session in render fig is: %s" % session
    
	fig = pyplot.figure()
	#fig, (ax1,ax2,ax3) = pyplot.subplots(3)
	
	# 1
	ax = fig.add_subplot(3,1,1)
	ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d/%y'))
	ax.xaxis.set_major_locator(matplotlib.dates.DayLocator())
	ax.plot(dateList_L_toPlot, session['yL'], '-o')
	
	# 2
	ax = fig.add_subplot(3,1,2)
	ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d/%y'))
	ax.xaxis.set_major_locator(matplotlib.dates.DayLocator())
	ax.plot(dateList_D_toPlot, session['yD'], '-o')
    
	# 3
	ax = fig.add_subplot(3,1,3)
	ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d/%y'))
	ax.xaxis.set_major_locator(matplotlib.dates.DayLocator())
	ax.plot(dateList_M_toPlot, session['yM'], '-o')
    
	fig.autofmt_xdate()
   	
	#fig1.savefig('./static/lunchPlotted.png')
	#fig2.savefig('./static/dinnerPlotted.png')
	#fig3.savefig('./static/miscPlotted.png')        	
	fig.savefig('./static/foodPlotted.png')
    
	canvas = FigureCanvas(fig)
	output = StringIO.StringIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	
	return response
#return render_template("postFig.html")
