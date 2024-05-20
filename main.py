from init.db_init import DbInitializer
from init.generators.dump_generator import DumpGenerator
from init.generators.roles_generator import RolesGenerator
from init.generators.tables_generator import TablesGenerator
from init.generators.users_generator import UsersGenerator
from db_manager import DBManager

from gui import GUI
import mysql


class Kernel:
    def __init__(self):
        self.role = None

    def run(self):
        gui = GUI()
        create_db = gui.create_db_modal()
        # Инициализация БД
        while create_db:
            try:
                root_login, root_password, host, port = gui.connect_to_db_screen()
                db_initer = DbInitializer(root_login, root_password, host, port)
                create_db = False
                try:
                    TablesGenerator.create_tables(db_initer.connector)
                    TablesGenerator.create_triggers(db_initer.connector)
                    TablesGenerator.create_procedures(db_initer.connector)
                    TablesGenerator.create_functions(db_initer.connector)
                    RolesGenerator.create_default_roles(db_initer.connector)
                    UsersGenerator.create_default_users(db_initer.connector)
                    DumpGenerator.create_dump(db_initer.connector)
                except mysql.connector.Error as error:
                    print(f"Failed to initialize database: {error}")
            except mysql.connector.Error as error:
                print(f"Failed to connect to database: {error}")

        # Начало работы проекта
        next_window_name = "change_user"
        while next_window_name != "exit":
            if next_window_name == "change_user":
                errors = True
                while errors:
                    try:
                        gui = GUI()
                        username, password, next_window_name = gui.sign_in()
                        db_manager = DBManager(username=username, password=password)
                        self.role = db_manager.get_my_role()
                        gui.set_db_manager(db_manager)
                        errors = False
                    except mysql.connector.Error as error:
                        print(f"Failed to sign in: {error}")
                        pass
                        # TODO: добавить окно с ошибкой.
            next_window_name = gui.handle_command(next_window_name, self.role)

        user_decision = input("Вы хотите очистить базу? (y/n): ")
        if user_decision == "y":
            RolesGenerator.delete_roles(db_manager.connector)
            UsersGenerator.delete_users(db_manager.connector)

            db_manager.drop_db()


kernel = Kernel()
kernel.run()

# TODO: Фильтрация записей
# TODO: Выкидывать ошибку, если добавляемое событие уже есть в БД
