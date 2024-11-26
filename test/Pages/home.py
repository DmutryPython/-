from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
                             QStackedWidget, QTableWidget, QTableWidgetItem)


class MainPage(QWidget):
    def __init__(self, navigate_to_commercial, navigate_to_production, navigate_to_technology):
        super().__init__()
        layout = QVBoxLayout()

        com_button = QPushButton("Коммерческая служба")
        com_button.clicked.connect(navigate_to_commercial)

        prod_button = QPushButton("Служба производства")
        prod_button.clicked.connect(navigate_to_production)

        tech_button = QPushButton("Служба технолога")
        tech_button.clicked.connect(navigate_to_technology)

        layout.addWidget(com_button)
        layout.addWidget(prod_button)
        layout.addWidget(tech_button)

        self.setLayout(layout)
