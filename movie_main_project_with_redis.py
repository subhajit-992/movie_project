import requests
import json
import html_to_json
import redis
redis_clint = redis.Redis(host='localhost', port=55000, username='default', password='redispw')

string = input("Enter your movie name: ")
#string.append(input("Enter your movie name: "))
print(string)



def main():
    # fetch movie from tastedive
    tastedive_data_3 = find_movie_tastedive_data(string)
    movie_name_list = []

    for elm in tastedive_data_3['Similar']['Results']:
        movie_name_list.append(elm['Name'])

    # fetch movie year from omdb
    movie_name_year_list = movie_year(movie_name_list)

    # fetch movie from omdb
    omdb_data_1 = find_movie_omdb_data(string)
    movie_name_with_year = []


    for m_name in omdb_data_1['Search']:
        movie_name_with_year.append([(m_name['Title']), (m_name['Year'])])

    for element in movie_name_year_list:
        if (element not in movie_name_with_year):
            movie_name_with_year.append(element)

    for i in movie_name_with_year:
        i[1] = int(i[1])

    # sort movie
    def sort_movie_name_with_year(o_ele):
        return o_ele[1]


    movie_name_with_year.sort(key=sort_movie_name_with_year, reverse=True)
    print("Recommended movies are: ")

    # print movie details
    length = len(movie_name_with_year)
    if (length < 10):
        for j in range(length):
            print("Movie Name: ", movie_name_with_year[j][0])
            print("year: ", movie_name_with_year[j][1])
            print("---------")
    else:
        for k in range(0, 10):
            print("Movie Name: ", movie_name_with_year[k][0])
            print("year: ", movie_name_with_year[k][1])
            print("---------")



def find_movie_tastedive_data(tag_string):
    x = "{}--{}".format(tag_string,"tastedive")
    print(x)
    movie = redis_clint.get(x)
    if movie is None:
        parameter = {"q": tag_string, "type": "movies", "limit": 5, "k": "443974-MovieMas-6RB39O3I"}
        tastedive_data = html_to_json.convert(requests.get("https://tastedive.com/api/similar?", params=parameter).text)
        tastedive_data_1 = json.loads(tastedive_data['_value'])
        redis_clint.set(x,json.dumps(tastedive_data_1,indent=2))
        print("from api")
        return tastedive_data_1
    else:
        tastedive_data_2 = json.loads(movie)
        print("from redis")
        return tastedive_data_2


def find_movie_omdb_data(tage_string):
    y = "{}--{}".format(tage_string,"omdb")
    print(y)
    movie = redis_clint.get(y)
    if movie is None:
        parameter = {"s": tage_string , "type": "movie", "apikey": "1247741c"}
        omdb_data_2 = requests.get("http://www.omdbapi.com/", params=parameter).json()
        redis_clint.set(y,json.dumps(omdb_data_2,indent=2))
        print("from api")
        return omdb_data_2
    else:
        omdb_data_3 = json.loads(movie)
        print("from redis")
        return omdb_data_3


def movie_year(list):
    movie_list = list
    m2_list = []

    for movie_name in movie_list:
        omdb_data = find_movie_omdb_data(movie_name)
        m2_list.append([omdb_data['Search'][0]['Title'], (omdb_data['Search'][0]['Year'])])

    return m2_list

if __name__ == "__main__":
    main()