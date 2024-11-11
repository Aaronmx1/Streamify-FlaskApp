from flask import Flask, render_template, json
from flask import redirect  # pip install Flask-SSLify
from flask_mysqldb import MySQL # pip install MySQL
from flask import request # pip install requests
import os
import database.db_connector as db

# Source: https://github.com/osu-cs340-ecampus/flask-starter-app/tree/master?tab=readme-ov-file

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


# --------------------------------------- #
#           Artists table
# --------------------------------------- #

# CREATE  [C in CRUD]
@app.route('/artists', methods=['POST', 'GET'])
def artist():
# Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == 'POST':
        # fire off if user presses the Add Person button
        if request.form.get("Add_Artist"):
            # grab user form inputs
            fName = request.form["fName"]
            lName = request.form["lName"]
            email = request.form["email"]
            
            # account for null first name AND last name AND email
            if fName == "" and lName == "" and email == "":
                # MySQL query to insert a new person into bsg_people with our form inputs
                query = "INSERT INTO Artists (fName, lName, email) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fName, lName, email))
                mysql.connection.commit()
            
            # account for null email
            elif email == "":
                query = "INSERT INTO Artists (fName, lName, email) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fName, lName, email))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Artists (fName, lName, email) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fName, lName, email))
                mysql.connection.commit()
        
            # redirect back to people page
            return redirect('/artists')

    # Grab bsg_people data so we send it to our template to display
    if request.method == 'GET':
        # mySQL query to grab all the people in bsg_people
        query = "SELECT artistId, fName, lName, email FROM Artists"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("artists.j2", data=data)


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
    return redirect('/artists')                                  # load page

# UPDATE [U in CRUD]
@app.route('/edit_artist/<int:id>', methods=['POST', 'GET'])    # create route
def edit_artist(id):                                            # set method
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
            fName = request.form['fName']
            lName = request.form['lName']
            email = request.form['email']

            # account for null first name AND last name
            if fName == "" and lName == "":
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE Artists SET fName = %s, lName = %s, email = NULL WHERE artistId = %s"   # create desired query
                cur = mysql.connection.cursor()
                cur.execute(query, (fName, lName, id))          # execute desired query
                mysql.connection.commit()

            # account for null homeworld
            elif email == "":
                query = "UPDATE Artists SET fName = %s, lName = %s, email = NULL WHERE artistId = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fName, lName, id))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Artists SET fName = %s, lName = %s, email = %s WHERE artistId = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fName, lName, email, id))
                mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect('/artists')


# --------------------------------------- #
#           Playlists table
# --------------------------------------- #

# CREATE  [C in CRUD]
@app.route('/playlists', methods=['POST', 'GET'])
def playlist():
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

            # account for userId being NULL
            elif userId == "":
                # MySQL query to insert a new playlist into Playlists with our form inputs
                query = "INSERT INTO Playlists (playlistName, playlistDescription, numberOfSongs) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (playlistName, playlistDescription, numberOfSongs))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Playlists (playlistName, playlistDescription, userId, numberOfSongs) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (playlistName, playlistDescription, userId, numberOfSongs))
                mysql.connection.commit()
        
            # redirect back to people page
            return redirect('/playlists')

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
        return render_template("playlists.j2", data=data)


# DELETE [D in CRUD]
# people.j2 href is routed here and supplies associated {{item.id}} to delete people by their id
@app.route('/delete_playlist/<int:id>')                           # create route
def delete_playlist(id):                                          # set method
    # MySQL query to delete the person with our passed id
    # grab form inputs
    query = "DELETE FROM Playlists WHERE playlistId = %s;"           # create desired query
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))                                   # execute desired query.  Including a comma after id in (id,) is necessary otherwise an error will be produced
    mysql.connection.commit()

    # redirect back to people page
    # /delete_people route exists only to perform deletion and is itself not a page that displays to the user
    return redirect('/playlists')                                  # load page

# UPDATE [U in CRUD]
@app.route('/edit_playlist/<int:id>', methods=['POST', 'GET'])    # create route
def edit_playlist(id):                                            # set method
    # 2 queries are necessary, one to retrieve information for user view and the other to populate the dropdown
    if request.method == 'GET':
        # MySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Playlists WHERE playlistId = %s" % (id) # create desired query      % (id) obtains edit_people(id) and passes it to %s in query
        cur = mysql.connection.cursor()
        cur.execute(query)                                      # execute desired query
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_playlist.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == 'POST':
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Playlist"):
            # grab user form inputs
            id = request.form['playlistId']
            playlistName = request.form['playlistName']
            playlistDescription = request.form['playlistDescription']
            userId = request.form['userId']
            numberOfSongs = request.form['numberOfSongs']

            # account for null numberOfSongs
            if numberOfSongs == "":
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE Playlists SET playlistName = %s, playlistDescription = %s, userId = %s, numberOfSongs = 0  WHERE playlistId = %s"   # create desired query
                cur = mysql.connection.cursor()
                cur.execute(query, (playlistName, playlistDescription, userId, id))          # execute desired query
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Playlists SET playlistName = %s, playlistDescription = %s, userId = %s, numberOfSongs = %s WHERE playlistId = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (playlistName, playlistDescription, userId, numberOfSongs, id))
                mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect('/playlists')


# --------------------------------------- #
#           Songs table
# --------------------------------------- #

# CREATE  [C in CRUD]
@app.route('/songs', methods=['POST', 'GET'])
def song():
# Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == 'POST':
        # fire off if user presses the Add Person button
        if request.form.get("Add_Song"):
            # grab user form inputs
            songName = request.form["songName"]
            albumId = request.form["albumId"]
            artistId = request.form["artistId"]
            genre = request.form["genre"]
            songLength = request.form["songLength"]
            totalStreams = request.form["totalStreams"]
            
            # account for songLength being NULL
            if songLength == "":
                # MySQL query to insert a new person into bsg_people with our form inputs
                query = "INSERT INTO Songs (songName, albumId, artistId, genre, totalStreams) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (songName, albumId, artistId, genre, totalStreams))
                mysql.connection.commit()

            # account for userId being NULL
            elif totalStreams == "":
                # MySQL query to insert a new playlist into Playlists with our form inputs
                query = "INSERT INTO Songs (songName, albumId, artistId, genre, songLength) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (songName, albumId, artistId, genre, songLength))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Songs (songName, albumId, artistId, genre, songLength, totalStreams) VALUES (%s, %s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (songName, albumId, artistId, genre, songLength, totalStreams))
                mysql.connection.commit()
        
            # redirect back to people page
            return redirect('/songs')

    # Grab bsg_people data so we send it to our template to display
    if request.method == 'GET':
        # mySQL query to grab all the people in bsg_people
        query = "SELECT songId, songName, albumId, artistId, genre, songLength, totalStreams FROM Songs"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        # Debugging output
        #print("Data fetched from database:", data)

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("songs.j2", data=data)


# DELETE [D in CRUD]
# song.j2 href is routed here and supplies associated {{item.id}} to delete song by their id
@app.route('/delete_song/<int:id>')                           # create route
def delete_song(id):                                          # set method
    # MySQL query to delete the person with our passed id
    # grab form inputs
    query = "DELETE FROM Songs WHERE songId = %s;"           # create desired query
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))                                   # execute desired query.  Including a comma after id in (id,) is necessary otherwise an error will be produced
    mysql.connection.commit()

    # redirect back to people page
    # /delete_people route exists only to perform deletion and is itself not a page that displays to the user
    return redirect('/songs')                                  # load page

# UPDATE [U in CRUD]
@app.route('/edit_song/<int:id>', methods=['POST', 'GET'])    # create route
def edit_song(id):                                            # set method
    # 2 queries are necessary, one to retrieve information for user view and the other to populate the dropdown
    if request.method == 'GET':
        # MySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Songs WHERE songId = %s" % (id) # create desired query      % (id) obtains edit_people(id) and passes it to %s in query
        cur = mysql.connection.cursor()
        cur.execute(query)                                      # execute desired query
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_song.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == 'POST':
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Song"):
            # grab user form inputs
            id = request.form['songId']
            songName = request.form["songName"]
            albumId = request.form["albumId"]
            artistId = request.form["artistId"]
            genre = request.form["genre"]
            songLength = request.form["songLength"]
            totalStreams = request.form["totalStreams"]

            # account for null songLength and totalSteams
            if songLength == '0' and totalStreams == '0':
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE Songs SET songName = %s, albumId = %s, artistId = %s, genre = %s WHERE songId = %s"   # create desired query
                cur = mysql.connection.cursor()
                cur.execute(query, (songName, albumId, artistId, genre))          # execute desired query
                mysql.connection.commit()

            # account for null songLength
            elif songLength == '0':
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE Songs SET songName = %s, albumId = %s, artistId = %s, genre = %s, totalStreams = %s WHERE songId = %s"   # create desired query
                cur = mysql.connection.cursor()
                cur.execute(query, (songName, albumId, artistId, genre, totalStreams))          # execute desired query
                mysql.connection.commit()

            # account for null totalStreams
            elif totalStreams == '0':
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE Songs SET songName = %s, albumId = %s, artistId = %s, genre = %s, songLength = %s WHERE songId = %s"   # create desired query
                cur = mysql.connection.cursor()
                cur.execute(query, (songName, albumId, artistId, genre, songLength))          # execute desired query
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Songs SET songName = %s, albumId = %s, artistId = %s, genre = %s, songLength = %s, totalStreams = %s WHERE songId = %s"   # create desired query
                cur = mysql.connection.cursor()
                cur.execute(query, (songName, albumId, artistId, genre, songLength, totalStreams))          # execute desired query
                mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect('/songs')

# --------------------------------------- #
#           Users table
# --------------------------------------- #

# CREATE  [C in CRUD]
@app.route('/users', methods=['POST', 'GET'])
def song():
# Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == 'POST':
        # fire off if user presses the Add Person button
        if request.form.get("Add_User"):
            # grab user form inputs
            fName = request.form["fName"]
            lName = request.form["lName"]
            email = request.form["email"]
            dob = request.form["dob"]
            subscriptionId = request.form["subscriptionId"]

            # MySQL query to insert a new person into bsg_people with our form inputs
            query = "INSERT INTO Artists (fName, lName, email, dob, subscriptionId) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (fName, lName, email, dob, subscriptionId))
            mysql.connection.commit()
        
            # redirect back to people page
            return redirect('/users')

    # Grab bsg_people data so we send it to our template to display
    if request.method == 'GET':
        # mySQL query to grab all the people in bsg_people
        query = "SELECT userId, fName, lName, email, dob, subscriptionId FROM Users"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        # Debugging output
        #print("Data fetched from database:", data)

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("users.j2", data=data)


# DELETE [D in CRUD]
# song.j2 href is routed here and supplies associated {{item.id}} to delete song by their id
@app.route('/delete_user/<int:id>')                           # create route
def delete_song(id):                                          # set method
    # MySQL query to delete the person with our passed id
    # grab form inputs
    query = "DELETE FROM Users WHERE userId = %s;"           # create desired query
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))                                   # execute desired query.  Including a comma after id in (id,) is necessary otherwise an error will be produced
    mysql.connection.commit()

    # redirect back to people page
    # /delete_people route exists only to perform deletion and is itself not a page that displays to the user
    return redirect('/users')                                  # load page

# UPDATE [U in CRUD]
@app.route('/edit_user/<int:id>', methods=['POST', 'GET'])    # create route
def edit_song(id):                                            # set method
    # 2 queries are necessary, one to retrieve information for user view and the other to populate the dropdown
    if request.method == 'GET':
        # MySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Users WHERE userId = %s" % (id) # create desired query      % (id) obtains edit_people(id) and passes it to %s in query
        cur = mysql.connection.cursor()
        cur.execute(query)                                      # execute desired query
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_user.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == 'POST':
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_User"):
            # grab user form inputs
            id = request.form['artistId']
            fName = request.form["fName"]
            lName = request.form["lName"]
            email = request.form["email"]
            dob = request.form["dob"]
            subscriptionId = request.form["subscriptionId"]

            # mySQL query to update the attributes of person with our passed id value
            query = "UPDATE Users SET fName = %s, lName = %s, email = %s, dob = %s WHERE userId = %s"   # create desired query
            cur = mysql.connection.cursor()
            cur.execute(query, (fName, lName, email, dob, subscriptionId))          # execute desired query
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect('/users')


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)