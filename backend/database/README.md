# Weclome to the Database

* below you will find an explanation for the code in the database as well as the purpose + whwat you need to do in order to update it and what to put in it.


The primary purpose of the database is to store our data. In this database we are storing all data related to the texbooks we use to power our AI model. This includes names of textbooks, authors, date, where it coming from, etc. In the _**text_files**_ folder you will find the actual contents of the text which will be analyzed. We want to store everything we do and keep track of when its being done and find interesting analytics for textbooks. 

__High level + setup__

Flow of the database (high level - for specific functions go lower) : Have a database that stores the sources our model is trained on. It will give us brief overviews of statistics for it so we can see what more we need and keep a well balanced model. We want the sources to come from textbooks, research papers, and images. What we do is we convert the pdfs in our folder _**file_sources**_ into txt files which are stored in _**text_files**_. We want this to happen automatically so we create a pipeline in text_scraper  called **_scaper.py_** to actually automate these processes. We use **_alembic_** for migration. 


Setup:  look at the requirements which should have up to date libraries. 
building using SQlAlchemy orm for mapping

To check the database updates and what the table looks like run in the terminal : 
psql -h localhost -U postgres -d pt_db 
just run basic sql commands to see the rows. Don't get to add the  ; very important or your command won't run 
Sometimes it gets stuck in your previous command for some reason do if you do control + c it will get you out of the stuck
In order to quit and go back to the .venv terminal or whatever terminal your using do \q

# to update the database

commands: 

**- Run Alembic revision –autogenerate -m “”  (its 2 dashes in front of autogenerate)**
**Alembic upgrade head**


# Whats in the tables

- A body part table that tracks what body parts textbooks refer too
- textbook table that tells us important information about the table
- Research paper that tells us important inforamtion about the paper. In this also feed articles that you find on the internet that are academically backed.
- Image table to store where images come from what page they were found and it it has context
- functions to automatically update counts and ids




