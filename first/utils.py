import sqlite3
from collections import Counter


class SearchDAO:

    def __init__(self, path):
        self.path = path

    def load_tablet(self):
        """Подключение таблицы"""
        with sqlite3.connect(self.path) as con:
            cursor = con.cursor()
        return cursor

    def search_by_title(self, title):
        """Сортировка таблицы по названию"""
        cursor = self.load_tablet()
        query = f"""SELECT title, country, release_year, listed_in, description
                           FROM netflix
                           WHERE title LIKE '{title}%'
                           ORDER BY release_year DESC
                           LIMIT 1"""
        cursor.execute(query)
        result = cursor.fetchall()[0]
        movie_title = {
            'title': result[0],
            'country': result[1],
            'release_year': result[2],
            'genre': result[3],
            'description': result[4]
        }
        return movie_title

    def search_by_year(self, year_1, year_2):
        """Сортировка таблицы по годам выпуска фильма"""
        cursor = self.load_tablet()
        movie_title = []
        query = f"""SELECT title,release_year
                           FROM netflix
                           WHERE release_year BETWEEN {year_1} AND {year_2}
                           ORDER BY release_year ASC 
                           LIMIT 100"""
        cursor.execute(query)
        result = cursor.fetchall()
        for i in range(len(result)):
            movie_title.append(
                {"title": result[i][0],
                 "release_year": result[i][1]}
            )
        return movie_title

    def search_by_rating(self, rating):
        """Сортировка таблицы по возрастному рейтингу"""
        cursor = self.load_tablet()
        rating_title = []
        parametrs = {'children': 'G',
                     'family': "'G', 'PG', 'PG-13'",
                     'adult': "'R','NC-17'",
                     }
        if rating not in parametrs:
            return f'Такой группы не существует'
        else:
            query = f"""SELECT title, rating, description
                    FROM netflix
                    WHERE rating in ({parametrs[rating]})
                    """
            cursor.execute(query)
            result = cursor.fetchall()
            for i in result:
                rating_title.append(
                    {"title": i[0],
                     "rating": i[1],
                     "description": i[2]}
                )
        return rating_title

    def search_by_genre(self, genre):
        """Сортировка таблицы по жанру"""
        cursor = self.load_tablet()
        query = f"""SELECT title, description
                            FROM netflix
                            WHERE listed_in LIKE '%{genre}%'
                            ORDER BY release_year DESC 
                            LIMIT 10
                            """
        cursor.execute(query)
        result = cursor.fetchall()
        genre = []
        for i in result:
            genre.append({"title": i[0],
                          "description": i[1]})
        return genre

    def search_by_actors(self, actor_1, actor_2):
        """Сортировка таблицы по двум актерам"""
        cursor = self.load_tablet()
        query = f"""SELECT "cast"
                        FROM netflix
                        WHERE "cast" LIKE '%{actor_1}%' AND "cast" LIKE '%{actor_2}%'
                        """
        cursor.execute(query)
        result = cursor.fetchall()
        act = []
        for i in result:
            act.extend(i[0].split(', '))
        cast = Counter(act)
        cast_list = []
        for actor, count in cast.items():
            if actor not in [actor_1, actor_2] and count > 2:
                cast_list.append(actor)
        return cast_list


    def search_by_all(self, type_movie, year, genre):
        """Сортировка таблицы по жанру,году и типу"""
        cursor = self.load_tablet()
        query = f"""SELECT title, description
                            FROM netflix
                            WHERE "type"='{type_movie}' 
                            AND release_year = '{year}' 
                            AND listed_in LIKE '%{genre}%'
                            """
        cursor.execute(query)
        result = cursor.fetchall()
        list = []
        for i in result:
            list.append({"title": i[0],
                         "description": i[1]})
        return list

