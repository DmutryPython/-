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
    ProductionShopName = sa.Column(sa.String(255)) #, sa.ForeignKey('production_shops.ShopID'))

    # production_tasks = relationship("ProductionTasks", back_populates="wood_product")
    # production_shop = relationship("ProductionShops", back_populates="wood_products")


class ProductionTasks(Base):
    __tablename__ = 'production_tasks'
    ProductionTaskID = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    TaskRegistrationDate = sa.Column(sa.Date)
    ProductionStartDate = sa.Column(sa.Date)

    OrderID = sa.Column(sa.Integer) #, sa.ForeignKey('orders.OrderID'))

    WoodProductName = sa.Column(sa.String(255)) #, sa.ForeignKey('wood_products.WoodProductName'))

    Shop = sa.Column(sa.String(255)) #, sa.ForeignKey('production_shops.ShopName'))
    AdditionalTaskInformation = sa.Column(sa.Text)
    TaskStatus = sa.Column(sa.String(255))

    # order = relationship("Orders", back_populates="production_tasks")
    # wood_product = relationship("WoodProducts", back_populates="production_tasks")
    # shop = relationship("ProductionShops", back_populates="production_tasks")
    # preparation_tasks = relationship("PreparationTasks", back_populates="production_task")


class PreparationTasks(Base):
    __tablename__ = 'preparation_tasks'
    PreparationTaskID = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    TaskRegistrationDate = sa.Column(sa.Date)
    ShopSectionCompletionDate = sa.Column(sa.Date)

    ProductionTaskID = sa.Column(sa.Integer) #, sa.ForeignKey('production_tasks.ProductionTaskID'))

    Shop = sa.Column(sa.String(255)) #, sa.ForeignKey('shop_sections.ShopSectionName'))

    TaskStatus = sa.Column(sa.String(255))


    # production_task = relationship("ProductionTasks", back_populates="preparation_tasks")
    # shop_section = relationship("ShopSections", back_populates="preparation_tasks")


class ProductionShops(Base):
    __tablename__ = 'production_shops'
    ShopID = sa.Column(sa.Integer, primary_key=True)
    ShopName = sa.Column(sa.String(255))

    # wood_products = relationship("WoodProducts", back_populates="production_shop") #back_populates corrected
    # production_tasks = relationship("ProductionTasks", back_populates="shop")
    # shop_sections = relationship("ShopSections", back_populates="shop")


class ShopSections(Base): # Added ShopSections class
    __tablename__ = 'shop_sections'
    ShopSectionID = sa.Column(sa.Integer, primary_key=True)
    ShopSectionName = sa.Column(sa.String(255))
    ShopName = sa.Column(sa.String, sa.ForeignKey('production_shops.ShopName'))

    # preparation_tasks = relationship("PreparationTasks", back_populates="shop_section")
    # shop = relationship("ProductionShops", back_populates="shop_sections")


class clienttab(Base):
    __tablename__ = 'client_tab'
    ClientID = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    ClientName = sa.Column(sa.String(255))
    ClientInfo = sa.Column(sa.String(255))


# @listens_for(ProductionTasks, 'before_insert')
# def receive_before_insert_production_task(mapper, connection, target):
#     session = sessionmaker(bind=connection)()
#     order = session.query(Orders).get(target.OrderID)
#     woodprod = session.query(WoodProducts).get(target.WoodProductName)
#     if order:
#         target.wood_type = order.WoodProduct
#         target.quantity = order.WoodProductQuantity
#     if woodprod:
#         target.workshop = woodprod.ProductionShopName
#     session.close()




import os



project_root = os.path.dirname(os.path.dirname(__file__)) #go up two directories
db_path = os.path.join(project_root, "sql", "wood_production.db")
absolute_path = os.path.abspath(db_path)


engine = sa.create_engine(f"sqlite:///{absolute_path}")

Base.metadata.create_all(engine)




