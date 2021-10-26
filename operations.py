import requests
from spotify_client import *
import pickle
from sklearn.neighbors import NearestNeighbors
import pandas as pd

data = pd.read_csv('final_complete_dataset.csv')
data.drop('Unnamed: 0',axis=1,inplace=True)


class Operation:

	def get_features(self,id):
		features = []
		client_id = none
		client_secret = none
		spotify = SpotifyAPI(client_id, client_secret)
		headers = spotify.get_resource_header()
		features_url = f"https://api.spotify.com/v1/audio-features/{id}"
		result = requests.get(features_url,headers=headers)
		response = result.json()
		features.append(response['danceability'])
		features.append(response['energy'])
		features.append(response['key'])
		features.append(response['loudness'])
		features.append(response['mode'])
		features.append(response['speechiness'])
		features.append(response['acousticness'])
		features.append(response['instrumentalness'])
		features.append(response['liveness'])
		features.append(response['valence'])
		features.append(response['tempo'])
		return features


	def model(self,features):
		model = pickle.load(open('saved_model.pkl', 'rb'))

		result = model.kneighbors([features])
		distances = result[0][0]
		similar_songs = result[1][0]
		# for i in similar_songs:
		#     print(data.iloc[i]['name'])
		return similar_songs
