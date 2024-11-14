/* 
 Streamify: Creation of Music Streaming Service backend tables
 Team 34
 Project Team:
    - Aaron Martinez
    - Tim Newell

Steps to run file:
    1. Save this file to directory
    2. Open terminal in that directory
    3. Type the following commands:
        a. mysql -u cs340_[ONID] -h classmysql.engr.oregonstate.edu -p
        b. * enter password when prompted *
        c. use cs340_[ONID];
        d. source DDL.SQL;
*/

-- Disable commits and foreign key checks to minimize import errors.  These are set back at the end of DDL import.
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT=0;

-- Drop existing tables to re-create tables
DROP TABLE IF EXISTS AddedSongs;
DROP TABLE IF EXISTS Collaborations;
DROP TABLE IF EXISTS Artists;
DROP TABLE IF EXISTS Playlists;
DROP TABLE IF EXISTS Songs;
DROP TABLE IF EXISTS LikedSongs;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Albums;
DROP TABLE IF EXISTS Subscriptions;


/*-------------------------------------------
*               CREATE tables
*/-------------------------------------------

-- AddedSongs table handles M:N relationship between Playlists and Songs
CREATE TABLE AddedSongs (
    addedSongsId int(11) NOT NULL AUTO_INCREMENT,
    playlistId int(11) NOT NULL,
    songId int(11) NOT NULL,
    PRIMARY KEY (addedSongsId),
    -- MUL: The column has a non-unique index, meaning it can contain duplicate values, but it's indexed for faster searches.
    -- KEY: Lists attribute as a key to be used as an index for foreign key matching
    CONSTRAINT FOREIGN KEY (playlistId) REFERENCES Playlists (playlistId)
        -- ON UPDATE CASCADE updated value and updates table
        ON UPDATE CASCADE
        -- ON DELETE RESTRICT will restrict deletions from being reflected on this table
        ON DELETE RESTRICT,    
    CONSTRAINT FOREIGN KEY (songId) REFERENCES Songs (songId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Collaborations table handles M:N relationship between Artists and Songs
CREATE TABLE Collaborations (
    collaborationId int(11) NOT NULL AUTO_INCREMENT,
    songId int(11) NOT NULL,
    artistId int(11) NOT NULL,
    primary key (collaborationId),
    CONSTRAINT FOREIGN KEY (artistId) REFERENCES Artists(artistId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT FOREIGN KEY (songId) REFERENCES Songs(songId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Artists table contains artist details
CREATE TABLE Artists (
    artistId int(11) NOT NULL AUTO_INCREMENT,
    fName varchar(50) NOT NULL,
    lName varchar(50) NOT NULL,
    email varchar(50) NOT NULL,
    PRIMARY KEY (artistId)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Playlists table contains system and user generated playlists
CREATE TABLE Playlists (
    playlistId int(11) NOT NULL AUTO_INCREMENT,
    playlistName varchar(50) NOT NULL,
    playlistDescription varchar(50) NOT NULL,
    userId int(11) NOT NULL,
    numberOfSongs int(11) NOT NULL DEFAULT 0,
    PRIMARY KEY (playlistId),
    CONSTRAINT FOREIGN KEY (userId) REFERENCES Users(userId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Songs table contains artist created songs
CREATE TABLE Songs (
    songId int(11) NOT NULL AUTO_INCREMENT,
    songName varchar(50) NOT NULL,
    albumId int(11) NOT NULL,
    artistId int(11) NOT NULL,
    genre varchar(50) NOT NULL,
    songLength time NOT NULL,
    totalStreams int(11) NOT NULL DEFAULT 0,
    PRIMARY KEY (songId),
    CONSTRAINT FOREIGN KEY (albumId) REFERENCES Albums (albumId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT FOREIGN KEY (artistId) REFERENCES Artists (artistId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Handles M:N relationship between Users and Songs
CREATE TABLE LikedSongs (
    likedSongsId int(11) NOT NULL AUTO_INCREMENT,
    songId int(11) NOT NULL,
    userId int(11) NOT NULL,
    PRIMARY KEY (likedSongsId),
    CONSTRAINT FOREIGN KEY (songId) REFERENCES Songs (songId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT FOREIGN KEY (userId) REFERENCES Users (userId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Users table which contains company user base
CREATE TABLE Users (
    userId int(11) NOT NULL AUTO_INCREMENT,
    fName varchar(50) NOT NULL,
    lName varchar(50) NOT NULL,
    email varchar(50) NOT NULL UNIQUE,
    dob date NOT NULL,
    subscriptionId int(11) NOT NULL,
    PRIMARY KEY (userId),
    CONSTRAINT FOREIGN KEY (subscriptionId) REFERENCES Subscriptions (subscriptionId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Albums table which contains collections of songs from artists
CREATE TABLE Albums (
    albumId int(11) NOT NULL AUTO_INCREMENT,
    albumName varchar(50) NOT NULL,
    recordStudio varchar(50) NOT NULL,
    yearReleased int(11) NOT NULL,
    artistId int(11) NOT NULL,
    numberOfSongs int(11) NOT NULL DEFAULT 0,
    PRIMARY KEY (albumId),
    CONSTRAINT FOREIGN KEY (artistId) REFERENCES Artists (artistId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Subscriptions table handles types of plans user base is subscribed to
CREATE TABLE Subscriptions (
    subscriptionId int(11) NOT NULL AUTO_INCREMENT,
    subscriptionDescription varchar(50) NOT NULL UNIQUE,
    price decimal(10,2) NOT NULL,
    numberOfSubscriptions int(11) DEFAULT 0,
    PRIMARY KEY (subscriptionId)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



/*-------------------------------------------
*       INSERT into tables
*/-------------------------------------------

-- Insert data into Subscriptions table
INSERT INTO Subscriptions (
    subscriptionDescription,
    price,
    numberOfSubscriptions
) VALUES (
    'Premium Individual',
    15,
    0
),
(
    'Premium Family',
    30,
    0
),
(
    'Free',
    0,
    0
);

-- Insert data into Users table
INSERT INTO Users (
    fName,
    lName,
    email,
    dob,
    subscriptionId
) VALUES (
    'Tim',
    'Newell',
    'tnewell@gmail.com',
    '2023-03-04',
    ( SELECT subscriptionId from Subscriptions WHERE subscriptionDescription = 'Premium Individual' )
),
(
    'Aaron',
    'Martinez',
    'amartinez@gmail.com',
    '2023-05-06',
    ( SELECT subscriptionId from Subscriptions WHERE subscriptionDescription = 'Premium Family' )
),
(
    'Elon',
    'Musk',
    'emusk@gmail.com',
    '2024-02-02',
    ( SELECT subscriptionId from Subscriptions WHERE subscriptionDescription = 'Free' )
);

-- Insert data into Artists table
INSERT INTO Artists(
    fName,
    lName,
    email
) VALUES (
    'John',
    'Mayer',
    'jmayer@gmail.com'
),
(
    'Ben',
    'Rector',
    'brector@gmail.com'
),
(
    'Jeff',
    'Buckley',
    'jbuckley@gmail.com'
),
(
    'Childish',
    'Gambino',
    'cgambino@gmail.com'
),
(
    'Taylor',
    'Swift',
    'tswift@gmail.com'
),
(
    'Post',
    'Malone',
    'pmalone@gmail.com'
);

-- Insert data into Albums table
INSERT INTO Albums(
    albumName, 
    recordStudio,
    yearReleased,
    artistId,
    numberOfSongs
) VALUES (
    'Continuum',
    'Aware Records LLC',
    2006,
    ( SELECT artistId from Artists WHERE fName = 'John' and lName = 'Mayer' ),
    12
),
(
    'Magic',
    'OK Kid Recordings LLC',
    2018,
    ( SELECT artistId from Artists WHERE fName = 'Ben' and lName = 'Rector' ),
    13
),
(
    'Grace',
    'Colombia Records',
    1994,
    ( SELECT artistId from Artists WHERE fName = 'Jeff' and lName = 'Buckley' ),
    11
),
(
    'Awaken, My Love!',
    'McDJ Entertainment',
    2016,
    ( SELECT artistId from Artists WHERE fName = 'Childish' and lName = 'Gambino' ),
    11
),
(
    'Tortured Poets Department',
    'Taylor Swift',
    2024,
    ( SELECT artistId from Artists WHERE fName = 'Taylor' and lName = 'Swift' ),
    16
);

-- Insert data into Songs table
INSERT INTO Songs(
    songName,
    albumId,
    artistId,
    genre,
    songLength,
    totalStreams
) VALUES (
    'Gravity',
    ( SELECT albumId from Albums WHERE albumName = 'Continuum' ),
    ( SELECT artistId from Artists WHERE fName = 'John' and lName = 'Mayer' ),
    'Blues',
    '4:05:0',
    0
),
(
    'Drive',
    ( SELECT albumId from Albums WHERE albumName = 'Magic' ),
    ( SELECT artistId from Artists WHERE fName = 'Ben' and lName = 'Rector' ),
    'Pop',
    '3:17:0',
    0
),
(
    "Lover You Should've Come Over",
    ( SELECT albumId from Albums WHERE albumName = 'Grace' ),
    ( SELECT artistId from Artists WHERE fName = 'Jeff' and lName = 'Buckley' ),
    'Alternative Rock',
    '6:44:0',
    0
),
(
    'Redbone',
    ( SELECT albumId from Albums WHERE albumName = 'Awaken, My Love!' ),
    ( SELECT artistId from Artists WHERE fName = 'Childish' and lName = 'Gambino' ),
    'R&B',
    '5:26:0',
    0
),
(
    'Fortnight',
    ( SELECT albumId from Albums WHERE albumName = 'Tortured Poets Department' ),
    ( SELECT artistId from Artists WHERE fName = 'Taylor' and lName = 'Swift' ),
    'Pop',
    '3:48:0',
    0
);

-- Insert data into Collaborations table
INSERT INTO Collaborations (
    songId,
    artistId
) VALUES (
    ( SELECT songId from Songs WHERE songName = 'Fortnight' ),
    ( SELECT artistId from Artists WHERE fName = 'Post' and lName = 'Malone' )
),
(
    ( SELECT songId from Songs WHERE songName = 'Gravity' ),
    ( SELECT artistId from Artists WHERE fName = 'Ben' and lName = 'Rector' )
),
(
    ( SELECT songId from Songs WHERE songName = 'Redbone' ),
    ( SELECT artistId from Artists WHERE fName = 'John' and lName = 'Mayer' )
);

-- Insert data into Playlists table
INSERT INTO Playlists (
    playlistName,
    playlistDescription,
    userId,
    numberOfSongs
) VALUES (
    'Good Songs',
    'Some good songs that I like',
    ( SELECT userId from Users WHERE email = 'tnewell@gmail.com' ),
    4
),
(
    'Bad Songs',
    "Songs that I don't like",
    ( SELECT userId from Users WHERE email = 'emusk@gmail.com' ),
    2
),
(
    'Other songs',
    'Various Songs',
    ( SELECT userId from Users WHERE email = 'amartinez@gmail.com' ),
    3
);

-- Insert data into AddedSongs table
INSERT INTO AddedSongs (
    playlistId,
    songId
) VALUES (
    ( SELECT playlistId from Playlists WHERE playlistName = 'Good Songs' ),
    ( SELECT songId from Songs WHERE songName = 'Gravity' )
),
(
    ( SELECT playlistId from Playlists WHERE playlistName = 'Good Songs' ),
    ( SELECT songId from Songs WHERE songName = 'Redbone' )    
),
(
    ( SELECT playlistId from Playlists WHERE playlistName = 'Good Songs' ),
    ( SELECT songId from Songs WHERE songName = 'Drive' )
),
(
    ( SELECT playlistId from Playlists WHERE playlistName = 'Good Songs' ),
    ( SELECT songId from Songs WHERE songName = "Lover You Should've Come Over" )
),
(
    ( SELECT playlistId from Playlists where playlistName = 'Bad Songs' ),
    ( SELECT songId from Songs WHERE songName = "Lover You Should've Come Over" )
),
(
    ( SELECT playlistId from Playlists where playlistName = 'Bad Songs' ),
    ( SELECT songId from Songs WHERE songName = 'Fortnight' )
);

-- Insert data into LikedSongs table
INSERT INTO LikedSongs (
    songId,
    userId
) VALUES(
    (SELECT songId from Songs WHERE songName = 'Gravity'),
    (SELECT userId from Users WHERE fName = 'Aaron' AND lName = 'Martinez')
),
(
    (SELECT songId from Songs WHERE songName = 'Drive'),
    (SELECT userId from Users WHERE fName = 'Tim' AND lName = 'Newell')
),
(
    (SELECT songId from Songs WHERE songName = 'Redbone'),
    (SELECT userId from Users WHERE fName = 'Elon' AND lName = 'Musk')
);

-- Enable commit and foreign key checks to catch errors
SET FOREIGN_KEY_CHECKS=1;
COMMIT;
