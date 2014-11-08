# -*- coding: utf-8 -*-
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from azoth.models import (
    Base,
    ActionBase,
    CopyBase,
    IndexBase,
    TimestampBase,
    LogicalDeleteBase,
    SmartBase,
    PowerBase,
    AUTO_INCREMENT,
    create_all,
    )
from azoth.sessions import SessionSetup
settings = {
    'sqlalchemy.url': 'sqlite://',
    'sqlalchemy.echo': True,
    }
SessionSetup.setup(settings)


# functional testing model

class ActionBaseTestModel(Base, ActionBase):
    __tablename__ = 'ActionBaseTestModel'
    __table_args__ = AUTO_INCREMENT,

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Unicode, default=u'aabbbcc')


class CopyBaseTestModel(Base, CopyBase):
    __tablename__ = 'CopyBaseTestModel'
    __table_args__ = AUTO_INCREMENT,
    id = sa.Column(sa.Integer, primary_key=True)
    boolean = sa.Column(sa.Boolean)
    big_integer = sa.Column(sa.BigInteger)
    integer = sa.Column(sa.Integer)
    float_ = sa.Column(sa.Float)
    string_ = sa.Column(sa.String)
    date_ = sa.Column(sa.Date)
    datetime_ = sa.Column(sa.DateTime)
    numeric_ = sa.Column(sa.Numeric)
    unicode_ = sa.Column(sa.Unicode)
    unicodetext_ = sa.Column(sa.UnicodeText)
    timestamp = sa.Column(sa.TIMESTAMP)

    def __eq__(self, other):
        return (self.boolean == other.boolean and
                self.big_integer == other.big_integer and
                self.integer == other.integer and
                self.float_ == other.float_ and
                self.string_ == other.string_ and
                self.date_ == other.date_ and
                self.datetime_ == other.datetime_ and
                self.numeric_ == other.numeric_ and
                self.unicode_ == other.unicode_ and
                self.unicodetext_ == other.unicodetext_ and
                self.timestamp == other.timestamp
                )


class IndexBaseTestModel(Base, IndexBase):
    __tablename__ = 'IndexBaseTestModel'
    __table_args__ = AUTO_INCREMENT,
    id = sa.Column(sa.Integer, primary_key=True)


class TimestampBaseTestModel(Base, ActionBase, TimestampBase):
    __tablename__ = 'TimestampBaseTestModel'
    __table_args__ = AUTO_INCREMENT,
    id = sa.Column(sa.Integer, primary_key=True)


class LogicalDeleteBaseTestModel(Base, LogicalDeleteBase):
    __tablename__ = 'LogicalDeleteBaseTestModel'
    __table_args__ = AUTO_INCREMENT,
    id = sa.Column(sa.Integer, primary_key=True)


# use case testing model


class User(Base, SmartBase):
    __tablename__ = 'User'
    __table_args__ = AUTO_INCREMENT,
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Unicode)
    organization_id = sa.Column(sa.Integer, sa.ForeignKey('Organization.id'),
                                nullable=False)
    organization = sa_orm.relationship('Organization')


class Organization(Base, PowerBase):
    __tablename__ = 'Organization'
    __table_args__ = AUTO_INCREMENT,
    id = sa.Column(sa.Integer, primary_key=True)

create_all()
