import mysql.connector

log = True


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
