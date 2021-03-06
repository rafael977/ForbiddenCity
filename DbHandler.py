# pylint: skip-file
from pymongo import MongoClient
from bson import ObjectId

class DbHandler:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.tripadvisor

        self.member_collection = self.db.member
        self.review_collection = self.db.review
        self.place_collection = self.db.place

    def insert_member(self, member):
        self.member_collection.save(member)

    def insert_reviews(self, reviews):
        for review in reviews:
            self.review_collection.save(review)

    def insert_places(self, places):
        for place in places:
            self.place_collection.save(place)

    def get_all_not_processed_member(self):
        return self.member_collection.find({'is_processed': False})

    def set_member_processed(self, member_id):
        self.member_collection.update({'_id':member_id}, {'$set':{'is_processed':True}})
