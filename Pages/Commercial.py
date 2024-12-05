from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel,QPushButton, QTableView
from PyQt6.QtCore import QEvent
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtGui import QColor
import csv
from .functions import PandasModel, table_input, ConditionalColorDelegate
import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker




class CommercialPage(QWidget):
    def __init__(self, navigate_to_lumber_input=None, navigate_to_client=None, order_page=None, navigate_back=None):
        super().__init__()

        self.tab = table_input()
        result_lumber = self.tab.result_lumber
        result_client = self.tab.result_client
        result_order = self.tab.result_order


        layout = QVBoxLayout()

        # Заголовок страницы
        label_description = QLabel("Коммерческая служба")

        # Кнопки навигации
        lumber_button = QPushButton("Добавить древесину")
        lumber_button.clicked.connect(navigate_to_lumber_input)

        client_button = QPushButton("Добавить клиента")
        client_button.clicked.connect(navigate_to_client)

        order_button = QPushButton("Добавить заказ")
        order_button.clicked.connect(order_page)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        # Таблицы для древесины и клиентов
        self.table_lumber = QTableView()
        self.model_lumber = PandasModel(result_lumber)
        self.table_lumber.setModel(self.model_lumber)

        self.table_client = QTableView()
        self.model_client = PandasModel(result_client)
        self.table_client.setModel(self.model_client)

        self.table_order = QTableView()
        self.model_order = PandasModel(result_order)
        self.table_order.setModel(self.model_order)
        self.table_order.setItemDelegate(ConditionalColorDelegate())

        # Загрузка данных из CSV


        # Добавляем виджеты в компоновку
        layout.addWidget(label_description)
        layout.addWidget(lumber_button)
        layout.addWidget(client_button)
        layout.addWidget(order_button)
        layout.addWidget(back_button)
        layout.addWidget(QLabel("Таблица древесины"))
        layout.addWidget(self.table_lumber)          # Таблица древесины
        layout.addWidget(QLabel("Таблица клиентов"))
        layout.addWidget(self.table_client)     # Таблица клиентов
        layout.addWidget(QLabel("Таблица заказов"))
        layout.addWidget(self.table_order)

        self.setLayout(layout)

        # self.table_order.itemChanged.connect(self.on_item_changed)

    def showEvent(self, event):
        """Вызывается каждый раз, когда виджет становится видимым."""
        self.update_tables()
        super().showEvent(event)

    def update_tables(self):
        """Обновляет данные в таблицах."""
        self.tab = table_input()
        result_lumber = self.tab.result_lumber  # Используйте существующий экземпляр TableInput
        result_client = self.tab.result_client
        result_order = self.tab.result_order

        self.model_lumber = PandasModel(result_lumber)
        self.table_lumber.setModel(self.model_lumber)

        self.model_client = PandasModel(result_client)
        self.table_client.setModel(self.model_client)

        self.model_order = PandasModel(result_order)
        self.table_order.setModel(self.model_order)
        self.table_order.setItemDelegate(ConditionalColorDelegate())
