import uuid
from datetime import datetime

from sqlalchemy import (
    Table, Column, DateTime, CHAR, Index, String, and_, ForeignKey
)
from sqlalchemy.orm import backref, relationship, foreign, column_property
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.associationproxy import association_proxy

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

class NameMixin(object):
    name = Column(String)

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


class HasNetworkMixin(object):
    @declared_attr
    def network_id(cls):
        return Column('network_id', ForeignKey('networks.id'))

    @declared_attr
    def network(cls):
        return relationship('Network')


class IsOwnedMixin(object):
    @declared_attr
    def _account_associations(cls):
        # Value we use for the 'related_type' field of the ownerships table.
        related_type = cls.__tablename__

        # Name of the attribute we attach to the OwnershipAssociation to
        # reference objects of the class we're being mixed-into.
        # E.g. ownership_association.related_obj_user
        proxy_related_attr_name = 'related_obj_%s' % cls.__name__.lower()

        # Add attributes onto the Account object so that we can use the
        # ownership association proxy stuff from that side too.
        # E.g. account.users.append(u)
        setattr(
            Account,
            '_%s_associations' % related_type,
            relationship(
                'OwnershipAssociation',
                primaryjoin=lambda: Account.id==OwnershipAssociation.account_id,
                foreign_keys=[OwnershipAssociation.account_id],
                cascade='all, delete-orphan'
            )
        )
        setattr(
            Account,
            related_type,
            association_proxy(
                '_%s_associations' % related_type,
                proxy_related_attr_name,
                creator=OwnershipAssociation.creator(
                    related_type, 
                    proxy_related_attr_name
                )
            )
        )


        # Add the accounts attribute to this mixed-into class, using the
        # ownerships association_proxy.
        cls.accounts = association_proxy(
            '_account_associations',
            'account',
            creator=OwnershipAssociation.creator(related_type, 'account')
        )

        return relationship(
            'OwnershipAssociation',
            primaryjoin=lambda: cls.id==OwnershipAssociation.related_id,
            foreign_keys=[OwnershipAssociation.related_id],
            backref=backref(proxy_related_attr_name, uselist=False),
            cascade='all, delete-orphan'
        )


# -----------------------------------------------------------------------------
# Associations
# -----------------------------------------------------------------------------

# Anything can be owned by an account (or multiple accounts)
class OwnershipAssociation(Base):
    __tablename__ = "ownerships"

    account_id = Column(UUID, primary_key=True)
    related_type = Column(String, primary_key=True)
    related_id = Column(UUID, primary_key=True)

    @classmethod
    def creator(cls, related_type, attr):
        """Provide a 'creator' function to use with the association proxy."""

        def create_ownership_association(obj):
            oa = OwnershipAssociation(related_type=related_type)
            setattr(oa, attr, obj)
            return oa

        return lambda obj: create_ownership_association(obj)




# -----------------------------------------------------------------------------
# Models (TODO: indexes)
# -----------------------------------------------------------------------------

# Base for anything generically useful.
class ModelBase(Base):
    __abstract__ = True

    # TODO: __declare_last__ isn't being called, I'm probably doing something silly
    # @classmethod
    # def __declare_last__(cls):
    #     import logging
    #     logging.warn(cls)
    #     # Merge together all the mapper_args and table_args from the mixins.
    #     cls.__mapper_args__ = dict()
    #     cls.__table_args__ = dict()
    #     Hmmm -- this won't work anyway, t is a type
    #     for t in reversed(cls.__mro__):
    #         if '__mapper_args__' in t:
    #             cls.__mapper_args__.update(t.__mapper_args__)
    #         if '__table_args__' in t:
    #             cls.__table_args__.update(t.__table_args__)


class Account(IdentifierMixin, TimestampMixin, NameMixin, ModelBase):
    __tablename__ = 'accounts'

    ownerships = relationship(
        'OwnershipAssociation',
        primaryjoin=lambda: Account.id==OwnershipAssociation.account_id,
        foreign_keys=[OwnershipAssociation.account_id],
        backref=backref('account'),
        cascade='all, delete-orphan'
    )


class User(IdentifierMixin, TimestampMixin, IsOwnedMixin, NameMixin, ModelBase):
    __tablename__ = 'users'


class Network(IdentifierMixin, TimestampMixin, IsOwnedMixin, HasNetworkMixin, ModelBase):
    __tablename__ = 'networks'


class Screen(IdentifierMixin, TimestampMixin, IsOwnedMixin, HasNetworkMixin, ModelBase):
    __tablename__ = 'screens'


class Channel(IdentifierMixin, TimestampMixin, IsOwnedMixin, ModelBase):
    __tablename__ = 'channels'


class App(IdentifierMixin, TimestampMixin, IsOwnedMixin, NameMixin, ModelBase):
    __tablename__ = 'apps'


class AppInstance(IdentifierMixin, TimestampMixin, IsOwnedMixin, HasNetworkMixin, ModelBase):
    __tablename__ = 'app_instances'