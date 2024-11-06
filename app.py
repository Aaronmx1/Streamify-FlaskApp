from flask import Flask, render_template, json
from flask import redirect  # pip install Flask-SSLify
from flask_mysqldb import MySQL # pip install MySQL
from flask import request # pip install requests
import os
import database.db_connector as db

# Source: https://github.com/osu-cs340-ecampus/flask-starter-app/tree/master?tab=readme-ov-file
# TODO: Left off on Step 7 - Building a Basic CRUD APP: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/README.md

# Configuration

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DATABASE')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT'))
app.config["MYSQL_CURSORCLASS"] = "DictCursor"          # required for tuple object to be converted to dictionary

mysql = MySQL(app)

# Create connection to database

db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")



# CREATE  [C in CRUD]
@app.route('/people', methods=['POST', 'GET'])
def people():
# Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == 'POST':
        # fire off if user presses the Add Person button
        if request.form.get("Add_Person"):
            # grab user form inputs
            fname = request.form["fname"]
            lname = request.form["lname"]
            homeworld = request.form["homeworld"]
            age = request.form["age"]
            
            # account for null age AND homeworld
            if age == "" and homeworld == "0":
                # MySQL query to insert a new person into bsg_people with our form inputs
                query = "INSERT INTO bsg_people (fname, lname) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname))
                mysql.connection.commit()
            
            # account for null homeworld
            elif homeworld == '0':
                query = "INSERT INTO bsg_people (fname, lname, age) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, age))
                mysql.connection.commit()

            # account for null age
            elif age == "":
                query = "INSERT INTO bsg_people (fname, lname, homeworld) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fnam, lname, homeworld))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO bsg_people (fname, lname, homeworld, age) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, age))
                mysql.connection.commit()
        
            # redirect back to people page
            return redirect('/people')

        # Grab bsg_people data so we send it to our template to display
    if request.method == 'GET':
        # mySQL query to grab all the people in bsg_people
        query = "SELECT bsg_people.id, fname, lname, bsg_planets.name AS homeworld, age FROM bsg_people LEFT JOIN bsg_planets ON homeworld = bsg_planets.id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab planet id/name data from our dropdown.  Dropdown created in people.j2 using jinja notation
        query2 = "SELECT id, name FROM bsg_planets"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        homeworld_data = cur.fetchall()     # contains the results of this query, both id and name of each planet
        
        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("people.j2", data=data, homeworlds=homeworld_data)


# DELETE [D in CRUD]
# people.j2 href is routed here and supplies associated {{item.id}} to delete people by their id
@app.route('/delete_people/<int:id>')                           # create route
def delete_people(id):                                          # set method
    # MySQL query to delete the person with our passed id
    # grab form inputs
    query = "DELETE FROM bsg_people WHERE id = '%s';"           # create desired query
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))                                   # execute desired query.  Including a comma after id in (id,) is necessary otherwise an error will be produced
    mysql.connection.commit()

    # redirect back to people page
    # /delete_people route exists only to perform deletion and is itself not a page that displays to the user
    return redirect('/people')                                  # load page

# UPDATE [U in CRUD]
@app.route('/edit_people/<int:id>', methods=['POST', 'GET'])    # create route
def edit_people(id):                                            # set method
    # 2 queries are necessary, one to retrieve information for user view and the other to populate the dropdown
    if request.method == 'GET':
        # MySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM bsg_people WHERE id = %s" % (id) # create desired query      % (id) obtains edit_people(id) and passes it to %s in query
        cur = mysql.connection.cursor()
        cur.execute(query)                                      # execute desired query
        data = cur.fetchall()

        # MySQL query to grab planet id/name data for our dropdown
        query2 = "SELECT id, name FROM bsg_planets"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        homeworld_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_people.j2", data=data, homeworlds=homeworld_data)

    # meat and potatoes of our update functionality
    if request.method == 'POST':
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Person"):
            # grab user form inputs
            id = request.form['personID']
            fname = request.form['fname']
            lname = request.form['lname']
            homeworld = request.form['homeworld']
            age = request.form['age']

            # account for null age AND homeworld
            if (age == "" or age == "None") and homeworld == "0":
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = NULL, bsg_people.age = NULL WHERE bsg_people.id = %s"   # create desired query
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, id))          # execute desired query
                mysql.connection.commit()

            # account for null homeworld
            elif homeworld == '0':
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = NULL, bsg_people.age = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, age, id))
                mysql.connection.commit()

            # account for null age
            elif age == "" or age == "None":
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = %s, bsg_people.age = NULL WHERE bsg_people.id = %s"   # create desired query
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, id))   # execute desired query
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = %s, bsg_people.age = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, age, id))
                mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect('/people')


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)