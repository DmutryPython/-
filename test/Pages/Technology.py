from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
                             QStackedWidget, QTableWidget, QTableWidgetItem)
from PyQt6.QtGui import QIntValidator
import csv
from .functions import update_list, load_csv_lumber

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
        load_csv_lumber(self, csv_file_path, table_widget)

    def update_list(self, path):
        update_list(self, path)