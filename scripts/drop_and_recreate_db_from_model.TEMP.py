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

from screencloud import sql
from screencloud.sql import models

# From https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/DropEverything
def drop_everything(engine):
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


@click.command()
def main():
    engine = sql.engine
    click.echo(' DANGER '.center(80, '='))
    click.echo(engine.url.__repr__().center(80))
    click.echo(''.center(80, '-'))
    click.confirm('Are you REALLY sure you want to drop the db?', abort=True)
    click.echo('You asked for it.  Dropping and re-creating all tables...')
    drop_everything(engine)
    models.Base.metadata.create_all(bind=engine)
    click.echo(''.center(80, '='))

if __name__ == '__main__':
    main()
