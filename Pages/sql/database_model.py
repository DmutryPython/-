import sqlalchemy as sa
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.event import listens_for

Base = declarative_base()

class Orders(Base):
    __tablename__ = 'orders'
    OrderID = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    WoodProductQuantity = sa.Column(sa.Integer)

    OrderRegistrationDate = sa.Column(sa.Date)
    OrderCompletionDate = sa.Column(sa.Date)
    ClientName = sa.Column(sa.String(255))
    AdditionalOrderInformation = sa.Column(sa.Text)
    OrderStatus = sa.Column(sa.String(255))

    WoodProductName = sa.Column(sa.String(255), sa.ForeignKey('wood_products.WoodProductName'))

    # production_tasks = relationship("ProductionTasks", back_populates="order")
    wood_products = relationship("WoodProducts", backref="order", lazy="joined")



class WoodProducts(Base):
    __tablename__ = 'wood_products'
    WoodProductName = sa.Column(sa.String(255), primary_key=True)
    ProductionTime = sa.Column(sa.Integer)
    ProductionShopName = sa.Column(sa.String(255), sa.ForeignKey('production_shops.ShopID'))

    production_shop = relationship("ProductionShops", backref="productionShop", lazy="joined")


class ProductionTasks(Base):
    __tablename__ = 'production_tasks'
    ProductionTaskID = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    TaskRegistrationDate = sa.Column(sa.Date)
    ProductionStartDate = sa.Column(sa.Date)

    OrderID = sa.Column(sa.Integer, sa.ForeignKey('orders.OrderID'))

    WoodProductsQuantity = sa.Column(sa.Integer)

    WoodProductName = sa.Column(sa.String(255), sa.ForeignKey('wood_products.WoodProductName'))

    Shop = sa.Column(sa.String(255), sa.ForeignKey('production_shops.ShopName'))
    AdditionalTaskInformation = sa.Column(sa.Text)

    order = relationship("Orders", backref="order", lazy="joined")
    wood_product = relationship("WoodProducts",  backref="wood", lazy="joined")
    shop = relationship("ProductionShops", backref="shop_name", lazy="joined")


class PreparationTasks(Base):
    __tablename__ = 'preparation_tasks'
    PreparationTaskID = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    TaskRegistrationDate = sa.Column(sa.Date)
    ShopSectionCompletionDate = sa.Column(sa.Date)

    ProductionTaskID = sa.Column(sa.Integer, sa.ForeignKey('production_tasks.ProductionTaskID'))

    Shop = sa.Column(sa.String(255), sa.ForeignKey('shop_sections.ShopSectionName'))
    TaskInfo = sa.Column(sa.String(255))
    TaskStatus = sa.Column(sa.String(255))


    production_task = relationship("ProductionTasks", backref="task", lazy="joined")
    shop_section = relationship("ShopSections", backref="section", lazy="joined")


class ProductionShops(Base):
    __tablename__ = 'production_shops'
    ShopID = sa.Column(sa.Integer, primary_key=True)
    ShopName = sa.Column(sa.String(255), unique=True)


class ShopSections(Base): # Added ShopSections class
    __tablename__ = 'shop_sections'
    ShopSectionName = sa.Column(sa.String(255), primary_key=True)
    ShopName = sa.Column(sa.String, sa.ForeignKey('production_shops.ShopName'))
    SectionParam = sa.Column(sa.String(255))

    # preparation_tasks = relationship("PreparationTasks", back_populates="shop_section")
    shop = relationship("ProductionShops", backref="shopName", lazy="joined")



class clienttab(Base):
    __tablename__ = 'client_tab'
    ClientID = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    ClientName = sa.Column(sa.String(255))
    ClientInfo = sa.Column(sa.String(255))







import os
import sys

def get_db_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "wood_production.db")


# Создание движка SQLAlchemy
db_path = get_db_path()
engine = sa.create_engine(f"sqlite:///{db_path}")

# Создание таблиц
Base.metadata.create_all(engine)




