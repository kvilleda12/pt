# PTI 
Your intelligent physical therapy asssitant

PTI is an AI powered bot that helps you with physical therapy in many ways. It gives you excersices you can do after telling it what body part you have problems with, guides you through excersices and analyzes them if you are doing them correctly. It also helps track a variety of data that can be used by others to hopefully revolutionize a sector or sectors of the body. 

**the breakdown of what you can find in the folders**


**FRONTEND**

Components: Built using React, Typsecript, and Tailwind 
3d Model, questionairre, dashboard with analytics


**Backend**

- Database: Built using SQLAlchemy and Alembic for migration. Hosted on Supabase. Connected to the frontend using FastAPI
- Scrapers: Built using Selenium, BeautifulSoup and help us gather resources for our LLM
- LLM: RAG tuned Llama3b using RAG-fusion
