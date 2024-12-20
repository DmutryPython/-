from .functions import PandasModel, table_input, ConditionalColorDelegate, DictTableModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableView

class TechnologyPage(QWidget):
    def __init__(self, navigate_to_lumber_input, productionTask_page, PreparationTasks_page, ProductionShop_page, ShopSection_page,
                 navigate_back):
        super().__init__()

        self.tab = table_input()
        result_lumber = self.tab.result_lumber
        result_preparation = self.tab.result_preparation_task
        result_shopSelection = self.tab.shop_section_list

        label_description = QLabel("Служба технолога")

        # Кнопка навигации
        button_second_page = QPushButton("Добавить древесину")
        button_second_page.clicked.connect(navigate_to_lumber_input)

        button_productionTask = QPushButton("Добавить задачу")
        button_productionTask.clicked.connect(productionTask_page)

        button_PreparationTasks = QPushButton("Добавить задачу на подготовку")
        button_PreparationTasks.clicked.connect(PreparationTasks_page)

        button_ProductionShop = QPushButton("Добавить цех")
        button_ProductionShop.clicked.connect(ProductionShop_page)

        button_ShopSection = QPushButton("Добавить секцию цеха")
        button_ShopSection.clicked.connect(ShopSection_page)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(navigate_back)

        # Таблица
        self.table_lumber = QTableView()
        self.model_lumber = PandasModel(result_lumber)
        self.table_lumber.setModel(self.model_lumber)

        self.table_preparation = QTableView()
        self.model_preparation = PandasModel(result_preparation)
        self.table_preparation.setModel(self.model_preparation)

        self.table_shopSelection = QTableView()
        self.model_shopSelection = DictTableModel(result_shopSelection)
        self.table_shopSelection.setModel(self.model_shopSelection)

        # Добавляем виджеты в компоновку
        layout = QVBoxLayout()
        layout.addWidget(label_description)
        layout.addWidget(button_second_page)
        layout.addWidget(button_productionTask)
        layout.addWidget(button_PreparationTasks)
        layout.addWidget(button_ProductionShop)
        layout.addWidget(button_ShopSection)
        layout.addWidget(back_button)
        layout.addWidget(QLabel("Таблица цехов"))
        layout.addWidget(self.table_shopSelection)
        layout.addWidget(QLabel("Таблица древесины"))
        layout.addWidget(self.table_lumber)
        layout.addWidget(QLabel("Таблица задач на остнастку"))
        layout.addWidget(self.table_preparation)

        self.setLayout(layout)

    def showEvent(self, event):
        """Вызывается каждый раз, когда виджет становится видимым."""
        self.update_tables()
        super().showEvent(event)

    def update_tables(self):
        """Обновляет данные в таблицах."""
        self.tab = table_input()
        result_lumber = self.tab.result_lumber

        self.model_lumber = PandasModel(result_lumber)
        self.table_lumber.setModel(self.model_lumber)