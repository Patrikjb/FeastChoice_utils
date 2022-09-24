import firebase_admin
from firebase_admin import firestore, credentials
import random

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def main(db):
    pass


def add_data(db):
    random_int = str(random.randint(1,20))
    test_document = {u'testing' : random_int}
    db.collection(u'testing').add(test_document)



# find max value from certain key in list of dicts
# return that value
def max_value_from_dicts(key, list_of_dicts):
    list_of_values = [d[key] for d in list_of_dicts if key in d]
    if list_of_values:
        return max(list_of_values)
    else:
        return 0


# adds serial number (sequenceInteger) 
# to all those documents that do not have one.
# needed for randomly to query documents from recipes.
def add_serial_number_to_all_documents(db):
    docs = db.collection('allRecipes').get()
    
    # find highest sequenceInteger
    dicts = []
    for doc in docs:
        doc_dict = doc.to_dict()
        dicts.append(doc_dict)

    current_max = max_value_from_dicts('sequenceInteger', dicts)
    
    for d in dicts:
        if "sequenceInteger" not in d:
            d['sequenceInteger'] = current_max + 1
            current_max = current_max + 1

    for doc, d in zip(docs, dicts):
        doc.reference.update({'sequenceInteger' : d['sequenceInteger']})

# needed to remove a field from allRecipes
def remove_field_from_all_docs(db):
    docs = db.collection(u'allRecipes').stream()

    for doc in docs:
        doc.reference.update({u'sequenceInteger' : firestore.DELETE_FIELD})


#queries one random document from collection
# based on field 'sequenceInteger'.
def query_random_document(db):
    random_int = random.randint(1,5000)


main(db)
