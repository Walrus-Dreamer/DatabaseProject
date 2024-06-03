import mysql.connector

log = True


class DumpGenerator:
    @staticmethod
    def __insert_buildings(cursor):
        cursor.execute(
            """
                    INSERT INTO building (name, type) VALUES 
                        ('Небесная башня', 'Театр'),
                        ('Сапфировый дом', 'Театр'),
                        ('Эмеральдовые вершины', 'Кинотеатр'),
                        ('Золотой горизонт', 'Кинотеатр'),
                        ('Дом культуры', 'Дворец культуры');
                    """
        )
        if log:
            print("\t-Buildings dump created successfully.")

    @staticmethod
    def __insert_impresarios(cursor):
        cursor.execute(
            """
                       INSERT INTO impresario (building_id, name, surname, age) VALUES 
                            (1, 'Алиса', 'Сизых', 28),
                            (2, 'Татьяна', 'Белая', 32),
                            (3, 'Сара', 'Тайлор', 27),
                            (4, 'Джон', 'Смит', 35),
                            (5, 'Мария', 'Джонсон', 42),
                            (1, 'Евгений', 'Уильямс', 29),
                            (2, 'Эмили', 'Блэк', 31),
                            (3, 'Уильям', 'Дэвис', 26),
                            (4, 'Оливия', 'Миллер', 39),
                            (5, 'Даниил', 'Польский', 33),
                            (1, 'София', 'Мур', 45),
                            (2, 'Михаил', 'Тайлор', 37),
                            (3, 'Эмма', 'Андерсон', 30),
                            (4, 'Александр', 'Томас', 34),
                            (5, 'Грейс', 'Джексон', 41);
                        """
        )
        if log:
            print("\t-Impresarios dump created successfully.")

    @staticmethod
    def __insert_genres(cursor):
        cursor.execute(
            """
                        INSERT INTO genre (name) VALUES
                            ('Драма'),
                            ('Комедия'),
                            ('Симфония'),
                            ('Опера'),
                            ('Романтика'),
                            ('Балет'),
                            ('Документальный'),
                            ('Мистика'),
                            ('Фантастика'),
                            ('Научно-популярный'),
                            ('Мюзикл'),
                            ('Анимация')
                        """
        )
        if log:
            print("\t-Genres dump created successfully.")

    @staticmethod
    def __insert_events(cursor):
        cursor.execute(
            """
                    INSERT INTO event (name, genre_name, impresario_id, building_id, event_date, box_office) VALUES
                            ('Последний вздох', 'Драма', 1, 1, '2022-01-01', 1000000),
                            ('Вставай', 'Комедия', 2, 2, '2022-02-02', 2000000),
                            ('Ее след', 'Романтика', 3, 3, '2022-03-03', 3000000),
                            ('Отличник с личной жизнью', 'Фантастика', 4, 4, '2022-04-04', 4000000),
                            ('Астрал', 'Мистика', 5, 5, '2022-05-05', 5000000),
                            ('Пара по психологии', 'Комедия', 6, 1, '2022-06-06', 6000000),
                            ('Щелкунчик', 'Балет', 7, 2, '2022-07-07', 7000000),
                            ('Лебединое озеро', 'Балет', 8, 3, '2022-08-08', 8000000),
                            ('Рад вас видеть', 'Комедия', 9, 4, '2022-09-09', 9000000),
                            ('Кошки', 'Мюзикл', 10, 5, '2022-10-10', 10000000),
                            ('Спящая красавица', 'Балет', 11, 1, '2022-11-11', 11000000),
                            ('Wall-e', 'Анимация', 12, 2, '2022-12-12', 12000000),
                            ('Дон Кихот', 'Балет', 13, 3, '2023-01-01', 13000000),
                            ('Баядерка', 'Балет', 14, 4, '2023-02-02', 14000000),
                            ('Жизель', 'Балет', 15, 5, '2023-03-03', 15000000);
                        """
        )
        if log:
            print("\t-Events dump created successfully.")

    @staticmethod
    def __insert_actors(cursor):
        cursor.execute(
            """
                       INSERT INTO actor (event_id, building_id, name, surname, age) VALUES 
                            (1, 1, 'Джон', 'До', 30),
                            (2, 2, 'Джейн', 'Смит', 25),
                            (4, 3, 'Сара', 'Уильямс', 28),
                            (5, 4, 'Алекс', 'Сизых', 32),
                            (6, 5, 'Эмили', 'Дэвис', 27),
                            (3, 1, 'Майк', 'Джонсон', 35),
                            (7, 2, 'Крис', 'Мартинез', 29),
                            (8, 3, 'Аманда', 'Гарция', 31),
                            (9, 4, 'Кевин', 'Родригез', 33),
                            (10, 5, 'Лаура', 'Лопез', 26),
                            (11, 1, 'Марк', 'Перез', 34),
                            (12, 2, 'Линда', 'Санчез', 30);
                        """
        )
        if log:
            print("\t-Actors dump created successfully.")

    @staticmethod
    def __insert_actor_genre_links(cursor):
        cursor.execute(
            """
                        INSERT INTO actor_genre_link (actor_id, genre_name) VALUES
                            (1, 'Драма'),
                            (2, 'Драма'),
                            (3, 'Драма'),
                            (2, 'Комедия'),
                            (3, 'Комедия'),
                            (4, 'Комедия'),
                            (3, 'Симфония'),
                            (4, 'Симфония'),
                            (5, 'Симфония'),
                            (4, 'Опера'),
                            (5, 'Опера'),
                            (6, 'Опера'),
                            (5, 'Романтика'),
                            (6, 'Романтика'),
                            (7, 'Романтика'),
                            (8, 'Романтика'),
                            (9, 'Балет'),
                            (7, 'Документальный'),
                            (8, 'Документальный'),
                            (8, 'Мистика'),
                            (9, 'Мистика'),
                            (10, 'Мистика'),
                            (11, 'Мистика'),
                            (7, 'Фантастика'),
                            (8, 'Фантастика'),
                            (9, 'Фантастика'),
                            (10, 'Научно-популярный'),
                            (11, 'Мюзикл'),
                            (12, 'Анимация');
                        """
        )
        if log:
            print("\t-Actor_genre_link dump created successfully.")

    @staticmethod
    def __insert_impresario_genre_links(cursor):
        cursor.execute(
            """
                        INSERT INTO impresario_genre_link (impresario_id, genre_name) VALUES
                            (1, 'Драма'),
                            (2, 'Драма'),
                            (3, 'Драма'),
                            (2, 'Комедия'),
                            (3, 'Комедия'),
                            (4, 'Комедия'),
                            (3, 'Симфония'),
                            (4, 'Симфония'),
                            (5, 'Симфония'),
                            (4, 'Опера'),
                            (5, 'Опера'),
                            (1, 'Опера'),
                            (5, 'Романтика'),
                            (1, 'Романтика'),
                            (2, 'Романтика'),
                            (3, 'Романтика'),
                            (4, 'Балет'),
                            (2, 'Документальный'),
                            (3, 'Документальный'),
                            (3, 'Мистика'),
                            (4, 'Мистика'),
                            (1, 'Мистика'),
                            (5, 'Мистика'),
                            (2, 'Фантастика'),
                            (1, 'Фантастика'),
                            (4, 'Фантастика'),
                            (1, 'Научно-популярный'),
                            (5, 'Мюзикл'),
                            (1, 'Анимация');
                        """
        )
        if log:
            print("\t-Impresario_genre_link dump created successfully.")

    @staticmethod
    def __insert_contests(cursor):
        cursor.execute(
            """
                        INSERT INTO contest (name, first_place_id, second_place_id, third_place_id) VALUES
                            ('Мисс вселенная', 3, 5, 8),
                            ('Лучшая роль первого плана', 1, 2, 3),
                            ('Лучшая роль второго плана', 6, 7, 8);
                        """
        )
        if log:
            print("\t-Contests dump created successfully.")

    @staticmethod
    def __insert_username_roles(cursor):
        cursor.execute(
            """
                        INSERT INTO username_role (username, role) VALUES
                            ('root@localhost', 'root_role'),
                            ('admin@localhost', 'admin_role'),
                            ('viewer@localhost', 'viewer_role'),
                            ('event_manager@localhost', 'event_manager_role'),
                            ('impresario@localhost', 'impresario_role');
                        """
        )
        if log:
            print("\t-Username_roles dump created successfully.")

    @staticmethod
    def __insert_event_ratings(cursor):
        cursor.execute(
            """
                        INSERT INTO event_rating (event_id, username, rating) VALUES
                            (1, 'Петя', 5),
                            (2, 'Петя', 4),
                            (3, 'Петя', 3),
                            (4, 'Петя', 2),
                            (5, 'Петя', 1),
                            (6, 'Петя', 5),
                            (7, 'Петя', 4),
                            (8, 'Петя', 3),
                            (9, 'Петя', 2),
                            (10, 'Петя', 1),
                            (11, 'Петя', 5),
                            (12, 'Петя', 4),
                            (13, 'Петя', 3),
                            (14, 'Петя', 2),
                            (1, 'Федя', 4),
                            (2, 'Федя', 3),
                            (3, 'Федя', 2),
                            (4, 'Федя', 1),
                            (5, 'Федя', 5),
                            (6, 'Федя', 4),
                            (7, 'Федя', 3),
                            (8, 'Федя', 2),
                            (9, 'Федя', 1),
                            (10, 'Федя', 5),
                            (11, 'Федя', 4),
                            (12, 'Федя', 3),
                            (13, 'Федя', 2),
                            (14, 'Федя', 1),
                            (15, 'Федя', 5);
                        """
        )
        if log:
            print("\t-Event_ratings dump created successfully.")

    @staticmethod
    def __insert_favorite_actor_links(cursor):
        cursor.execute(
            """
                        INSERT INTO favorite_actor_link (actor_id, username) VALUES
                            (1, 'viewer'),
                            (2, 'viewer'),
                            (3, 'viewer'),
                            (4, 'viewer'),
                            (5, 'viewer'),
                            (6, 'viewer'),
                            (7, 'viewer');
                        """
        )
        if log:
            print("\t-Event_rating_links dump created successfully.")

    @staticmethod
    def create_dump(connector):
        cursor = connector.cursor()
        if log:
            print("\ncreate_dump log:")
        try:
            DumpGenerator.__insert_buildings(cursor)
            DumpGenerator.__insert_impresarios(cursor)
            DumpGenerator.__insert_genres(cursor)
            DumpGenerator.__insert_events(cursor)
            DumpGenerator.__insert_actors(cursor)
            DumpGenerator.__insert_actor_genre_links(cursor)
            DumpGenerator.__insert_impresario_genre_links(cursor)
            DumpGenerator.__insert_contests(cursor)
            DumpGenerator.__insert_username_roles(cursor)
            DumpGenerator.__insert_event_ratings(cursor)
            DumpGenerator.__insert_favorite_actor_links(cursor)
            if log:
                print("\t-Dump created successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Failed to create dump: {}".format(error))
