import tkinter as tk
from tkinter import ttk

# TODO: Добавить конкурсы.


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
    Connects to the database screen, where a
    user can enter the connection details.
    This function does not take any parameters.
    It does not return anything.
    """

    def connect_to_db_screen(self):
        self.current_window = tk.Tk()
        self.current_window.title("Подключение к базе данных")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        page_description_label = tk.Label(
            self.current_window,
            text="На данной странице необходимо подключиться к БД как root пользователь. После этого будет создан администратор БД.",
        )
        default_login_btn = tk.Button(
            self.current_window,
            text="Вход по умолчанию (логин: root, без пароля).",
            command=self.__default_login,
        )
        login_btn = tk.Button(
            self.current_window,
            text="Вход c вводом логина и пароля",
            command=lambda: self.__open_login_window(has_root_window=True),
        )
        page_description_label.pack()
        default_login_btn.pack()
        login_btn.pack()

        self.current_window.mainloop()
        return self.username, self.password

    def set_db_manager(self, db_manager):
        self.db_manager = db_manager

    def __pick_role(self, role_name):
        self.role = role_name
        self.current_window.destroy()

    def sign_in(self):
        self.current_window = tk.Tk()
        self.current_window.title("Вход в систему")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)
        self.__open_login_window()
        self.current_window.mainloop()

        return self.username, self.password

    def get_role(self):
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

        header_text = None
        match role:
            case "admin_role":
                header_text = "Меню для зрителя"
            case "viewer_role":
                header_text = "Меню для зрителя"
            case "event_manager_role":
                header_text = "Меню для событий"
            case "impresario_role":
                header_text = "Меню для импресарио"

        header_label = tk.Label(self.current_window, text=header_text)
        header_label.pack()

        # Общие для всех кнопки:
        actors_page_btn = tk.Button(
            self.current_window,
            text="Страница актеров",
            command=lambda: self.__set_next_window("actors_page"),
        )
        events_page_btn = tk.Button(
            self.current_window,
            text="Страница событий",
            command=lambda: self.__set_next_window("events_page"),
        )
        impresarios_page_btn = tk.Button(
            self.current_window,
            text="Страница импресарио",
            command=lambda: self.__set_next_window("impresarios_page"),
        )
        buildings_page_btn = tk.Button(
            self.current_window,
            text="Страница зданий",
            command=lambda: self.__set_next_window("buildings_page"),
        )
        contests_page_btn = tk.Button(
            self.current_window,
            text="Страница конкурсов",
            command=lambda: self.__set_next_window("contests_page"),
        )

        actors_page_btn.pack()
        events_page_btn.pack()
        impresarios_page_btn.pack()
        buildings_page_btn.pack()
        contests_page_btn.pack()

        match role:
            case "admin_role":
                pass
            case "viewer_role":
                pass
            case "event_manager_role":
                create_event_btn = tk.Button(
                    self.current_window,
                    text="Создать событие",
                    command=lambda: self.__set_next_window("create_event"),
                )
                create_event_btn.pack()
            case "impresario_role":
                pass
        exit_btn = tk.Button(
            self.current_window,
            text="Завершить работу",
            command=lambda: self.__set_next_window("exit"),
        )
        exit_btn.pack()

        self.current_window.mainloop()
        return self.next_window_name

    def __filter_actors(self):
        self.current_window = tk.Tk()
        self.current_window.title("Фильтрация актеров")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)

        self.current_window.mainloop()

    def __actors_page(self):
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

    def __events_page(self):
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

    def __impresarios_page(self):
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

    def __buildings_page(self):
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

    def __contests_page(self):
        self.current_window = tk.Tk()
        self.current_window.title("Конкурсы")
        self.current_window.geometry("1280x720")
        self.current_window.resizable(1, 1)
        events = self.db_manager.select_contests()

        # Создание таблицы для отображения данных
        table = ttk.Treeview(
            self.current_window,
            columns=(
                "name",
                "first_place",
                "second_place",
                "third_place",
            ),
        )
        table["show"] = "headings"
        table.heading("name", text="Название конкурса")
        table.heading("first_place", text="Первое место")
        table.heading("second_place", text="Второе место")
        table.heading("third_place", text="Третье место")

        # Вставка данных в таблицу
        for row in events:
            first_place = f"{row[1]} {row[2]}"  # Объединяем имя и фамилию первого места
            second_place = (
                f"{row[3]} {row[4]}"  # Объединяем имя и фамилию второго места
            )
            third_place = (
                f"{row[5]} {row[6]}"  # Объединяем имя и фамилию третьего места
            )
            table.insert(
                "", "end", values=[row[0], first_place, second_place, third_place]
            )

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

        impresario_label = tk.Label(self.current_window, text="Выберите импресарио:")
        impresario_label.pack()
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
            case "actors_page":
                next_window = self.__actors_page()
            case "events_page":
                next_window = self.__events_page()
            case "impresarios_page":
                next_window = self.__impresarios_page()
            case "buildings_page":
                next_window = self.__buildings_page()
            case "create_event":
                next_window = self.__create_event()
            case "contests_page":
                next_window = self.__contests_page()
        return next_window
