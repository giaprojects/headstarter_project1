# Headstarter Project 1
## Group Members: Bamlak Assaye,Gia Liu, Kimberly Toro, Nicole Shaker
# Song Recommendation Using Vector Database 

<img width="1726" alt="Screenshot 2024-06-05 at 14 40 11" src="https://github.com/gialiubc/Weaviate_Song_Recommendation_App/assets/141379548/2da80a6a-ad75-4c82-a459-cb640f17b527">

## Overview

In this project, a web app is created to get song recommendations to user's playlist with the search from two million songs that are vectorized and stored in vector database. What you'll expect in this project:

- Part 1 Data Manipulation: Data cleaning, transformation, and loading into weaviate vector database. I use my own vectors (Embeddings).
- Part 2 Similarity Search: Perform similarity search with an user input of a playlist and find from the database 20 songs that are most similar to the songs from the user's playlist. This would make the recommendation.
- Part 3 App backend : Set up App backend with Python Flask.
- Part 4 App frontend : Using HTML, CSS, JavaScript to create the visualization of the song recommendation app.
  
## Files
Everything is organized in the following way:

- Coding_notebook folder : contains all the codes in jupyter notebook which we used for creating the app. 
- app.py file : Use this to run the app.
- Other folders for running the app :
  - static folder : includes css, js, img folders;
  - templates folder : includes index.html for landing page and result.html for song recommendation result page;
  - Resources folder : includes a scaler saved for scaling the vectors.

## Similarity Search for Recommendations
We perform a similarity search in the database to the songs in the user's input playlist.
The vector database returns us with 20 songs that has the shortest distance (most similar) to the input vector. We use these recommended songs to give recommendation and visualize a application page with album cover and 10-20 second audio preview.

## Step-By-Stepy Instructions of the App
- Step 1 : Go to spotify playlist, click on the '...' (three dots), click on 'Share' and click on 'Copy Link To Playlist'. This will copy the playlist uri.
<img width="1221" alt="screenshot" src="https://github.com/gialiubc/Weaviate_Song_Recommendation_App/assets/141379548/e28d48ac-4f92-4d61-a921-8795c2145cd3">


- Step 2 : Go to the app landing page, paste the copied link to the search box, and click on 'Recommend More Songs'.
<img width="1349" alt="Screenshot 2024-06-05 at 15 39 55" src="https://github.com/gialiubc/Weaviate_Song_Recommendation_App/assets/141379548/751ac9f0-9d42-458e-937d-4df64d13bf8a">


- Step 3 : Get your recommendations and preview the album and audio track (if applicable)!
<img width="1473" alt="Screenshot 2024-06-05 at 15 48 29" src="https://github.com/gialiubc/Weaviate_Song_Recommendation_App/assets/141379548/777b222d-c0df-40ce-9d9f-48b8e93095b6">


