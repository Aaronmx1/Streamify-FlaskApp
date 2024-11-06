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

#@app.route('/')
#def root():
#    return render_template("main.j2")


# --------------------------------------- #
#           Artists table
# --------------------------------------- #

# CREATE  [C in CRUD]
@app.route('/artist', methods=['POST', 'GET'])
def artist():
# Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == 'POST':
        # fire off if user presses the Add Person button
        if request.form.get("Add_Artist"):
            # grab user form inputs
            fname = request.form["fname"]
            lname = request.form["lname"]
            email = request.form["email"]
            
            # account for null first name AND last name AND email
            if fname == "" and lname == "" and email == "":
                # MySQL query to insert a new person into bsg_people with our form inputs
                query = "INSERT INTO Artists (fname, lname, email) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, email))
                mysql.connection.commit()
            
            # account for null email
            elif email == "":
                query = "INSERT INTO Artists (fname, lname, email) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, email))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Artists (fname, lname, email) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, email))
                mysql.connection.commit()
        
            # redirect back to people page
            return redirect('/artist')

    # Grab bsg_people data so we send it to our template to display
    if request.method == 'GET':
        # mySQL query to grab all the people in bsg_people
        query = "SELECT artistId, fname, lname FROM Artists"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("artist.j2", data=data)


# DELETE [D in CRUD]
# people.j2 href is routed here and supplies associated {{item.id}} to delete people by their id
@app.route('/delete_artist/<int:id>')                           # create route
def delete_artist(id):                                          # set method
    # MySQL query to delete the person with our passed id
    # grab form inputs
    query = "DELETE FROM Artists WHERE artistId = %s;"           # create desired query
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))                                   # execute desired query.  Including a comma after id in (id,) is necessary otherwise an error will be produced
    mysql.connection.commit()

    # redirect back to people page
    # /delete_people route exists only to perform deletion and is itself not a page that displays to the user
    return redirect('/artist')                                  # load page

# UPDATE [U in CRUD]
@app.route('/edit_artist/<int:id>', methods=['POST', 'GET'])    # create route
def edit_people(id):                                            # set method
    # 2 queries are necessary, one to retrieve information for user view and the other to populate the dropdown
    if request.method == 'GET':
        # MySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Artists WHERE artistId = %s" % (id) # create desired query      % (id) obtains edit_people(id) and passes it to %s in query
        cur = mysql.connection.cursor()
        cur.execute(query)                                      # execute desired query
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_artist.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == 'POST':
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Artist"):
            # grab user form inputs
            id = request.form['artistId']
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']

            # account for null first name AND last name
            if fname == "" and lname == "":
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE Artists SET fname = %s, lname = %s, email = NULL WHERE artistId = %s"   # create desired query
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, id))          # execute desired query
                mysql.connection.commit()

            # account for null homeworld
            elif email == "":
                query = "UPDATE Artists SET fname = %s, lname = %s, email = NULL WHERE artistId = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, id))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Artists SET fname = %s, lname = %s, email = %s WHERE artistId = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, email, id))
                mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect('/artist')


# --------------------------------------- #
#           Playlists table
# --------------------------------------- #

# CREATE  [C in CRUD]
@app.route('/playlist', methods=['POST', 'GET'])
def artist():
# Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == 'POST':
        # fire off if user presses the Add Person button
        if request.form.get("Add_Playlist"):
            # grab user form inputs
            playlistName = request.form["playlistName"]
            playlistDescription = request.form["playlistDescription"]
            userId = request.form["userId"]
            numberOfSongs = request.form["numberOfSongs"]
            
            # account for numberOfSongs being NULL
            if numberOfSongs == "":
                # MySQL query to insert a new person into bsg_people with our form inputs
                query = "INSERT INTO Playlists (playlistName, playlistDescription, userId) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (playlistName, playlistDescription, userId))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Playlists (playlistName, playlistDescription, userId, numberOfSongs) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (playlistName, playlistDescription, userId, numberOfSongs))
                mysql.connection.commit()
        
            # redirect back to people page
            return redirect('/playlist')

    # Grab bsg_people data so we send it to our template to display
    if request.method == 'GET':
        # mySQL query to grab all the people in bsg_people
        query = "SELECT playlistId, playlistName, playlistDescription, userId, numberOfSongs FROM Playlists"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        # Debugging output
        #print("Data fetched from database:", data)

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("artist.j2", data=data)


# DELETE [D in CRUD]
# people.j2 href is routed here and supplies associated {{item.id}} to delete people by their id
@app.route('/delete_artist/<int:id>')                           # create route
def delete_artist(id):                                          # set method
    # MySQL query to delete the person with our passed id
    # grab form inputs
    query = "DELETE FROM Artists WHERE artistId = %s;"           # create desired query
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))                                   # execute desired query.  Including a comma after id in (id,) is necessary otherwise an error will be produced
    mysql.connection.commit()

    # redirect back to people page
    # /delete_people route exists only to perform deletion and is itself not a page that displays to the user
    return redirect('/artist')                                  # load page

# UPDATE [U in CRUD]
@app.route('/edit_artist/<int:id>', methods=['POST', 'GET'])    # create route
def edit_people(id):                                            # set method
    # 2 queries are necessary, one to retrieve information for user view and the other to populate the dropdown
    if request.method == 'GET':
        # MySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Artists WHERE artistId = %s" % (id) # create desired query      % (id) obtains edit_people(id) and passes it to %s in query
        cur = mysql.connection.cursor()
        cur.execute(query)                                      # execute desired query
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_artist.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == 'POST':
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Artist"):
            # grab user form inputs
            id = request.form['artistId']
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']

            # account for null first name AND last name
            if fname == "" and lname == "":
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE Artists SET fname = %s, lname = %s, email = NULL WHERE artistId = %s"   # create desired query
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, id))          # execute desired query
                mysql.connection.commit()

            # account for null homeworld
            elif email == "":
                query = "UPDATE Artists SET fname = %s, lname = %s, email = NULL WHERE artistId = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, id))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Artists SET fname = %s, lname = %s, email = %s WHERE artistId = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, email, id))
                mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect('/artist')

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)