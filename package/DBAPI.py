import pymongo as pm
from pymongo import MongoClient

DOMAIN = '172.18.0.3'
PORT = 27017

client = MongoClient(
    host = [ str(DOMAIN) + ":" + str(PORT) ],
    serverSelectionTimeoutMS = 3000, # 3 second timeout
    username = "comet",
    password = "12345",
)

def makedb(mydb):
    mydb = client[mydb]
    return mydb

def makecollection(mydb, mycol):
    mydb = makedb(mydb)
    mycol = mydb[mycol]
    return mycol

def insert(mydb, mycol, mydict):
    mycol = makecollection(mydb, mycol)
    inserted = mycol.insert_one(mydict)
    return inserted

def delete_many(mydb, mycol, params):

    mycol = pm.collection.Collection(makedb(mydb), mycol)
    deleted = mycol.delete_many(params)
    return deleted

def query_col(mydb, mycol, params = {'_id':False}):

    mycol = pm.collection.Collection(makedb(mydb), mycol)

    for idx, x in enumerate(mycol.find(projection = params)):
        print(idx + 1, x,'\n')

def visualize_contents(mydb, mycol):

    mycol = pm.collection.Collection(makedb(mydb), mycol)
    cursor = mycol.find()
    print('Fields: \n', cursor[0].keys())

def substructure_filter(mydb, mycol, field = 'smiles tags'):

    mycol = pm.collection.Collection(makedb(mydb), mycol)
    cursor = mycol.find()

    for idx1, x in enumerate(cursor):
        field_dict = x[field]

        for idx2, i in enumerate(field_dict):
            print('\n\n\n', i, '\n\n\n')
            if 'nH' in i:
                print('yes!')
            else:
                print('no!')


    #for x in mycol.find():
    #    print(x)
'''
cursor = db['collection'].find({})
for document in cursor: 
    print(document.keys())  # print all fields of this document. 
    '''

visualize_contents('chem_dbs','zinc15')

'''

x = mycol.insert_one(mydict)
print(x)
print(client.list_database_names())
print(mydb.list_collection_names())
print(x.inserted_id)

for x in mycol.find():
    print(x)


'''
