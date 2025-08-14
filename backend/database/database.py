import sqlalchemy
from sqlalchemy import create_engine, ForeignKey, inspect, Integer, CheckConstraint, String, UniqueConstraint, Boolean, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, select, func, update, Enum, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column, Session, sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os

#in the table for any new row increase the textbook_id by one. insert a string which links to the pdf name
#I want the size of teh converted file into txt. So we take the file size of the txt
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

#port 5432

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not found. Please create a .env file.")

db = create_engine(DATABASE_URL, connect_args= {"options": '-c search_path=training_sources,frontend_data,public'},)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)
Base = declarative_base()

class BP(Base):
    __tablename__ = "part"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)  # 1 for upper half, 2 for lower half
    upper_count:Mapped[int] = mapped_column(Integer) 
    lower_count:Mapped[int] = mapped_column(Integer)
    __table_args__ = (
        CheckConstraint('id IN ( 1, 2, 3)', name='check_valid_bp_id'), {'schema': 'training_sources'}#makes sure only 1 and 2 are the valuable 
    )

# neck, chest, l/r shoulder, l/r tricep, l/r bicep, abdomen, back, l/r hamstring, l/r quad, l/r calf, l/r ankle, everything
BODY_PART_LABELS = ('n', 'c', 'ls', 'rs', 'lt', 'rt', 'lb', 'rb', 'a', 'b', 'lh', 'rh', 'lq', 'rq', 'lc', 'rc', 'la', 'ra', 'e')

class Body(Base):
    __tablename__ = "body_part_counts"
    __table_args__ = {'schema': 'training_sources'}
    labels = ('n', 'f', 'h', 'a', 'l', 's', 'c', 'b', 'e') #only these labels can be assigned. n for neck, f for feet, h for head, a for arms, l for legs, s for shoudlers, c for chest, b for back, m for multi (no specfiication in the title)
    id: Mapped[str] = mapped_column(
        Enum(*BODY_PART_LABELS, name='body_id_enum'), 
        primary_key=True
    )
    counts:Mapped[int] = mapped_column(Integer)
    source_part_id:Mapped[int] = mapped_column(Integer, ForeignKey("training_sources.part.id"))
    textbooks:Mapped[list['Textbook']] = relationship("Textbook", back_populates="part") #can have multiple textbooks
    research_papers:Mapped[list['Research_paper']] = relationship("Research_paper", back_populates='part') #can have miltiple research papers
    reports: Mapped[list["ProblemReport"]] = relationship(back_populates="body_part")

class Textbook(Base):
    __tablename__ = "textbook_sources"
    textbook_id:Mapped[int]= mapped_column(Integer, primary_key=True, index=True, unique=True) #make sure constraints are true
    textbook_name:Mapped[str] = mapped_column(String)
    author:Mapped[str] = mapped_column(String)
    size:Mapped[int] = mapped_column(Integer)
    date_added:Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    where:Mapped[str] = mapped_column(String)
    part_id:Mapped[str] = mapped_column(Enum(*Body.labels, name='body_id_enum'), ForeignKey('training_sources.body_part_counts.id')) #points to the id in body parts
    part:Mapped['Body'] = relationship("Body", back_populates="textbooks") #can acess the body
    images:Mapped[list['Image']] = relationship('Image', back_populates='textbook') #textbooks can have many images
    __table_args__ = (
        UniqueConstraint('textbook_name', 'author', name='uq_textbook_author'), {'schema': 'training_sources'}
    )
    
class Research_paper(Base):
    __tablename__ = "research_paper_sources"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    paper_name:Mapped[str] = mapped_column(String)
    size:Mapped[int] = mapped_column(Integer)
    date:Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    where:Mapped[str] = mapped_column(String)
    part_id:Mapped[str] = mapped_column(Enum(*Body.labels, name='body_id_enum'), ForeignKey("training_sources.body_part_counts.id")) #point to body parts id
    part:Mapped['Body'] = relationship("Body", back_populates="research_papers") #can acess Body
    images:Mapped[list['Image']] = relationship('Image', back_populates='paper') #can have multiple images
    __table_args__ = (
        UniqueConstraint('paper_name', name='uq_textbook'), {'schema': 'training_sources'}
    )

class Image(Base):
    __tablename__ = "image_sources"
    __table_args__ = {'schema': 'training_sources'}
    iid:Mapped[str] = mapped_column(String, primary_key=True) # 
    date_added:Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow) #current time
    size:Mapped[int] = mapped_column(Integer)
    file_name:Mapped[str] = mapped_column(String)
    textbook_id:Mapped[int] = mapped_column(Integer, ForeignKey('training_sources.textbook_sources.textbook_id'), nullable=True) #points to the textbook_id
    textbook:Mapped['Textbook'] = relationship("Textbook", back_populates='images') #has access to the object
    paper_id:Mapped[int] = mapped_column(Integer, ForeignKey('training_sources.research_paper_sources.id'), nullable=True) #points to paper
    paper:Mapped['Research_paper'] = relationship("Research_paper", back_populates='images') #has access to paper
    page:Mapped[int] = mapped_column(Integer)
    has_context: Mapped[bool] = mapped_column(Boolean, default=True)

#this is where the front end schema starts 
#its called frontend_data
#creating for user_authetication

class User(Base):
    __tablename__ = "users"
    __table_args__ = ({'schema': 'frontend_data'})

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(Date, nullable=True)

    reports: Mapped[list["ProblemReport"]] = relationship(back_populates="user")

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    #most recent login
    last_login_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    #login history
    login_history: Mapped[list["LoginHistory"]] = relationship(back_populates="user")

class ProblemReport(Base):
    __tablename__ = "problem_reports"
    __table_args__ = ({'schema': 'frontend_data'})
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("frontend_data.users.id"), nullable=False, index=True)
    user: Mapped["User"] = relationship(back_populates="reports")

    # This column will store the foreign key
    body_part_id: Mapped[str] = mapped_column(
        # Enum(*BODY_PART_LABELS, name='body_id_enum'),
        ForeignKey('training_sources.body_part_counts.id'),
        nullable=False
    )

    body_part: Mapped["Body"] = relationship(back_populates="reports")
    
    # --- Questionnaire ---
    had_this_problem_before: Mapped[bool] = mapped_column(Boolean, server_default="0", nullable=False)
    previous_problem_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    what_helped_before: Mapped[str] = mapped_column(Text, nullable=True)
    
    # General History
    had_physical_therapy_before: Mapped[bool] = mapped_column(Boolean, server_default="0", nullable=False)
    previous_unrelated_problem: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Personal Opinion 
    opinion_cause: Mapped[str] = mapped_column(Text, nullable=True)
    pain_worse: Mapped[str] = mapped_column(Text, nullable=True)
    pain_better: Mapped[str] = mapped_column(Text, nullable=True)
    goal_for_pt: Mapped[str] = mapped_column(Text, nullable=True)

class LoginHistory(Base):
    __tablename__ = "login_history"
    __table_args__ = ({'schema': 'frontend_data'})

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("frontend_data.users.id"), nullable=False, index=True)
    
    # timestamp for one login
    login_timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    # You could also store other info here, like IP address or device type
    ip_address: Mapped[str] = mapped_column(String(100), nullable=True)

    user: Mapped["User"] = relationship(back_populates="login_history")
    
#textbook count in body. Summarizes the resources for each given label so we can know which parts we need to get more sources for
async def update_single_body_count(session, body_id: str):
    t_count = await session.scalar(
        select(func.count()).select_from(Textbook).where(Textbook.part_id == body_id)
    )
    
    r_count = await session.scalar(
        select(func.count()).select_from(Research_paper).where(Research_paper.part_id == body_id)
    )

    await session.execute(
        update(Body)
        .where(Body.id == body_id)
        .values(counts=(t_count or 0) + (r_count or 0))
    )
#summaries the body parts so we cna see how many resources pertain to lower and half
async def update_bp_count(session, bp_id: int):
    b_count = await session.scalar(
        select(func.count()).select_from(Body).where(Body.where == bp_id)
    )
    await session.execute(
        update(BP)
        .where(BP.id == bp_id)
        .values(upper_count=b_count if bp_id == 1 else 0,
                lower_count=b_count if bp_id == 2 else 0)
    )


def main() -> None:
    Base.metadata.create_all(db)

if __name__ == "__main__":
    main()
    inspector = inspect(db)
    table_names = inspector.get_table_names()
    print("Tables", table_names)
