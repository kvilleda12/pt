import asyncio
import asyncpg
import sqlalchemy
from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, select, func, update, Enum
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime

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


db = sqlalchemy.create_engine("postgre:///:memory") #initialize database
session = sessionmaker(bind = db) 

Base = declarative_base() #template for the tbales 

# every class is a table
class BP(Base): 
    
    __tablename__ = "part"
    labels = (1,2)
    id:Mapped[Enum] = mapped_column(Enum(*labels), name = 'bp_id_enum', primary_key= True) #let the #1 denote upper half and the #2 denote the lower half. 
    upper_count:Mapped[int] = mapped_column() #count teh total number of upper from our sources
    lower_count:Mapped[int] = mapped_column() #count the total number of lower from our sources
    
class Body(Base): 
    __tablename__ = "body_part_counts"
    labels = ('n', 'f', 'h', 'a', 'l', 's', 'c', 'b') #labels to be used for key configuration
    id:Mapped[Enum] =mapped_column(Enum(*labels, name = 'Body_id_enum'), primary_key= True) 
    counts :Mapped[int] = mapped_column()
    where: Mapped[int] = mapped_column(ForeignKey("part.id"))
    textbooks: Mapped[list["Textbook"]] = relationship("Textbook", back_populates="part") #multiple textbooks can conenct to this one body aprt
    research_papers:Mapped[list["Research_paper"]] = relationship("Research_paper", back_populates= 'part') #multiple papers populate to the same body 


class Textbook(Base): 
    __tablename__ = "textbook_sources"
    textbook_id:Mapped[int] =  mapped_column(primary_key= True, index = True, Unique = True)
    textbook_name:Mapped[str] = mapped_column()
    size:Mapped[int] = mapped_column()
    date_added:Mapped[datetime] = mapped_column(DateTime, default = datetime.utcnow)
    where:Mapped[str] = mapped_column()
    part: Mapped[str] = mapped_column(ForeignKey('body_part_counts.id')) #points to an id from the Body class
    part: Mapped["Body"] = relationship("Body", back_populates="textbooks")
    image:Mapped[list["Image"]] = relationship('Image', back_populates ='textbook_id' )
    


    
class Research_paper(Base): 
    __tablename__ = "research_paper_sources"
    id:Mapped[int] =mapped_column(primary_key= True, index = True, Unique = True)
    paper_name:Mapped[str] = mapped_column()
    size:Mapped[int] = mapped_column()
    date:Mapped[DateTime] = mapped_column(DateTime, default= datetime.utcnow)
    where:Mapped[str] = mapped_column()
    part:Mapped[str] = mapped_column(ForeignKey("body_part_counts.id")) #points to an id from the Body class
    part: Mapped["Body"] = relationship("Body", back_populates="research_papers")
    image:Mapped[list["Image"]] = relationship('Image', back_populates= 'paper_id')


class Image(Base): 
    __tablename__ = "image_sources" 
    id:Mapped[int] =mapped_column( primary_key= True, index = True, Unique = True)
    date_added:Mapped[DateTime] = mapped_column(DateTime, default= datetime.utcnow)
    size:Mapped[int] = mapped_column()
    file_name:Mapped[str] = mapped_column() 
    textbook_id:Mapped[int] =mapped_column(ForeignKey('textbook_sources.id'),nullable = True) #points to textbook_id
    textbook_id:Mapped["Textbook"] = relationship("Textbook", back_populates= 'image')
    paper_id:Mapped[int]= mapped_column(ForeignKey('research_paper_sources.id'), nullable = True) #points to research paper_id
    paper_id:Mapped["Research_paper"] = relationship("Research_paper", back_populates= 'image')



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

async def update_bp_count(session, BP_id = int):
    b_count = await session.scalar(
        select(func.count().select_from(Body).where(Body.part == BP.id))
    )
    await session.execute( 
        update(BP)
        .where (BP.id == BP_id)
        .values(counts = (b_count or 0))
    )


def main() -> None: 
    Base.metadata.create_all(db)

    





