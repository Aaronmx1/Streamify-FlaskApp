# Streamify - FlaskApp
Hosting MySQL database using Flask and Jinja<br>

Music Streaming frontend and backend handled in Python/Flask<br>

Streamify Music Streaming Service/Database<br>

**A. Overview**<br>
Our system, Streamify, aims to provide a streamlined database-driven platform that allows administrators to manage essential components of a music streaming service.<br>
Streamify would serve as an internal tool for managing artists, albums, songs, and user-generated playlists, ensuring that music libraries are organized efficiently.<br>
The system will allow administrators to:<br>

  - Add and manage new songs, albums, and artists.<br>
  - Monitor the total number of streams for each artist and track.<br>
  - Organize songs into user-created playlists.<br>
  - Allow users to create profiles and subscribe to different subscription tiers.<br>
  - Allow users to keep track of songs that they like.<br>

The platform will manage millions of tracks from thousands of artists as well as keep track of the streaming history of millions of users, making it a perfect solution for music distribution.<br>
With this reliable back-end database, Streamify will ensure accurate tracking of streams, easy management of content, and efficient generation of user playlists to offer a premium experience for both administrators and users.<br>

**B. Database Outline**<br>

**Entities**<br>

- **Songs**: This table stores information about individual songs<br>
  - **Attributes**<br>
    - `songId`: int, Primary Key, auto_increment, not NULL<br>
    - `songName`: varchar, not NULL<br>
    - `albumId`: int, not NULL, Foreign Key<br>
    - `artistId`: int, not NULL, Foreign Key<br>
    - `genre`: varchar, not NULL<br>
    - `songLength`: time, NOT NULL<br>
    - `totalStreams`: int, not NULL<br>
  - **Relationships**<br>
    - A M:1 relationship exists between Songs and Albums. `albumId` in Songs references the Albums table.<br>
    - A M:1 relationship exists between Songs and Artists. `artistId` in Songs references the Artists table.<br>
    - A M:N relationship exists between Songs and Users. An intersection table `LikedSongs` manages this relationship.<br>

- **Artists**: This table stores information about the artists who post music to the platform<br>
  - **Attributes**<br>
    - `artistId`: int, Primary Key, auto_increment, not NULL<br>
    - `artistName`: varchar, not NULL<br>
    - `fName`: varchar, not NULL<br>
    - `lName`: varchar, not NULL<br>
    - `email`: varchar, not NULL<br>
  - **Relationships**<br>
    - A 1:M relationship exists between Artists and Songs. `artistId` in Songs references the Artists table.<br>
    - A 1:M relationship exists between Artists and Albums. `artistId` in Albums references the Artists table.<br>
    - A M:N relationship exists between Artists and Songs. An intersection table `Collaborations` manages this relationship.<br>

- **Albums**: This table contains information about albums released by artists<br>
  - **Attributes**<br>
    - `albumId`: int, Primary Key, auto_increment, not NULL<br>
    - `albumName`: varchar, not NULL<br>
    - `recordStudio`: varchar<br>
    - `yearReleased`: int, not NULL<br>
    - `artistId`: int, Foreign Key<br>
    - `numberOfSongs`: int, not NULL, Default 0<br>
  - **Relationships**<br>
    - A 1:M relationship exists between Albums and Songs. `albumId` in Songs references the Albums table.<br>
    - A M:1 relationship exists between Albums and Artists. `artistId` in Albums references the Artists table.<br>

- **Users**: This table stores user profile information<br>
  - **Attributes**<br>
    - `userId`: int, Primary Key, auto_increment, not NULL<br>
    - `username`: varchar, not NULL<br>
    - `fName`: varchar, not NULL<br>
    - `lName`: varchar, not NULL<br>
    - `email`: varchar, not NULL, Unique<br>
    - `dob`: date, not NULL<br>
  - **Relationships**<br>
    - A M:N relationship exists between Users and Songs. An intersection table `LikedSongs` manages this relationship.<br>

- **LikedSongs**: This table facilitates the M:N relationship between Users and Songs.<br>
  - **Attributes**<br>
    - `likedSongsId`: int, Primary Key, auto_increment<br>
    - `songId`: int, unique, not NULL, Foreign Key<br>
    - `userId`: int, unique, not NULL, Foreign Key<br>
  - **Relationships**<br>
    - A M:1 relationship exists between LikedSongs and Songs.<br>
    - A M:1 relationship exists between LikedSongs and Users.<br>

**C. Entity Relationship Diagram:**<br>
![MusicSchema](https://github.com/user-attachments/assets/7e06d868-5eab-46c1-b5a3-2739dd51c1ff)
