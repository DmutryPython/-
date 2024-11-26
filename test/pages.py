from PyQt6.QtWidgets import (QDateEdit, QComboBox, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QMessageBox)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QDate
import csv
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Pages.sql.database_model import Base, Orders, clienttab
import logging
from Pages.sql.database_model import WoodProducts
import os


db_path = os.path.join("Pages", "sql", "wood_production.db")
absolute_path = os.path.abspath(db_path)


class Lumber_input(QWidget):
    def __init__(self, navigate_back, commercial_page, production_page, technology_page):
        super().__init__()

        self.setWindowTitle("Add New Lumber")
        engine = create_engine(f"sqlite:///{absolute_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.commercial_page = commercial_page
        self.production_page = production_page
        self.technology_page = technology_page

        label_text = QLabel("Введите вид древесины:")
        self.lumber_input = QLineEdit()
        self.lumber_input.setPlaceholderText("вид")

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_lumber_to_csv)

        self.time_prod = QLineEdit()
        self.time_prod.setValidator(QIntValidator())
        self.time_prod.setPlaceholderText("время производства")

        self.workshop = QLineEdit()
        self.workshop.setValidator(QIntValidator())
        self.workshop.setPlaceholderText("workshop")

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        layout = QVBoxLayout()
        layout.addWidget(label_text)
        layout.addWidget(self.lumber_input)
        layout.addWidget(self.time_prod)
        layout.addWidget(self.workshop)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def save_lumber_to_csv(self):
        lumber_type = self.lumber_input.text()
        time_prod = self.time_prod.text()
        workshop = self.workshop.text()
        if lumber_type:
            new_order = WoodProducts(
                WoodProductName=lumber_type,
                ProductionTime=time_prod,
                ProductionShopID=workshop
            )

            self.session.add(new_order)
            self.session.commit()
            QMessageBox.information(self, "Success", "Order added successfully!")


        else:
            QMessageBox.warning(self, "Ошибка", "Введите вид древесины для сохранения.")


class client(QWidget):
    def __init__(self, navigate_back, commercial_page):
        super().__init__()

        self.setWindowTitle("Add New client")
        engine = create_engine(f"sqlite:///{absolute_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.commercial_page = commercial_page

        label_text = QLabel("Имя клиента")
        self.lumber_input = QLineEdit()
        self.lumber_input.setPlaceholderText("Имя клиента")

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_client_to_csv)

        self.line_edit_int = QLineEdit()
        self.line_edit_int.setPlaceholderText("Информация")

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        layout = QVBoxLayout()
        layout.addWidget(label_text)
        layout.addWidget(self.lumber_input)
        layout.addWidget(self.line_edit_int)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def save_client_to_csv(self):
        client_name = self.lumber_input.text()
        info = self.line_edit_int.text()
        if client_name:
            new_order = clienttab(
                ClientName=client_name,
                ClientInfo=info,
            )

            self.session.add(new_order)
            self.session.commit()
            QMessageBox.information(self, "Success", "Order added successfully!")
        else:
            QMessageBox.warning(self, "Ошибка", "Введите имя для сохранения")


class order(QWidget):
    def __init__(self, navigate_back, commercial_page, production_page):
        super().__init__()

        self.setWindowTitle("Add New Order")
        engine = create_engine(f"sqlite:///{absolute_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.commercial_page = commercial_page
        self.production_page = production_page

        self.combo_box = QComboBox(self)
        self.status_list = ['Черновик', 'Согласован клиентом', 'Принят в производство', 'Выполнен']
        self.combo_box.addItems(self.status_list)

        self.date_order = QDateEdit(self)
        self.date_order.setDate(QDate.currentDate())

        self.deadline = QDateEdit(self)
        self.deadline.setDate(QDate.currentDate())

        self.client = QLineEdit()
        self.client.setPlaceholderText("Информация о клиенте")

        self.lumber = QLineEdit()
        self.lumber.setPlaceholderText("пиломатериал")

        self.quantity_lumber = QLineEdit()
        self.quantity_lumber.setValidator(QIntValidator())
        self.quantity_lumber.setPlaceholderText("кол-во пиломатериала")

        self.note = QLineEdit()
        self.note.setPlaceholderText("пометка")

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.add_order)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("дата заказа"))
        layout.addWidget(self.date_order)
        layout.addWidget(QLabel("срок заказа"))
        layout.addWidget(self.deadline)
        layout.addWidget(self.client)
        layout.addWidget(self.lumber)
        layout.addWidget(self.quantity_lumber)
        layout.addWidget(self.note)
        layout.addWidget(self.combo_box)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def add_order(self):
        try:
            #Get data from input fields (add error handling as needed)
            date_order = self.date_order.date().toPyDate()
            deadline = self.deadline.date().toPyDate()
            client = self.client.text()
            lumber = self.lumber.text()
            quantity_lumber = self.quantity_lumber.text()
            note = self.note.text()
            status = self.combo_box.currentText()

            if status != 'Черновик':
                if not all([date_order, deadline, client, quantity_lumber, lumber]):
                    QMessageBox.warning(self, "Ошибка", "Введены не все данные")
                    return

                # try:
                #     quantity_lumber = int(quantity_lumber_str)
                # except ValueError:
                #     QMessageBox.warning(self, "Ошибка", "Некорректное количество пиломатериала")
                #     return

            if date_order >= deadline:
                QMessageBox.warning(self, "Ошибка", "Срок заказа должен быть позже даты заказа")
                return


            new_order = Orders(OrderRegistrationDate=date_order,
                               OrderCompletionDate=deadline,
                               ClientID=client,
                               WoodProductID=lumber,  # Use the ID from the database
                               WoodProductQuantity=quantity_lumber,
                               AdditionalOrderInformation=note,
                               OrderStatus=status)

            self.session.add(new_order)
            self.session.commit()
            QMessageBox.information(self, "Success", "Order added successfully!")


        except exc.SQLAlchemyError as e:
            self.session.rollback()  # Rollback transaction on error
            QMessageBox.critical(self, "Database Error", f"Database error: {e}")
            logging.exception(f"Database error: {e}")  # Log the error for debugging

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
            logging.exception(f"An unexpected error occurred: {e}")








