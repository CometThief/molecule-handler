import pymongo as pm
from pymongo import MongoClient

DOMAIN = '172.19.0.3'
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
    mycol.insert_one(mydict)

#def delete(my, mycol, mydict):


def visualize_contents(mydb, mycol):
    a = pm.collection.Collection(makedb(mydb), mycol)
    b = makecollection(mydb, mycol)
    #print(a)
    c = {'_id': False, 'zinc tags':True}
    for idx, x in enumerate(b.find(projection = c)):
        print(idx + 1, x)

    #for x in mycol.find():
    #    print(x)

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
