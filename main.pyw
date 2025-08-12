from tkinter import *
from tkinter import messagebox, scrolledtext
import sys
from pygame import mixer
from datetime import datetime
import os
from tkinter.font import Font

class App:  # Основной класс
    def __init__(self, root):  # Конструктор класса
        self.root = root
        self.root.title('Comandrix - ПКС')
        self.root.geometry('600x470')
        self.root.resizable(False, False)
        self.sounds_enabled = True
        self.time_label = None
        self.file_counter = 0
        self.file_icons = []  # Для хранения ссылок на иконки файлов
        self.editor_open = False
        self.current_editing_file = None  # Путь к редактируемому файлу
        self.storage_path = 'Storage'
        self.after_id = None  # Для отмены after-вызова
        self.ensure_storage()

    def check_dos_font(self):

        # Проверяем, существует ли шрифт DOSFont
        try:
            test_font = Font(family="DOSFont", size=12)
            actual_font = test_font.actual()
            
            # Если tkinter подменил шрифт, actual['family'] может отличаться
            if actual_font['family'] != "DOSFont":
                raise RuntimeError("Шрифт DOSFont не найден")
        except:
            # Если шрифт не найден, показываем предупреждение
            messagebox.showwarning(
                "Ошибка шрифта",
                "Шрифт DOSFont не установлен в системе!\n"
                "Некоторые элементы интерфейса могут отображаться некорректно.\n\n"
                "Вы можете установить шрифт в папке проекта."
            )

    def ensure_storage(self):
        # Создаёт папку Storage, если её нет
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def load_files_from_storage(self):
        # Загружает файлы из хранилища и отображает их на рабочем столе
        # Сначала очищаем старые иконки
        self.clear_file_icons()
        
        # Затем загружаем файлы
        files = [f for f in os.listdir(self.storage_path) if f.endswith('.txt')]
        self.file_counter = len(files)
        
        # Остальной код метода остается без изменений
        x_pos = 20
        y_pos = 40
        spacing = 35
        
        for idx, filename in enumerate(files):
            filepath = os.path.join(self.storage_path, filename)
            
            if y_pos + 30 > 380:
                overflow_label = Label(
                    self.desktop_frame_screen,
                    text="[...]",
                    font=('DOSFont', 18), bg='black', fg='gray')
                overflow_label.place(x=x_pos, y=y_pos)
                break
                
            file_icon = Label(
                self.desktop_frame_screen,
                text=f"▄ {filename}",
                font=('DOSFont', 18), bg='black', fg='lime')
            file_icon.place(x=x_pos, y=y_pos)
            file_icon.bind("<Button-1>", lambda e, path=filepath: self.open_file_context(path))
            
            self.file_icons.append({
                'label': file_icon,
                'name': filename,
                'path': filepath,
                'x': x_pos,
                'y': y_pos
            })
            
            y_pos += spacing

    def create_menu(self):  # Filedialog-меню
        main_menu = Menu(self.root)
        self.root.config(menu=main_menu)

        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_separator()
        file_menu.add_command(label='Выход', command=self.exit)

        main_menu.add_cascade(label='Файл', menu=file_menu)

        help_menu = Menu(main_menu, tearoff=0)
        help_menu.add_command(label='Справка', command=self.show_help)
        main_menu.add_cascade(label='Помощь', menu=help_menu)

    def start_sound(self):  # Начальный звук
        if self.sounds_enabled:
            try:
                mixer.music.load('snd/beep.mp3')
                mixer.music.play()
            except Exception as e:
                pass

    def button_sound(self):  # Звуки кнопок
        if self.sounds_enabled:
            try:
                mixer.music.load('snd/beep.mp3')
                mixer.music.play()
            except Exception as e:
                pass

    def error_sound(self):  # Звуки кнопок
        if self.sounds_enabled:
            try:
                mixer.music.load('snd/error.mp3')
                mixer.music.play()
            except Exception as e:
                pass

    def toggle_sounds(self):  # Функция выключения звуков
        self.sounds_enabled = not self.sounds_enabled
        self.turn_off_sounds_var.set(not self.sounds_enabled)

    def set_up_frame(self):  # Начальный фрейм
        self.main_frame = Frame(self.root, bg='black')
        self.main_frame.pack(fill='both', expand=True)

    def set_up_elements(self):  # Расставляем элементы загрузочного экрана
        self.main_label = Label(self.main_frame, text='- Добро пожаловать в Computerix!\nВыберите пункт загрузки',
                                font=('DOSFont', 18), bg='black', fg='lime')

        self.start_button = Button(self.main_frame, text='<Войти в систему>', command=self.get_started,
                                   font=('DOSFont', 18), bg='black', fg='lime',
                                   activebackground='black', activeforeground='white',
                                   relief=FLAT, borderwidth=0, highlightthickness=0)

        self.turn_off_sounds_var = BooleanVar(value=False)
        self.turn_off_sounds_checkbox = Checkbutton(
            self.main_frame, text='<Выключить системные звуки>',
            font=f'{'DOSFont'} 18',
            variable=self.turn_off_sounds_var,
            command=self.toggle_sounds,
            bg='black', fg='lime',
            activebackground='black',
            activeforeground='lime',
            selectcolor='black',
            relief=FLAT, borderwidth=0, highlightthickness=0)

        self.exit_button = Button(self.main_frame, text='<Завершить сеанс>', command=self.exit,
                                  font=('DOSFont', 18), bg='black', fg='lime',
                                  activebackground='black', activeforeground='white',
                                  relief=FLAT, borderwidth=0, highlightthickness=0)

        self.start_terminal_button = Button(self.main_frame, text='<Запустить терминал>', command=self.error_sound,
                                            font=('DOSFont', 18), bg='black', fg='lime',
                                            activebackground='black', activeforeground='white',
                                            relief=FLAT, borderwidth=0, highlightthickness=0)

        self.start_button.place(x=10, y=400)
        self.exit_button.place(x=360, y=400)
        self.turn_off_sounds_checkbox.place(x=20, y=300)
        self.start_terminal_button.place(x=10, y=350)
        self.main_label.place(x=50, y=20)

    def update_loading_text(self, step, total_steps=2):  # Текст загрузки
        dots = "." * ((step % 4) + 1)
        self.get_started_label.config(
            text=f'- Выполняется инициализация{dots}')

        if step < total_steps * 4:
            self.root.after(200, lambda: self.update_loading_text(
                step + 1, total_steps))
        elif step == total_steps * 4:
            self.get_started_label.config(text='- Запуск командного центра')
            self.root.after(1500, self.desktop_frame)

    def get_started(self):  # Псевдо-загрузочный экран
        self.button_sound()
        self.main_frame.destroy()

        self.get_started_frame = Frame(self.root, bg='black')
        self.get_started_frame.pack(fill='both', expand=True)

        self.get_started_process_label = Label(
            self.get_started_frame, text='ЭТАПЫ:',
            font=('DOSFont', 18), bg='black', fg='lime')
        self.get_started_process_label.place(x=20, y=20)

        self.get_started_label = Label(
            self.get_started_frame, text='- Выполняется инициализация',
            font=('DOSFont', 18), bg='black', fg='lime')
        self.get_started_label.place(x=50, y=60)

        self.update_loading_text(0)

    # БИЛДЕРЫ ОКОН

    def error_window_file_delete_builder(self):
        error_label = Label(self.desktop_frame_screen,
                            text=f"______[Ошибка]______\n|                  |\n| Невозможно удалить |\n|                  |\n|                  |\n-----------------",
                            font=('DOSFont', 18), bg='black', fg='lime')

        error_button = Button(self.desktop_frame_screen, text="■",
                              font=('DOSFont', 18), bg='black', fg='lime',
                              activebackground='black', activeforeground='white',
                              relief=FLAT, borderwidth=0, highlightthickness=0,
                              command=lambda: (error_label.destroy(), error_button.destroy()))

        error_label.place(x=140, y=120)
        error_button.place(x=380, y=123)

        error_label.lift()
        error_button.lift()

    def congrat_window_file_delete_builder(self):
        congrat_label = Label(self.desktop_frame_screen,
                            text=f"______[Успех]______\n|                  |\n|Успешно удален файл!|\n|                  |\n|                  |\n------------------",
                            font=('DOSFont', 18), bg='black', fg='lime')

        congrat_button = Button(self.desktop_frame_screen, text="■",
                                font=('DOSFont', 18), bg='black', fg='lime',
                                activebackground='black', activeforeground='white',
                                relief=FLAT, borderwidth=0, highlightthickness=0,
                                command=lambda: (congrat_label.destroy(), congrat_button.destroy()))

        congrat_label.place(x=140, y=120)
        congrat_button.place(x=380, y=123)

        # Поднимаем поверх других элементов
        congrat_label.lift()
        congrat_button.lift()

    def create_new_file(self):
        # Создаёт новый файл и сразу открывает редактор
        self.button_sound()
        self.file_counter += 1
        filename = f"Файл{self.file_counter}.txt"
        filepath = os.path.join(self.storage_path, filename)

        # Создаём пустой файл
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("")

        # Открываем редактор
        self.open_editor(filepath, filename)

    def open_file_context(self, filepath):
        # Открывает контекст редактирования существующего файла
        filename = os.path.basename(filepath)
        self.open_editor(filepath, filename)

    def open_editor(self, filepath, filename):
        # Открывает текстовый редактор для файла
        if self.editor_open:
            return
        self.editor_open = True

        self.button_sound()

        # Уничтожаем текущий фрейм
        for widget in self.root.winfo_children():
            widget.destroy()

        # Создаём редактор
        editor_frame = Frame(self.root, bg='black')
        editor_frame.pack(fill='both', expand=True)

        # Заголовок
        title_label = Label(editor_frame, text=f"Editrix. Редак.: {filename}",
                            font=('DOSFont', 18), bg='black', fg='lime')
        title_label.pack(pady=10)

        # Текстовое поле
        self.text_area = Text(editor_frame, font=('DOSFont', 18),
                              bg='black', fg='lime', insertbackground='lime',
                              relief=FLAT, wrap=WORD, height=15)
        self.text_area.pack(fill='both', expand=True, padx=20, pady=10)

        self.text_area.tag_config(
            "sel", background="white", foreground="black")

        # Читаем содержимое файла
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self.text_area.insert(END, content)
        except Exception as e:
            self.error_sound()

        # Кнопки
        button_frame = Frame(editor_frame, bg='black')
        button_frame.pack(pady=10)

        save_button = Button(button_frame, text='Сохранить', font=('DOSFont', 18),
                             bg='black', fg='lime', activebackground='black',
                             activeforeground='white', relief=FLAT, borderwidth=0,
                             command=lambda: self.save_file(filepath, editor_frame))
        save_button.pack(side=LEFT, padx=10)

        cancel_button = Button(button_frame, text='Отмена', font=('DOSFont', 18),
                               bg='black', fg='lime', activebackground='black',
                               activeforeground='white', relief=FLAT, borderwidth=0,
                               command=lambda: self.cancel_edit(editor_frame))
        cancel_button.pack(side=LEFT, padx=10)

        # Сохраняем путь к файлу
        self.current_editing_file = filepath

    def save_file(self, filepath, editor_frame):  # Сохранение файлов
        # Сохраняет содержимое редактора в файл
        try:
            content = self.text_area.get(1.0, END)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content.rstrip('\n'))  # Убираем лишний перенос
            self.button_sound()
            self.close_editor(editor_frame)
        except Exception as e:
            pass

    def clear_file_icons(self):
        # Удаляет все иконки файлов с рабочего стола
        for icon in self.file_icons:
            icon['label'].destroy()
        self.file_icons = []  # Очищаем список

    def delete_file(self):
        # Удаляет выбранный файл
        self.button_sound()

        if not hasattr(self, 'current_right_clicked_file') or not self.current_right_clicked_file:
            return

        filepath = self.current_right_clicked_file
        filename = os.path.basename(filepath)

        if filename == "README.txt":
            self.error_sound()
            self.error_window_file_delete_builder()
            return
            
        try:
            os.remove(filepath)
            # Полностью перезагружаем список файлов
            self.load_files_from_storage()
            self.congrat_window_file_delete_builder()
        except Exception as e:
            pass

    def cancel_edit(self, editor_frame):  # Отмена редактирования файлов
        self.close_editor(editor_frame)

    def close_editor(self, editor_frame):
        # Закрывает редактор и возвращается на рабочий стол
        editor_frame.destroy()
        self.button_sound()
        self.editor_open = False
        self.current_editing_file = None
        self.desktop_frame()  # Перезагружаем рабочий стол

    def popup_context_create(self, event):
        self.x = event.x
        self.y = event.y

        # Проверяем, попали ли мы по файлу
        clicked_on_file = False
        self.current_right_clicked_file = None  # Сбрасываем

        for icon in self.file_icons:
            # Простая проверка попадания по координатам
            if (icon['x'] <= event.x <= icon['x'] + 400 and  # Ширина иконки ~200 пикселей
                    icon['y'] <= event.y <= icon['y'] + 30):  # Высота ~30
                clicked_on_file = True
                self.current_right_clicked_file = icon['path']
                break

        # Создаём контекстное меню
        context_menu = Menu(tearoff=0, font=(
            'DOSFont', 18), bg='black', fg='lime', selectcolor='lime', activebackground='white', activeforeground='black')
        if clicked_on_file:
            context_menu.add_command(
                label='Удалить',
                command=self.delete_file
            )
        else:
            context_menu.add_command(
                label='Создать файл',
                command=self.create_new_file
            )

        context_menu.post(event.x_root, event.y_root)

    def update_time(self):  # Обновление времени
        if hasattr(self, 'time_label') and self.time_label and self.time_label.winfo_exists():
            current_time = datetime.now().strftime("%H:%M")
            self.time_label.config(  # Верхняя панель
                text=f"[--Comandrix--]----------------[:-{current_time}-:]")
            self.after_id = self.root.after(
                1000, self.update_time)  # Сохраняем ID
        else:
            self.after_id = None

    def parameters(self):  # Параметры системы, фрейм
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.sounds_enabled:
            try:
                mixer.music.load('snd/beep.mp3')
                mixer.music.play()
            except Exception as e:
                self.error_sound()

        # Создаём фрейм меню
        self.parameters_frame = Frame(self.root, bg='black')
        self.parameters_frame.pack(fill='both', expand=True)

        # Заголовок
        title_label = Label(self.parameters_frame, text="Параметры:",
                            font=('DOSFont', 18), bg='black', fg='lime')
        title_label.pack(pady=1)

        self.turn_off_sounds_checkbox = Checkbutton(
            self.parameters_frame, text='<Выключить системные звуки>      |',
            font=f'{'DOSFont'} 18',
            variable=self.turn_off_sounds_var,
            command=self.toggle_sounds,
            bg='black', fg='lime',
            activebackground='black',
            activeforeground='lime',
            selectcolor='black',
            relief=FLAT, borderwidth=0, highlightthickness=0)

        exit_parameters_button = Button(self.parameters_frame, text='[<]', command=self.desktop_frame,
                                        font=('DOSFont', 18), bg='black', fg='lime',
                                        activebackground='black', activeforeground='white',
                                        relief=FLAT, borderwidth=0, highlightthickness=0)

        self.turn_off_sounds_checkbox.place(x=23, y=50)
        exit_parameters_button.place(x=0, y=395)

    def start_menu(self):
        # Уничтожаем текущий фрейм
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.sounds_enabled:
            try:
                mixer.music.load('snd/start.mp3')
                mixer.music.play()
            except Exception as e:
                pass

        # Создаём фрейм меню
        self.start_menu_frame = Frame(self.root, bg='black')
        self.start_menu_frame.pack(fill='both', expand=True)

        # Заголовок
        title_label = Label(self.start_menu_frame, text=f"Выберите функцию:",
                            font=('DOSFont', 18), bg='black', fg='lime')
        title_label.pack(pady=1)

        # Кнопки
        return_button = Button(self.start_menu_frame, text='[Рабочий стол]', command=self.desktop_frame,
                               font=('DOSFont', 18), bg='black', fg='lime',
                               activebackground='black', activeforeground='white',
                               relief=FLAT, borderwidth=0, highlightthickness=0)
        terminal_button = Button(self.start_menu_frame, text='[Открыть терминал]', command=self.terminal_session,
                                 font=('DOSFont', 18), bg='black', fg='lime',
                                 activebackground='black', activeforeground='white',
                                 relief=FLAT, borderwidth=0, highlightthickness=0)
        parameters_button = Button(self.start_menu_frame, text='[Параметры]', command=self.parameters,
                                   font=('DOSFont', 18), bg='black', fg='lime',
                                   activebackground='black', activeforeground='white',
                                   relief=FLAT, borderwidth=0, highlightthickness=0)
        exit_button = Button(self.start_menu_frame, text='[Завершить сеанс]', command=self.exit,
                             font=('DOSFont', 18), bg='black', fg='lime',
                             activebackground='black', activeforeground='white',
                             relief=FLAT, borderwidth=0, highlightthickness=0)

        return_button.place(x=200, y=60)
        terminal_button.place(x=180, y=150)
        parameters_button.place(x=213, y=230)
        exit_button.place(x=180, y=310)

    def terminal_session(self):
        # Очищаем предыдущие виджеты
        for widget in self.root.winfo_children():
            widget.destroy()

        # Создаём фрейм терминала
        self.terminal_frame = Frame(self.root, bg='black')
        self.terminal_frame.pack(fill='both', expand=True)

        # Область вывода (read-only)
        self.output_area = scrolledtext.ScrolledText(
            self.terminal_frame,
            bg='black',
            fg='green',
            insertbackground='green',
            font=('DOSFont', 12),
            state='disabled',  # Блокируем прямое редактирование
            relief=FLAT,
            wrap=WORD
        )
        self.output_area.pack(expand=True, fill='both', padx=5, pady=5)

        # Поле ввода (снизу)
        input_frame = Frame(self.terminal_frame, bg='black')
        input_frame.pack(fill='x', padx=5, pady=5)

        # Приглашение для ввода (">>> ")
        self.prompt_label = Label(
            input_frame,
            text=">>> ",
            bg='black',
            fg='green',
            font=('DOSFont', 12)
        )
        self.prompt_label.pack(side='left')

        # Само поле ввода
        self.input_entry = Entry(
            input_frame,
            bg='black',
            fg='green',
            insertbackground='green',
            font=('DOSFont', 12),
            relief=FLAT
        )
        self.input_entry.pack(side='left', fill='x', expand=True)
        # Enter = выполнить команду
        self.input_entry.bind('<Return>', self.process_command)
        self.input_entry.focus_set()  # Фокус на поле ввода

        # Выводим приветственное сообщение
        self.print_output(
            "Comandrix Terminal v1.0\nВведите 'help' для списка команд\n")

    def print_output(self, text):
        # Выводит текст в терминал
        self.output_area.configure(state='normal')  # Временно разблокируем
        self.output_area.insert('end', text)
        self.output_area.configure(state='disabled')  # Снова блокируем
        self.output_area.see('end')  # Автопрокрутка вниз

    def process_command(self, event):
        # Обрабатывает команду из терминала
        command = self.input_entry.get().strip()  # Получаем команду
        self.input_entry.delete(0, 'end')  # Очищаем поле ввода

        if not command:  # Если команда пустая, выводим ничего
            return

        # Выводим введенную команду
        self.print_output(f">>> {command}\n")

        # Обработка команд
        if command.lower() in ('quit'):
            self.desktop_frame()  # Возвращаемся на рабочий стол
        elif command.lower() == 'help':
            self.print_output(
                "Доступные команды:\n  help - справка\n  quit - завершить сессию терминала\n  cls - очистить терминал\n  create <имя> - создать файл\n  del <имя> - удалить файл\n")
        elif command.lower() == 'cls':
            self.output_area.configure(state='normal')
            self.output_area.delete(1.0, 'end')  # Очищаем терминал
            self.output_area.configure(state='disabled')
        elif command.lower().startswith('create '):
            self.create_file_from_terminal(command[7:])
        elif command.lower().startswith('del '):
            self.delete_file_from_terminal(command[4:])
        else:
            self.print_output(f"Ошибка: команда '{command}' не найдена.\n")

        # Добавляем новое приглашение
        self.print_output(">>> ")

    def create_file_from_terminal(self, filename):
        # Создает файл через терминал
        if not filename:
            self.print_output("Ошибка: укажите имя файла\n")
            return

        # Добавляем расширение .txt, если его нет
        if not filename.lower().endswith('.txt'):
            filename += '.txt'

        filepath = os.path.join(self.storage_path, filename)

        try:
            # Проверяем, существует ли файл
            if os.path.exists(filepath):
                self.print_output(
                    f"Ошибка: файл '{filename}' уже существует\n")
                return

            # Создаем файл
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("")

            self.print_output(f"Файл '{filename}' успешно создан\n")

            # Обновляем список файлов на рабочем столе
            if hasattr(self, 'desktop_frame_screen'):
                self.load_files_from_storage()

        except Exception as e:
            pass

    def delete_file_from_terminal(self, filename):
        # Удаляет файл через терминал
        if not filename:
            self.print_output("Ошибка: укажите имя файла\n")
            return

        # Добавляем расширение .txt, если его нет
        if not filename.lower().endswith('.txt'):
            filename += '.txt'

        filepath = os.path.join(self.storage_path, filename)

        try:
            # Проверяем, существует ли файл
            if not os.path.exists(filepath):
                self.print_output(f"Ошибка: файл '{filename}' не найден\n")
                return
            # elif filename == "README.txt": # Для безопасности
            #     self.print_output(f"Недопустимое название элемента, удаление невозможно\n")
            #     return
            elif filename == "main.pyw":
                self.print_output(
                    f"Этот элемент является частью системы, удаление невозможно\n")
                return
            # elif filename == "DOSFont.ttf":
            #     self.print_output(f"Этот элемент является сопутствующим элементом системы, удаление невозможно\n")
            #     return
            # elif filename == "README.md":
            #     self.print_output(f"Этот элемент является сопутствующим элементом системы, удаление невозможно\n")
            #     return

            # Удаляем файл
            os.remove(filepath)
            self.print_output(f"Файл '{filename}' успешно удален\n")

            # Обновляем список файлов на рабочем столе
            if hasattr(self, 'desktop_frame_screen'):
                self.load_files_from_storage()

        except Exception as e:
            pass

    def desktop_frame(self):
        # Создаёт рабочий стол и загружает файлы
        self.ensure_storage()

        if self.sounds_enabled:
            try:
                mixer.music.load('snd/start.mp3')
                mixer.music.play()
            except Exception as e:
                pass

        # Отменяем предыдущий after-вызов, чтобы не было конфликта
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        # Уничтожаем предыдущие виджеты
        for widget in self.root.winfo_children():
            widget.destroy()

        self.desktop_frame_screen = Frame(self.root, bg='black')
        self.desktop_frame_screen.pack(fill='both', expand=True)

        # Привязываем контекстное меню
        self.desktop_frame_screen.bind('<Button-3>', self.popup_context_create)

        # Загружаем файлы
        self.load_files_from_storage()

        # Панель времени
        current_time = datetime.now().strftime("%H:%M")
        self.time_label = Label(
            self.desktop_frame_screen,
            text=f"[--Comandrix--]----------------[:-{current_time}-:]",
            font=('DOSFont', 18), bg='black', fg='lime')
        self.time_label.pack(pady=1)

        # Запускаем обновление времени
        self.after_id = self.root.after(1000, self.update_time)  # Сохраняем ID

        # Кнопка пуск
        self.start_button = Button(
            self.desktop_frame_screen,
            text="----\n|(S)|\n----",
            font=('DOSFont', 18), bg='black', fg='lime',
            activebackground='black', activeforeground='lime',
            relief=FLAT, borderwidth=0, highlightthickness=0, command=self.start_menu)
        self.start_button.place(x=0, y=395)

    def exit(self):
        sys.exit()

    def show_help(self):
        messagebox.showinfo(
            title='О программе',
            message='Система командной строки для узкоспециализируемых работ, с текстовым интерфейсом\n\nПКС - Персональная командная строка\nРазработчик: Роман Чомахидзе')


if __name__ == "__main__":
    mixer.init()
    root = Tk()
    app = App(root)
    app.check_dos_font()
    app.create_menu()
    app.set_up_frame()
    app.start_sound()
    app.set_up_elements()
    root.mainloop()
