"""Greenthumbs bookings site"""
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
import os
from datetime import datetime


# Import pymongo and initialize client
from pymongo import MongoClient


host = os.environ.get('MONGODB_URI','mongodb://localhost:27017/GreenThumps')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.Greenthumbs
appointments = db.appointments

app = Flask(__name__)

@app.route('/')
def index():
    """Show Index Page."""
    return render_template('index.html')
    
@app.route('/book_appointment')
def show_book_appointment_form():
    """Show Book Appointment Form"""
    return render_template('book_appointment.html')

@app.route('/book_appointment', methods=['POST'])
def submit_appointment():
    """Submit new appointment."""
    print(request.form)
    appointment = {

       'firstname':request.form.get('firstname'),
       'lastname':request.form.get('lastname'),
       'address':request.form.get('address'),
       'city':request.form.get('city'),
       'state':request.form.get('state'),
       'zipcode':request.form.get('zipcode'),
       'bday':request.form.get('bday'),
       'service':request.form.get('service'), 
       'date':request.form.get('date'),
       'time':request.form.get('time'),
   }
    appointment_id = appointments.insert_one(appointment).inserted_id
    return redirect(url_for('appointment_show', appointment_id=appointment_id))

@app.route('/appointment_show/<appointment_id>')
def appointment_show(appointment_id):
    """Show a single appointment."""
    appointment = appointments.find_one({'_id': ObjectId(appointment_id)})
    return render_template('appointment_show.html', appointment=appointment)

@app.route('/appointment/<appointment_id>/edit')
def appointment_edit(appointment_id):
    """Show the edit form for an appointment."""
    appointment = appointments.find_one({'_id': ObjectId(appointment_id)})
    return render_template('appointment_edit.html', appointment=appointment, title='Edit Appointment')

@app.route('/appointment/<appointment_id>', methods=['POST'])
def appointment_update(appointment_id):
    """Submit an edited appointment."""
    updated_appointment = {
        'firstname':request.form.get('firstname'),
        'lastname':request.form.get('lastname'),
        'address':request.form.get('address'),
        'city':request.form.get('city'),
        'state':request.form.get('state'),
        'zipcode':request.form.get('zipcode'),
        'bday':request.form.get('bday'),
        'service':request.form.get('service'), 
        'date':request.form.get('date'),
        'time':request.form.get('time'),
       }

    appointments.update_one({'_id': ObjectId(appointment_id)}, {'$set': updated_appointment})
    return redirect(url_for('appointment_show', appointment_id=appointment_id))


@app.route('/appointment/<appointment_id>/delete', methods=['POST'])
def appointment_delete(appointment_id):
    """Delete one appointment."""
    appointments.delete_one({'_id': ObjectId(appointment_id)})
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)