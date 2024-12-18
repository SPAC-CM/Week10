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
    _connected : bool = False
    def __init__(self):
        if not self._connected:
            self.engine_uri = f"mysql+pymysql://root:SPAC-SQLBOI2024@127.0.0.1/SMT"
            engine = create_engine(self.engine_uri)
            self.metadata = create_tables(MetaData())
            self.metadata.create_all(engine)
            Session = sessionmaker(bind = create_engine(self.engine_uri))
            self.session = Session()
            self.engine = engine
            self.create_procedures()
            self._connected = True

    #Adds an item to the database
    def add_item(self, item : DeclarativeMeta):
        self.session.add(item)
        self.session.commit()

    #Gets the query associated with the demon table
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

    #Gets the query associated with the alignment table
    def get_alignment_query(self,parametor : str, item_value : str):
        match parametor.lower():
            case "id":
                return self.session.query(Alignments).filter(Alignments.ID == int(item_value))
            case "name":
                return self.session.query(Alignments).filter(Alignments.name == item_value)
            case _:
                raise Exception("Parametor not recognized for aligments")

    #Gets the query associated with the race table
    def get_race_query(self, parametor : str, item_value : str):
        match parametor.lower():
            case "id":
                return self.session.query(Races).filter(Races.ID == int(item_value))
            case "name":
                return self.session.query(Races).filter(Races.name == item_value)
            case "alignment_id":
                return self.session.query(Races).filter(Races.alignment_id == int(item_value))

    #Single call to get a query for a table
    def get_query(self, table_name : str, parametor : str, item_value : str):
        try:
            #Checks which table the query is for
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
    
    #Gets items from the a table with the name table_name.
    def get_item(self,table_name : str,parametor : str,item_value : str):
        #Gets the query
        item = self.get_query(table_name,parametor,item_value)

        #Gets all elements in the query
        return item.all()

    #Function to do multiple querries on one go. The kwargs must be on the form kwarg_1 = (table,parametor,item_value)
    def multi_query(self,**kwargs):
        queries = []

        #Goes trhu all item in the kwargs dir
        for key in kwargs.keys():
            table, parametor, item_value = kwargs[key]
            queries.append(self.get_query(table,parametor, item_value))
        
        #The item can be seen as all elements that fullfill all queries i.e you want to find all demons that are level 12 and of a specific race.
        #Thus the final element is the intersection between all demons with level of 12 and all demons of a specific race
        item = queries[0]
        for i in range(1,len(queries)):
            item = item.intersect(queries[i])
        return item.all()

    #Gets a table
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

    #Gets the keys of a specific table
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

    #Fucntion to update the race table. The item value is the query item we want to update
    def update_race(self, item, parametor: str, value : str):
        match parametor.lower():
            case "name":
                item.update({Races.name: value})
            case "alignment":
                item.update({Races.alignment_id:int(value)})
            case _:
                raise Exception("Parametor not recognized for race")
        self.session.commit()

    #Fucntion to update the alignment table. The item value is the query item we want to update
    def update_alignment(self, item, parametor: str, value : str):
        match parametor.lower():
            case "name":
                item.update({Alignments.name : value})
            case _:
                raise Exception("Parametor not recognized for alignment")
        self.session.commit()

    #Fucntion to update the demon table. The item value is the query item we want to update
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
    
    #Genaric function to update a table
    def update_item(self, table_name : str, parametor : str, item_value : str, update_parametor : str, update_value):

        #Gets an item where the item_value matches the value of the column with name parameter
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

    #Function to delete items from the database
    def delete_item(self,table_name : str, parametor : str, value : str):
        entry = self.get_query(table_name,parametor,value)
        entry.delete()
        self.session.commit()

    #To get image I use some sub queries and specific functions on the column like SUBSTRING to make it less messy these queries are made as a stored procedure
    def create_procedures(self):

        #Reads from the stored_procedures file found in utils folder
        file_name = os.path.join("utils","stored_procedures.sql")
        with open(file_name, 'r') as f:
            queries = f.read().split("--#--new--#")
            for query in queries:
                self.session.execute(sqlalchemy.text(query))
            self.session.commit()

    #Function to get the image length. Uses the stored procedures
    def get_image_length(self,demon_id : str):
        return self.session.execute(sqlalchemy.text(f"CALL get_image_length({int(demon_id)},@length)")).mappings().all()[0]['LENGTH(image)']


    #Function to get the image in chonks. Uses the stored procedures
    def get_chonked_image(self,demon_id : str):

        #Gets the length of the image
        length = self.get_image_length(demon_id)

        #The size of the chunk is 255 char
        chonk_size = 255

        #Defines the number of chonks the image has
        chonks = int(length/chonk_size)

        #The lenght of the image is probably not a multiple of 255, so we define the rest chonk size if any
        rest = length % chonk_size 
        i = 0
        
        #Creates an empy string for the image
        image = ""

        #SQL substrings start at position 1 and not 0
        index = 1
        while i < chonks:
            image += self.session.execute(sqlalchemy.text(f"CALL get_chonked_image({int(demon_id)},{index},{chonk_size},@im)")).mappings().all()[0]['SUBSTRING(image,start_index,end_index)']
            index += chonk_size
            i+=1

        #Gets the rest of the image if it is not a multiple of 255. The sql return an empty string if end_index = 0 aka the image is a multiple of 255
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
