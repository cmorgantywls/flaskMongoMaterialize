import os
from app import app
from flask import render_template, request, redirect

from flask_pymongo import PyMongo
#lines 1-5 import a bunch of tools we are using.

#assume you'll use this configuration in the lines below if you are using Mongo!
# name of database
app.config['MONGO_DBNAME'] = 'test' 

# URI of database
app.config['MONGO_URI'] = 'changetoYourURI'

mongo = PyMongo(app)


# INDEX

@app.route('/') #homepage!
@app.route('/index') #homepage!
def index():
    #Connect to the DB with the mongo object
    collection=mongo.db.events #looks at mongo object -> goes to database -> finds events collection
    #Use the .find() method to return all of the events
    events = collection.find({})
    return render_template('index.html', events = events)

#This route will handle the POST of our form. It should also be able to redirect to homepage on a GET request
@app.route('/addevent', methods=["GET","POST"]) #this will be another page to add events.
def add_event():
    if request.method=="GET":    #if we go through URL (GET) -> show us the form && page!
        return render_template('add_event.html')
    else:  #else if we POST through this URL -> send the info in and show us the homepage
        eventName=request.form["eventName"] #from the form, save the eventName from dict
        eventDate=request.form["eventDate"] #from the form, save the eventDate from dict
        
        event = {"event":eventName,"date":eventDate} #the thing we want to put into mongo
        collection = mongo.db.events #connect to mongoDB in this route
        collection.insert(event) #insert the event into that collection!
        #we have all CRUD operations for Mongo - we can look those up later. :)
        return redirect('/') #we want them to go away from the form so they can't double-add the event
        #GET-POST-GET sandwich