import requests
import json
string = []
string.append(input("Enter your movie name: "))
print(string)

#fetch movie data from tastedive
parameter = {"q":string,"type":"movies","limit":5,"k":"443974-MovieMas-0409BAUL"}
tastedive_data = requests.get("https://tastedive.com/api/similar?",params = parameter).json()
movie_name_list = []

for elm in tastedive_data['Similar']['Results']:
    movie_name_list.append(elm['Name'])

#fetch movie year from omdb 
def movie_year(list):
    movie_list = list
    m2_list=[]
    
    for movie_name in movie_list:
        parameter = {"s":movie_name,"type":"movie","apikey":"1247741c"}
        omdb_data = requests.get("http://www.omdbapi.com/",params = parameter).json()
        m2_list.append([omdb_data['Search'][0]['Title'],(omdb_data['Search'][0]['Year'])])

    return m2_list

movie_name_year_list= movie_year(movie_name_list)
parameter = {"s":string,"type":"movie","apikey":"1247741c"}
omdb_data_1 = requests.get("http://www.omdbapi.com/",params = parameter).json()
movie_name_with_year = []

for m_name in omdb_data_1['Search']:
    movie_name_with_year.append([(m_name['Title']),(m_name['Year'])])

for element in movie_name_year_list:
    if(element not in movie_name_with_year):
        movie_name_with_year.append(element)

for i in movie_name_with_year:
    i[1]=int(i[1])

def sort_movie_name_with_year(o_ele):
    return o_ele[1]

movie_name_with_year.sort(key=sort_movie_name_with_year,reverse=True)
print("Recommended movies are: ")

#print movie details
length = len(movie_name_with_year)
if (length<10):
    for j in range(length):
        print("Movie Name: ",movie_name_with_year[j][0])
        print("year: " ,movie_name_with_year[j][1])
        print("---------")
else:
    for k in range(0,10):
        print("Movie Name: ",movie_name_with_year[k][0])
        print("year: " ,movie_name_with_year[k][1])
        print("---------")

