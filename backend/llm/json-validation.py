from dataclasses import dataclass, asdict 
import json


#ids need to start off witha  digit related to the body part it is talkng about 


class Chunk: 
    id = int
    source = str
    related_questions = str
    general_body_part = str
    category_of_answers = str
    content = str
    start_char = str

