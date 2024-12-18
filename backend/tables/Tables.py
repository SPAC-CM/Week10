from sqlalchemy import Table, Column, TEXT, Float, Integer, String, MetaData, ForeignKeyConstraint
from sqlalchemy.sql.schema import MetaData

#Creates the actual tables along with foreign key constraint.
#It both creates to table for the ORM but also for the database if there are no tables
#The metadata is the ORM intern store for table definitions
def create_tables(metadata : MetaData):

    #The alignment table
    Alignments = Table(
            'Alignments', metadata,
            Column("ID", Integer, primary_key=True, autoincrement=True),
            Column("name", String(15), nullable=False)
    )

    #The race table
    Races = Table(
            'Races', metadata,
            Column("ID", Integer, primary_key=True, autoincrement=True),
            Column("name", String(15), nullable=False),
            Column("alignment_id", Integer, nullable=False),
            ForeignKeyConstraint(["alignment_id"],["Alignments.ID"]),
    )

    #The demon table
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
