from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from tables import Base

#An object the Alignment table
class Alignments(Base):

    #The name of the table
    __tablename__ = 'Alignments'

    #The columns of the table
    ID = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)


    #A to string funciton
    def __repr__(self):
        return (f"{self.ID}, {self.name}")
