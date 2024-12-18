from sqlalchemy import Table, Column, TEXT, Float, Integer, String, MetaData, ForeignKeyConstraint
from sqlalchemy.sql.schema import MetaData
def create_tables(metadata : MetaData):

    Alignments = Table(
            'Alignments', metadata,
            Column("ID", Integer, primary_key=True, autoincrement=True),
            Column("name", String(15), nullable=False)
    )

    Races = Table(
            'Races', metadata,
            Column("ID", Integer, primary_key=True, autoincrement=True),
            Column("name", String(15), nullable=False),
            Column("alignment_id", Integer, nullable=False),
            ForeignKeyConstraint(["alignment_id"],["Alignments.ID"]),
    )

    Demons = Table(
            'Demons', metadata,
            Column("ID", Integer, primary_key=True, autoincrement=True),
            Column("name", String(15), nullable=False),
            Column("level", Integer, nullable=False),
            Column("image", TEXT(20000) ,nullable=True),
            Column("alignment_id", Integer, nullable=False),
            Column("race_id", Integer, nullable=False),
            ForeignKeyConstraint(["alignment_id"],["Alignments.ID"]),
            ForeignKeyConstraint(["race_id"],["Races.ID"])
    )

    return metadata
