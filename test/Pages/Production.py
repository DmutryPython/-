from .functions import PandasModel, table_input, ConditionalColorDelegate
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableView


class ProductionPage(QWidget):
    def __init__(self, navigate_to_lumber_input, order_page, navigate_back):
        super().__init__()

        self.tab = table_input()
        result_lumber = self.tab.result_lumber
        result_order = self.tab.result_order

        label_description = QLabel("Служба производства")

        lumber_button = QPushButton("Добавить древесину")
        lumber_button.clicked.connect(navigate_to_lumber_input)

        order_button = QPushButton("Добавить заказ")
        order_button.clicked.connect(order_page)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        # Таблицы для древесины и клиентов
        self.table_lumber = QTableView()
        self.model_lumber = PandasModel(result_lumber)
        self.table_lumber.setModel(self.model_lumber)


        self.table_order = QTableView()
        self.model_order = PandasModel(result_order)
        self.table_order.setModel(self.model_order)
        self.table_order.setItemDelegate(ConditionalColorDelegate())

        # Добавляем виджеты в компоновку
        layout = QVBoxLayout()
        layout.addWidget(label_description)
        layout.addWidget(lumber_button)
        layout.addWidget(order_button)
        layout.addWidget(back_button)
        layout.addWidget(QLabel("Таблица древесины"))
        layout.addWidget(self.table_lumber)  # Таблица древесины
        layout.addWidget(QLabel("Таблица заказов"))
        layout.addWidget(self.table_order)

        self.setLayout(layout)


    def showEvent(self, event):
        """Вызывается каждый раз, когда виджет становится видимым."""
        self.update_tables()
        super().showEvent(event)

    def update_tables(self):
        """Обновляет данные в таблицах."""
        self.tab = table_input()
        result_lumber = self.tab.result_lumber
        result_order = self.tab.result_order

        self.model_lumber = PandasModel(result_lumber)
        self.table_lumber.setModel(self.model_lumber)

        self.model_order = PandasModel(result_order)
        self.table_order.setModel(self.model_order)
        self.table_order.setItemDelegate(ConditionalColorDelegate())
