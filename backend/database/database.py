import asyncio
import asyncpg
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column, Session

#in teh table for any new row increase the textbook_id by one. insert a string which links to the pdf name
#I want the size of teh converted file into tc. So we take the file size of the txt
#keep a date tracker 
#what cite did u get it from. no need for link 

###also want to create a research paper table. Use a rearch paper id and just uodate it by one when we actually end u\
#adding it to the database. Again put the name as a string. this will be taken from teh text scraper. Size will be converted 
#into a txt. add the date which is autoamticalley updated. And then where u got it form which you migth have to do manaually

#also need an iamge_table. In this table we are going to put the image_id, the date, and the size. We will aslo add where 
#the image came from or what paper it came from. Null if didnt come from one or the other 


async def db_creation():  #initilizng the database creation
    #NEED ADMIN ACCESS FOR THIS 
    conn = await asyncpg.connect(
        user = "postgres",
        password = 'Joshua2014', 
        host = "localhost",
        database = "postgres"
        )
    try: #just checking to see if it was created correctly 
        await conn.execute("CREATE DATABASE pt_db;")
        print("Database 'pt_db' created successfully!")
    except asyncpg.exceptions.DuplicateDatabaseError:
        print("Database already exists.")
    finally:
        await conn.close()
asyncio.run(db_creation())

Base = declarative_base() #template for the tbales 


# every class is a table
class Textbook(Base): 
    __tablename__ = "textbook_sources"
    textbook_id = Column(Integer, primary_key= True)
    textbook_name = Column(String)
    size = Column(float)
    date_added = Column(DateTime)
    where = Column(String)

    
class Research_paper(Base): 
    __tablename__ = "research_paper_sources"
    id = Column(Integer, primary_key= True)
    paper_name = Column(String)
    size = Column(float) 
    date = Column(DateTime)
    where = Column(String)

class Image(Base): 
    __tablename__ = "image_sources" 
    id = Column(Integer, primary_key= id)
    date_added = Column(DateTime)
    size = Column(Integer)
    file_name= Column(String)
    textbook_id = Column(Integer, ForeignKey('textbook_sources.id'))
    textbook = relationship(Textbook)
    paper_id = Column(Integer, ForeignKey('research_paper_sources'))
    paper = relationship(Research_paper)









