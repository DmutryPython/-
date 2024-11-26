from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
                             QStackedWidget, QTableWidget, QTableWidgetItem)

from PyQt6.QtGui import QColor
from PyQt6.QtCore import QEvent
import csv

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
        layout.addWidget(self.table)          # Таблица древесины
        layout.addWidget(QLabel("Таблица заказов"))
        layout.addWidget(self.table_order)

        self.setLayout(layout)

        self.table_order.itemChanged.connect(self.on_item_changed)

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


    def load_csv_order(self, csv_file_path, table_widget):
        # Очищаем таблицу перед загрузкой новых данных
        table_widget.setRowCount(0)

        # Открываем CSV-файл и читаем данные
        with open(csv_file_path, "r", newline="") as file:
            reader = csv.reader(file)

            self.table_order.setColumnCount(7)
            self.table_order.setHorizontalHeaderLabels(["Дата заказа", "Сроки", "Клиент", "Вид лесопродукции",
                                                        "Кол-во лесопродукции, шт.", "Дополнительная информация",
                                                        "статус"])

            # Читаем строки данных и добавляем их в таблицу
            for row_index, row_data in enumerate(reader):
                table_widget.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(cell_data)
                    table_widget.setItem(row_index, col_index, item)  # Используем объект item для добавления в таблицу

                    if col_index == 6:  # Индекс 6 для "Статус"
                        status = cell_data.lower()

                        # Применяем цвет в зависимости от статуса
                        if status == "согласован клиентом":
                            item.setBackground(QColor(255, 165, 0))  # Оранжевый для "Согласован клиентом"
                        elif status == "принят в производство":
                            item.setBackground(QColor(255, 255, 0))  # Желтый для "Принят в производство"
                        elif status == "выполнен":
                            item.setBackground(QColor(0, 255, 0))  # Зеленый для "Выполнен"
                        else:
                            item.setBackground(QColor(255, 255, 255))  # По умолчанию без выделения (для "Черновика")

    def showEvent(self, event: QEvent):
        # Вызываем метод загрузки данных из CSV каждый раз при отображении страницы
        if event.type() == QEvent.Type.Show:
            self.load_csv_order("resources/client.csv", self.table_order)
        super().showEvent(event)

    def on_item_changed(self):
        # После изменения ячейки вызываем сохранение данных в CSV
        self.save_table_order_changes()

    def save_table_order_changes(self):
        row_count = self.table_order.rowCount()
        col_count = self.table_order.columnCount()
        data = []

        for row in range(row_count):
            row_data = []
            for col in range(col_count):
                cell_item = self.table_order.item(row, col)
                cell_data = cell_item.text() if cell_item else ""
                row_data.append(cell_data)
            data.append(row_data)

        # Запись обновленных данных в CSV-файл
        with open("resources/client.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)


    def update_lumber_list(self):
        self.load_csv_lumber("resources/lumber_types.csv", self.table)


    def update_client_list(self):
        self.load_csv_order("resources/client.csv", self.table_order)