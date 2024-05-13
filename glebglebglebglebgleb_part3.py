import mysql.connector


# user_login = input("Enter your login: ")

# user_answer = input("Does your database has password? (y/n): ")
# user_password = None
# if user_answer == "y":
#     user_password = input("Enter your password: ")

# user_answer = input("Do you want to enable logging? (y/n): ")
# log = False
# if user_answer == "y":
#     log = True
log = True


class DbInitializer:
    def __init__(self, username="root", password=None):
        self.username = username
        self.password = password
        connector = mysql.connector.connect(
            host="localhost", user=username, password=password
        )
        connector.autocommit = True
        cursor = connector.cursor()
        if log:
            print("\ndb_initer log:")
        try:
            cursor.execute("CREATE DATABASE theatre")
            if log:
                print("\t-Database created successfully.")
        except mysql.connector.Error:
            if log:
                print("\t-Database already exists.")

        self.connector = mysql.connector.connect(
            host="localhost", user="root", password=password, database="theatre"
        )
        self.connector.autocommit = True
        self.cursor = self.connector.cursor()

    # TODO: close connector and cursor in destructor
    # def __del__(self):
    #     self.cursor.close()
    #     self.connector.close()

    def drop_db(self):
        self.connector = mysql.connector.connect(
            host="localhost", user=self.username, password=self.password
        )
        self.connector.autocommit = True
        self.cursor = self.connector.cursor()
        if log:
            print("\ndrop_db log:")
        try:
            self.cursor.execute("DROP DATABASE theatre")
            if log:
                print("\t-Database deleted successfully.")
        except mysql.connector.Error as error:
            if log:
                print(f"\t-Dropping database failed: {error}.")


class TablesGenerator:
    # TODO: move into TriggersGenerator
    @staticmethod
    def __add_building_triggers(cursor):
        try:
            cursor.execute(
                """
                        CREATE TRIGGER set_creation_date
                                BEFORE INSERT ON building
                                FOR EACH ROW
                                BEGIN
                                    SET NEW.creation_date = NOW();
                                END;
                        """
            )
            if log:
                print("\t-Trigger 'set_creation_date' created successfully.")
        except mysql.connector.Error as error:
            if log:
                print(
                    f"\t-Trigger 'set_creation_date' was not created due to: {error}."
                )

    @staticmethod
    def __add_impresario_triggers(cursor):
        try:
            cursor.execute(
                """
                        CREATE TRIGGER set_impresario_creation_date
                                BEFORE INSERT ON impresario
                                FOR EACH ROW
                                BEGIN
                                    SET NEW.creation_date = NOW();
                                END;
                        """
            )
            if log:
                print("\t-Trigger 'set_impresario_creation_date' created successfully.")
        except mysql.connector.Error as error:
            if log:
                print(
                    f"\t-Trigger 'set_impresario_creation_date' was not created due to: {error}."
                )

    @staticmethod
    def __add_genre_triggers(cursor):
        try:
            cursor.execute(
                """
                        CREATE TRIGGER set_genre_creation_date
                                BEFORE INSERT ON genre
                                FOR EACH ROW
                                BEGIN
                                    SET NEW.creation_date = NOW();
                                END;
                        """
            )
            if log:
                print("\t-Trigger 'set_genre_creation_date' created successfully.")
        except mysql.connector.Error as error:
            if log:
                print(
                    f"\t-Trigger 'set_genre_creation_date' was not created due to: {error}."
                )

    @staticmethod
    def __add_event_triggers(cursor):
        try:
            cursor.execute(
                """
                        CREATE TRIGGER set_event_creation_date
                                BEFORE INSERT ON event
                                FOR EACH ROW
                                BEGIN
                                    SET NEW.creation_date = NOW();
                                END;
                        """
            )
            if log:
                print("\t-Trigger 'set_event_creation_date' created successfully.")
        except mysql.connector.Error as error:
            if log:
                print(
                    f"\t-Trigger 'set_event_creation_date' was not created due to: {error}."
                )

    @staticmethod
    def __add_actor_triggers(cursor):
        try:
            cursor.execute(
                """
                        CREATE TRIGGER set_actor_creation_date
                                BEFORE INSERT ON actor
                                FOR EACH ROW
                                BEGIN
                                    SET NEW.creation_date = NOW();
                                END;
                        """
            )
            if log:
                print("\t-Trigger 'set_actor_creation_date' created successfully.")
            cursor.execute(
                """
                           CREATE TRIGGER check_name_surname_no_digits
                                BEFORE INSERT ON actor
                                FOR EACH ROW
                                BEGIN
                                    IF NEW.name REGEXP '[0-9]' THEN
                                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Name cannot contain digits';
                                    END IF;
                                    IF NEW.surname REGEXP '[0-9]' THEN
                                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Surname cannot contain digits';
                                    END IF;
                                END
                            """
            )
            if log:
                print("\t-Trigger 'check_name_surname_no_digits' created successfully.")

        except mysql.connector.Error as error:
            if log:
                print(f"\t-Failed to create trigger: {error}.")

    @staticmethod
    def __add_actor_genre_link_triggers(cursor):
        try:
            cursor.execute(
                """
                        CREATE TRIGGER set_actor_genre_link_creation_date
                                BEFORE INSERT ON actor_genre_link
                                FOR EACH ROW
                                BEGIN
                                    SET NEW.creation_date = NOW();
                                END;
                        """
            )
            if log:
                print(
                    "\t-Trigger 'set_actor_genre_link_creation_date' created successfully."
                )
        except mysql.connector.Error as error:
            if log:
                print(
                    f"\t-Trigger 'set_actor_genre_link_creation_date' was not created due to: {error}."
                )

    @staticmethod
    def __add_impresario_genre_link_triggers(cursor):
        try:
            cursor.execute(
                """
                        CREATE TRIGGER set_impresario_genre_link_creation_date
                                BEFORE INSERT ON impresario_genre_link
                                FOR EACH ROW
                                BEGIN
                                    SET NEW.creation_date = NOW();
                                END;
                        """
            )
            if log:
                print(
                    "\t-Trigger 'set_impresario_genre_link_creation_date' created successfully."
                )
        except mysql.connector.Error as error:
            if log:
                print(
                    f"\t-Trigger 'set_impresario_genre_link_creation_date' was not created due to: {error}."
                )

    @staticmethod
    def __add_contest_triggers(cursor):
        try:
            cursor.execute(
                """
                        CREATE TRIGGER set_contest_creation_date
                                BEFORE INSERT ON contest_table
                                FOR EACH ROW
                                BEGIN
                                    SET NEW.creation_date = NOW();
                                END;
                        """
            )
            if log:
                print("\t-Trigger 'set_contest_creation_date' created successfully.")
        except mysql.connector.Error as error:
            if log:
                print(
                    f"\t-Trigger 'set_contest_creation_date' was not created due to: {error}."
                )

    # TODO: вынести генерацию каждой процедуры в отдельную функцию
    @staticmethod
    def __add_functions(cursor):
        try:
            cursor.execute(
                """
                           CREATE FUNCTION get_impresario_count(building_id INT) RETURNS INT DETERMINISTIC
                                BEGIN
                                    DECLARE count INT;
                                    SELECT COUNT(*) INTO count FROM impresario WHERE impresario.building_id = building_id;
                                    RETURN count;
                                END
                            """
            )
            if log:
                print("\t-Function 'get_impresario_count' created successfully.")
            cursor.execute(
                """
                           CREATE FUNCTION get_genre_by_name(genre_name VARCHAR(255)) RETURNS VARCHAR(255) DETERMINISTIC
                                BEGIN
                                    DECLARE genre VARCHAR(255);
                                    SELECT name INTO genre FROM genre WHERE name = genre_name;
                                    RETURN genre;
                                END
                           """
            )
            if log:
                print("\t-Function 'get_genre_by_name' created successfully.")
        except mysql.connector.Error as error:
            if log:
                print(f"\t-Failed to create functions: {error}.")

    @staticmethod
    def __add_procedures(cursor):
        try:
            cursor.execute(
                """
                            CREATE PROCEDURE get_impresario_by_id(IN id INT)
                            BEGIN
                                SELECT * FROM impresario WHERE impresario.id = id;
                            END
                            """
            )
            if log:
                print("\t-Procedure 'get_impresario_by_id' created successfully.")

            cursor.execute(
                """
                           CREATE PROCEDURE add_building(IN building_name VARCHAR(255))
                                BEGIN
                                    INSERT INTO building (name) VALUES (building_name);
                                END
                           """
            )
            if log:
                print("\t-Procedure 'add_building' created successfully.")

            cursor.execute(
                """
                           CREATE PROCEDURE add_impresario(IN building_id INT, IN name VARCHAR(255), IN surname VARCHAR(255), IN age INT)
                                BEGIN
                                    INSERT INTO impresario (building_id, name, surname, age, creation_date) VALUES (building_id, name, surname, age, creation_date);
                                END
                           """
            )
            if log:
                print("\t-Procedure 'add_impresario' created successfully.")

            cursor.execute(
                """
                           CREATE PROCEDURE add_event(IN name VARCHAR(255), IN genre_name VARCHAR(255), IN impresario_id INT)
                                BEGIN
                                    INSERT INTO event (name, genre_name, impresario_id) VALUES (name, genre_name, impresario_id);
                                END
                           """
            )
            if log:
                print("\t-Procedure 'add_event' created successfully.")

        except mysql.connector.Error as error:
            if log:
                print(f"\t-Failed to create procedures: {error}.")

    @staticmethod
    def __create_building_table(cursor):
        cursor.execute(
            """
                            CREATE TABLE IF NOT EXISTS building (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255),
                                creation_date TIMESTAMP
                            )"""
        )
        if log:
            print("\t-Table 'building' created successfully.")

    @staticmethod
    def __create_impresario_table(cursor):
        cursor.execute(
            """
                            CREATE TABLE IF NOT EXISTS impresario (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                building_id INT,
                                name VARCHAR(255),
                                surname VARCHAR(255),
                                age INT,
                                creation_date TIMESTAMP,
                           
                                FOREIGN KEY (building_id) REFERENCES building(id)
                            )"""
        )
        if log:
            print("\t-Table 'impresario' created successfully.")

    @staticmethod
    def __create_genre_table(cursor):
        cursor.execute(
            """
                            CREATE TABLE IF NOT EXISTS genre (
                                name VARCHAR(255) PRIMARY KEY,
                                creation_date TIMESTAMP
                            )"""
        )
        if log:
            print("\t-Table 'genre' created successfully.")

    @staticmethod
    def __create_event_table(cursor):
        cursor.execute(
            """
                            CREATE TABLE IF NOT EXISTS event (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255),
                                genre_name VARCHAR(255),
                                impresario_id INT,
                                creation_date TIMESTAMP,

                                FOREIGN KEY (genre_name) REFERENCES genre(name),
                                FOREIGN KEY (impresario_id) REFERENCES impresario(id)
                            )"""
        )
        if log:
            print("\t-Table 'event' created successfully.")

    def __create_actor_table(cursor):
        cursor.execute(
            """
                            CREATE TABLE IF NOT EXISTS actor (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                event_id INT,
                                building_id INT,
                                name VARCHAR(255),
                                surname VARCHAR(255),
                                age INT,
                                creation_date TIMESTAMP,

                                FOREIGN KEY (event_id) REFERENCES event(id),
                                FOREIGN KEY (building_id) REFERENCES building(id)
                            )"""
        )
        if log:
            print("\t-Table 'actor' created successfully.")

    @staticmethod
    def __create_actor_genre_link_table(cursor):
        cursor.execute(
            """
                            CREATE TABLE IF NOT EXISTS actor_genre_link (
                                actor_id INT,
                                genre_name VARCHAR(255),
                                creation_date TIMESTAMP,

                                FOREIGN KEY (actor_id) REFERENCES actor(id) ON DELETE CASCADE,
                                FOREIGN KEY (genre_name) REFERENCES genre(name) ON DELETE CASCADE
                            )"""
        )
        if log:
            print("\t-Table 'actor_genre_link' created successfully.")

    @staticmethod
    def __create_impresario_genre_link_table(cursor):
        cursor.execute(
            """
                            CREATE TABLE IF NOT EXISTS impresario_genre_link (
                                impresario_id INT,
                                genre_name VARCHAR(255),
                                creation_date TIMESTAMP,

                                FOREIGN KEY (impresario_id) REFERENCES impresario(id) ON DELETE CASCADE,
                                FOREIGN KEY (genre_name) REFERENCES genre(name) ON DELETE CASCADE
                            )"""
        )
        if log:
            print("\t-Table 'impresario_genre_link' created successfully.")

    @staticmethod
    def __create_contest_table(cursor):
        cursor.execute(
            """
                            CREATE TABLE IF NOT EXISTS contest (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255),
                                creation_date TIMESTAMP,

                                first_place_id INT,
                                second_place_id INT,
                                third_place_id INT,

                                FOREIGN KEY (first_place_id) REFERENCES actor(id),
                                FOREIGN KEY (second_place_id) REFERENCES actor(id),
                                FOREIGN KEY (third_place_id) REFERENCES actor(id)
                            )"""
        )
        if log:
            print("\t-Table 'impresario_genre_link' created successfully.")

    @staticmethod
    def create_tables(connector):
        cursor = connector.cursor()
        if log:
            print("\ncreate_tables log:")
        try:
            TablesGenerator.__create_building_table(cursor)
            TablesGenerator.__create_impresario_table(cursor)
            TablesGenerator.__create_genre_table(cursor)
            TablesGenerator.__create_event_table(cursor)
            TablesGenerator.__create_actor_table(cursor)
            TablesGenerator.__create_actor_genre_link_table(cursor)
            TablesGenerator.__create_impresario_genre_link_table(cursor)
            TablesGenerator.__create_contest_table(cursor)
        except mysql.connector.Error as error:
            if log:
                print("\t-Failed to create table: {}".format(error))

    @staticmethod
    def create_triggers(connector):
        cursor = connector.cursor()
        if log:
            print("\ncreate_triggers log:")
        try:
            TablesGenerator.__add_building_triggers(cursor)
            TablesGenerator.__add_impresario_triggers(cursor)
            TablesGenerator.__add_genre_triggers(cursor)
            TablesGenerator.__add_event_triggers(cursor)
            TablesGenerator.__add_actor_triggers(cursor)
            TablesGenerator.__add_actor_genre_link_triggers(cursor)
            TablesGenerator.__add_impresario_genre_link_triggers(cursor)
            TablesGenerator.__add_contest_triggers(cursor)
        except mysql.connector.Error as error:
            if log:
                print("\t-Failed to create trigger: {}".format(error))

    @staticmethod
    def create_procedures(connector):
        cursor = connector.cursor()
        if log:
            print("\ncreate_procedures log:")
        try:
            TablesGenerator.__add_procedures(cursor)
        except mysql.connector.Error as error:
            if log:
                print("\t-Failed to create procedure: {}".format(error))

    @staticmethod
    def create_functions(connector):
        cursor = connector.cursor()
        if log:
            print("\ncreate_functions log:")
        try:
            TablesGenerator.__add_functions(cursor)
        except mysql.connector.Error as error:
            if log:
                print("\t-Failed to create function: {}".format(error))


class DumpGenerator:
    @staticmethod
    def __insert_buildings(cursor):
        cursor.execute(
            """
                    INSERT INTO building (name) VALUES 
                        ('Небесная башня'),
                        ('Сапфировый дом'),
                        ('Эмеральдовые вершины'),
                        ('Золотой горизонт'),
                        ('Дом культуры');
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
                    INSERT INTO event (name, genre_name, impresario_id) VALUES
                            ('Последний вздох', 'Драма', 1),
                            ('Вставай', 'Комедия', 2),
                            ('Ее след', 'Романтика', 3),
                            ('Отличник с личной жизнью', 'Фантастика', 4),
                            ('Астрал', 'Мистика', 5),
                            ('Пара по психологии', 'Комедия', 6),
                            ('Щелкунчик', 'Балет', 7),
                            ('Лебединое озеро', 'Балет', 8),
                            ('Рад вас видеть', 'Комедия', 9),
                            ('Кошки', 'Мюзикл', 10),
                            ('Спящая красавица', 'Балет', 11),
                            ('Wall-e', 'Анимация', 12),
                            ('Дон Кихот', 'Балет', 13),
                            ('Баядерка', 'Балет', 14),
                            ('Жизель', 'Балет', 15);
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
                            (12, 'Анимация')
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
                            (1, 'Анимация')
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
                            ('Лучшая роль второго плана', 6, 7, 8)
                        """
        )
        if log:
            print("\t-Actor_genre_link dump created successfully.")

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
            if log:
                print("\t-Dump created successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Failed to create dump: {}".format(error))


class RolesGenerator:
    @staticmethod
    def __refresh_roles(cursor):
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'admin';")
            cursor.execute("DROP USER 'admin'@'localhost';")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'viewer';")
            cursor.execute("DROP USER 'viewer'@'localhost';")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'event_manager';")
            cursor.execute("DROP USER 'event_manager'@'localhost';")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))
        try:
            cursor.execute("DELETE FROM mysql.user WHERE User LIKE 'impresario';")
            cursor.execute("DROP USER 'impresario'@'localhost';")
        except mysql.connector.Error as error:
            if log:
                print("\t-Error: {}".format(error))

        cursor.execute("FLUSH PRIVILEGES;")

    @staticmethod
    def __add_admin_role(cursor):
        cursor.execute("CREATE ROLE 'admin'@'localhost';")
        cursor.execute("GRANT ALL ON theatre.* TO 'admin'@'localhost';")
        if log:
            print("-Admin role created successfully.")

    @staticmethod
    def __add_viewer_role(cursor):
        cursor.execute("CREATE ROLE 'viewer'@'localhost';")
        cursor.execute("GRANT SELECT ON theatre.* TO 'viewer'@'localhost';")
        if log:
            print("-Viewer role created successfully.")

    @staticmethod
    def __add_event_manager_role(cursor):
        cursor.execute("CREATE ROLE 'event_manager'@'localhost';")
        cursor.execute("GRANT SELECT ON theatre.* TO 'event_manager'@'localhost';")
        cursor.execute("GRANT INSERT ON theatre.event TO 'event_manager'@'localhost';")
        cursor.execute("GRANT UPDATE ON theatre.event TO 'event_manager'@'localhost';")
        if log:
            print("-Event manager role created successfully.")

    @staticmethod
    def __add_impresario_role(cursor):
        cursor.execute("CREATE ROLE 'impresario'@'localhost';")
        cursor.execute("GRANT SELECT ON theatre.* TO 'impresario'@'localhost';")
        cursor.execute("GRANT INSERT ON theatre.event TO 'impresario'@'localhost';")
        cursor.execute("GRANT INSERT ON theatre.contest TO 'impresario'@'localhost';")
        cursor.execute("GRANT UPDATE ON theatre.event TO 'impresario'@'localhost';")
        if log:
            print("-Impresario role created successfully.")

    @staticmethod
    def create_roles(connector):
        cursor = connector.cursor()
        if log:
            print("\ncreate_roles log:")
        try:
            RolesGenerator.__refresh_roles(cursor)
            RolesGenerator.__add_admin_role(cursor)
            RolesGenerator.__add_viewer_role(cursor)
            RolesGenerator.__add_event_manager_role(cursor)
            RolesGenerator.__add_impresario_role(cursor)
            if log:
                print("\t-Roles created successfully.")
        except mysql.connector.Error as error:
            if log:
                print("\t-Failed to create roles: {}".format(error))


class DBManager:
    def __init__(self, connector):
        self.cursor = connector.cursor()

    def select_all_from(self, table_name):
        # TODO: add make this function in db
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()

    def select_actors(self):
        self.cursor.execute(
            """
                            SELECT actor.id,
                                    event.name as event_name,
                                    building.name as building_name,
                                    actor.name,
                                    actor.surname,
                                    actor.age,
                                    actor.creation_date
                            FROM actor
                            JOIN event ON actor.event_id = event.id
                            JOIN building ON actor.building_id = building.id
                            """
        )
        return self.cursor.fetchall()

    def select_buildings(self):
        self.cursor.execute("SELECT * FROM building")
        return self.cursor.fetchall()

    def select_events(self):
        self.cursor.execute(
            """
                            SELECT event.id,
                                    event.name,
                                    event.genre_name,
                                    impresario.name as impresario_name,
                                    impresario.surname as impresario_surname,
                                    event.creation_date
                            FROM event
                            JOIN impresario ON event.impresario_id = impresario.id
                            """
        )
        return self.cursor.fetchall()

    def select_impresarios(self):
        self.cursor.execute(
            """
                            SELECT impresario.id,
                                    building.name,
                                    impresario.name,
                                    impresario.surname,
                                    impresario.age,
                                    impresario.creation_date
                            FROM impresario
                            JOIN building ON impresario.building_id = building.id
                            """
        )
        return self.cursor.fetchall()

    def select_genres(self):
        self.cursor.execute("SELECT * FROM genre")
        return self.cursor.fetchall()

    def select_contests(self):
        self.cursor.execute(
            """
            SELECT c.name AS contest_name, 
                a1.name AS first_place_name, a1.surname AS first_place_surname,
                a2.name AS second_place_name, a2.surname AS second_place_surname,
                a3.name AS third_place_name, a3.surname AS third_place_surname
            FROM contest c
            JOIN actor a1 ON c.first_place_id = a1.id
            JOIN actor a2 ON c.second_place_id = a2.id
            JOIN actor a3 ON c.third_place_id = a3.id;

            """
        )
        return self.cursor.fetchall()

    def insert_event(self, name, genre_name, impresario_id):
        self.cursor.execute(
            f"CALL add_event('{name}', '{genre_name}', {impresario_id})"
        )

    def print_select_all(self, table_name):
        print(f"{table_name}:")
        result = ""
        for row in self.select_all(table_name):
            print(result)
            result += repr(row) + "\n"
        return result
