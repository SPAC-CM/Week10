from tables.Demons import *
from tables.Alignments import *
from tables.Races import *
from sqlalchemy.orm.decl_api import DeclarativeMeta

class Factory(object):

    def create_race(self, name : str, alignment : int) -> DeclarativeMeta:
        race : DeclarativeMeta = Races()
        race.name = name
        race.alignment_id = alignment
        return race

    def create_alignment(self, name : str) -> DeclarativeMeta:
        alignment : DeclarativeMeta = Alignments()
        alignment.name = name
        return alignment


    def create_demon(self,name : str, level : int, alignment : int, race : int) -> DeclarativeMeta:
        demon : DeclarativeMeta = Demons()
        demon.name = name
        demon.level = level
        demon.alignment_id = alignment
        demon.race_id = race
        return demon

    def create_element(self, data : dict) -> DeclarativeMeta:
        try:
            table_name = data["table_name"]
            match table_name.lower():
                case "demon":
                    return self.create_demon(data["name"],data["level"],data["alignment"],data["race"])
                case "alignment":
                    return self.create_alignment(data["name"])
                case "race":
                    return self.create_race(data["name"], data["alignment"])
                case _:
                    raise Exception("Table name not recognized")

        except Exception as e:
            print(e)

if __name__ == "__main__":
    factory = Factory()
    demon_data = {"name": "test"}
    facotry.create_element("demon",demon_data)
