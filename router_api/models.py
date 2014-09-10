import uuid
from datetime import datetime

from sqlalchemy import Table, Column, DateTime, CHAR, Index
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import backref, relationship

Base = declarative_base()

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

UUID = CHAR(32)

def generate_uuid():
    return uuid.uuid4().hex


# -----------------------------------------------------------------------------
# Mixins
# -----------------------------------------------------------------------------

class IdentifierMixin(object):
    id = Column(UUID, primary_key=True, default=generate_uuid)


class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    deleted_at = Column(DateTime)

    # hack to move the columns to the end
    created_at._creation_order = 9997
    updated_at._creation_order = 9998
    deleted_at._creation_order = 9999


class HasAccountMixin(object):
    @declared_attr
    def account_id(cls):
        return Column('account_id', ForeignKey('accounts.id'))

    @declared_attr
    def account(cls):
        return relationship('Account')


class HasNetworkMixin(object):
    @declared_attr
    def network_id(cls):
        return Column('network_id', ForeignKey('networks.id'))

    @declared_attr
    def network(cls):
        return relationship('Network')


# -----------------------------------------------------------------------------
# Associations
# -----------------------------------------------------------------------------

accounts_users_table = Table(
    'accounts_users',
    Base.metadata,
    Column('account_id', UUID, ForeignKey('accounts.id')),
    Column('user_id', UUID, ForeignKey('users.id'))
)


# -----------------------------------------------------------------------------
# Models (TODO: indexes)
# -----------------------------------------------------------------------------

# Base for anything generically useful
class ModelBase(Base):
    __abstract__ = True


class Account(IdentifierMixin, TimestampMixin, ModelBase):
    __tablename__ = 'accounts'

    users = relationship(
        'User',
        secondary=accounts_users_table,
        backref='accounts'
    )


class User(IdentifierMixin, TimestampMixin, ModelBase):
    __tablename__ = 'users'

    # accounts via backref on Account


class Network(IdentifierMixin, TimestampMixin, HasAccountMixin, HasNetworkMixin, ModelBase):
    __tablename__ = 'networks'


class Screen(IdentifierMixin, TimestampMixin, HasAccountMixin, HasNetworkMixin, ModelBase):
    __tablename__ = 'screens'


class App(IdentifierMixin, TimestampMixin, HasAccountMixin, ModelBase):
    __tablename__ = 'apps'


class AppInstance(IdentifierMixin, TimestampMixin, ModelBase):
    __tablename__ = 'app_instances'
