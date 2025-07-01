# Copyright © 2023-2025, Indiana University
# BSD 3-Clause License

from flask import Flask, render_template, url_for, redirect, request
import csv 
from flaskapp import database as db


app = Flask(__name__)
#Data management: loading and saving 


#Routing and application logic
@app.route("/")
def render_index():
    return render_template("index.html",equipment=db.get_equipment())

@app.route("/equipment/")
def render_equipment():
    return render_template("equipment.html", equipment = db.get_equipment())

@app.route("/people/")
def render_people():
    return render_template("people.html", people = db.get_people())


#Project v1 work
@app.route("/guest_reservation/")
def render_guests():
    return render_template("guest_res.html", checkin_people = db.get_checkin_people(), checkout_people = db.get_checkout_people())

@app.route('/submit_checkin/<int:id>', methods=['POST'])
def submit_checkin(id):
    rent = 'rent_equipment' in request.form
    pass_type = request.form.get('pass_type')
    boot = request.form.get('boot_size')
    ski = request.form.get('ski_size')
    pole = request.form.get('pole_size')

    db.checkin_person(id, pass_type, rent, boot, ski, pole)
    return redirect(url_for('render_guests'))

@app.route('/checkin/<int:id>')
def render_checkin_form(id):
    person = db.get_one_person(id)
    boot_sizes = db.get_available_boot_sizes()
    ski_sizes = db.get_available_ski_sizes()
    pole_sizes = db.get_available_pole_sizes()

    return render_template('checkin.html', person=person, boot_sizes=boot_sizes, ski_sizes=ski_sizes, pole_sizes=pole_sizes)

@app.route('/submit_checkout/<int:id>')
def submit_checkout(id):
    db.checkout_person(id)
    return redirect(url_for('render_guests'))

#
#
#
@app.route('/people/<person_id>/')
def render_person(person_id) :
    return render_template('person.html', person = db.get_one_person(int(person_id)))

@app.route('/equipment/add/', methods=['GET', 'POST'])
def handle_new_equipment():
     if request.method == "GET":
          
        return render_template("equipment_form.html")
     else:
         name = request.form['name'] 
         Quantity = request.form['max'] 
         Max_quantity= request.form['max'] 

         assert name
         assert Quantity.isdigit()
         assert Max_quantity.isdigit()

         new_equipment = {
         'name': name,
         'maxquantity': Max_quantity,
         'quantity': Quantity,
         'category': 'Miscellaneous'
         }
         db.add_equipment(new_equipment)
         return redirect(url_for('render_equipment'))

@app.route('/people/add/', methods=['GET', 'POST'])
def handle_new_person(): 
    if request.method == "GET":
        return render_template("people_form.html")
    else:
         name = request.form['name'] 
         email = request.form['email'] 
         Inchheight = request.form['inchheight'] 
         Feetheight = request.form['feetheight']
         ShoeSize = request.form['shoe_size']
         assert name.strip()
         assert email.strip()
         assert Inchheight.isdigit()
         assert Feetheight.isdigit()
         height = int(Feetheight) * 12 + int(Inchheight)
         new_person = {
         'name': name,
         'email': email,
         'height': height,
         'shoesize': ShoeSize
         }
         db.add_person(new_person)
         return redirect(url_for('render_people'))

@app.route('/people/<person_id>/edit/', methods=["GET"])
def render_people_edit(person_id) :
    return render_template('people_edit.html', person = db.get_one_person(int(person_id)))

@app.route('/people/<person_id>/update/', methods=["POST"])
def handle_person_update(person_id): 
    name = request.form['name'] 
    email = request.form['email'] 
    Inchheight = request.form['inchheight'] 
    Feetheight = request.form['feetheight']
    ShoeSize = request.form['shoe_size']

    assert name.strip()
    assert email.strip()
    assert Inchheight.isdigit()
    assert Feetheight.isdigit()

    height = int(Feetheight) * 12 + int(Inchheight)
    person = {
    'id':person_id,
    'name': name,
    'email': email,
    'height': height,
    'shoesize': ShoeSize
    }
    db.update_person(person)
    return redirect(url_for('render_people'))
'''
@app.route('/people/<person_id>/edit/', methods=["GET", "POST"])
def edit_person(person_id):
    if request.method == "GET":
        person = db.get_one_person(int(person_id))
        return render_template("people_edit.html", person=person)
    else:
        name = request.form["name"]
        email = request.form["email"]
        Inchheight = request.form["inchheight"]
        Feetheight = request.form["feetheight"]
        ShoeSize = request.form["shoe_size"]
        height = int(Feetheight) * 12 + int(Inchheight)

        person = {
            "id": person_id,
            "name": name,
            "email": email,
            "height": height,
            "shoesize": ShoeSize,
        }
        db.update_person(person)
        return redirect(url_for("render_people"))
'''