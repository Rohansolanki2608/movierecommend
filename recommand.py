import json
import pandas as pd
import requests

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

def giveRecommendation(chosenMovieIndex):
    myURL = 'http://127.0.0.1:5000/'
    myData = {"Index" : chosenMovieIndex}
    dataJSON = json.dumps(myData)
    myHeader = {"content-type" : "application/json"}
    response = requests.post(url=myURL, data=dataJSON, headers=myHeader)
    result = json.loads(response.text)
    sortedMovies = result["Movies"]
    return sortedMovies

if __name__ == '__main__':
    try:
        movieUserLikes = input("Please enter a movie: ")
        numberOfRecs = int(input("How many movie recommendation? "))
        movieIndex = int(getIndex(movieUserLikes))
        sortedMovies = giveRecommendation(movieIndex)

        i = 1
        print("\nTop", numberOfRecs, "movies you might like:")

        for movie in sortedMovies:
            print("{}. {}".format(i,getTitle(movie)))
            i +=1
            if i > numberOfRecs:
                break
    except IndexError:
        print("Sorry we don't have that movie")
    except:
        print("Error")
