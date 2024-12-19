# FlaskApp
Hosting MySQL database using Flask

Music Streaming frontend and backend handled in Python/Flask

Streamify Music Streaming Service/Database

**Overview**
Our system, Streamify, aims to provide a streamlined database-driven
platform that allows administrators to manage essential components of a
music streaming service.
Streamify would serve as an internal tool for managing artists, albums,
songs, and user-generated playlists, ensuring that music libraries are
organized efficiently. 
The system will allow administrators to:

  ● Add and manage new songs, albums, and artists.
  
  ● Monitor the total number of streams for each artist and track.
  
  ● Organize songs into user-created playlists.
  
  ● Allow users to create profiles and subscribe to different subscription
    tiers.
    
  ● Allow users to keep track of songs that they like

The platform will manage millions of tracks from thousands of artists as well
as keep track of the streaming history of millions of users, making it a
perfect solution for music distribution. With this reliable back-end database,
Streamify will ensure accurate tracking of streams, easy management of
content, and efficient generation of user playlists to offer a premium
experience for both administrators and users.


**B. Database Outline**

**Entities**

  ● Songs: This table stores information about individual songs <br>
    ○ &nbsp;Attributes<br>
      ■ &nbsp;songId: int, Primary Key, auto_increment, not NULL<br>
      ■ &nbsp;songName: varchar, not NULL<br>
      ■ &nbsp;albumId: int, not NULL, Foreign Key<br>
      ■ &nbsp;artistId: int, not NULL, Foreign Key<br>
      ■ &nbsp;&nbsp;genre: varchar, not NULL<br>
      ■ songLength: time, NOT NULL<br>
      ■ totalStreams: int, not NULL
    ○ Relationships
      ■ A M:1 relationship exists between Songs and Albums.
      albumId in Songs references the Albums table.
      ■ A M:1 relationship exists between Songs and Artists.
      artistId in Songs references the Artists table.
      ■ A M:N relationship exists between Songs and Users. An
      intersection table LikedSongs manages this relationship.
  
  ● Artists: This table stores information about the artists who post
  music to the platform
  ○ Attributes
    ■ artistId: int, Primary Key, auto_increment, not NULL
    ■ artistName: varchar, not NULL
    ■ fName: varchar, not NULL
    ■ fName: varchar, not NULL
    ■ email: varchar, not NULL
  ○ Relationships
    ■ A 1:M relationship exists between Artists and Songs.
    artistId in Songs references the Artists table.
    ■ A 1:M relationship exists between Artists and Albums.
    artistId in Albums references the Artists table.
    ■ A M:N relationship exists between Artists and Songs. An
    intersection table Collaborations manages this
    relationship.

● Albums: This table contains information about albums released by
artists
  ○ Attributes:
    ■ albumId: int, Primary Key, auto_increment, not NULL
    ■ albumName: varchar, not NULL
    ■ recordStudio: varchar
    ■ yearReleased: int, not NULL
    ■ artistId: int, Foreign Key
    ■ numberOfSongs: int, not NULL, Default 0
  ○ Relationships
    ■ A 1:M relationship exists between Albums and Songs.
    albumId in Songs references the Albums table.
    ■ A M:1 relationship exists betweenAlbums and Artists.
    artistId in Albums references the Artists table.

● Users: This table stores user profile information
  ○ Attributes:
    ■ userId: int, Primary Key, auto_increment, not NULL
    ■ username: varchar, not NULL
    ■ fName: varchar, not NULL
    ■ fName: varchar, not NULL
    ■ email: varchar, not NULL, Unique
    ■ dob: date, not NULL
  ○ Relationships:
    ■ A M:N relationship exists betweenUsers and Songs . An
    intersection table LikedSongs manages this relationship.

● LikedSongs: This table facilitates the M:N relationship between
Users and Songs.
  ○ Attributes:
    ■ likedSongsId: int, Primary Key, auto_increment
    ■ songId: int, unique, not NULL, Foreign Key
    ■ userId: int, unique, not NULL, Foreign Key
  ○ Relationships:
    ■ A M:1 relationship exists between LikedSongs and
    Songs.
    ■ A M:1 relationship exists between LikedSongs and
    Users

**C. Entity Relationship Diagram:**
![MusicSchema](https://github.com/user-attachments/assets/0a7c77de-8d27-42d8-8eee-3f2fa144830a)
