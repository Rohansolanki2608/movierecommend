#Importing the libraries
import pickle
import numpy as np
import pandas as pd
import requests
from flask import Flask, render_template, request

#Global variables
app = Flask(__name__) #Creating the API
loadedModel = pickle.load(open('Model.sav', 'rb'))


#Loading the form
@app.route('/', methods=['GET'])
def Home():
	return render_template('movie.html')


#Handling the data
df = pd.read_csv('movie_dataset.csv')
featuresList = ['genres', 'keywords', 'cast', 'director']

for features in featuresList:
    df[features] = df[features].fillna(' ')

def combineFeatures(row):
    return row['genres'] + " " + row['keywords'] + " " + row['cast'] + " " + row['director']

def getTitle(index):
    return df[df.index==index]['title'].values[0]

def getIndex(title):
    return df[df.title==title]['index'].values[0]

df['combined_features'] = df.apply(combineFeatures, axis=1)


#User defined functions
@app.route('/recommend', methods=['POST'])
def sendRecommend():
	#Getting the input
	movieUserLikes = request.form['movie']
	numberOfRecs = int(request.form['recnumber'])

	movieIndex = getIndex(movieUserLikes)

	#Recommendation
	similarMovies = list(enumerate(loadedModel[movieIndex]))
	sortedMovies = sorted(similarMovies, key = lambda x:x[1], reverse=True)[1:]
	returnMovies = [index for (index, sim) in sortedMovies]

	#Returning the response
	sendTitle = "Top " + str(numberOfRecs) + " movies similar to " + movieUserLikes
	sendRecs = ""
	i = 1

	for movie in returnMovies:
		sendRecs += str(i) + ". " + getTitle(movie) + "\n"
		i += 1
		if i > numberOfRecs:
			break

	return render_template('movie.html', movie_user_likes=sendTitle, movie_recs=sendRecs)

#Main function
if __name__ == '__main__':
	app.run(debug=True)
