from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from flask import Flask, render_template, json
from flask import redirect  # pip install Flask-SSLify
from flask_mysqldb import MySQL # pip install MySQL
import MySQLdb
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

# db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")


# --------------------------------------- #
#           Artists table           -- AM: COMPLETED 11/11
# --------------------------------------- #

# CREATE  [C in CRUD]
@app.route('/artists', methods=['POST', 'GET'])
def view_artists():
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
        query = "SELECT artistId, fName AS 'First Name', lName AS 'Last Name', email AS 'Email' FROM Artists"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("artists.j2", data=data)


# DELETE [D in CRUD]
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

        # render edit_artist page passing our query data
        return render_template("edit_artist.j2", data=data)

    # POST method
    if request.method == 'POST':
        # fire off if user clicks the 'Edit Artist' button
        if request.form.get("Edit_Artist"):
            # grab user form inputs
            id = request.form['artistId']
            fName = request.form['fName']
            lName = request.form['lName']
            email = request.form['email']

            # account for null first name AND last name
            if fName == "" and lName == "":
                # mySQL query to update the attributes of Artist with our passed id value
                query = "UPDATE Artists SET fName = %s, lName = %s, email = NULL WHERE artistId = %s"   # create desired query
                cur = mysql.connection.cursor()
                cur.execute(query, (fName, lName, id))          # execute desired query
                mysql.connection.commit()

            # account for null email
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

            # redirect back to artists page after we execute the update query
            return redirect('/artists')

# --------------------------------------- #
#           Songs table             -- AM: COMPLETED 11/11
# --------------------------------------- #

# CREATE  [C in CRUD]
@app.route('/songs', methods=['POST', 'GET'])
def view_songs():
# Separate out the request methods, in this case this is for a POST
    # insert a song into the Song entity
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
            
            # Expected input for Songs 
            query = "INSERT INTO Songs (songName, albumId, artistId, genre, songLength, totalStreams) VALUES (%s, %s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (songName, albumId, artistId, genre, songLength, totalStreams))
            mysql.connection.commit()
        
            # redirect back to songs page
            return redirect('/songs')

    # Grab song data so we send it to our template to display
    if request.method == 'GET':
        # mySQL query to grab all the people in Songs
        query = "SELECT Songs.songId, Songs.songName AS 'Song Name', Albums.albumName AS 'Album Name', CONCAT(Artists.fName, ' ', Artists.lName) AS 'Artist Name', Songs.genre AS 'Genre', Songs.songLength AS 'Song Length', Songs.totalStreams AS 'Total Streams' FROM Songs INNER JOIN Albums ON Songs.albumId = Albums.albumId INNER JOIN Artists ON Songs.artistId = Artists.artistId"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        
        # mySQL query to grab all the album names in Albums
        query2 = "SELECT albumId, albumName FROM Albums"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        albums_data = cur.fetchall()

        # mySQL query to grab all the people in Artists
        query3 = "SELECT artistId, CONCAT(fName, ' ', lName) AS artistName FROM Artists"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        artists_data = cur.fetchall()

        # render songs page passing our query data
        return render_template("songs.j2", data=data, albums=albums_data, artists=artists_data)


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
    # /delete_song route exists only to perform deletion and is itself not a page that displays to the user
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

        # MySQL query to grab albumId and albumName from Album
        query2 = "SELECT albumId, albumName FROM Albums" # create desired query
        cur = mysql.connection.cursor()
        cur.execute(query2)                                      # execute desired query
        album_data = cur.fetchall()

        # MySQL query to grab albumId and albumName from Album
        query3 = "SELECT artistId, CONCAT(fName, ' ', lName) AS artistName FROM Artists" # create desired query
        cur = mysql.connection.cursor()
        cur.execute(query3)                                      # execute desired query
        artist_data = cur.fetchall()

        # render edit_song page passing our query data
        return render_template("edit_song.j2", data=data, albums=album_data, artists=artist_data)

    # POST method
    if request.method == 'POST':
        # fire off if user clicks the 'Edit Song' button
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
            query = "UPDATE Songs SET songName = %s, albumId = (SELECT albumId FROM Albums WHERE albumId = %s), artistId = (SELECT artistId FROM Artists Where artistId = %s), genre = %s, songLength = %s, totalStreams = %s WHERE songId = %s"   # create desired query
            cur = mysql.connection.cursor()
            cur.execute(query, (songName, albumId, artistId, genre, songLength, totalStreams, id))          # execute desired query
            mysql.connection.commit()   

            # redirect back to people page after we execute the update query
            return redirect('/songs')

# --------------------------------------- #
#           Users table             -- AM: COMPLETED 11/11
# --------------------------------------- #

# CREATE  [C in CRUD]
@app.route('/users', methods=['POST', 'GET'])
def view_users():
# Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == 'POST':
        # fire off if user presses the Add User button
        if request.form.get("Add_User"):
            # grab user form inputs
            fName = request.form["fName"]
            lName = request.form["lName"]
            email = request.form["email"]
            dob = request.form["dob"]

            # MySQL query to insert a new person into Users with our form inputs
            query = "INSERT INTO Users (fName, lName, email, dob) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (fName, lName, email, dob))
            mysql.connection.commit()
        
            # redirect back to users page
            return redirect('/users')

    # Grab User data so we send it to our template to display
    if request.method == 'GET':
        # mySQL query to grab all the people in Users
        query = "SELECT userId, fName AS 'First Name', lName AS 'Last Name', email AS 'Email', dob AS 'DOB' FROM Users"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render users page passing our query data
        return render_template("users.j2", data=data)


# DELETE [D in CRUD]
# user.j2 href is routed here and supplies associated {{item.id}} to delete song by their id
@app.route('/delete_user/<int:id>')                           # create route
def delete_user(id):                                          # set method
    # MySQL query to delete the person with our passed id
    # grab form inputs
    query = "DELETE FROM Users WHERE userId = %s;"           # create desired query
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))                                   # execute desired query.  Including a comma after id in (id,) is necessary otherwise an error will be produced
    mysql.connection.commit()

    # redirect back to people page
    # /delete_users route exists only to perform deletion and is itself not a page that displays to the user
    return redirect('/users')                                  # load page

# UPDATE [U in CRUD]
@app.route('/edit_user/<int:id>', methods=['POST', 'GET'])    # create route
def edit_user(id):                                            # set method
    # 2 queries are necessary, one to retrieve information for user view and the other to populate the dropdown
    if request.method == 'GET':
        # MySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Users WHERE userId = %s" % (id) # create desired query      % (id) obtains edit_people(id) and passes it to %s in query
        cur = mysql.connection.cursor()
        cur.execute(query)                                      # execute desired query
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_user.j2", data=data)

    # POST method
    if request.method == 'POST':
        # fire off if user clicks the 'Edit User' button
        if request.form.get("Edit_User"):
            # grab user form inputs
            id = request.form['userId']
            fName = request.form["fName"]
            lName = request.form["lName"]
            email = request.form["email"]
            dob = request.form["dob"]

            # mySQL query to update the attributes of person with our passed id value
            query = "UPDATE Users SET fName = %s, lName = %s, email = %s, dob = %s WHERE userId = %s"   # create desired query
            cur = mysql.connection.cursor()
            cur.execute(query, (fName, lName, email, dob, id))          # execute desired query
            mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect('/users')

# --------------------------------------- #
#           Albums table        -- AM: COMPLETED 11/11
# --------------------------------------- #

# CREATE  [C in CRUD]
@app.route('/albums', methods=['POST', 'GET'])
def view_albums():
# Separate out the request methods, in this case this is for a POST
    # insert a person into the Albums entity
    if request.method == 'POST':
        # fire off if user presses the Add Person button
        if request.form.get("Add_Album"):
            # grab user form inputs
            albumName = request.form["albumName"]
            recordStudio = request.form["recordStudio"]
            yearReleased = request.form["yearReleased"]
            artistId = request.form["artistId"]
            numberOfSongs = request.form["numberOfSongs"]

            if numberOfSongs == '0': 
                # MySQL query to insert a new person into Albums with our form inputs
                query = "INSERT INTO Albums (albumName, recordStudio, yearReleased, artistId, numberOfSongs = 0) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (albumName, recordStudio, yearReleased, artistId))
                mysql.connection.commit()

            else:
                # MySQL query to insert a new album into Albums with our form inputs
                query = "INSERT INTO Albums (albumName, recordStudio, yearReleased, artistId, numberOfSongs) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (albumName, recordStudio, yearReleased, artistId, numberOfSongs))
                mysql.connection.commit()
        
            # redirect back to albums page
            return redirect('/albums')

    # Grab Album data so we send it to our template to display
    if request.method == 'GET':
        # mySQL query to grab all the albums in Albums
        query = "SELECT Albums.albumId, Albums.albumName AS 'Album Name', Albums.recordStudio AS 'Record Studio', Albums.yearReleased AS 'Year Released', CONCAT(Artists.fName, ' ', Artists.lName) AS 'Artist Name', Albums.numberOfSongs AS 'Number of Songs' FROM Albums INNER JOIN Artists ON Albums.artistId = Artists.artistId"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab Artists id/name for our dropdown
        query2 = "SELECT artistId, CONCAT(fName, ' ', lName) AS artistName FROM Artists"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        artists_data = cur.fetchall()

        # render albums page passing our query data
        return render_template("albums.j2", data=data, artists=artists_data)


# DELETE [D in CRUD]
# user.j2 href is routed here and supplies associated {{item.id}} to delete song by their id
@app.route('/delete_album/<int:id>')                           # create route
def delete_album(id):                                          # set method
    # MySQL query to delete the person with our passed id
    # grab form inputs
    query = "DELETE FROM Albums WHERE albumId = %s;"           # create desired query
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))                                   # execute desired query.  Including a comma after id in (id,) is necessary otherwise an error will be produced
    mysql.connection.commit()

    # redirect back to people page
    # /delete_album route exists only to perform deletion and is itself not a page that displays to the user
    return redirect('/albums')                                  # load page

# UPDATE [U in CRUD]
@app.route('/edit_album/<int:id>', methods=['POST', 'GET'])    # create route
def edit_album(id):                                            # set method
    # 2 queries are necessary, one to retrieve information for user view and the other to populate the dropdown
    if request.method == 'GET':
        # MySQL query to grab the info of the album with our passed id
        query = "SELECT * FROM Albums WHERE albumId = %s" % (id) # create desired query      % (id) obtains edit_album(id) and passes it to %s in query
        cur = mysql.connection.cursor()
        cur.execute(query)                                      # execute desired query
        data = cur.fetchall()

        # mySQL query to grab Artists id/name for our dropdown
        query2 = "SELECT artistId, CONCAT(fName, ' ', lName) AS artistName FROM Artists"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        artists_data = cur.fetchall()

        # render edit_album page passing our query data
        return render_template("edit_album.j2", data=data, artists=artists_data)

    # POST method
    if request.method == 'POST':
        # fire off if user clicks the 'Edit Album' button
        if request.form.get("Edit_Album"):
            # grab album form inputs
            id = request.form['albumId']
            albumName = request.form["albumName"]
            recordStudio = request.form["recordStudio"]
            yearReleased = request.form["yearReleased"]
            artistId = request.form["artistId"]
            numberOfSongs = request.form["numberOfSongs"]

            # mySQL query to update the attributes of album with our passed id value
            query = "UPDATE Albums SET albumName = %s, recordStudio = %s, yearReleased = %s, artistId = (SELECT artistId FROM Artists WHERE artistId = %s), numberOfSongs = %s WHERE albumId = %s"   # create desired query
            cur = mysql.connection.cursor()
            cur.execute(query, (albumName, recordStudio, yearReleased, artistId, numberOfSongs, id))          # execute desired query
            mysql.connection.commit()

            # redirect back to albums page after we execute the update query
            return redirect('/albums')

# --------------------------------------- #
#           LikedSongs table      -- AM: COMPLETED 11/13  
# --------------------------------------- #

# CREATE  [C in CRUD]
@app.route('/likedSongs', methods=['POST', 'GET'])
def view_likedSongs():
# Separate out the request methods, in this case this is for a POST
    # insert a liked song into the LikedSong entity
    if request.method == 'POST':
        # fire off if user presses the Add Person button
        if request.form.get("Add_LikedSong"):
            # grab user form inputs
            songId = request.form["songId"]
            userId = request.form["userId"]

            # MySQL query to insert a new song into LikedSongs with our form inputs
            query = "INSERT INTO LikedSongs (songId, userId) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (songId, userId))
            mysql.connection.commit()
        
            # redirect back to likedSongs page
            return redirect('/likedSongs')

    # Grab likedSongs data so we send it to our template to display
    if request.method == 'GET':
        # mySQL query to grab all the songs in LikedSongs
        query = "SELECT LikedSongs.likedSongsId, Songs.songName AS 'Song Name', CONCAT(Users.fName, ' ', Users.lName) AS Username FROM LikedSongs INNER JOIN Songs ON LikedSongs.songId = Songs.songId INNER JOIN Users ON LikedSongs.userId = Users.userId"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab Songs id/name for our dropdown
        query2 = "SELECT songId, songName FROM Songs"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        songs_data = cur.fetchall()

        # mySQL query to grab Users id/name for our dropdown
        query3 = "SELECT userId, CONCAT(fName, ' ', lName) as userName FROM Users"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        users_data = cur.fetchall()

        # render edit_likedSongs page passing our query data
        return render_template("likedSongs.j2", data=data, songs=songs_data, users=users_data)


# DELETE [D in CRUD]
# user.j2 href is routed here and supplies associated {{item.id}} to delete song by their id
@app.route('/delete_likedSong/<int:id>')                           # create route
def delete_likedSong(id):                                          # set method
    # MySQL query to delete the person with our passed id
    # grab form inputs
    query = "DELETE FROM LikedSongs WHERE likedSongsId = %s;"           # create desired query
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))                                   # execute desired query.  Including a comma after id in (id,) is necessary otherwise an error will be produced
    mysql.connection.commit()

    # redirect back to likedSongs page
    # /delete_likedSongs route exists only to perform deletion and is itself not a page that displays to the user
    return redirect('/likedSongs')                                  # load page

# UPDATE [U in CRUD]
@app.route('/edit_likedSong/<int:id>', methods=['POST', 'GET'])    # create route
def edit_likedSong(id):                                            # set method
    # 2 queries are necessary, one to retrieve information for user view and the other to populate the dropdown
    if request.method == 'GET':
        # MySQL query to grab the info of the likedSongs with our passed id
        query = "SELECT * FROM LikedSongs WHERE likedSongsId = %s" % (id) # create desired query
        cur = mysql.connection.cursor()
        cur.execute(query)                                      # execute desired query
        data = cur.fetchall()

        # mySQL query to grab Songs id/name for our dropdown
        query2 = "SELECT songId, songName FROM Songs"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        songs_data = cur.fetchall()

        # mySQL query to grab Users id/name for our dropdown
        query3 = "SELECT userId, CONCAT(fName, ' ', lName) AS userName FROM Users"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        users_data = cur.fetchall()

        # render edit_likedSong page passing our query data
        return render_template("edit_likedSong.j2", data=data, songs=songs_data, users=users_data)

    # POST method
    if request.method == 'POST':
        # fire off if user clicks the 'Edit LikedSong' button
        if request.form.get("Edit_LikedSong"):
            # grab user form inputs
            id = request.form['likedSongsId']
            songId = request.form["songId"]
            userId = request.form["userId"]

            # mySQL query to update the attributes of person with our passed id value
            query = "UPDATE LikedSongs SET songId = %s, userId = %s WHERE likedSongsId = %s"   # create desired query
            cur = mysql.connection.cursor()
            cur.execute(query, (songId, userId, id))          # execute desired query
            mysql.connection.commit()

            # redirect back to likedSongs page after we execute the update query
            return redirect('/likedSongs')



# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)
