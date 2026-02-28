import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QTextEdit, QToolBar, QMenu, QFileDialog, QMessageBox, 
                             QSplitter, QStatusBar, QLabel, QDialog, QVBoxLayout,
                             QTreeWidget, QTreeWidgetItem, QTextBrowser)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QKeySequence, QTextCursor, QFont, QIcon, QPixmap, QPainter, QColor


class CodeEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()
        
    def setup_editor(self):
        font = QFont("Courier New", 11)
        font.setFixedPitch(True)
        self.setFont(font)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.setPlaceholderText("Введите текст программы...")
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Tab:
            self.insertPlainText("    ")
        else:
            super().keyPressEvent(event)
            
    def get_current_line(self):
        cursor = self.textCursor()
        return cursor.blockNumber() + 1
        
    def get_current_column(self):
        cursor = self.textCursor()
        return cursor.columnNumber() + 1
        
    def set_error_position(self, line, column):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        
        for _ in range(line - 1):
            cursor.movePosition(QTextCursor.MoveOperation.Down)
            
        for _ in range(column - 1):
            cursor.movePosition(QTextCursor.MoveOperation.Right)
            
        self.setTextCursor(cursor)
        self.ensureCursorVisible()


def create_icon(char):
    pixmap = QPixmap(24, 24)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setPen(QColor("#FFFFFF"))
    painter.setFont(QFont("Segoe UI", 14))
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, char)
    painter.end()
    return QIcon(pixmap)


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Справка - Руководство пользователя")
        self.setGeometry(300, 300, 700, 600)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Разделы справки")
        self.tree.setMaximumWidth(250)
        
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.text_browser)
        splitter.setSizes([250, 450])
        
        layout.addWidget(splitter)
        
        self.populate_tree()
        self.tree.itemClicked.connect(self.show_help_content)
        
    def populate_tree(self):
        file_item = QTreeWidgetItem(["Меню Файл"])
        file_item.addChild(QTreeWidgetItem(["Создать (Ctrl+N)"]))
        file_item.addChild(QTreeWidgetItem(["Открыть (Ctrl+O)"]))
        file_item.addChild(QTreeWidgetItem(["Сохранить (Ctrl+S)"]))
        file_item.addChild(QTreeWidgetItem(["Сохранить как (Ctrl+Shift+S)"]))
        file_item.addChild(QTreeWidgetItem(["Выход (Ctrl+Q)"]))
        self.tree.addTopLevelItem(file_item)
        
        edit_item = QTreeWidgetItem(["Меню Правка"])
        edit_item.addChild(QTreeWidgetItem(["Отмена (Ctrl+Z)"]))
        edit_item.addChild(QTreeWidgetItem(["Повтор (Ctrl+Y)"]))
        edit_item.addChild(QTreeWidgetItem(["Вырезать (Ctrl+X)"]))
        edit_item.addChild(QTreeWidgetItem(["Копировать (Ctrl+C)"]))
        edit_item.addChild(QTreeWidgetItem(["Вставить (Ctrl+V)"]))
        edit_item.addChild(QTreeWidgetItem(["Удалить (Del)"]))
        edit_item.addChild(QTreeWidgetItem(["Выделить все (Ctrl+A)"]))
        self.tree.addTopLevelItem(edit_item)
        
        text_item = QTreeWidgetItem(["Меню Текст"])
        text_item.addChild(QTreeWidgetItem(["Постановка задачи"]))
        text_item.addChild(QTreeWidgetItem(["Грамматика"]))
        text_item.addChild(QTreeWidgetItem(["Классификация грамматики"]))
        text_item.addChild(QTreeWidgetItem(["Метод анализа"]))
        text_item.addChild(QTreeWidgetItem(["Тестовый пример"]))
        text_item.addChild(QTreeWidgetItem(["Список литературы"]))
        text_item.addChild(QTreeWidgetItem(["Исходный код программы"]))
        self.tree.addTopLevelItem(text_item)
        
        run_item = QTreeWidgetItem(["Меню Пуск"])
        run_item.addChild(QTreeWidgetItem(["Запустить анализатор (F5)"]))
        self.tree.addTopLevelItem(run_item)
        
        help_item = QTreeWidgetItem(["Меню Справка"])
        help_item.addChild(QTreeWidgetItem(["Вызов справки (F1)"]))
        help_item.addChild(QTreeWidgetItem(["О программе"]))
        self.tree.addTopLevelItem(help_item)
        
        toolbar_item = QTreeWidgetItem(["Панель инструментов"])
        toolbar_item.addChild(QTreeWidgetItem(["Новый"]))
        toolbar_item.addChild(QTreeWidgetItem(["Открыть"]))
        toolbar_item.addChild(QTreeWidgetItem(["Сохранить"]))
        toolbar_item.addChild(QTreeWidgetItem(["Отмена"]))
        toolbar_item.addChild(QTreeWidgetItem(["Повтор"]))
        toolbar_item.addChild(QTreeWidgetItem(["Копировать"]))
        toolbar_item.addChild(QTreeWidgetItem(["Вырезать"]))
        toolbar_item.addChild(QTreeWidgetItem(["Вставить"]))
        toolbar_item.addChild(QTreeWidgetItem(["Пуск"]))
        toolbar_item.addChild(QTreeWidgetItem(["Справка"]))
        toolbar_item.addChild(QTreeWidgetItem(["О программе"]))
        self.tree.addTopLevelItem(toolbar_item)
        
        self.tree.expandAll()
        
    def show_help_content(self, item, column):
        text = item.text(column)
        
        help_contents = {
            "Меню Файл": """
                <h2>Меню Файл</h2>
                <p>Содержит команды для работы с файлами.</p>
            """,
            "Создать (Ctrl+N)": """
                <h3>Создать (Ctrl+N)</h3>
                <p><b>Назначение:</b> Создание нового пустого файла.</p>
                <p><b>Где находится:</b> Меню "Файл" → "Создать"</p>
                <p><b>Горячая клавиша:</b> Ctrl+N</p>
                <p><b>Описание:</b> Очищает область редактирования и сбрасывает имя текущего файла. 
                Если текущий файл содержит несохраненные изменения, программа предложит сохранить их.</p>
            """,
            "Открыть (Ctrl+O)": """
                <h3>Открыть (Ctrl+O)</h3>
                <p><b>Назначение:</b> Открытие существующего файла.</p>
                <p><b>Где находится:</b> Меню "Файл" → "Открыть"</p>
                <p><b>Горячая клавиша:</b> Ctrl+O</p>
                <p><b>Описание:</b> Открывает диалог выбора файла. Поддерживаются текстовые файлы (*.txt) и все файлы (*.*).
                После открытия файла его содержимое отображается в области редактирования.</p>
            """,
            "Сохранить (Ctrl+S)": """
                <h3>Сохранить (Ctrl+S)</h3>
                <p><b>Назначение:</b> Сохранение текущего файла.</p>
                <p><b>Где находится:</b> Меню "Файл" → "Сохранить"</p>
                <p><b>Горячая клавиша:</b> Ctrl+S</p>
                <p><b>Описание:</b> Сохраняет изменения в текущем файле. Если файл еще не был сохранен,
                открывается диалог "Сохранить как" для выбора имени и расположения файла.</p>
            """,
            "Сохранить как (Ctrl+Shift+S)": """
                <h3>Сохранить как (Ctrl+Shift+S)</h3>
                <p><b>Назначение:</b> Сохранение файла под новым именем.</p>
                <p><b>Где находится:</b> Меню "Файл" → "Сохранить как"</p>
                <p><b>Горячая клавиша:</b> Ctrl+Shift+S</p>
                <p><b>Описание:</b> Открывает диалог для сохранения файла с новым именем и расположением.
                После сохранения новый файл становится текущим.</p>
            """,
            "Выход (Ctrl+Q)": """
                <h3>Выход (Ctrl+Q)</h3>
                <p><b>Назначение:</b> Завершение работы программы.</p>
                <p><b>Где находится:</b> Меню "Файл" → "Выход"</p>
                <p><b>Горячая клавиша:</b> Ctrl+Q</p>
                <p><b>Описание:</b> Закрывает приложение. При наличии несохраненных изменений
                программа предложит сохранить их перед выходом.</p>
            """,
            "Меню Правка": """
                <h2>Меню Правка</h2>
                <p>Содержит команды для редактирования текста.</p>
            """,
            "Отмена (Ctrl+Z)": """
                <h3>Отмена (Ctrl+Z)</h3>
                <p><b>Назначение:</b> Отмена последнего действия.</p>
                <p><b>Где находится:</b> Меню "Правка" → "Отмена"</p>
                <p><b>Горячая клавиша:</b> Ctrl+Z</p>
                <p><b>Описание:</b> Отменяет последнее изменение в тексте. Можно отменить несколько действий последовательно.</p>
            """,
            "Повтор (Ctrl+Y)": """
                <h3>Повтор (Ctrl+Y)</h3>
                <p><b>Назначение:</b> Повтор отмененного действия.</p>
                <p><b>Где находится:</b> Меню "Правка" → "Повтор"</p>
                <p><b>Горячая клавиша:</b> Ctrl+Y</p>
                <p><b>Описание:</b> Возвращает отмененное действие. Работает только после использования команды "Отмена".</p>
            """,
            "Вырезать (Ctrl+X)": """
                <h3>Вырезать (Ctrl+X)</h3>
                <p><b>Назначение:</b> Вырезание выделенного текста.</p>
                <p><b>Где находится:</b> Меню "Правка" → "Вырезать"</p>
                <p><b>Горячая клавиша:</b> Ctrl+X</p>
                <p><b>Описание:</b> Удаляет выделенный текст и помещает его в буфер обмена.</p>
            """,
            "Копировать (Ctrl+C)": """
                <h3>Копировать (Ctrl+C)</h3>
                <p><b>Назначение:</b> Копирование выделенного текста.</p>
                <p><b>Где находится:</b> Меню "Правка" → "Копировать"</p>
                <p><b>Горячая клавиша:</b> Ctrl+C</p>
                <p><b>Описание:</b> Копирует выделенный текст в буфер обмена без удаления.</p>
            """,
            "Вставить (Ctrl+V)": """
                <h3>Вставить (Ctrl+V)</h3>
                <p><b>Назначение:</b> Вставка текста из буфера обмена.</p>
                <p><b>Где находится:</b> Меню "Правка" → "Вставить"</p>
                <p><b>Горячая клавиша:</b> Ctrl+V</p>
                <p><b>Описание:</b> Вставляет текст из буфера обмена в позицию курсора.</p>
            """,
            "Удалить (Del)": """
                <h3>Удалить (Del)</h3>
                <p><b>Назначение:</b> Удаление выделенного текста.</p>
                <p><b>Где находится:</b> Меню "Правка" → "Удалить"</p>
                <p><b>Горячая клавиша:</b> Del</p>
                <p><b>Описание:</b> Удаляет выделенный текст без помещения в буфер обмена.</p>
            """,
            "Выделить все (Ctrl+A)": """
                <h3>Выделить все (Ctrl+A)</h3>
                <p><b>Назначение:</b> Выделение всего текста.</p>
                <p><b>Где находится:</b> Меню "Правка" → "Выделить все"</p>
                <p><b>Горячая клавиша:</b> Ctrl+A</p>
                <p><b>Описание:</b> Выделяет весь текст в области редактирования.</p>
            """,
            "Меню Текст": """
                <h2>Меню Текст</h2>
                <p>Содержит информацию о языковом процессоре.</p>
                <p><i>Все функции этого меню будут реализованы в следующих лабораторных работах.</i></p>
            """,
            "Постановка задачи": """
                <h3>Постановка задачи</h3>
                <p><b>Назначение:</b> Отображение постановки задачи лабораторной работы.</p>
                <p><b>Где находится:</b> Меню "Текст" → "Постановка задачи"</p>
                <p><b>Описание:</b> Функция будет реализована позже.</p>
            """,
            "Грамматика": """
                <h3>Грамматика</h3>
                <p><b>Назначение:</b> Отображение грамматики языка.</p>
                <p><b>Где находится:</b> Меню "Текст" → "Грамматика"</p>
                <p><b>Описание:</b> Функция будет реализована позже.</p>
            """,
            "Классификация грамматики": """
                <h3>Классификация грамматики</h3>
                <p><b>Назначение:</b> Отображение классификации грамматики по Хомскому.</p>
                <p><b>Где находится:</b> Меню "Текст" → "Классификация грамматики"</p>
                <p><b>Описание:</b> Функция будет реализована позже.</p>
            """,
            "Метод анализа": """
                <h3>Метод анализа</h3>
                <p><b>Назначение:</b> Отображение метода синтаксического анализа.</p>
                <p><b>Где находится:</b> Меню "Текст" → "Метод анализа"</p>
                <p><b>Описание:</b> Функция будет реализована позже.</p>
            """,
            "Тестовый пример": """
                <h3>Тестовый пример</h3>
                <p><b>Назначение:</b> Отображение тестового примера работы анализатора.</p>
                <p><b>Где находится:</b> Меню "Текст" → "Тестовый пример"</p>
                <p><b>Описание:</b> Функция будет реализована позже.</p>
            """,
            "Список литературы": """
                <h3>Список литературы</h3>
                <p><b>Назначение:</b> Отображение списка использованной литературы.</p>
                <p><b>Где находится:</b> Меню "Текст" → "Список литературы"</p>
                <p><b>Описание:</b> Функция будет реализована позже.</p>
            """,
            "Исходный код программы": """
                <h3>Исходный код программы</h3>
                <p><b>Назначение:</b> Отображение исходного кода приложения.</p>
                <p><b>Где находится:</b> Меню "Текст" → "Исходный код программы"</p>
                <p><b>Описание:</b> Функция будет реализована позже.</p>
            """,
            "Меню Пуск": """
                <h2>Меню Пуск</h2>
                <p>Содержит команду для запуска анализатора.</p>
            """,
            "Запустить анализатор (F5)": """
                <h3>Запустить анализатор (F5)</h3>
                <p><b>Назначение:</b> Запуск синтаксического анализатора.</p>
                <p><b>Где находится:</b> Меню "Пуск" → "Запустить анализатор"</p>
                <p><b>Горячая клавиша:</b> F5</p>
                <p><b>Описание:</b> Запускает анализ текста в области редактирования.
                Результаты отображаются в области вывода. Функция будет полностью реализована позже.</p>
            """,
            "Меню Справка": """
                <h2>Меню Справка</h2>
                <p>Содержит команды для получения помощи и информации о программе.</p>
            """,
            "Вызов справки (F1)": """
                <h3>Вызов справки (F1)</h3>
                <p><b>Назначение:</b> Открытие руководства пользователя.</p>
                <p><b>Где находится:</b> Меню "Справка" → "Вызов справки"</p>
                <p><b>Горячая клавиша:</b> F1</p>
                <p><b>Описание:</b> Открывает окно справки с подробным описанием всех функций программы.</p>
            """,
            "О программе": """
                <h3>О программе</h3>
                <p><b>Назначение:</b> Отображение информации о программе.</p>
                <p><b>Где находится:</b> Меню "Справка" → "О программе"</p>
                <p><b>Описание:</b> Показывает окно с информацией о версии программы, авторе и используемых технологиях.</p>
            """,
            "Панель инструментов": """
                <h2>Панель инструментов</h2>
                <p>Содержит кнопки для быстрого доступа к основным функциям программы.</p>
                <p>При наведении на кнопку отображается всплывающая подсказка с описанием.</p>
            """,
            "Новый": """
                <h3>Новый</h3>
                <p><b>Назначение:</b> Создание нового файла.</p>
                <p><b>Где находится:</b> Панель инструментов → кнопка "Новый"</p>
                <p><b>Горячая клавиша:</b> Ctrl+N</p>
                <p><b>Описание:</b> Создает новый пустой файл. При наличии несохраненных изменений предлагает их сохранить.</p>
            """,
            "Открыть": """
                <h3>Открыть</h3>
                <p><b>Назначение:</b> Открытие существующего файла.</p>
                <p><b>Где находится:</b> Панель инструментов → кнопка "Открыть"</p>
                <p><b>Горячая клавиша:</b> Ctrl+O</p>
                <p><b>Описание:</b> Открывает диалог выбора файла для загрузки.</p>
            """,
            "Сохранить": """
                <h3>Сохранить</h3>
                <p><b>Назначение:</b> Сохранение текущего файла.</p>
                <p><b>Где находится:</b> Панель инструментов → кнопка "Сохранить"</p>
                <p><b>Горячая клавиша:</b> Ctrl+S</p>
                <p><b>Описание:</b> Сохраняет изменения в текущем файле.</p>
            """,
            "Отмена": """
                <h3>Отмена</h3>
                <p><b>Назначение:</b> Отмена последнего действия.</p>
                <p><b>Где находится:</b> Панель инструментов → кнопка "Отмена"</p>
                <p><b>Горячая клавиша:</b> Ctrl+Z</p>
                <p><b>Описание:</b> Отменяет последнее изменение в тексте.</p>
            """,
            "Повтор": """
                <h3>Повтор</h3>
                <p><b>Назначение:</b> Повтор отмененного действия.</p>
                <p><b>Где находится:</b> Панель инструментов → кнопка "Повтор"</p>
                <p><b>Горячая клавиша:</b> Ctrl+Y</p>
                <p><b>Описание:</b> Возвращает отмененное действие.</p>
            """,
            "Копировать": """
                <h3>Копировать</h3>
                <p><b>Назначение:</b> Копирование выделенного текста.</p>
                <p><b>Где находится:</b> Панель инструментов → кнопка "Копировать"</p>
                <p><b>Горячая клавиша:</b> Ctrl+C</p>
                <p><b>Описание:</b> Копирует выделенный текст в буфер обмена.</p>
            """,
            "Вырезать": """
                <h3>Вырезать</h3>
                <p><b>Назначение:</b> Вырезание выделенного текста.</p>
                <p><b>Где находится:</b> Панель инструментов → кнопка "Вырезать"</p>
                <p><b>Горячая клавиша:</b> Ctrl+X</p>
                <p><b>Описание:</b> Вырезает выделенный текст в буфер обмена.</p>
            """,
            "Вставить": """
                <h3>Вставить</h3>
                <p><b>Назначение:</b> Вставка текста из буфера обмена.</p>
                <p><b>Где находится:</b> Панель инструментов → кнопка "Вставить"</p>
                <p><b>Горячая клавиша:</b> Ctrl+V</p>
                <p><b>Описание:</b> Вставляет текст из буфера обмена.</p>
            """,
            "Пуск": """
                <h3>Пуск</h3>
                <p><b>Назначение:</b> Запуск анализатора.</p>
                <p><b>Где находится:</b> Панель инструментов → кнопка "Пуск"</p>
                <p><b>Горячая клавиша:</b> F5</p>
                <p><b>Описание:</b> Запускает синтаксический анализатор.</p>
            """,
            "Справка": """
                <h3>Справка</h3>
                <p><b>Назначение:</b> Вызов справки.</p>
                <p><b>Где находится:</b> Панель инструментов → кнопка "Справка"</p>
                <p><b>Горячая клавиша:</b> F1</p>
                <p><b>Описание:</b> Открывает окно справки.</p>
            """,
            "О программе": """
                <h3>О программе</h3>
                <p><b>Назначение:</b> Информация о программе.</p>
                <p><b>Где находится:</b> Панель инструментов → кнопка "О программе"</p>
                <p><b>Описание:</b> Показывает информацию о программе.</p>
            """
        }
        
        if text in help_contents:
            self.text_browser.setHtml(help_contents[text])
        else:
            parent = item.parent()
            if parent:
                parent_text = parent.text(0)
                if parent_text in help_contents:
                    self.text_browser.setHtml(help_contents[parent_text])


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.text_changed = False
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Compiler")
        self.setGeometry(200, 200, 1000, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.create_editor_and_output()
        self.create_menu_bar()
        self.create_toolbar()
        
        layout.addWidget(self.splitter)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("Готов к работе")
        self.status_bar.addWidget(self.status_label)
        
        self.editor.textChanged.connect(self.update_status)
        self.editor.textChanged.connect(self.on_text_changed)
        
        self.apply_styles()
        
    def apply_styles(self):
        self.setStyleSheet("""
            QToolBar {
                background-color: #2c3e50;
                border: none;
                padding: 4px;
            }
            QToolBar QToolButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 4px;
                margin: 1px;
                font-size: 11px;
            }
            QToolBar QToolButton:hover {
                background-color: #34495e;
                border-radius: 3px;
            }
            QToolBar QToolButton:pressed {
                background-color: #3d566e;
            }
            QMenuBar {
                background-color: #ecf0f1;
                color: #2c3e50;
            }
            QMenuBar::item:selected {
                background-color: #bdc3c7;
            }
            QStatusBar {
                background-color: #ecf0f1;
                color: #2c3e50;
            }
            QTextEdit {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
            }
        """)
        
    def create_editor_and_output(self):
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        
        self.editor = CodeEditor()
        self.splitter.addWidget(self.editor)
        
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setPlaceholderText("Результаты работы языкового процессора...")
        self.splitter.addWidget(self.output_area)
        
        self.splitter.setSizes([500, 200])
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("Файл")
        
        new_action = QAction("Создать", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("Открыть", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("Сохранить", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Сохранить как", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Выход", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        edit_menu = menubar.addMenu("Правка")
        
        undo_action = QAction("Отмена", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Повтор", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("Вырезать", self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self.editor.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("Копировать", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.editor.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Вставить", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)
        
        delete_action = QAction("Удалить", self)
        delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        delete_action.triggered.connect(self.delete_text)
        edit_menu.addAction(delete_action)
        
        edit_menu.addSeparator()
        
        select_all_action = QAction("Выделить все", self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_all_action)
        
        text_menu = menubar.addMenu("Текст")
        
        task_action = QAction("Постановка задачи", self)
        task_action.triggered.connect(self.show_message)
        text_menu.addAction(task_action)
        
        grammar_action = QAction("Грамматика", self)
        grammar_action.triggered.connect(self.show_message)
        text_menu.addAction(grammar_action)
        
        classification_action = QAction("Классификация грамматики", self)
        classification_action.triggered.connect(self.show_message)
        text_menu.addAction(classification_action)
        
        method_action = QAction("Метод анализа", self)
        method_action.triggered.connect(self.show_message)
        text_menu.addAction(method_action)
        
        example_action = QAction("Тестовый пример", self)
        example_action.triggered.connect(self.show_message)
        text_menu.addAction(example_action)
        
        references_action = QAction("Список литературы", self)
        references_action.triggered.connect(self.show_message)
        text_menu.addAction(references_action)
        
        source_action = QAction("Исходный код программы", self)
        source_action.triggered.connect(self.show_message)
        text_menu.addAction(source_action)
        
        run_menu = menubar.addMenu("Пуск")
        run_action = QAction("Запустить анализатор", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(self.run_analyzer)
        run_menu.addAction(run_action)
        
        help_menu = menubar.addMenu("Справка")
        
        help_action = QAction("Вызов справки", self)
        help_action.setShortcut(QKeySequence.StandardKey.HelpContents)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        toolbar = QToolBar("Панель инструментов")
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.addToolBar(toolbar)
        
        new_action = QAction("Новый", self)
        new_icon = QIcon.fromTheme("document-new")
        if new_icon.isNull():
            new_icon = create_icon("📄")
        new_action.setIcon(new_icon)
        new_action.setToolTip("Создать новый файл (Ctrl+N)")
        new_action.triggered.connect(self.new_file)
        toolbar.addAction(new_action)
        
        open_action = QAction("Открыть", self)
        open_icon = QIcon.fromTheme("document-open")
        if open_icon.isNull():
            open_icon = create_icon("📂")
        open_action.setIcon(open_icon)
        open_action.setToolTip("Открыть существующий файл (Ctrl+O)")
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        save_action = QAction("Сохранить", self)
        save_icon = QIcon.fromTheme("document-save")
        if save_icon.isNull():
            save_icon = create_icon("💾")
        save_action.setIcon(save_icon)
        save_action.setToolTip("Сохранить текущий файл (Ctrl+S)")
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        undo_action = QAction("Отмена", self)
        undo_icon = QIcon.fromTheme("edit-undo")
        if undo_icon.isNull():
            undo_icon = create_icon("↩")
        undo_action.setIcon(undo_icon)
        undo_action.setToolTip("Отменить последнее действие (Ctrl+Z)")
        undo_action.triggered.connect(self.editor.undo)
        toolbar.addAction(undo_action)
        
        redo_action = QAction("Повтор", self)
        redo_icon = QIcon.fromTheme("edit-redo")
        if redo_icon.isNull():
            redo_icon = create_icon("↪")
        redo_action.setIcon(redo_icon)
        redo_action.setToolTip("Повторить отмененное действие (Ctrl+Y)")
        redo_action.triggered.connect(self.editor.redo)
        toolbar.addAction(redo_action)
        
        toolbar.addSeparator()
        
        copy_action = QAction("Копировать", self)
        copy_icon = QIcon.fromTheme("edit-copy")
        if copy_icon.isNull():
            copy_icon = create_icon("📋")
        copy_action.setIcon(copy_icon)
        copy_action.setToolTip("Копировать выделенный текст (Ctrl+C)")
        copy_action.triggered.connect(self.editor.copy)
        toolbar.addAction(copy_action)
        
        cut_action = QAction("Вырезать", self)
        cut_icon = QIcon.fromTheme("edit-cut")
        if cut_icon.isNull():
            cut_icon = create_icon("✂")
        cut_action.setIcon(cut_icon)
        cut_action.setToolTip("Вырезать выделенный текст (Ctrl+X)")
        cut_action.triggered.connect(self.editor.cut)
        toolbar.addAction(cut_action)
        
        paste_action = QAction("Вставить", self)
        paste_icon = QIcon.fromTheme("edit-paste")
        if paste_icon.isNull():
            paste_icon = create_icon("📌")
        paste_action.setIcon(paste_icon)
        paste_action.setToolTip("Вставить текст из буфера обмена (Ctrl+V)")
        paste_action.triggered.connect(self.editor.paste)
        toolbar.addAction(paste_action)
        
        toolbar.addSeparator()
        
        run_action = QAction("Пуск", self)
        run_icon = QIcon.fromTheme("media-playback-start")
        if run_icon.isNull():
            run_icon = create_icon("▶")
        run_action.setIcon(run_icon)
        run_action.setToolTip("Запустить анализатор (F5)")
        run_action.triggered.connect(self.run_analyzer)
        toolbar.addAction(run_action)
        
        toolbar.addSeparator()
        
        help_action = QAction("Справка", self)
        help_icon = QIcon.fromTheme("help-contents")
        if help_icon.isNull():
            help_icon = create_icon("?")
        help_action.setIcon(help_icon)
        help_action.setToolTip("Вызов справки (F1)")
        help_action.triggered.connect(self.show_help)
        toolbar.addAction(help_action)
        
        about_action = QAction("О программе", self)
        about_icon = QIcon.fromTheme("help-about")
        if about_icon.isNull():
            about_icon = create_icon("i")
        about_action.setIcon(about_icon)
        about_action.setToolTip("Информация о программе")
        about_action.triggered.connect(self.show_about)
        toolbar.addAction(about_action)
            
    def new_file(self):
        if self.maybe_save():
            self.editor.clear()
            self.current_file = None
            self.text_changed = False
            self.setWindowTitle("Compiler - Новый файл")
            self.status_label.setText("Создан новый файл")
            
    def open_file(self):
        if self.maybe_save():
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Открыть файл", "", 
                "Текстовые файлы (*.txt);;Все файлы (*.*)"
            )
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        self.editor.setPlainText(file.read())
                    self.current_file = file_path
                    self.text_changed = False
                    self.setWindowTitle(f"Compiler - {os.path.basename(file_path)}")
                    self.status_label.setText(f"Открыт файл: {file_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл: {str(e)}")
                    
    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(self.editor.toPlainText())
                self.text_changed = False
                self.status_label.setText(f"Файл сохранен: {os.path.basename(self.current_file)}")
                return True
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")
                return False
        else:
            return self.save_file_as()
            
    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл как", "", 
            "Текстовые файлы (*.txt);;Все файлы (*.*)"
        )
        if file_path:
            self.current_file = file_path
            return self.save_file()
        return False
        
    def maybe_save(self):
        if self.text_changed:
            reply = QMessageBox.question(
                self, "Сохранение", 
                "Файл был изменен. Сохранить изменения?",
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                return self.save_file()
            elif reply == QMessageBox.StandardButton.Cancel:
                return False
        return True
        
    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()
            
    def on_text_changed(self):
        self.text_changed = True
        
    def update_status(self):
        cursor = self.editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        chars = len(self.editor.toPlainText())
        self.status_label.setText(f"Строка: {line}, Колонка: {col} | Символов: {chars}")
        
    def delete_text(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            cursor.removeSelectedText()
            
    def run_analyzer(self):
        self.output_area.append("Запуск синтаксического анализатора...")
        self.output_area.append("Эта функция будет реализована в следующей лабораторной работе.")
        
    def show_message(self):
        sender = self.sender()
        if sender:
            QMessageBox.information(self, sender.text(), 
                                   f"Функция '{sender.text()}' будет реализована позже.")
        
    def show_help(self):
        help_dialog = HelpDialog(self)
        help_dialog.exec()
        
    def show_about(self):
        about_text = """
        <h2>Compiler</h2>
        <p><b>Версия:</b> 1.0</p>
        <p><b>Автор:</b> Марков Д.Д.</p>
        <p><b>Описание:</b> Текстовый редактор с графическим интерфейсом,
        разработанный в рамках лабораторной работы.</p>
        <p><b>Технологии:</b> Python 3.x, PyQt6</p>
        <p><b>Год:</b> 2026</p>
        """
        
        QMessageBox.about(self, "О программе", about_text)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Compiler")
    app.setApplicationDisplayName("Compiler")
    app.setOrganizationName("Student")
    
    window = TextEditor()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()