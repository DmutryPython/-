from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
                             QStackedWidget, QTableWidget, QTableWidgetItem)

from PyQt6.QtGui import QColor
from PyQt6.QtCore import QEvent
import csv
from .functions import update_list, load_csv_lumber, load_csv_order, load_csv_client, save_table_order_changes


class ProductionPage(QWidget):
    def __init__(self, navigate_to_lumber_input, order_page, navigate_back):
        super().__init__()
        layout = QVBoxLayout()

        # Заголовок страницы
        label_description = QLabel("Служба производства")

        # Кнопки навигации
        lumber_button = QPushButton("Добавить древесину")
        lumber_button.clicked.connect(navigate_to_lumber_input)

        order_button = QPushButton("Добавить заказ")
        order_button.clicked.connect(order_page)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        # Таблицы для древесины и клиентов
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Вид лесопродукции", "Количество"])

        self.table_order = QTableWidget()

        # Загрузка данных из CSV
        self.load_csv_lumber("resources/lumber_types.csv", self.table)
        self.load_csv_order("resources/client.csv", self.table_order)

        # Добавляем виджеты в компоновку
        layout.addWidget(label_description)
        layout.addWidget(lumber_button)
        layout.addWidget(order_button)
        layout.addWidget(back_button)
        layout.addWidget(QLabel("Таблица древесины"))
        layout.addWidget(self.table)  # Таблица древесины
        layout.addWidget(QLabel("Таблица заказов"))
        layout.addWidget(self.table_order)

        self.setLayout(layout)

        self.table_order.itemChanged.connect(self.on_item_changed)

    def load_csv_lumber(self, csv_file_path, table_widget):
        load_csv_lumber(self, csv_file_path, table_widget)

    def load_csv_order(self, csv_file_path, table_widget):
        load_csv_order(self, csv_file_path, table_widget)

    def showEvent(self, event: QEvent):
        # Вызываем метод загрузки данных из CSV каждый раз при отображении страницы
        if event.type() == QEvent.Type.Show:
            load_csv_order(self, "resources/client.csv", self.table_order)
        super().showEvent(event)

    def on_item_changed(self):
        save_table_order_changes(self)

    def update_list(self, path):
        update_list(self, path)
