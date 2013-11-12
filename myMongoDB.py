# MongoDB wins! (>> SQL-Alchemy, > SQLite3)
# ... because: it can save whole dictionaries to db

import pymongo
import datetime

#from app import db
#class Meal_Type(db.Document):
#	lunch = db.StringField(max_length=255)
#	dinner = db.StringField(max_length=255)
#	misc = db.StringField(max_length=255)
#	today_date = db.DateTimeField(default=datetime.datetime.now)

def setup_db():
	# establish a connection
	con = pymongo.Connection()

	# this is the database in MongoDB
	db = con.fooddata

	# debugging:  print db

	# this is table -- or, collection in Mondo DB -- I care about within the aforementioned database
	food_entries = db.food_entries

	return food_entries

def insertData_to_db(collection, dictToInsert):
	#globalMealTest = {
	#			"lunch": [54],
	#			"dinner": [],
	#			"misc":	[6]
	#		}
	#food_entries.insert(globalMealTest)

	# 1.) INSERT
	collection.insert(dictToInsert)
	
	# 2.) FIND
	meals = collection.find()
	#meals = collection.find_one()
	print ""
	print "###################"
	print "INSERT & FIND TEST"
	print "###################"
	print "%d instances in food_entries collection" % collection.count()

	for meal in meals:
		print meal
	print ""
