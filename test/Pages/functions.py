import csv
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
                             QStackedWidget, QTableWidget, QTableWidgetItem, QStyledItemDelegate)
from PyQt6.QtCore import QAbstractTableModel, Qt

from PyQt6.QtGui import QColor

import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker



class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            row = self._data[index.row()]
            column_name = self.headerData(index.column(), Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
            try:
                return str(row[column_name])
            except KeyError:
                print(f"KeyError: {column_name} not found in row {row}")
                return "N/A"  # Or handle the error as needed
        return None

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        if self._data:
            try:
                return len(self._data[0])
            except IndexError:
                print("IndexError: _data is empty or rows have inconsistent lengths.")
                return 0
        return 0

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if self._data:
                    try:
                        column_names = list(self._data[0].keys())
                        return column_names[section]
                    except IndexError:
                        print("IndexError: _data is empty or rows have inconsistent lengths.")
                        return None
            else:
                return str(section + 1)
        return None


from PyQt6.QtGui import QBrush, QColor

class ConditionalColorDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        status_column_index = index.model().headerData(index.column(), Qt.Orientation.Horizontal,
                                                       Qt.ItemDataRole.DisplayRole)
        if status_column_index == "OrderStatus":  # Проверяем, является ли колонка колонкой "status"
            value = index.model().data(index, Qt.ItemDataRole.DisplayRole)
            color = None
            if value == "Согласован клиентом":
                color = QColor(QColor("red"))
            elif value == "Принят в производство":
                color = QColor(QColor("yellow"))
            elif value == "Выполнен":
                color = QColor(QColor("green"))

            if color:
                option.rect.adjust(2, 2, -2, -2)  # небольшое отступление от краев
                painter.fillRect(option.rect, color)
        super().paint(painter, option, index)


class table_input():
    def __init__(self):
        project_root = os.path.dirname(os.path.dirname(__file__))
        db_path = os.path.join(project_root, "Pages", "sql", "wood_production.db")
        absolute_path = os.path.abspath(db_path)

        engine = sa.create_engine(f"sqlite:///{absolute_path}")
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            query_lumber = sa.text("SELECT * FROM wood_products")
            result_lumber = session.execute(query_lumber).mappings().all()  # Use mappings to get dictionary-like rows

        except sa.exc.OperationalError as e:
            result_lumber = []

        try:
            query_client = sa.text("SELECT * FROM client_tab")
            result_client = session.execute(query_client).mappings().all()
        except sa.exc.OperationalError as e:
            result_client = []

        try:
            query_order = sa.text("SELECT * FROM orders")
            result_order = session.execute(query_order).mappings().all()

        except sa.exc.OperationalError as e:
            result_order = []

        self.result_lumber = result_lumber
        self.result_client = result_client
        self.result_order = result_order


