from PyQt6.QtWidgets import (QDateEdit, QComboBox, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QMessageBox, QTableView)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QDate
import csv
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .sql.database_model import Base, Orders, clienttab
import logging
from .sql.database_model import WoodProducts
import os
import sqlalchemy as sa
from .functions import table_input, update_tables, PandasModel
import sys




class Lumber(QWidget):
    def __init__(self, navigate_back):
        super().__init__()

        self.tab = table_input()
        self.session = self.tab.session

        result_lumber = self.tab.result_lumber
        self.table_lumber = QTableView()
        self.model_lumber = PandasModel(result_lumber)
        self.table_lumber.setModel(self.model_lumber)

        label_text = QLabel("Введите вид древесины:")
        self.lumber_input = QLineEdit()
        self.lumber_input.setPlaceholderText("вид")

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_lumber)

        self.time_prod = QLineEdit()
        self.time_prod.setValidator(QIntValidator())
        self.time_prod.setPlaceholderText("время производства")

        self.workshop = QComboBox(self)
        self.workshop_list = self.session.execute(sa.select(sa.column('ShopSectionName')).
                                                select_from(sa.table('shop_sections'))).scalars().all()
        self.workshop.addItems(self.workshop_list)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        layout = QVBoxLayout()
        layout.addWidget(self.table_lumber)
        layout.addWidget(label_text)
        layout.addWidget(self.lumber_input)
        layout.addWidget(self.time_prod)
        layout.addWidget(self.workshop)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def save_lumber(self):
        try:
            lumber_type = self.lumber_input.text()
            time_prod = self.time_prod.text()
            workshop = self.workshop.currentText()
            if lumber_type:
                new_order = WoodProducts(
                    WoodProductName=lumber_type,
                    ProductionTime=time_prod,
                    ProductionShopName=workshop
                )

                self.session.add(new_order)
                self.session.commit()
                QMessageBox.information(self, "Success", "Order added successfully!")


            else:
                QMessageBox.warning(self, "Ошибка", "Введите вид древесины для сохранения.")
        except sa.exc.IntegrityError as e:
            self.session.rollback()
            QMessageBox.warning(self, "Ошибка", "Ошибка: Значение уже существует.")

    def showEvent(self, event):
        """Вызывается каждый раз, когда виджет становится видимым."""
        self.update_Shop()
        self.update_tables()
        super().showEvent(event)

    def update_Shop(self):
        update_tables(self, 'shop_sections', 'ShopSectionName', self.workshop)

    def update_tables(self):
        self.tab = table_input()
        result_lumber = self.tab.result_lumber

        self.model_lumber = PandasModel(result_lumber)
        self.table_lumber.setModel(self.model_lumber)
