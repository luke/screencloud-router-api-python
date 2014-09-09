import uuid
from datetime import datetime

from sqlalchemy import Table, Column, DateTime, CHAR
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
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
# Models
# -----------------------------------------------------------------------------

class Account(IdentifierMixin, TimestampMixin, Base):
    __tablename__ = 'accounts'

    users = relationship(
        'User',
        secondary=accounts_users_table,
        backref='accounts'
    )


class User(IdentifierMixin, TimestampMixin, Base):
    __tablename__ = 'users'

    # accounts via backref on Account
    


class Network(IdentifierMixin, TimestampMixin, Base):
    __tablename__ = 'networks'


class Screen(IdentifierMixin, TimestampMixin, Base):
    __tablename__ = 'screens'


class App(IdentifierMixin, TimestampMixin, Base):
    __tablename__ = 'apps'


class AppInstance(IdentifierMixin, TimestampMixin, Base):
    __tablename__ = 'app_instances'




# type Identified struct {
#       Id string `gorm:"primary_key:yes" sql:"type:uuid primary key default uuid_generate_v4()" json:"id" binding:"required"`
# }

# type Timestamped struct {
#       CreatedAt time.Time `json:"created_at"`
#       UpdatedAt time.Time `json:"updated_at"`
#       DeletedAt time.Time `json:"deleted_at"`
# }

# type Associated struct {
#       Owner     UUID     `json:"owner" binding:"required"`
#       Group     []string `json:"group"`
#       AccountId UUID     `json:"account_id"`
# }

# type Named struct {
#       Name string `json:"name" binding:"required"`
# }

# type Located struct {
#       PlaceId UUID `json:"place_id"`
# }

# type Networked struct {
#       NetworkId string `sql:"type:uuid" json:"network_id"`
# }
