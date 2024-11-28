from PyQt6.QtWidgets import (QDateEdit, QComboBox, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QMessageBox)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QDate
import csv
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .sql.database_model import Base, Orders, clienttab
import logging
from .sql.database_model import ShopSections
import os
import sqlalchemy as sa


db_path = os.path.join("Pages", "sql", "wood_production.db")
absolute_path = os.path.abspath(db_path)
from .functions import table_input


class ShopSection(QWidget):
    def __init__(self, navigate_back):
        super().__init__()

        tab = table_input()
        self.session = tab.session

        self.section_input = QLineEdit()
        self.section_input.setPlaceholderText("наименование секции")

        self.production_shop = QComboBox(self)
        self.production_shop_list = self.session.execute(sa.select(sa.column('ShopName')).
                                                select_from(sa.table('production_shops'))).scalars().all()
        self.production_shop.addItems(self.production_shop_list)

        self.sectionParam_input = QLineEdit()
        self.sectionParam_input.setPlaceholderText("параметры секции")

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_shop)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        layout = QVBoxLayout()
        layout.addWidget(self.section_input)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def save_shop(self):
        try:
            shopsection = self.section_input.text()
            shop = self.production_shop.currentText()
            param = self.sectionParam_input.text()
            if shop:
                new_order = ShopSections(
                    ShopSectionName=shopsection,
                    ShopName=shop,
                    SectionParam=param

                )

                self.session.add(new_order)
                self.session.commit()
                QMessageBox.information(self, "Success", "Order added successfully!")


            else:
                QMessageBox.warning(self, "Ошибка", "Введите наименование цеха")
        except sa.exc.IntegrityError as e:
            QMessageBox.warning(self, "Ошибка", "Ошибка: Значение уже существует.")

    def showEvent(self, event):
        """Вызывается каждый раз, когда виджет становится видимым."""
        self.update_tables()
        super().showEvent(event)

    def update_tables(self):
        index = self.layout().indexOf(self.production_shop)  # Находим индекс quantity_lumber
        self.tab = table_input()
        self.session = self.tab.session
        # Удаляем старый ComboBox
        self.layout().removeWidget(self.production_shop)
        self.production_shop.deleteLater()

        # Создаем новый ComboBox и добавляем его в layout
        self.production_shop = QComboBox(self)
        self.production_shop_list = self.session.execute(sa.select(sa.column('ShopName')).
                                                         select_from(sa.table('production_shops'))).scalars().all()
        self.production_shop.addItems(self.production_shop_list)
        self.layout().insertWidget(index, self.production_shop) # Добавляем в layout

        # Обновляем layout, чтобы изменения отобразились
        self.layout().update()
        self.update()