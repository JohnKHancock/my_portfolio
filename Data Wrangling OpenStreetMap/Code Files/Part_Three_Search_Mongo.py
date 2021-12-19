from pymongo import MongoClient
import pprint as pp


#==============================================================================
# 8.	Using Mongo DB Queries
#==============================================================================

def get_db(db_name):
      client = MongoClient('localhost:27017')
      db = client[db_name]
      return db
  
db = get_db('cities')

def find_city():
    projection={"_id":0, "address.city":1}
    city = db.Detroit.find({"address.city": {"$exists" : 1}},projection)     
       
    for c in city:
        pp.pprint (c)
    
    
def find_country():
    projection={"_id":0, "address.country":1}
    country = db.Detroit.find({"address.country": {"$exists" : 1}},projection)     
       
    for c in country:
        pp.pprint (c)    

def find_postcodes():
    projection={"_id":0, "address.postcode":1}
    postcodes= db.Detroit.find({"address.postcode": {"$exists" : 1}},projection)     
       
    for c in postcodes:
        pp.pprint (c)
    

def find_addresses():
    projection={"_id":0, "address.street":1}
    streets= db.Detroit.find({"address.street": {"$exists" : 1}},projection)     
       
    for c in streets:
        pp.pprint (c)

user_stats = {} 

def calc_users():
    projection = {"created.user": 1, "_id":0}
    query = {"created.user" : {"$ne":[]}}
    users = db.Detroit.find(query,projection)
    
    for user in users:
        key = user["created"]["user"]
        if key in user_stats:
            user_stats[key] += 1
        else:
            user_stats[key] = 1
    
    return user_stats


def sort_by_value(dict):
    sort_by_value= sorted(dict.items(), key = lambda t:t[1],reverse=True)
    return sort_by_value

def find_notes():
    projection={"_id":0, "note":1}
    notes = db.Detroit.find({"note": {"$exists" : 1}},projection)     
       
    for n in notes:
        pp.pprint (n)

#Uncomment these functions to run it against the data

#find_city()
#find_country()
#find_postcodes()
#find_addresses()
#calc_users()
#pp.pprint(sort_by_value(user_stats))
#find_notes()