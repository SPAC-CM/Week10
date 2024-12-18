from sqlalchemy import Column, Integer, String, ForeignKey, TEXT
from sqlalchemy.orm import sessionmaker, relationship
from tables import Base

class Demons(Base):
    __tablename__ = 'Demons'

    ID = Column(Integer, primary_key=True)
    name = Column(String, nullable = False)
    level = Column(Integer, nullable = False)
    image = Column(TEXT(20000), nullable = True)
    alignment_id = Column(Integer, ForeignKey('Alignments.ID'))
    race_id = Column(Integer, ForeignKey('Races.ID'))

    alignment = relationship("Alignments", foreign_keys=[alignment_id])
    race = relationship("Races", foreign_keys=[race_id])

    def __repr__(self):
        return (f"{self.ID}, {self.name}, {self.level}, {self.image}, {self.alignment_id}, {self.race_id}")
