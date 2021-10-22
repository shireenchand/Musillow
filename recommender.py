import streamlit as st
import requests
from spotify_client import *
from operations import *
import pandas as pd
import webbrowser


print(socket.gethostname())
data = pd.read_csv('final_complete_dataset.csv')
data.drop('Unnamed: 0',axis=1,inplace=True)
artists = []
key = 0

client_id = "031c4cbfe3014f87a965573acdc08d89"
client_secret = "57c7e6134fb742ac8d45334118ea71ce"
spotify = SpotifyAPI(client_id, client_secret)

st.sidebar.markdown("<h1 style='text-align: center; color: black;'>MUSILLOW</h1>", unsafe_allow_html=True)
st.sidebar.write("Enter name of song along with the artist to narrow down the results!!")

song = st.sidebar.text_input(label="Enter song")
# print(song)
if song == "":
	song = 'stay'
try:
	result = spotify.search({"track":f"{song}"},search_type='track')
	id = result['tracks']['items'][0]['id']


	for i in range(len(result['tracks']['items'][0]['artists'])):
		artists.append(result['tracks']['items'][0]['artists'][i]['name'])

	img_url = result['tracks']['items'][0]['album']['images'][1]['url']
	name = result['tracks']['items'][0]['name']
	st.sidebar.image(img_url,caption=name)

	str = ""
	index = 0
	for artist in artists:
		str += artist
		index += 1
		if len(artists) <= 1 or index == len(artists):
			continue
		str += ", "
	st.sidebar.write(str)
	footer = '<p>Developed by <a text-align: center;"" href="https://www.linkedin.com/in/shireen-chand/" target="_blank">Shireen Chand</a></p>'
	st.sidebar.markdown('###')
	# st.sidebar.markdown('###')
	st.sidebar.markdown(footer,unsafe_allow_html=True)


	# top_tracks_url = "https://api.spotify.com/v1/artists/{id}/top-tracks"


	operations = Operation()
	features = operations.get_features(id)
	similar_songs = operations.model(features)
	songs = []
	for i in similar_songs:
		dictionary = {
		'name':data.iloc[i]['name'],
		'artists':data.iloc[i]['Artists'],
		'url':data.iloc[i]['img_url'],
		'track_link':data.iloc[i]['track_link'],
		'preview_url':data.iloc[i]['preview_url'],
		}
		songs.append(dictionary)
		dictionary = {}




	# songs = [{
	# 	'name':'Cut to the feeling',
	# 	'url':"https://i.scdn.co/image/ab67616d00001e027359994525d219f64872d3b1"
	# },
	# {
	# 	'name':'Circles',
	# 	'url':"https://i.scdn.co/image/ab67616d00001e029478c87599550dd73bfa7e02"
	# }]


	col1, col2 = st.columns(2)
	columns = [col1,col2]

	for i in range(len(songs)):
		with col1:
			if songs[i]['name'] in name and list(songs[i]['artists']).sort() == artists.sort():
				continue
			else:
				# st.image(songs[i]['url'],width=250)
				img = '<img src={} alt="picture" style="width:250px;height:250px;">'
				st.markdown(img.format(songs[i]['url']), unsafe_allow_html=True)
				st.markdown("#")

		with col2:
			def local_css(file_name):
				with open(file_name) as f:
					st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
			
			local_css("style.css")
			str = ""
			for letter in songs[i]['artists']:
				if letter == '[' or letter == ']' or letter == "'":
					continue
				str += str.join(letter)
			html_string = '''
			<div style="width:500px;height:250px;border:1px solid #D6AD60;">
			<h3>{}</h3>
			<h4>{}</h4>
			<a href="{}"><button className="bn632-hover bn22">Play on Spotify</button></a>
			<br>
			<br>
			<a href="{}"><button className="btn41-43 btn-41">Listen to a Preview</button></a>
			</div>
			'''
			st.markdown(html_string.format(songs[i]['name'],str,songs[i]['track_link'],songs[i]['preview_url']),unsafe_allow_html=True)
			st.markdown("#")

except:
	st.markdown("<h1 style='text-align: center; color: black;'>COULD NOT FIND THE SONG!!!</h1>", unsafe_allow_html=True)
	st.markdown("<h2 style='text-align: center; color: black;'>Check the spelling or add the name of the artist as well</h2>", unsafe_allow_html=True)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


 


		

















