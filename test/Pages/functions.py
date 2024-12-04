import csv
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
                             QStackedWidget, QTableWidget, QTableWidgetItem, QStyledItemDelegate, QComboBox)
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex

from PyQt6.QtGui import QColor

import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from .sql.database_model import ShopSections, ProductionShops



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

        try:
            query_product_task = sa.text("SELECT * FROM production_tasks")
            result_product_task = session.execute(query_product_task).mappings().all()
        except:
            result_product_task = []

        try:
            query_preparation_task = sa.text("SELECT * FROM preparation_tasks")
            result_preparation_task = session.execute(query_preparation_task).mappings().all()
        except:
            result_preparation_task = []

        try:
            query_shop = sa.text("SELECT * FROM production_shops")
            result_production_shop = session.execute(query_shop).mappings().all()
        except:
            result_production_shop = []

        try:
            query_shop_section = sa.text("SELECT * FROM shop_sections")
            result_shop_section = session.execute(query_shop_section).mappings().all()
        except:
            result_shop_section = []

        try:
            query_shop_list = sa.text("SELECT ShopName FROM production_shops")
            shop_list = session.execute(query_shop_list).mappings().all()
            shop_section_list = {}
            for i in shop_list:
                k = i['ShopName']
                el = session.query(ShopSections).filter(ShopSections.ShopName == k).all()
                string_el = [str(item.ShopSectionName) for item in el]
                shop_section_list[k] = string_el

        except sa.exc.OperationalError as e:
            shop_section_list = {}
            print(e)

        self.session = Session()
        self.result_lumber = result_lumber
        self.result_client = result_client
        self.result_order = result_order
        self.result_product_task = result_product_task
        self.result_preparation_task = result_preparation_task
        self.result_production_shop = result_production_shop
        self.result_shop_section = result_shop_section
        self.shop_section_list = shop_section_list



def update_tables(self, nametab, column, obj):
    index = self.layout().indexOf(obj)  # Находим индекс quantity_lumber
    self.tab = table_input()
    self.session = self.tab.session

    self.layout().removeWidget(obj)

    obj.clear()
    lt = map(str, self.session.execute(sa.select(sa.column(column)).select_from(sa.table(nametab))).scalars().all())
    obj.addItems(lt)
    self.layout().insertWidget(index, obj)

    self.layout().update()
    self.update()


class DictTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = self._transform_data(data) #Data transformation happens here
        self.headers = self._data[0] if self._data else []
        self.rows = self._data[1:] if self._data else []

    def _transform_data(self, data):
        if not data:
            return []

        headers = list(data.keys())
        max_len = max(len(v) for v in data.values() if v) if data else 0
        rows = []
        for i in range(max_len):
            row = []
            for header in headers:
                if data.get(header):
                    try:
                        row.append(data[header][i])
                    except IndexError:
                        row.append("")
                else:
                    row.append("")
            rows.append(row)
        return [headers] + rows


    def rowCount(self, parent=QModelIndex()):
        return len(self.rows)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers) if self.headers else 0

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            col = index.column()
            if 0 <= row < len(self.rows) and 0 <= col < len(self.headers):
                return str(self.rows[row][col])
            else:
                return ""

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]
            else:
                return str(section + 1)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]
            else:
                return str(section + 1)

