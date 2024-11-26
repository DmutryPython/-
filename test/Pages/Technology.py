from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
                             QStackedWidget, QTableWidget, QTableWidgetItem)
from PyQt6.QtGui import QIntValidator
import csv

class TechnologyPage(QWidget):
    def __init__(self, navigate_to_lumber_input, navigate_back):
        super().__init__()
        layout = QVBoxLayout()

        # Заголовок страницы
        label_description = QLabel("Служба технолога")

        # Кнопка навигации
        button_second_page = QPushButton("Добавить древесину")
        button_second_page.clicked.connect(navigate_to_lumber_input)
        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Название", "Количество"])

        # Загрузка данных из CSV
        self.load_csv_lumber("resources/lumber_types.csv", self.table)

        # Добавляем виджеты в компоновку
        layout.addWidget(label_description)
        layout.addWidget(button_second_page)
        layout.addWidget(back_button)
        layout.addWidget(self.table)  # Добавляем таблицу на страницу

        self.setLayout(layout)

    def load_csv_lumber(self, csv_file_path, table_widget):
        # Очищаем таблицу перед загрузкой новых данных
        table_widget.setRowCount(0)

        # Открываем CSV-файл и читаем данные
        with open(csv_file_path, "r", newline="") as file:
            reader = csv.reader(file)

            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(["Вид лесопродукции", "цена"])

            # Читаем строки данных и добавляем их в таблицу
            for row_index, row_data in enumerate(reader):
                table_widget.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(cell_data)
                    table_widget.setItem(row_index, col_index, item)

    def update_lumber_list(self):
        # Метод для обновления данных в таблице
        self.load_csv_lumber("resources/lumber_types.csv", self.table)