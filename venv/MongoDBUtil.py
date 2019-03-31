from pymongo import MongoClient
class MongoPersist:

    def insertIntoMongodb(self,data):
        try:
            conn = MongoClient()
            print("Connection successful")
        except:
            print("could not connect to mongo db")

        db = conn.database
        collection = db.testCollection
        result = collection.insert(data)

        return result


    def searchMongodb(self, input):
        try:
            conn = MongoClient()
            print("Connection successful")
        except:
            print("could not connect to mongo db")

        db = conn.database
        collection = db.testCollection
        #collection.create_index([("person_name", "text")])
        #cursor = collection.find({"$text": {"$search": input}})
        cursor = collection.find({"person_name":{ '$regex': input}})
        for output in cursor:
            print(output)

        return {'short-reviews':output['short-reviews'],'long-reviews':output['long-reviews']}

    def searchContent(self, website,brand):
        try:
            conn = MongoClient()
            print("Connection successful")
        except:
            print("could not connect to mongo db")

        db = conn.database
        collection = db.testCollection

        cursor = collection.find({"website":website,"brand":brand})
        for output in cursor:
            print(output)

        return output