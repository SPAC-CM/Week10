from sqlalchemy import create_engine, MetaData, select, delete
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.orm.decl_api import DeclarativeMeta
from tables.Tables import *
from tables.table_factory import *

#The ORM connection between the database and API
class SQL_Manager(object):

    #Insures that no other instances of the ORM can exist at any given point
    _instance = None
    def __new__(cls):
        if not isinstance(cls._instance,cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    #Creates the manager and initializes the connection
    def __init__(self):
        self.engine_uri = f"mysql+pymysql://root:SPAC-SQLBOI2024@127.0.0.1/SMT"
        engine = create_engine(self.engine_uri)
        self.metadata = create_tables(MetaData())
        self.metadata.create_all(engine)
        Session = sessionmaker(bind = create_engine(self.engine_uri))
        self.session = Session()
        self.engine = engine
        self.create_procedures()

    def add_item(self, item : DeclarativeMeta):
        self.session.add(item)
        self.session.commit()

    def get_demon_query(self,parametor : str, item_value : str):
        match parametor.lower():
            case "id":
                return self.session.query(Demons).filter(Demons.ID == int(item_value))
            case "name":
                return self.session.query(Demons).filter(Demons.name == item_value)
            case "level":
                return self.session.query(Demons).filter(Demons.level == int(item_value))
            case "alignment":
                return self.session.query(Demons).filter(Demons.alignment_id == int(item_value))
            case "race":
                return self.session.query(Demons).filter(Demons.race_id == int(item_value))
            case _:
                raise Exception("Parametor not recognized for demons")

    def get_alignment_query(self,parametor : str, item_value : str):
        match parametor.lower():
            case "id":
                return self.session.query(Alignments).filter(Alignments.ID == int(item_value))
            case "name":
                return self.session.query(Alignments).filter(Alignments.name == item_value)
            case _:
                raise Exception("Parametor not recognized for aligments")

    def get_race_query(self, parametor : str, item_value : str):
        match parametor.lower():
            case "id":
                return self.session.query(Races).filter(Races.ID == int(item_value))
            case "name":
                return self.session.query(Races).filter(Races.name == item_value)
            case "alignment_id":
                return self.session.query(Races).filter(Races.alignment_id == int(item_value))

    def get_query(self, table_name : str, parametor : str, item_value : str):
        try:
            match table_name.lower():
                case "demon" | "demons":
                    return self.get_demon_query(parametor,item_value)
                case "race" | "races":
                    return self.get_race_query(parametor,item_value)
                case "alignment" | "alignments":
                    return self.get_race_query(parametor,item_value)
                case _:
                    raise Exception("Table name not recognized")
        except Exception as e:
            print(e)

    def get_item(self,table_name : str,parametor : str,item_value : str):
        item = self.get_query(table_name,parametor,item_value)
        return item.all()

    def multi_query(self,**kwargs):
        queries = []

        for key in kwargs.keys():
            table, parametor, item_value = kwargs[key]
            queries.append(self.get_query(table,parametor, item_value))

        item = queries[0]
        for i in range(1,len(queries)):
            item = item.intersect(queries[i])
        return item.all()

    def get_table(self, table_name : str):
        try:
            match table_name.lower():
                case "demon" | "demons":
                    cmd = select(Demons)
                case "alignment" | "alignments":
                    cmd = select(Alignments)
                case "race" | "races":
                    cmd = select(Races)
                case _:
                    raise Exception("Table name not recognized")
            table = self.session.execute(cmd)
            return table
        except Exception as e:
            print(e)

    def get_keys(self,table_name : str):
        try:
            match table_name.lower():
                case "demon" | "demons":
                    return self.metadata.tables["Demons"].columns.keys()
                case "alignment" | "alignments":
                    return self.metadata.tables["Alignments"].columns.keys()
                case "race" | "races":
                    return self.metadata.tables["Races"].columns.keys()
                case _:
                    raise Exception("Table name not recognized")
        except Exception as e:
            print(e)

    def update_race(self, item, parametor: str, value : str):
        match parametor.lower():
            case "name":
                item.update({Races.name: value})
            case "alignment":
                item.update({Races.alignment_id:int(value)})
            case _:
                raise Exception("Parametor not recognized for race")
        self.session.commit()

    def update_alignment(self, item, parametor: str, value : str):
        match parametor.lower():
            case "name":
                item.update({Alignments.name : value})
            case _:
                raise Exception("Parametor not recognized for alignment")
        self.session.commit()

    def update_demon(self,item,parametor : str, value):
        match parametor.lower():
            case "name":
                item.update({Demons.name : str(value)})
            case "level":
                item.update({Demons.level : int(value)})
            case "alignment":
                item.update({Demons.alignment_id : int(value)})
            case "race":
                item.update({Demons.race_id : int(value)})
            case "image":
                item.update({Demons.image : value})
            case _:
                raise Exception("Parametor not recognized for demons")
        self.session.commit()

    def delete_item(self,table_name : str, parametor : str, value : str):
        entry = self.get_query(table_name,parametor,value)
        entry.delete()
        self.session.commit()

    def update_item(self, table_name : str, parametor : str, item_value : str, update_parametor : str, update_value):
        item = self.get_query(table_name,parametor,item_value)
        try:
            match table_name.lower():
                case "demon" | "demons":
                    return self.update_demon(item, update_parametor,update_value)
                case "alignment" | "alignments":
                    return self.update_alignment(item, update_parametor,update_value)
                case "race" | "races":
                    return self.update_race(item, update_parametor, update_value)
                case _:
                    raise Exception("Table name not recognized")

            self.session.commit()
        except Exception as e:
            print(e)

    def create_procedures(self):
        file_name = os.path.join("utils","stored_procedures.sql")
        with open(file_name, 'r') as f:
            queries = f.read().split("--#--new--#")
            for query in queries:
                self.session.execute(sqlalchemy.text(query))
            self.session.commit()

    def get_image_length(self,demon_id : str):
        return self.session.execute(sqlalchemy.text(f"CALL get_image_length({int(demon_id)},@length)")).mappings().all()[0]['LENGTH(image)']


    def get_chonked_image(self,demon_id : str):
        length = self.get_image_length(demon_id)
        chonk_size = 255
        chonks = int(length/chonk_size)
        rest = length % chonk_size 
        i = 0
        image = ""
        index = 1
        while i < chonks:
            image += self.session.execute(sqlalchemy.text(f"CALL get_chonked_image({int(demon_id)},{index},{chonk_size},@im)")).mappings().all()[0]['SUBSTRING(image,start_index,end_index)']
            index += chonk_size
            i+=1

        image += self.session.execute(sqlalchemy.text(f"CALL get_chonked_image({int(demon_id)},{index},{rest},@im)")).mappings().all()[0]['SUBSTRING(image,start_index,end_index)']

        return image

if __name__ == "__main__":
    manager = SQL_Manager()
    #manager.login("root","SPAC-SQLBOI2024","127.0.0.1")
    factory = Factory()
    alignment_dict = {"table_name":"alignment","name" : "neutral"}
    race_dict = {"table_name":"race" ,"name" : "Fairy", "alignment": 1}
    demon_dict = {"table_name":"demon","name" : "Jack Frost", "level": 12, "alignment": 1, "race": 1}
    #alignment = factory.create_element(data = alignment_dict)
    #race = factory.create_element(data = race_dict)
    #demon = factory.create_element(data = demon_dict)
    #manager.add_item(alignment)
    #manager.add_item(race)
    #manager.add_item(demon)
    #manager.update_item("demon","id","1","name","Jack Frost")
    image = manager.get_chonked_image("1")
    print(image)
