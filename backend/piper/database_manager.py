from sqlalchemy.orm import Session
from backend.database.database import SessionLocal, Body, BP, Research_paper, Textbook

UPPER_BODY_LABELS = {'n', 'h', 'a', 's', 'c', 'b'}
LOWER_BODY_LABELS = {'f', 'l'}

def add_paper_to_db(paper_info: dict):
    """Adds a new research paper to the database and updates counts."""
    db: Session = SessionLocal()
    try:
        if db.query(Research_paper).filter(Research_paper.paper_name == paper_info['title']).first():
            print(f"Skipping duplicate paper: {paper_info['title']}")
            return None

        new_paper = Research_paper(
            paper_name=paper_info['title'],
            size=paper_info.get('size', 0),
            where=paper_info['path'],
            part_id=paper_info['part_id']
        )
        db.add(new_paper)

        body_part = db.query(Body).filter(Body.id == paper_info['part_id']).first()
        if body_part:
            body_part.counts = (body_part.counts or 0) + 1
        else:
            source_id = 1 if paper_info['part_id'] in UPPER_BODY_LABELS else 2
            db.add(Body(id=paper_info['part_id'], counts=1, source_part_id=source_id))

        bp_id_to_update = 1 if paper_info['part_id'] in UPPER_BODY_LABELS else 2
        bp_record = db.query(BP).filter(BP.id == bp_id_to_update).first()
        if bp_record:
            if bp_id_to_update == 1:
                bp_record.upper_count = (bp_record.upper_count or 0) + 1
            else:
                bp_record.lower_count = (bp_record.lower_count or 0) + 1
        else:
            db.add(BP(id=bp_id_to_update, upper_count=(1 if bp_id_to_update == 1 else 0), lower_count=(1 if bp_id_to_update == 2 else 0)))

        db.commit()
        db.refresh(new_paper)
        print(f"✅ Added paper '{paper_info['title']}'. New ID: {new_paper.id}.")
        return new_paper.id
    except Exception as e:
        print(f"❌ DB Error adding paper: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def add_textbook_to_db(textbook_info: dict):
    """Adds a new textbook to the database and updates counts."""
    db: Session = SessionLocal()
    try:
        if db.query(Textbook).filter(Textbook.textbook_name == textbook_info['title'], Textbook.author == textbook_info['author']).first():
            print(f"Skipping duplicate textbook: {textbook_info['title']}")
            return None

        new_textbook = Textbook(
            textbook_name=textbook_info['title'],
            author=textbook_info['author'],
            size=textbook_info.get('size', 0),
            where=textbook_info['path'],
            part_id=textbook_info['part_id']
        )
        db.add(new_textbook)

        body_part = db.query(Body).filter(Body.id == textbook_info['part_id']).first()
        if body_part:
            body_part.counts = (body_part.counts or 0) + 1
        else:
            source_id = 1 if textbook_info['part_id'] in UPPER_BODY_LABELS else 2
            db.add(Body(id=textbook_info['part_id'], counts=1, source_part_id=source_id))
        
        bp_id_to_update = 1 if textbook_info['part_id'] in UPPER_BODY_LABELS else 2
        bp_record = db.query(BP).filter(BP.id == bp_id_to_update).first()
        if bp_record:
            if bp_id_to_update == 1:
                bp_record.upper_count = (bp_record.upper_count or 0) + 1
            else:
                bp_record.lower_count = (bp_record.lower_count or 0) + 1
        else:
            db.add(BP(id=bp_id_to_update, upper_count=(1 if bp_id_to_update == 1 else 0), lower_count=(1 if bp_id_to_update == 2 else 0)))

        db.commit()
        db.refresh(new_textbook)
        print(f"✅ Added textbook '{textbook_info['title']}'. New ID: {new_textbook.textbook_id}.")
        return new_textbook.textbook_id
    except Exception as e:
        print(f"❌ DB Error adding textbook: {e}")
        db.rollback()
        return None
    finally:
        db.close()