import HTML
from flask import Flask, render_template

HTML_test = Flask(__name__)

@HTML_test.route('/')
def index():	
	table_data = [
		['Last name', 'First name', 'Age'],
		['Trocchia', 'Scott', '24'],
		['Trocchia', 'Stan', '61']
		]
	htmlcode = HTML.table(table_data)
	return render_template("HTMLCODE.html", htmlcode = htmlcode)

if __name__ == '__main__':
	HTML_test.run(debug=True)
