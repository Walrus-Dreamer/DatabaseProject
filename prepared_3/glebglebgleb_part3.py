import mysql.connector
import mysql
import tkinter as tk
from tkinter import ttk

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
        except mysql.connector.Error:
            if log:
                print("\t-Database does not exist.")


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
                            ('Film Screening', 'Анимация', 12),
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
    def __insert_actor_genre_link(cursor):
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
    def __insert_impresario_genre_link(cursor):
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
            DumpGenerator.__insert_actor_genre_link(cursor)
            DumpGenerator.__insert_impresario_genre_link(cursor)
        except mysql.connector.Error as error:
            if log:
                print("\t-Failed to create dump: {}".format(error))


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


class GUI:
    def __init__(self):
        self.current_window = None
        self.next_window_name = None
        self.db_manager = None

    def __default_login(self):
        self.username = "root"
        self.password = None
        self.current_window.destroy()

    def __submit(self, login_window, entry_username, entry_password):
        self.username = entry_username.get()
        self.password = entry_password.get()
        login_window.destroy()
        self.current_window.destroy()

    def __open_login_window(self):
        login_window = tk.Toplevel(self.current_window)
        login_window.title("Вход")

        label_username = tk.Label(login_window, text="Логин:")
        label_username.pack()

        entry_username = tk.Entry(login_window)
        entry_username.pack()

        label_password = tk.Label(login_window, text="Пароль:")
        label_password.pack()

        entry_password = tk.Entry(login_window, show="*")
        entry_password.pack()

        button_submit = tk.Button(
            login_window,
            text="Войти",
            command=lambda: self.__submit(
                login_window=login_window,
                entry_username=entry_username,
                entry_password=entry_password,
            ),
        )

        button_submit.pack()

    """
    Connects to the database screen, where a user can enter the connection details.
    This function does not take any parameters.
    It does not return anything.
    """

    def connect_to_db_screen(self):
        self.login_input = ""
        self.password_input = ""

        self.current_window = tk.Tk()
        self.current_window.title("Подключение к базе данных")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        default_login_btn = tk.Button(
            self.current_window, text="Вход по умолчанию", command=self.__default_login
        )
        login_btn = tk.Button(
            self.current_window,
            text="Вход c вводом логина и пароля",
            command=self.__open_login_window,
        )
        default_login_btn.pack()
        login_btn.pack()

        self.current_window.mainloop()
        return self.username, self.password

    def set_db_manager(self, db_manager):
        self.db_manager = db_manager

    def __pick_role(self, role_name):
        self.role = role_name
        self.current_window.destroy()

    def select_role(self):
        self.current_window = tk.Tk()
        self.current_window.title("Выбор роли")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        label = tk.Label(self.current_window, text="Выберите роль:")
        assistant_btn = tk.Button(
            self.current_window,
            text="Зритель",
            command=lambda: self.__pick_role("viewer"),
        )
        my_events_btn = tk.Button(
            self.current_window,
            text="Менеджер событий",
            command=lambda: self.__pick_role("event_manager"),
        )

        label.pack()
        assistant_btn.pack()
        my_events_btn.pack()

        self.current_window.mainloop()
        return self.role

    def __set_next_window(self, next_window_name):
        self.next_window_name = next_window_name
        self.current_window.destroy()

    def __main_menu(self, role):
        self.current_window = tk.Tk()
        self.current_window.title("Главное меню")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)
        self.next_window_name = "exit"

        match role:
            case "viewer":
                viewer_label = tk.Label(self.current_window, text="Меню для зрителя")
                show_actors_btn = tk.Button(
                    self.current_window,
                    text="Показать актеров",
                    command=lambda: self.__set_next_window("show_actors"),
                )
                show_events_btn = tk.Button(
                    self.current_window,
                    text="Показать события",
                    command=lambda: self.__set_next_window("show_events"),
                )
                show_impresarios_btn = tk.Button(
                    self.current_window,
                    text="Показать импресарио",
                    command=lambda: self.__set_next_window("show_impresarios"),
                )
                show_buildings_btn = tk.Button(
                    self.current_window,
                    text="Показать здания",
                    command=lambda: self.__set_next_window("show_buildings"),
                )
                exit_btn = tk.Button(
                    self.current_window,
                    text="Завершить работу",
                    command=lambda: self.__set_next_window("exit"),
                )

                viewer_label.pack()
                show_actors_btn.pack()
                show_events_btn.pack()
                show_impresarios_btn.pack()
                show_buildings_btn.pack()
                exit_btn.pack()
            case "event_manager":
                impresario_label = tk.Label(
                    self.current_window, text="Меню для менеджера событий"
                )
                show_actors_btn = tk.Button(
                    self.current_window,
                    text="Показать актеров",
                    command=lambda: self.__set_next_window("show_actors"),
                )
                show_events_btn = tk.Button(
                    self.current_window,
                    text="Показать события",
                    command=lambda: self.__set_next_window("show_events"),
                )
                show_impresarios_btn = tk.Button(
                    self.current_window,
                    text="Показать импресарио",
                    command=lambda: self.__set_next_window("show_impresarios"),
                )
                show_buildings_btn = tk.Button(
                    self.current_window,
                    text="Показать здания",
                    command=lambda: self.__set_next_window("show_buildings"),
                )
                create_event_btn = tk.Button(
                    self.current_window,
                    text="Создать событие",
                    command=lambda: self.__set_next_window("create_event"),
                )
                exit_btn = tk.Button(
                    self.current_window,
                    text="Завершить работу",
                    command=lambda: self.__set_next_window("exit"),
                )

                impresario_label.pack()
                show_actors_btn.pack()
                show_events_btn.pack()
                show_impresarios_btn.pack()
                show_buildings_btn.pack()
                create_event_btn.pack()
                exit_btn.pack()

        self.current_window.mainloop()
        return self.next_window_name

    def __filter_actors(self):
        self.current_window = tk.Tk()
        self.current_window.title("Фильтрация актеров")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        self.current_window.mainloop()

    def __show_actors(self):
        self.current_window = tk.Tk()
        self.current_window.title("Актеры")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)
        actors = self.db_manager.select_actors()

        # Создание таблицы для отображения данных
        table = ttk.Treeview(
            self.current_window,
            columns=(
                "Event name",
                "Building name",
                "Name",
                "Surname",
                "Age",
                "Creation Date",
            ),
        )
        table["show"] = "headings"
        table.heading("Event name", text="Название события")
        table.heading("Building name", text="Названия здания")
        table.heading("Name", text="Имя актера")
        table.heading("Surname", text="Фамилия актера")
        table.heading("Age", text="Возраст актера")
        table.heading("Creation Date", text="Дата создания записи")

        # Вставка данных в таблицу
        for row in actors:
            table.insert("", "end", values=row[1:])  # Не отображаем id

        # Размещение таблицы на окне
        table.pack()
        # filter_button = tk.Button(self.current_window, text='Фильтр', command=self.__filter_actors)
        # filter_button.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __show_events(self):
        self.current_window = tk.Tk()
        self.current_window.title("События")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)
        events = self.db_manager.select_events()

        # Создание таблицы для отображения данных
        table = ttk.Treeview(
            self.current_window,
            columns=(
                "Event name",
                "Genre name",
                "Impresario name",
                "Impresario surname",
                "Creation Date",
            ),
        )
        table["show"] = "headings"
        table.heading("Event name", text="Название события")
        table.heading("Genre name", text="Название жанра")
        table.heading("Impresario name", text="Имя импресарио")
        table.heading("Impresario surname", text="Фамилия импресарио")
        table.heading("Creation Date", text="Дата создания записи")

        # Вставка данных в таблицу
        for row in events:
            table.insert("", "end", values=row[1:])  # Не отображаем id

        # Размещение таблицы на окне
        table.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __show_impresarios(self):
        self.current_window = tk.Tk()
        self.current_window.title("Импресарио")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)
        impresarios = self.db_manager.select_impresarios()

        # Создание таблицы для отображения данных
        table = ttk.Treeview(
            self.current_window,
            columns=(
                "Building name",
                "Impresario name",
                "Impresario surname",
                "Impresario age",
                "Creation Date",
            ),
        )
        table["show"] = "headings"
        table.heading("Building name", text="Название здания")
        table.heading("Impresario name", text="Имя импресарио")
        table.heading("Impresario surname", text="Фамилия импресарио")
        table.heading("Impresario age", text="Возраст импресарио")
        table.heading("Creation Date", text="Дата создания записи")

        # Вставка данных в таблицу
        for row in impresarios:
            table.insert("", "end", values=row[1:])  # Не отображаем id

        # Размещение таблицы на окне
        table.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __show_buildings(self):
        self.current_window = tk.Tk()
        self.current_window.title("Здания")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)
        buildings = self.db_manager.select_buildings()

        # Создание таблицы для отображения данных
        table = ttk.Treeview(
            self.current_window, columns=("Building name", "Creation Date")
        )
        table["show"] = "headings"
        table.heading("Building name", text="Название здания")
        table.heading("Creation Date", text="Дата создания записи")

        # Вставка данных в таблицу
        for row in buildings:
            table.insert("", "end", values=row[1:])  # Не отображаем id

        # Размещение таблицы на окне
        table.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def __to_main_menu(self):
        if self.current_window:
            self.current_window.destroy()
        return "main_menu"

    def __create_event(self):
        self.current_window = tk.Tk()
        self.current_window.title("Добавление события")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        # Получаем названия жанров
        genres = [genre[0] for genre in self.db_manager.select_genres()]
        # Получаем id, имена и фамилии импресарио
        impresarios = {
            impresario[0]: impresario[2] + " " + impresario[3]
            for impresario in self.db_manager.select_impresarios()
        }

        event_name_label = tk.Label(self.current_window, text="Название события:")
        event_name_label.pack()
        event_name_entry = tk.Entry(self.current_window)
        event_name_entry.pack()

        genre_label = tk.Label(self.current_window, text="Выберите жанр:")
        genre_label.pack()
        genre_combobox = ttk.Combobox(
            self.current_window, values=genres, state="readonly"
        )
        genre_combobox.pack()

        impresario_combobox = ttk.Combobox(
            self.current_window, values=list(impresarios.values())
        )
        impresario_combobox.pack()

        def submit():
            event_name = event_name_entry.get()
            genre_name = genre_combobox.get()

            # Получаем id импресарио по выбранному ФИО
            selected_full_name = impresario_combobox.get()
            selected_id = [
                key for key, value in impresarios.items() if value == selected_full_name
            ][0]

            self.db_manager.insert_event(event_name, genre_name, selected_id)
            self.current_window.destroy()

        submit_button = tk.Button(self.current_window, text="Добавить", command=submit)
        submit_button.pack()

        main_menu_button = tk.Button(
            self.current_window,
            text="Вернуться в главное меню",
            command=self.__to_main_menu,
        )
        main_menu_button.pack()

        self.current_window.mainloop()
        return "main_menu"

    def handle_command(self, command, role):
        next_window = "exit"
        match command:
            case "main_menu":
                next_window = self.__main_menu(role)
            case "show_actors":
                next_window = self.__show_actors()
            case "show_events":
                next_window = self.__show_events()
            case "show_impresarios":
                next_window = self.__show_impresarios()
            case "show_buildings":
                next_window = self.__show_buildings()
            case "create_event":
                next_window = self.__create_event()
        return next_window


class Kernel:
    def __init__(self):
        self.role = None

    def run(self):
        gui = GUI()
        login, password = gui.connect_to_db_screen()
        db_initer = DbInitializer(login, password)
        try:
            TablesGenerator.create_tables(db_initer.connector)
            TablesGenerator.create_triggers(db_initer.connector)
            TablesGenerator.create_procedures(db_initer.connector)
            TablesGenerator.create_functions(db_initer.connector)
            DumpGenerator.create_dump(db_initer.connector)
        except mysql.connector.Error as error:
            print(f"Failed to generate data: {error}")

        self.role = gui.select_role()
        db_manager = DBManager(db_initer.connector)
        gui.set_db_manager(db_manager)

        next_window_name = "main_menu"
        while next_window_name != "exit":
            next_window_name = gui.handle_command(next_window_name, self.role)
        db_initer.drop_db()


kernel = Kernel()
kernel.run()


# начало sql запросов:
"""
CREATE DATABASE theatre

DROP DATABASE theatre

CREATE TRIGGER set_creation_date
    BEFORE INSERT ON building
    FOR EACH ROW
    BEGIN
        SET NEW.creation_date = NOW();
    END;

CREATE TRIGGER set_impresario_creation_date
    BEFORE INSERT ON impresario
    FOR EACH ROW
    BEGIN
        SET NEW.creation_date = NOW();
    END;

CREATE TRIGGER set_genre_creation_date
    BEFORE INSERT ON genre
    FOR EACH ROW
    BEGIN
        SET NEW.creation_date = NOW();
    END;

CREATE TRIGGER set_event_creation_date
    BEFORE INSERT ON event
    FOR EACH ROW
    BEGIN
        SET NEW.creation_date = NOW();
    END;

CREATE TRIGGER set_actor_creation_date
    BEFORE INSERT ON actor
    FOR EACH ROW
    BEGIN
        SET NEW.creation_date = NOW();
    END;

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

CREATE TRIGGER set_actor_genre_link_creation_date
    BEFORE INSERT ON actor_genre_link
    FOR EACH ROW
    BEGIN
        SET NEW.creation_date = NOW();
    END;

CREATE FUNCTION get_impresario_count(building_id INT) RETURNS INT DETERMINISTIC
    BEGIN
        DECLARE count INT;
        SELECT COUNT(*) INTO count FROM impresario WHERE impresario.building_id = building_id;
        RETURN count;
    END

CREATE FUNCTION get_genre_by_name(genre_name VARCHAR(255)) RETURNS VARCHAR(255) DETERMINISTIC
    BEGIN
        DECLARE genre VARCHAR(255);
        SELECT name INTO genre FROM genre WHERE name = genre_name;
        RETURN genre;
    END

CREATE PROCEDURE get_impresario_by_id(IN id INT)
    BEGIN
        SELECT * FROM impresario WHERE impresario.id = id;
    END

CREATE PROCEDURE add_building(IN building_name VARCHAR(255))
    BEGIN
        INSERT INTO building (name) VALUES (building_name);
    END

CREATE PROCEDURE add_impresario(IN building_id INT, IN name VARCHAR(255), IN surname VARCHAR(255), IN age INT, IN creation_date TIMESTAMP)
    BEGIN
        INSERT INTO impresario (building_id, name, surname, age, creation_date) VALUES (building_id, name, surname, age, creation_date);
    END

CREATE TABLE IF NOT EXISTS building (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    creation_date TIMESTAMP
)

CREATE TABLE IF NOT EXISTS impresario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    building_id INT,
    name VARCHAR(255),
    surname VARCHAR(255),
    age INT,
    creation_date TIMESTAMP,

    FOREIGN KEY (building_id) REFERENCES building(id)
)

CREATE TABLE IF NOT EXISTS genre (
    name VARCHAR(255) PRIMARY KEY,
    creation_date TIMESTAMP
)

CREATE TABLE IF NOT EXISTS event (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    genre_name VARCHAR(255),
    impresario_id INT,
    creation_date TIMESTAMP,

    FOREIGN KEY (genre_name) REFERENCES genre(name),
    FOREIGN KEY (impresario_id) REFERENCES impresario(id)
)

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
)

CREATE TABLE IF NOT EXISTS actor_genre_link (
    actor_id INT,
    genre_name VARCHAR(255),
    creation_date TIMESTAMP,

    FOREIGN KEY (actor_id) REFERENCES actor(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_name) REFERENCES genre(name) ON DELETE CASCADE
)

INSERT INTO building (name) VALUES 
    ('Небесная башня'),
    ('Сапфировый дом'),
    ('Эмеральдовые вершины'),
    ('Золотой горизонт'),
    ('Дом культуры');

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
    ('Film Screening', 'Анимация', 12),
    ('Дон Кихот', 'Балет', 13),
    ('Баядерка', 'Балет', 14),
    ('Жизель', 'Балет', 15);

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
# конец sql запросов.
