from backend.database.database import SessionLocal, BP, Body 

#we do this to preopulate BP and body because we only need specfici values in those tbales 
#prevents errors from coming later on
def populating(): 
    db = SessionLocal()

    #making sure that BP only contrains 1 and 2. 1 for upper half and 2 for lower half. 3 for everything or multi
    for part_id in (1, 2, 3):
        if not db.get(BP,part_id): 
            db.add(BP(id = part_id, upper_count = 0, lower_count = 0))
    
    #labels as define in our database.py
    upper_labels = {'n', 'h', 'a', 's', 'c', 'b'}      
    lower_labels = {'f', 'l'}                        
    misc_labels  = {'e'}

    for label in Body.labels: #assigning the labels to where they belong
        if not db.get(Body, label):
            if label in upper_labels:
                p = 1
            elif label in lower_labels:
                p = 2
            else:  # includes 'e'
                p = 3
            db.add(Body(id=label, counts=0, where=p))

    db.commit()
    db.close()
    print('added')

if __name__ == "__main__":
    populating()