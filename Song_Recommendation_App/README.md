# Song Recommendation Using Weaviate Vector Database 

<img width="1726" alt="Screenshot 2024-06-05 at 14 40 11" src="https://github.com/gialiubc/Weaviate_Song_Recommendation_App/assets/141379548/2da80a6a-ad75-4c82-a459-cb640f17b527">

## Overview
This project is a response to Weaviate's Machine Learning Engineer Challenge, Track 1 and Track 2.1.

In this project, a web app is created to get song recommendations to user's playlist with the search from two million songs that are vectorized and stored in Weaviate vector database. What you'll expect in this project:

- Part 1 Data Manipulation: Data cleaning, transformation, and loading into weaviate vector database. I use my own vectors (Embeddings).
- Part 2 Similarity Search: Perform similarity search with an user input of a playlist and find from the database 20 songs that are most similar to the songs from the user's playlist. This would make the recommendation.
- Part 3 App backend : Set up App backend with Python Flask.
- Part 4 App frontend : Using HTML, CSS, JavaScript to create the visualization of the song recommendation app.
  
## Files
I have upload all the files and folders that I used to create the app. Everything is organized in the following way:

- Coding_notebook folder : contains all the codes in jupyter notebook which I used for creating the app. 
- app.py file : Use this to run the app.
- Other folders for running the app :
  - static folder : includes css, js, img folders;
  - templates folder : includes index.html for landing page and result.html for song recommendation result page;
  - Resources folder : includes a scaler saved for scaling the vectors.

## Data ETL and Vector Database
The data used for this project is based on the project Jammin'_With_Spotify. The data is slightly modified in order to adjust to this project. The original ETL of the dataset will not be explained here, and for more details please go to https://github.com/gialiubc/Jammin_With_Spotify/tree/main.

Each song track has feautres such as danceability, energy, key, mode (minor or major), speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms, and time_signature (beats per bar), which is considered to be its 'numerical' representation, so we use these features as its search vectors.

Therefore, we create two datasets as output. One contains the scaled track features (embeddings) as vector information of each track. The other one contains track information such as track uri, track_href etc.

- scaled_vec_tracks.csv data file :
  - Vector Columns: 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms','key_none', 'key_0', 'key_1', 'key_2', 'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 'key_9', 'key_10', 'key_11', 'mode_minor', 'mode_major', 'time_signature_0', 'time_signature_1', 'time_signature_2', 'time_signature_3', 'time_signature_4', 'time_signature_5', 'time_signature_6', 'time_signature_7'
- vec_tracks.csv data file :
  - Vector Columns + 'id', 'track_uri','track_href','analysis_url'

Since there are over two million tracks in total, loading the vectors into the database may take a while.

## Similarity Search for Recommendations
After we set up the database, we can start performing the similarity search. We need an user playlist input, which is the playlist uri we can find in our Spotify playlist. We perform an aggregation on all the tracks in the playlist by calculating the mean of the track features excluding 'mode', 'key', 'time signature'. 'mode', 'key', 'time signature' are more like categorical data so we use dummy variables to represent them. The same approach is used when creating the track vectors.

The vector database returns us with 20 songs that has the shortest distance (most similar) to the input vector. We use these recommended songs to give recommendation and visualize a application page with album cover and 10-20 second audio preview.

## Step-By-Stepy Instructions of the App
- Step 1 : Go to spotify playlist, click on the '...' (three dots), click on 'Share' and click on 'Copy Link To Playlist'. This will copy the playlist uri.
<img width="1221" alt="screenshot" src="https://github.com/gialiubc/Weaviate_Song_Recommendation_App/assets/141379548/e28d48ac-4f92-4d61-a921-8795c2145cd3">


- Step 2 : Go to the app landing page, paste the copied link to the search box, and click on 'Recommend More Songs'.
<img width="1349" alt="Screenshot 2024-06-05 at 15 39 55" src="https://github.com/gialiubc/Weaviate_Song_Recommendation_App/assets/141379548/751ac9f0-9d42-458e-937d-4df64d13bf8a">


- Step 3 : Get your recommendations and preview the album and audio track (if applicable)!
<img width="1473" alt="Screenshot 2024-06-05 at 15 48 29" src="https://github.com/gialiubc/Weaviate_Song_Recommendation_App/assets/141379548/777b222d-c0df-40ce-9d9f-48b8e93095b6">


## Disclaimer
This project is based on my other group project 'Jammin_With_Spotify'. Please contact me if you have any questions.
