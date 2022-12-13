import requests
import json
import html_to_json
import redis
# from __future__ import annotation
from abc import ABC, abstractmethod

redis_clint = redis.Redis(host='localhost', port=55000, username='default', password='redispw')
string = input("Enter your movie name: ")


class Movie_Api(ABC):
    @abstractmethod
    def find_movie_data(self):
        pass

#movie fetch from omdb
class Movie_Api_omdb(Movie_Api):
    def __init__(self, string):
        self.string = string

    def find_movie_data(self):
        y = "{}--{}".format(self.string, "omdb")
        print(y)
        movie = redis_clint.get(y)
        if movie is None:
            parameter = {"s": self.string, "type": "movie", "apikey": "1247741c"}
            omdb_data_2 = requests.get("http://www.omdbapi.com/", params=parameter).json()
            redis_clint.set(y, json.dumps(omdb_data_2, indent=2))
            print("from api")
            return omdb_data_2
        else:
            omdb_data_3 = json.loads(movie)
            print("from redis")
            return omdb_data_3

#movie fetch from tastedive
class Movie_Api_tastedive(Movie_Api):
    def __init__(self, string):
        self.string = string

    def find_movie_data(self):
        x = "{}--{}".format(self.string, "tastedive")
        print(x)
        movie = redis_clint.get(x)
        if movie is None:
            parameter = {"q": self.string, "type": "movies", "limit": 5, "k": "443974-MovieMas-6RB39O3I"}
            tastedive_data = html_to_json.convert(
                requests.get("https://tastedive.com/api/similar?", params=parameter).text)
            tastedive_data_1 = json.loads(tastedive_data['_value'])
            redis_clint.set(x, json.dumps(tastedive_data_1, indent=2))
            print("from api")
            return tastedive_data_1
        else:
            tastedive_data_2 = json.loads(movie)
            print("from redis")
            return tastedive_data_2


class creator(ABC):

    @abstractmethod
    def moviename_with_year(self):
        pass

    @abstractmethod
    def Movie_year_in_int(self):
        pass


class taste_data(ABC):

    @abstractmethod
    def movie_from_taste_name(self):
        pass

    @abstractmethod
    def moviename_year_list(self):
        pass

    @abstractmethod
    def movie_year(self, list):
        pass

    @abstractmethod
    def movie_from_both(self):
        pass

#process only omdb data
class concrete_creator_1(creator):
    def __init__(self, string):
        self.string = string
        self.sort_movie_type_2 = sort_movie_type_2()

    def moviename_with_year(self):
        omdb_obj_1 = Movie_Api_omdb(string)
        omdb_data_1 = omdb_obj_1.find_movie_data()
        movie_name_with_year_1 = []

        for m_name in omdb_data_1['Search']:
            movie_name_with_year_1.append([(m_name['Title']), (m_name['Year'])])
        return movie_name_with_year_1

    def Movie_year_in_int(self):
        movie_name_with_year = []
        movie_name_with_year = concrete_creator_1.moviename_with_year(self)
        for i in movie_name_with_year:
            i[1] = int(i[1])
        return movie_name_with_year

#process both omdb and tastedive data
class concrete_creator_2(creator, taste_data):
    def __init__(self, string):
        self.string = string
        self.sort_movie_type_1 = sort_movie_type_1()

    def moviename_with_year(self):
        omdb_obj_2 = Movie_Api_omdb(string)
        omdb_data_1 = omdb_obj_2.find_movie_data()
        movie_name_with_year_2 = []

        for m_name in omdb_data_1['Search']:
            movie_name_with_year_2.append([(m_name['Title']), (m_name['Year'])])
        return movie_name_with_year_2

    def movie_from_taste_name(self):
        tastedive_obj = Movie_Api_tastedive(string)
        tastedive_data_3 = tastedive_obj.find_movie_data()
        movie_name_list = []

        for elm in tastedive_data_3['Similar']['Results']:
            movie_name_list.append(elm['Name'])
            return movie_name_list

    def moviename_year_list(self):
        movie_from_tastename = []
        movie_from_tastename = concrete_creator_2.movie_from_taste_name(self)
        movie_name_year_list = []
        movie_name_year_list = concrete_creator_2.movie_year(self, movie_from_tastename)
        return movie_name_year_list

    def movie_year(self, list):
        movie_list = list
        m2_list = []

        for movie_name in movie_list:
            omdb_data = Movie_Api_omdb(movie_name).find_movie_data()
            m2_list.append([omdb_data['Search'][0]['Title'], (omdb_data['Search'][0]['Year'])])

        return m2_list

    def movie_from_both(self):
        movie_name_with_year_1 = []

        movie_name_year_list = []
        movie_name_year_list = concrete_creator_2.moviename_year_list(self)
        movie_name_with_year_2 = []
        movie_name_with_year_2 = concrete_creator_2.moviename_with_year(self)

        for element in movie_name_year_list:
            if (element not in movie_name_with_year_2):
                movie_name_with_year_2.append(element)

        movie_name_with_year_1 = movie_name_with_year_2
        return movie_name_with_year_1

    def Movie_year_in_int(self):
        movie_name_with_year = []
        movie_name_with_year = concrete_creator_2.movie_from_both(self)
        for i in movie_name_with_year:
            i[1] = int(i[1])
        return movie_name_with_year


class sort_movie(ABC):
    @abstractmethod
    def sort_movie_by_year(self):
        pass

    @abstractmethod
    def print_movie(self):
        pass


class sort_movie_type_1(sort_movie):
    def __init__(self, string_1=string):
        self.string = string_1

    def sort_movie_by_year(self):

        movie_name_with_year = []
        movie_name_with_year = concrete_creator_2.Movie_year_in_int(self)

        def sort_movie_name_with_year(o_ele):
            return o_ele[1]

        movie_name_with_year.sort(key=sort_movie_name_with_year, reverse=True)

        movie_name_with_year_print = []
        movie_name_with_year_print = movie_name_with_year
        return movie_name_with_year_print

    def print_movie(self):
        print("Recommended movies are: ")
        movie_name_with_year_print_1 = []
        movie_name_with_year_print_1 = sort_movie_type_1.sort_movie_by_year(self)
        length = len(movie_name_with_year_print_1)
        if (length < 10):
            for j in range(length):
                print("Movie Name: ", movie_name_with_year_print_1[j][0])
                print("year: ", movie_name_with_year_print_1[j][1])
                print("---------")
        else:
            for k in range(0, 10):
                print("Movie Name: ", movie_name_with_year_print_1[k][0])
                print("year: ", movie_name_with_year_print_1[k][1])
                print("---------")


class sort_movie_type_2(sort_movie):
    def __init__(self, string_1=string):
        self.string = string_1

    def sort_movie_by_year(self):

        movie_name_with_year = []
        movie_name_with_year = concrete_creator_1.Movie_year_in_int(self)

        def sort_movie_name_with_year(o_ele):
            return o_ele[1]

        movie_name_with_year.sort(key=sort_movie_name_with_year, reverse=True)

        movie_name_with_year_print = []
        movie_name_with_year_print = movie_name_with_year
        return movie_name_with_year_print

    def print_movie(self):
        print("Recommended movies are: ")
        movie_name_with_year_print_1 = []
        movie_name_with_year_print_1 = sort_movie_type_2.sort_movie_by_year(self)
        length = len(movie_name_with_year_print_1)
        if (length < 5):
            for j in range(length):
                print("Movie Name: ", movie_name_with_year_print_1[j][0])
                print("year: ", movie_name_with_year_print_1[j][1])
                print("---------")
        else:
            for k in range(0, 5):
                print("Movie Name: ", movie_name_with_year_print_1[k][0])
                print("year: ", movie_name_with_year_print_1[k][1])
                print("---------")


def client_code(creator: creator):
    creator.sort_movie_type_1.print_movie()


if __name__ == "__main__":
    client_code(concrete_creator_2(string))



#There are two object     concrete_creator_1   ,     concrete_creator_2
   #when you use concrete_creator_1 , you should use creator.sort_movie_type_1.print_movie() in client_code

   #when you use concrete_creator_2 , you should use creator.sort_movie_type_2.print_movie() in client_code 









    
