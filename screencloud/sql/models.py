import uuid
from datetime import datetime
from collections import namedtuple

from sqlalchemy import (
    Table, Column, DateTime, CHAR, Index, String, Text, and_, ForeignKey,
)
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy.orm import (
    backref, relationship, foreign, column_property, remote
)
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
        return relationship('Network', backref=cls.__tablename__)


class AssociatedAccountsMixin(object):
    @declared_attr
    def _account_associations(cls):
        # Value we use for the 'related_type' field of the account_associations
        # table.
        related_type = cls.__tablename__

        # Name of the attribute we attach to the AccountAssociation to
        # reference objects of the class we're being mixed-into.
        # E.g. account_association.related_obj_user
        proxy_related_attr_name = 'related_obj_%s' % cls.__name__.lower()

        # Add attributes onto the Account object so that we can use the
        # account association proxy stuff from that side too.
        # E.g. account.users.append(u)
        setattr(
            Account,
            '_%s_associations' % related_type,
            relationship(
                'AccountAssociation',
                primaryjoin=lambda: Account.id==AccountAssociation.account_id,
                foreign_keys=[AccountAssociation.account_id],
                cascade='all, delete-orphan'
            )
        )
        setattr(
            Account,
            related_type,
            association_proxy(
                '_%s_associations' % related_type,
                proxy_related_attr_name,
                creator=AccountAssociation.creator(
                    related_type,
                    proxy_related_attr_name
                ),
            )
        )


        # Add the accounts attribute to this mixed-into class, using the
        # accounts association_proxy.
        cls.accounts = association_proxy(
            '_account_associations',
            'account',
            creator=AccountAssociation.creator(related_type, 'account')
        )

        return relationship(
            'AccountAssociation',
            primaryjoin=lambda: cls.id==AccountAssociation.related_id,
            foreign_keys=[AccountAssociation.related_id],
            backref=backref(proxy_related_attr_name, uselist=False),
            cascade='all, delete-orphan'
        )


# -----------------------------------------------------------------------------
# Associations
# -----------------------------------------------------------------------------

# Anything can be related to an account (or multiple accounts)
class AccountAssociation(Base):
    __tablename__ = "account_associations"

    account_id = Column(UUID, primary_key=True)
    related_type = Column(String, primary_key=True)
    related_id = Column(UUID, primary_key=True)

    @classmethod
    def creator(cls, related_type, attr):
        """
        Provide a 'creator' function to use with the association proxy.
        """
        def create_account_association(obj):
            oa = AccountAssociation(related_type=related_type)
            setattr(oa, attr, obj)
            return oa

        return lambda obj: create_account_association(obj)




# -----------------------------------------------------------------------------
# Models (TODO: indexes)
# -----------------------------------------------------------------------------

class ModelBase(Base):
    """
    Base SQLAlchemy Model for anything generically useful.
    """
    __abstract__ = True

    def _to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Account(IdentifierMixin, TimestampMixin, ModelBase):
    """
    An account in the system.

    This is the main access control object.  Most other objects in the system
    are associated to accounts via the AssociatedAccountsMixin.
    """
    __tablename__ = 'accounts'

    name = Column(String)

    associations = relationship(
        'AccountAssociation',
        primaryjoin=lambda: Account.id==AccountAssociation.account_id,
        foreign_keys=[AccountAssociation.account_id],
        backref=backref('account'),
        cascade='all, delete-orphan'
    )


class User(IdentifierMixin, TimestampMixin, AssociatedAccountsMixin, ModelBase):
    """
    A user in the system.
    """
    __tablename__ = 'users'

    name = Column(String)
    email = Column(String)


class UserIdentity(TimestampMixin, ModelBase):
    """
    A way for a user to identify themselves.

    E.g:
        UserIdentity(
            type=basic,
            identifier='a-username',
            data={"password": "some-hashed-secret"}
        )

        UserIdentity(
            type=google,
            identifier='some-google-identifier',
            data={...}
        )
    """
    __tablename__ = 'user_identities'

    type = Column(String, primary_key=True)
    identifier = Column(String, primary_key=True)
    data = Column(JSON)
    user_id = Column(UUID, ForeignKey(User.id), nullable=False)
    user = relationship(
        User,
        backref=backref('identities', cascade='all, delete-orphan')
    )

    @classmethod
    def _construct_pk_tuple(cls, type, identifier):
        """
        Helper to retrieve a primary key tuple that can be used with a
        session.query(UserIdentity).get(pk_tuple) request.  It's here because
        the order of keys in the tuple depends on the order the primary keys are
        specified in this class.
        """
        return type, identifier
    


class Player(IdentifierMixin, TimestampMixin, ModelBase):
    """
    A player represents the primary software that is run on a screen and
    interacts with screencloud to load apps etc.
    """
    __tablename__ = 'players'

    name = Column(String)
    version = Column(String)
    url = Column(String)


class Remote(
    IdentifierMixin, TimestampMixin, AssociatedAccountsMixin, ModelBase
):
    """
    A remote is an app that a user uses to interact with screencloud.

    E.g. The ScreenBox iOS app.
    """
    __tablename__ = 'remotes'

    name = Column(String)


class Network(
    IdentifierMixin, TimestampMixin, AssociatedAccountsMixin, ModelBase
):
    """
    A network is primarily a grouping mechanism.  Used by screens and the apps
    that can play on them.

    Networks are hierarchical (tree structure) via the parent/children
    attributes.
    """
    __tablename__ = 'networks'

    name = Column(String)

    parent_id = Column(UUID, ForeignKey('networks.id'))
    parent = relationship(
        'Network',
        primaryjoin='Network.parent_id == remote(Network.id)',
        backref=backref('children', cascade='all, delete-orphan')
    )

    player_id = Column(UUID, ForeignKey(Player.id))
    player = relationship(Player, backref=backref('networks'))


class App(IdentifierMixin, TimestampMixin, HasNetworkMixin, ModelBase):
    """
    An app is software that is run on a screen (via a player).
    """
    __tablename__ = 'apps'

    name = Column(String)
    keywords = Column(ARRAY(String))
    description = Column(Text)
    setup_link = Column(String)
    edit_link = Column(String)


class AppInstance(
    IdentifierMixin, TimestampMixin, HasNetworkMixin, ModelBase
):
    """
    An app + config specific to a user.
    """
    __tablename__ = 'app_instances'

    app_id = Column(UUID, ForeignKey(App.id))
    app = relationship(App, backref=backref('app_instances'))
    settings = Column(JSON)
