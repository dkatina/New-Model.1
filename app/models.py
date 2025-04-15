from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


ticket_mechanic = db.Table(
    "ticket_mechanic",
    Base.metadata,
    db.Column("ticket_id", db.ForeignKey("service_tickets.id")),
    db.Column("mechanic_id", db.ForeignKey("mechanics.id"))
)


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(db.String(320), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(16), nullable=False)

    tickets: Mapped[List['Service_Ticket']] = db.relationship(back_populates='customer')

class Mechanic(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(db.String(320), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(16), nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    tickets: Mapped[List['Service_Ticket']] = db.relationship(secondary=ticket_mechanic, back_populates="mechanics")

class Service_Ticket(Base):
    __tablename__ = "service_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_date: Mapped[date] = mapped_column(nullable=False)
    VIN: Mapped[str] = mapped_column(db.String(18), nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(320), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"))

    customer: Mapped['Customer'] = db.relationship(back_populates="tickets")
    mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=ticket_mechanic, back_populates="tickets")
    ticket_items: Mapped[List['SerialItem']] = db.relationship(back_populates = 'ticket')


class ItemDesc(Base):
    __tablename__ = "item_descs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

    serial_items: Mapped[List['SerialItem']] = db.relationship(back_populates = 'description')


class SerialItem(Base):
    __tablename__ = "serial_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    description_id: Mapped[int] = mapped_column(db.ForeignKey("item_descs.id"))
    ticket_id: Mapped[int] = mapped_column(db.ForeignKey("service_tickets.id"), nullable=True)

    description: Mapped['ItemDesc'] = db.relationship(back_populates = 'serial_items')
    ticket: Mapped['Service_Ticket'] = db.relationship(back_populates = 'ticket_items')