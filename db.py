import pymongo 
def get_database(mongouri = "mongodb://localhost:27017/"):
    client = pymongo.MongoClient(mongouri)
    db = client["MedSyncAI"]
    return db