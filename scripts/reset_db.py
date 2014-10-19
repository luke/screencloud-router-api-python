import sys, os
sys.path.append(os.path.realpath(os.pardir))

import click
from sqlalchemy.engine import reflection
from sqlalchemy import create_engine
from sqlalchemy.schema import (
    MetaData,
    Table,
    DropTable,
    ForeignKeyConstraint,
    DropConstraint,
    )

from screencloud import sql as sc_sql
from screencloud import redis as sc_redis
from screencloud.sql import models as sc_sql_models
from screencloud.redis import keys as sc_redis_keys


# From https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/DropEverything
def sql_drop_everything(engine):
    conn = engine.connect()
    trans = conn.begin()
    inspector = reflection.Inspector.from_engine(engine)

    # Gather all data first before dropping anything.  Some DBs lock after
    # things have been dropped in a transaction.
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((),(),name=fk['name'])
            )
        t = Table(table_name,metadata,*fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()


@click.group()
def cli():
    """
    Reset all data and structure of the dbs.
    """
    click.echo(' DANGER '.center(80, '='))


@cli.command('sql')
def sql():
    """
    Drop and recreate all tables in the sql db.
    """
    engine = sc_sql.engine
    click.echo(engine.url.__repr__().center(80))
    click.echo(''.center(80, '-'))
    click.confirm('Are you REALLY sure you want to drop the db?', abort=True)
    click.echo('You asked for it.  Dropping and re-creating all tables...')
    sql_drop_everything(engine)
    sc_sql_models.Base.metadata.create_all(bind=engine)
    click.echo(' Done '.center(80, '='))


@cli.command('redis')
def redis():
    """
    Delete all keys known to the screencloud api from the redis db.
    """
    client = sc_redis.client_factory()
    key_matcher = sc_redis_keys.PREFIX + '*'
    click.echo(sc_redis.config['REDIS_DB_URI'].center(80))
    click.echo(''.center(80, '-'))
    click.confirm(
        'Are you REALLY sure you want to delete the keys "%s"' % key_matcher,
        abort=True
    )
    click.echo('You asked for it.  Deleting all keys (inefficiently)...')
    for key in client.keys(key_matcher):
        client.delete(key)
    click.echo(' Done '.center(80, '='))


if __name__ == '__main__':
    cli()
