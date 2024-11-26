import csv
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
                             QStackedWidget, QTableWidget, QTableWidgetItem)

from PyQt6.QtGui import QColor

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


def load_csv_client(self, csv_file_path, table_widget):
    # Очищаем таблицу перед загрузкой новых данных
    table_widget.setRowCount(0)

    # Открываем CSV-файл и читаем данные
    with open(csv_file_path, "r", newline="") as file:
        reader = csv.reader(file)

        self.table_name.setColumnCount(2)
        self.table_name.setHorizontalHeaderLabels(["имя", "информация"])

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


def update_list(self, path):
    self.load_csv_lumber(path, self.table)



