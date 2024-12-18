from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from tables import Base

class Races(Base):
    __tablename__ = 'Races'

    ID = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    alignment_id = Column(Integer, ForeignKey('Alignments.ID'))

    alignment = relationship("Alignments", foreign_keys=[alignment_id])

    def __repr__(self):
        return (f"{self.ID}, {self.name}, {self.alignment_id}")
