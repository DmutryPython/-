from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QIntValidator  # Здесь импортируется QIntValidator
from sqlalchemy import *
from sqlalchemy.orm import *
import logging
from .functions import table_input, update_tables
from .sql.database_model import ProductionTasks


class PreparationTasks(QWidget):
    def __init__(self, navigate_back):
        super().__init__()

        layout = QVBoxLayout()
        tab = table_input()
        self.session = tab.session

        self.setWindowTitle("Добавить задание на подготовку")

        self.date_registration = QDateEdit(self)
        self.date_registration.setDate(QDate.currentDate())
        self.date_start = QDateEdit(self)
        self.date_start.setDate(QDate.currentDate())

        self.productionTask_id = QComboBox(self)
        self.productionTasks = self.session.execute(select(column('ProductionTaskID')).
                                                    select_from(table('production_tasks'))).scalars().all()
        self.productionTask_id.addItems(self.productionTasks)

        self.workshop = QComboBox(self)
        self.shopname = self.session.execute(select(column('ShopName')).
                                             select_from(table('production_shops'))).scalars().all()
        self.workshop.addItems(self.shopname)

        self.additional_info = QLineEdit(self)
        self.additional_info.setPlaceholderText("Дополнительная информация")

        self.status = QComboBox(self)
        self.status_list = ["Создан", "Выполнен"]
        self.status.addItems(self.status_list)

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.add_task)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        layout.addWidget(QLabel("Дата регистрации:"))
        layout.addWidget(self.date_registration)
        layout.addWidget(QLabel("Дата начала:"))
        layout.addWidget(self.date_start)
        layout.addWidget(QLabel("Номер задачи:"))
        layout.addWidget(self.productionTask_id)
        layout.addWidget(QLabel("Цех:"))
        layout.addWidget(self.workshop)
        layout.addWidget(QLabel("Дополнительная информация:"))
        layout.addWidget(self.additional_info)
        layout.addWidget(QLabel("Статус:"))
        layout.addWidget(self.status)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def update_productionTask_id(self):
        update_tables(self, 'orders', 'OrderID', self.productionTask_id)

    def update_workshops(self):
        update_tables(self, 'production_shops', 'ShopName', self.workshop)

    def showEvent(self, event):
        """Вызывается каждый раз, когда виджет становится видимым."""
        self.update_productionTask_id()
        self.update_workshops()
        super().showEvent(event)


    def add_task(self):
        try:
            date_registration = self.date_registration.date().toPyDate()
            date_start = self.date_start.date().toPyDate()
            workshop = self.workshop.currentText()
            productiontaskid = self.productionTask_id.currentText()
            status = self.status.currentText()

            new_task = ProductionTasks(TaskRegistrationDate=date_registration,
                                       ProductionStartDate=date_start,
                                       ProductionTaskID=productiontaskid,
                                       Shop=workshop,
                                       TaskStatus=status)

            self.session.add(new_task)
            self.session.commit()
            QMessageBox.information(self, "Success", "Task added successfully!")

        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            logging.exception(f"An error occurred: {e}")
