from flask import Flask, request, render_template, render_template_string
import pickle
import numpy as np
from scipy.spatial import distance 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
import random
from sklearn.preprocessing import StandardScaler
import time
import urllib.parse as parse
import weaviate
import weaviate.classes.query as wq
import requests
import urllib.parse as parse
# Import the API key
from config import spotify_key
from config import wv_key


# Load Weaviate API key information into env variables
os.environ['WCS_URL'] = "https://rnwhml87r4abadfbxe8rw.c0.us-west3.gcp.weaviate.cloud"

os.environ['WCS_API_KEY'] = wv_key
os.environ['OPENAI_APIKEY'] = "enter_credentials"

# Load Spotify API key information into env variables
os.environ['SPOTIPY_CLIENT_ID']='9f172ceff97148c787ef9e867e28a19f'  # "SPOTIPY" is not a typo
os.environ['SPOTIPY_CLIENT_SECRET']=spotify_key
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:3000'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# Import the scaler
scalerfile = 'Resources/scaler.sav'
scaler = pickle.load(open(scalerfile, 'rb'))

# Instantiate your client (not shown). e.g.:ss
headers = {
    "X-OpenAI-Api-Key": os.environ['OPENAI_APIKEY']
}  # Replace with your OpenAI API key

client = weaviate.connect_to_wcs(
    cluster_url=os.environ['WCS_URL'],  # Replace with your WCS URL
    auth_credentials=weaviate.auth.AuthApiKey(
        os.environ['WCS_API_KEY']
    ),  # Replace with your WCS key
    headers=headers,
    skip_init_checks=True
)




# Create function which converts a playlist into its mean without touching the categorical variables
def playlist_mean(df):   
    df_avg=pd.DataFrame()
    df_avg.at[0,'danceability']=df['danceability'].mean()
    df_avg.at[0,'energy']=df['energy'].mean()
    df_avg.at[0,'loudness']=df['loudness'].mean()
    df_avg.at[0,'speechiness']=df['speechiness'].mean()
    df_avg.at[0,'acousticness']=df['acousticness'].mean()
    df_avg.at[0,'instrumentalness']=df['instrumentalness'].mean()
    df_avg.at[0,'liveness']=df['liveness'].mean()
    df_avg.at[0,'valence']=df['valence'].mean()
    df_avg.at[0,'tempo']=df['tempo'].mean()
    df_avg.at[0,'duration_ms']=df['duration_ms'].mean()
    df_avg.at[0,'key']=df['key'].mode().iloc[0]
    df_avg.at[0,'mode']=df['mode'].mode().iloc[0]
    df_avg.at[0,'time_signature']=df['time_signature'].mode().iloc[0]


    df_avg=df_avg.astype({"key":'int',"mode":'int',"time_signature":'int'})     # Does not remove the decimal ".0" even if it is an integer!
    df_avg['key']=df_avg['key'].astype(str)     # adding this line seems to convert "key", "mode", and "time_signature" to objects...


    df_avg=df_avg.assign(key_none=0,key_0=0,key_1=0,key_2=0,key_3=0,key_4=0,key_5=0,key_6=0,key_7=0,key_8=0,key_9=0,key_10=0,key_11=0,\
                mode_minor=0,mode_major=0,\
                time_signature_0=0,time_signature_1=0,time_signature_2=0,time_signature_3=0,time_signature_4=0,time_signature_5=0,time_signature_6=0,time_signature_7=0,)


    if df_avg.iloc[0]['key']==-1:
        df_avg.at[0,'key_none']=1
    else:
        col_name='key_'+str(df_avg.iloc[0]['key']) 
        df_avg.at[0,col_name]=1

    col_name='time_signature_'+str(df_avg.iloc[0]['time_signature']) 
    df_avg.at[0,col_name]=1

    if df_avg.iloc[0]['mode']==0:
        df_avg.at[0,'mode_minor']=1
    else:
        df_avg.at[0,'mode_major']=1   

    return df_avg

# Create function which converts a playlist into its weighted average via stddev without touching the categorical variables
def  playlist_mean_std(df):   
    df_avg=pd.DataFrame()
    df_avg.at[0,'danceability']=df['danceability'].mean()
    df_avg.at[0,'danceability_std']=df['danceability'].std()
    df_avg.at[0,'energy']=df['energy'].mean()
    df_avg.at[0,'energy_std']=df['energy'].std()
    df_avg.at[0,'loudness']=df['loudness'].mean()
    df_avg.at[0,'loudness_std']=df['loudness'].std()
    df_avg.at[0,'speechiness']=df['speechiness'].mean()
    df_avg.at[0,'speechiness_std']=df['speechiness'].std()
    df_avg.at[0,'acousticness']=df['acousticness'].mean()
    df_avg.at[0,'acousticness_std']=df['acousticness'].std()
    df_avg.at[0,'instrumentalness']=df['instrumentalness'].mean()
    df_avg.at[0,'instrumentalness_std']=df['instrumentalness'].std()
    df_avg.at[0,'liveness']=df['liveness'].mean()
    df_avg.at[0,'liveness_std']=df['liveness'].std()
    df_avg.at[0,'valence']=df['valence'].mean()
    df_avg.at[0,'valence_std']=df['valence'].std()
    df_avg.at[0,'tempo']=df['tempo'].mean()
    df_avg.at[0,'tempo_std']=df['tempo'].std()
    df_avg.at[0,'duration_ms']=df['duration_ms'].mean()
    df_avg.at[0,'duration_ms_std']=df['duration_ms'].std()
    df_avg.at[0,'key']=df['key'].mode().iloc[0]
    df_avg.at[0,'mode']=df['mode'].mode().iloc[0]
    df_avg.at[0,'time_signature']=df['time_signature'].mode().iloc[0]


    df_avg=df_avg.astype({"key":'int',"mode":'int',"time_signature":'int'})     # Does not remove the decimal ".0" even if it is an integer!
    df_avg['key']=df_avg['key'].astype(str)     # adding this line seems to convert "key", "mode", and "time_signature" to objects...


    df_avg=df_avg.assign(key_none=0,key_0=0,key_1=0,key_2=0,key_3=0,key_4=0,key_5=0,key_6=0,key_7=0,key_8=0,key_9=0,key_10=0,key_11=0,\
                mode_minor=0,mode_major=0,\
                        time_signature_0=0,time_signature_1=0,time_signature_2=0,time_signature_3=0,time_signature_4=0,time_signature_5=0,time_signature_6=0,time_signature_7=0)



    if df_avg.iloc[0]['key']==-1:
        df_avg.at[0,'key_none']=1
    else:
        col_name='key_'+str(df_avg.iloc[0]['key']) 
        # df_avg.at[0,col_name]=df_avg.iloc[0]['key']
        df_avg.at[0,col_name]=1

    col_name='time_signature_'+str(df_avg.iloc[0]['time_signature']) 
    # df_avg.at[0,col_name]=df_avg.iloc[0]['time_signature']
    df_avg.at[0,col_name]=1

    if df_avg.iloc[0]['mode']==0:
        df_avg.at[0,'mode_minor']=1
    else:
        df_avg.at[0,'mode_major']=1   

    return df_avg

# Function used to create dummy variables for input to ML model from base track feature data
def dummy_variables(data):
    key_to_add = ['key_none', 'key_0', 'key_1', 'key_2',
    'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 'key_9', 'key_10',
    'key_11']
    mode_to_add = ['mode_minor', 'mode_major']
    signature_to_add = ['time_signature_0', 'time_signature_1', 'time_signature_2', 'time_signature_3', 
                        'time_signature_4', 'time_signature_5', 'time_signature_6', 'time_signature_7']
    y = -1
    for x in key_to_add:
        for i in data:
            if i['key'] == y:
                i[x] = 1
            else:
                i[x] = 0
        y+=1
    for i in data:
        if i['mode'] == 1:
            i[mode_to_add[0]] = 0
            i[mode_to_add[1]] = 1
        else:
            i[mode_to_add[0]] = 1
            i[mode_to_add[1]] = 0
    time_signature = 0
    for x in signature_to_add:
        for i in data:
            if i['time_signature'] == time_signature:
                i[x] = 1
            else:
                i[x] = 0
        time_signature +=1

# Function used to gather playlist information from Spotify
def gather_playlist_data(playlist_uri):
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    user_playist_track_uri = []
    for i in range (0,1000,100):
        playlist_info = spotify.playlist_items(playlist_uri, offset=i, limit=100)
        for x in range(0,len(playlist_info['items'])):
            user_playist_track_uri.append(playlist_info['items'][x]['track']['uri'])
        if len(playlist_info['items']) < 100:
            break
            
    return user_playist_track_uri

# Function used to gather track feature data
def gather_track_features(uri_track_list):
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    b = len(uri_track_list)
    results_full = []
    for i in range(0,b,100):
        if (b - i) < 100:
            x=uri_track_list[i:i+(b-i)]
            y=spotify.audio_features(x)
            results_full = results_full + y
        else:
            x=uri_track_list[i:i+100]
            y=spotify.audio_features(x)
            results_full = results_full + y
        time.sleep(0.5)

    return results_full

# Function for getting the album vector with album link input
def query(playlist_uri): 
    # Parse out playlist uri from playlist link
    res = parse.urlparse(playlist_uri)
    res.path[10:-1]

    # Establish a connection with the Spotify API
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    # Gather all track URI's from the user's playlist
    global user_playist_track_uri
    user_playist_track_uri = gather_playlist_data(playlist_uri)

    # Request track data from spotify on the 5 track slice from the user playlist
    data = gather_track_features(user_playist_track_uri)

    # Create dummy variable cells for later input into the model
    dummy_variables(data)

    # Create dataframe from data and create a copy for later use
    user_playlist_data_df = pd.DataFrame(data, columns=['danceability','energy', 'loudness', 'speechiness',
                'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms','key','mode','time_signature', 
                'mode_minor', 'mode_major','key_none', 'key_0', 'key_1', 
                'key_2', 'key_3', 'key_4', 'key_5', 'key_6', 'key_7', 'key_8', 
                'key_9', 'key_10', 'key_11', 'time_signature_0', 'time_signature_1',
                'time_signature_2', 'time_signature_3', 'time_signature_4', 'time_signature_5',
                'time_signature_6', 'time_signature_7'])
    # Create a copy of df
    user_playlist_vector_df = user_playlist_data_df.copy()
    # Create the weighted data from the users_playlist
    mean_user_playlist_vector_df = playlist_mean(user_playlist_vector_df)
    # Drop columns not needed for scaling
    mean_user_playlist_vector_df = mean_user_playlist_vector_df.drop(['key', 'mode', 'time_signature'], axis=1)
    scalerfile = 'Resources/scaler.sav'
    # Load scaler and scale the vector
    scaler = pickle.load(open(scalerfile, 'rb'))
    scaled_mean_user_playlist_data = scaler.transform(mean_user_playlist_vector_df)
    # Transform data to list format
    playlist_vector = scaled_mean_user_playlist_data.tolist()[0]

    return playlist_vector

# Create Flask routes
app = Flask(__name__)

@app.route('/')
def home():
    results={}
    return render_template('index.html')

@app.route('/model_recommendation', methods=['POST','GET'])
def model_recommendation():
    if request.method == 'POST':
        # Extract input features from the request
        playlist_uri = str(request.form['track1'])
        # Get the vector using query function
        query_vector = query(playlist_uri)
        # Get the collection
        tracks = client.collections.get("Tracks")
        # Perform query
        response = tracks.query.near_vector(
            near_vector=query_vector,  # A list of floating point numbers
            limit=20,
            return_metadata=wq.MetadataQuery(distance=True),
            
        )
        # Store the response in a list
        recommend_track_uri_list = []
        for o in response.objects:
            recommend_track_uri_list.append(o.properties["track_uri"])
    

        # Check if recommended song already exist in user's playlist
        recommend_track_uri_df = pd.DataFrame(recommend_track_uri_list)
        recommend_track_uri_df = recommend_track_uri_df[~recommend_track_uri_df.isin(user_playist_track_uri)]   
        recommend_track_list = list(recommend_track_uri_df[0])

        # If list empty, return message
        if len(recommend_track_list) == 0:
             return render_template('index.html', "The recommended playlist's contain no songs that were not already in the user's playlist")
        
        # Gather information from spotify on the 5 songs to recommend
        tracks_info = spotify.tracks(recommend_track_list)

        # Compile recommended track data
        results = []
        for x in range(0,len(recommend_track_list)):
            result_dict = {}
            result_dict['Track URI'] = tracks_info['tracks'][x]['uri']
            result_dict['Album Cover'] = tracks_info['tracks'][x]['album']['images'][0]['url']
            result_dict['Track Name'] = tracks_info['tracks'][x]['name']
            result_dict['Artist Name'] = tracks_info['tracks'][x]['artists'][0]['name']
            result_dict['Preview URL'] = tracks_info['tracks'][x]['preview_url']
            results.append(result_dict)

        return render_template('result.html', result1=results[0], result2=results[1], result3=results[2], result4=results[3], result5=results[4],
                               result6=results[5], result7=results[6], result8=results[7], result9=results[8], result10=results[9],
                               result11=results[10], result12=results[11], result13=results[12], result14=results[13], result15=results[14],
                               result16=results[15], result17=results[16], result18=results[17], result19=results[18], result20=results[19])

# Run the Flask App locally
if __name__ == '__main__':
    app.run(debug=True)