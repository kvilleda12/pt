import asyncio
import asyncpg
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, select, func, update
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

## I also want to create a database for tracking exactly where stuff is coming from and what type of data im using
#have a section for top and bottom half. The specifically go into muscle group categories. Shoudlers, arms, upper 
# half of legs, lower half 
#  neck, hands, back, Chest 
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
class BP(Base): 
    
    __tablename__ = "part"
    id = Column(Integer (1,2), primary_key= True) #let the #1 denote upper half and the #2 denote the lower half. 
    upper_count = Column(Integer, ) #count teh total number of upper from our sources
    lower_count = Column(Integer, ) #count the total number of lower from our sources
    
class Body(Base): 
    __tablename__ = "body_part_counts"
    id = Column(String('n', 'f', 'h', 'a', 'l', 's', 'c', 'b'), primary_key= True) 
    counts = Column(Integer)
    


class Textbook(Base): 
    __tablename__ = "textbook_sources"
    textbook_id = Column(Integer, primary_key= True)
    textbook_name = Column(String)
    size = Column(float)
    date_added = Column(DateTime)
    where = Column(String)
    part = Column(String), ForeignKey('Body.id')


    
class Research_paper(Base): 
    __tablename__ = "research_paper_sources"
    id = Column(Integer, primary_key= True)
    paper_name = Column(String)
    size = Column(float) 
    date = Column(DateTime)
    where = Column(String)
    part = Column(String, ForeignKey("body_part_counts.id"))

class Image(Base): 
    __tablename__ = "image_sources" 
    id = Column(Integer, primary_key= True)
    date_added = Column(DateTime)
    size = Column(Integer)
    file_name= Column(String)
    textbook_id = Column(Integer, ForeignKey('textbook_sources.id'))
    textbook = relationship(Textbook)
    paper_id = Column(Integer, ForeignKey('research_paper_sources'))
    paper = relationship(Research_paper)



#function to populate the sums of body_parts.count. Directly links research paper and textbook to the Body table
async def update_single_body_count(session, body_id: str):
    #count matches in textbooks
    t_count = await session.scalar(
        select(func.count()).select_from(Textbook).where(Textbook.part == body_id)
    )
    
    # Count matches in resources
    r_count = await session.scalar(
        select(func.count()).select_from(Research_paper).where(Research_paper.part == body_id)
    )

    # Update body_part_counts
    await session.execute(
        update(Body)
        .where(Body.id == body_id)
        .values(counts=(t_count or 0) + (r_count or 0))
    )





