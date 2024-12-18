from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from tables import Base

#A table representing the race
class Races(Base):

    #The name of the table
    __tablename__ = 'Races'

    #Columns associated with the race
    ID = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)

    #A race also has an alignment i.e all faries are neutral
    alignment_id = Column(Integer, ForeignKey('Alignments.ID'))

    alignment = relationship("Alignments", foreign_keys=[alignment_id])

    #A to string method
    def __repr__(self):
        return (f"{self.ID}, {self.name}, {self.alignment_id}")
