from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from tables import Base

class Alignments(Base):
    __tablename__ = 'Alignments'

    ID = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)


    def __repr__(self):
        return (f"{self.ID}, {self.name}")
