from sqlalchemy import Column, Integer, String, ForeignKey, TEXT
from sqlalchemy.orm import sessionmaker, relationship
from tables import Base

#A class representing the demon table
class Demons(Base):

    #The table name
    __tablename__ = 'Demons'

    #The columns of the table
    ID = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    level = Column(Integer, nullable = False)

    #Image is nullable just so that it is not required to give an image along with the creation of the element
    image = Column(TEXT(20000), nullable = True)

    #A demon must have an alignment and a race associated with it. Thus we have some foreign key constraints for the ID's of the other two tables
    alignment_id = Column(Integer, ForeignKey('Alignments.ID'))
    race_id = Column(Integer, ForeignKey('Races.ID'))

    #Explicit foreign key constraint
    alignment = relationship("Alignments", foreign_keys=[alignment_id])
    race = relationship("Races", foreign_keys=[race_id])
    
    #A to string function
    def __repr__(self):
        return (f"{self.ID}, {self.name}, {self.level}, {self.image}, {self.alignment_id}, {self.race_id}")
